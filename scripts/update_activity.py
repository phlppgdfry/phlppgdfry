"""Refresh public GitHub activity and a repository-owned SVG. No dependencies."""
from collections import Counter
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import re
import subprocess
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OWNER = 'phlppgdfry'
START, END = '<!-- ACTIVITY:START -->', '<!-- ACTIVITY:END -->'

def api(path):
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if not token:
        return json.loads(subprocess.check_output(['gh', 'api', path], text=True))
    req = Request('https://api.github.com/' + path, headers={
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'phlppgdfry-profile-updater',
    })
    with urlopen(req, timeout=30) as response:
        return json.load(response)

def md(value):
    return re.sub(r'([\\`*_{}\[\]()<>|])', r'\\\1', str(value).replace('\n', ' '))

def replace_block(text, block):
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError('Expected exactly one activity marker pair')
    before, rest = text.split(START)
    old, after = rest.split(END)
    return before + START + '\n' + block + '\n' + END + after

def collect():
    repos=[]
    for page in range(1, 101):
        batch=api(f'users/{OWNER}/repos?per_page=100&type=owner&page={page}')
        repos.extend(batch)
        if len(batch)<100: break
    else:
        raise ValueError('Unexpected repository pagination limit')
    repos=[r for r in repos if not r.get('private') and not r.get('fork') and r['name'].lower()!=OWNER]
    releases=[]
    # A fixed, explicit selection keeps the scheduled API budget modest.
    for name in ['ClickTrack','MirrorMate-App','docurelay-field','portops-ai','Logistics-Master','shipment-tracking-platform']:
        for r in api(f'repos/{OWNER}/{name}/releases?per_page=5'):
            if not r['draft'] and not r['prerelease'] and r.get('published_at'):
                releases.append(dict(project=name, **r))
    return repos, sorted(releases,key=lambda r:r['published_at'],reverse=True)[:4]

def render(repos,releases,date):
    active=[r for r in repos if not r['archived']]
    recent=sorted([r for r in active if r.get('pushed_at')],key=lambda r:r['pushed_at'],reverse=True)[:5]
    rows=['![Public repository snapshot](assets/activity.svg)', '', '**Recently pushed repositories**', '', '| Repository | Latest push (UTC) |', '| :--- | :--- |']
    rows += [f"| [{md(r['name'])}]({r['html_url']}) | {r['pushed_at'][:10]} |" for r in recent]
    rows += ['', '**Latest stable releases from the featured release watchlist**', '']
    rows += [f"- [{md(r['project'])} · {md(r['tag_name'])}]({r['html_url']}) — {r['published_at'][:10]}" for r in releases] or ['No stable releases published in the watched repositories yet.']
    rows += ['', f'<sub>Snapshot: {date} UTC · Public, owned, non-fork repositories; profile repository excluded. Release watchlist: ClickTrack, MirrorMate, DocuRelay, PortOps, Logistics Master and Shipment Tracking.</sub>']
    counts=Counter(r['language'] for r in active if r.get('language'))
    langs=' / '.join(f'{name} {count}' for name,count in counts.most_common(5))
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="194" viewBox="0 0 960 194" role="img" aria-label="Public GitHub repository snapshot">
<rect width="960" height="194" rx="16" fill="#0b1119"/>
<text x="28" y="31" font-family="monospace" font-size="13" fill="#a2b2c4">PUBLIC WORK / {escape(date)} UTC</text>
<g font-family="Arial,sans-serif" font-size="38" font-weight="bold" fill="#c8f135">
<text x="28" y="87">{len(active)}</text><text x="338" y="87">{len(repos)-len(active)}</text><text x="648" y="87">{len(counts)}</text></g>
<g font-family="Arial,sans-serif" font-size="16" fill="#edf4fa"><text x="28" y="117">Non-archived repositories</text><text x="338" y="117">Archived repositories</text><text x="648" y="117">Primary languages</text></g>
<text x="28" y="160" font-family="monospace" font-size="13" fill="#55ddec">{escape(langs)}</text>
<text x="28" y="181" font-family="Arial,sans-serif" font-size="11" fill="#a2b2c4">Language counts describe non-archived repositories, not proficiency or lines of code.</text></svg>'''
    return '\n'.join(rows),svg

def main():
    # Collect everything before writing: API failure preserves the last good snapshot.
    repos,releases=collect()
    if not repos: raise ValueError('Empty repository response; keeping existing snapshot')
    block,svg=render(repos,releases,datetime.now(timezone.utc).strftime('%Y-%m-%d'))
    readme=ROOT/'README.md'
    updated=replace_block(readme.read_text(),block)
    (ROOT/'assets/activity.svg').write_text(svg)
    readme.write_text(updated)

if __name__=='__main__': main()
