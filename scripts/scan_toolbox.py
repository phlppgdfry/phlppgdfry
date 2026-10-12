"""Check data/toolbox.json against every repository. Needs an authenticated GitHub CLI; no other dependencies.

Each repository is cloned shallow and sparse (manifests, CI workflows and Swift sources only) into a cache
folder. A tool's `detect` regex runs against one text per repository: file paths, manifest contents, Swift
imports as `import:Module` and GitHub languages as `lang:Name`.

    python3 scripts/scan_toolbox.py              # report stale tools, broken evidence links, unlisted dependencies
    python3 scripts/scan_toolbox.py --fill       # also set `repo` for tools that have no public evidence link yet
"""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OWNER = 'phlppgdfry'
REGISTRY = ROOT / 'data/toolbox.json'
SPARSE = ['package.json', 'requirements*.txt', 'pyproject.toml', '*.csproj', 'Package.swift', 'project.yml',
          'Dockerfile', '*compose*.yml', '*compose*.yaml', 'build.gradle*', 'libs.versions.toml', 'pom.xml',
          '.github/workflows/*', 'wrangler.toml', 'vercel.json', 'Fastfile', '.pre-commit-config.yaml',
          'dbt_project.yml', 'schema.prisma', 'Pulumi.yaml', '*.swift', '!node_modules/']
NOT_DEPS = {'version', 'node', 'npm', 'schedule'}
DEP = re.compile(r'"([@\w./-]+)":\s*"[\^~<>=*\d]|PackageReference Include="([^"]+)"')

def gh(*args):
    return subprocess.check_output(['gh', *args], text=True)

def repositories():
    rows = json.loads(gh('repo', 'list', OWNER, '--limit', '500', '--json', 'name,isPrivate,isFork,isArchived'))
    return [r for r in rows if not r['isFork'] and r['name'] != OWNER]

def haystack(repo, cache):
    name, path = repo['name'], cache / repo['name']
    git = lambda *a: subprocess.run(['git', '-C', str(path), *a], capture_output=True, text=True)
    if not path.exists():
        url = f'https://github.com/{OWNER}/{name}.git'
        if subprocess.run(['git', 'clone', '-q', '--depth', '1', '--filter=blob:none', '--no-checkout', url, str(path)],
                          capture_output=True).returncode:
            return name, ''
        git('sparse-checkout', 'set', '--no-cone', *SPARSE)
        git('checkout', '-q')
    else:
        git('pull', '-q', '--depth', '1')
    parts = git('ls-files').stdout.splitlines()
    for file in path.rglob('*'):
        if not file.is_file() or '.git' in file.parts:
            continue
        text = file.read_text(errors='ignore')
        parts += ['import:' + m for m in re.findall(r'^(?:@\w+ )?import (\w+)', text, re.M)] if file.suffix == '.swift' else [text]
    try:
        parts += ['lang:' + lang for lang in json.loads(gh('api', f'repos/{OWNER}/{name}/languages'))]
    except subprocess.CalledProcessError:
        pass
    return name, '\n'.join(parts)

def tools(registry):
    return [tool for section in registry['sections'] for tool in section['tools']]

def main():
    registry = json.loads(REGISTRY.read_text())
    cache = Path(tempfile.gettempdir()) / 'toolbox-scan'
    cache.mkdir(exist_ok=True)
    repos = repositories()
    public = {r['name'] for r in repos if not r['isPrivate']}
    with ThreadPoolExecutor(8) as pool:
        texts = dict(pool.map(lambda r: haystack(r, cache), repos))
    problems = []
    for tool in tools(registry):
        if 'detect' not in tool:
            continue
        rule = re.compile(tool['detect'], re.M)
        hits = sorted(name for name, text in texts.items() if rule.search(text))
        hits_public = [h for h in hits if h in public]
        if not hits:
            problems.append(f"stale     {tool['name']}: no repository matches {tool['detect']!r}")
        elif tool.get('repo') and tool['repo'] not in hits_public:
            problems.append(f"evidence  {tool['name']}: {tool['repo']} no longer matches; public hits: {', '.join(hits_public) or 'none'}")
        elif not tool.get('repo') and hits_public and '--fill' in sys.argv:
            tool['repo'] = Counter({h: len(rule.findall(texts[h])) for h in hits_public}).most_common(1)[0][0]
        print(f"{tool['name']:<24} {len(hits):>3} repos  {', '.join(hits[:6])}{' …' if len(hits) > 6 else ''}")
    deps = Counter()
    for text in texts.values():
        deps.update({npm or f'Include="{nuget}"' for npm, nuget in DEP.findall(text)} - NOT_DEPS)
    rules = [re.compile(t['detect'], re.M) for t in tools(registry) if 'detect' in t]
    unlisted = [f'{d} ({n})' for d, n in deps.most_common()
                if n >= 3 and not any(r.search(d if d.startswith('Include') else f'"{d}":') for r in rules)]
    print('\n' + ('\n'.join(problems) or 'No stale tools or broken evidence links.'))
    print('\nnpm and NuGet packages in 3+ repositories without a toolbox entry (libraries are left out on purpose):')
    print('  ' + ', '.join(re.sub(r'Include="([^"]+)"', r'\1', u) for u in unlisted[:60]))
    if '--fill' in sys.argv:
        REGISTRY.write_text(json.dumps(registry, indent=1, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    main()
