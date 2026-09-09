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

def render(repos,releases,date,showcase=None):
    showcase = showcase or []
    offered = Counter(item["kind"] for item in showcase)
    active=[r for r in repos if not r['archived']]
    recent=sorted([r for r in active if r.get('pushed_at')],key=lambda r:r['pushed_at'],reverse=True)[:5]
    rows=['![Ways to explore the portfolio](assets/activity.svg)', '', '**Try the featured work:** ' + ' · '.join(f"[{md(item['name'])}]({item['url']})" for item in showcase), '', '**Recently pushed repositories**', '', '| Repository | Latest push (UTC) |', '| :--- | :--- |']
    rows += [f"| [{md(r['name'])}]({r['html_url']}) | {r['pushed_at'][:10]} |" for r in recent]
    rows += ['', '**Latest stable releases from the featured release watchlist**', '']
    rows += [f"- [{md(r['project'])} · {md(r['tag_name'])}]({r['html_url']}) — {r['published_at'][:10]}" for r in releases] or ['No stable releases published in the watched repositories yet.']
    rows += ['', f'<sub>Snapshot: {date} UTC · Public, owned, non-fork repositories; profile repository excluded. Release watchlist: ClickTrack, MirrorMate, DocuRelay, PortOps, Logistics Master and Shipment Tracking.</sub>']
    langs=f'{len(active)} non-archived repos / {len(repos)-len(active)} archived / {len(releases)} recent stable releases shown'
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="194" viewBox="0 0 960 194" role="img" aria-label="Ways to explore the curated portfolio">
<rect width="960" height="194" rx="16" fill="#0b1119"/>
<text x="28" y="31" font-family="monospace" font-size="13" fill="#a2b2c4">EXPLORE THE WORK / {escape(date)} UTC</text>
<g font-family="Arial,sans-serif" font-size="38" font-weight="bold" fill="#c8f135">
<text x="28" y="87">{offered["app"]}</text><text x="338" y="87">{offered["browser_demo"]}</text><text x="648" y="87">{offered["recorded_workflow"]}</text></g>
<g font-family="Arial,sans-serif" font-size="16" fill="#edf4fa"><text x="28" y="117">Mac apps to explore</text><text x="338" y="117">Browser demo</text><text x="648" y="117">Recorded workflow</text></g>
<text x="28" y="160" font-family="monospace" font-size="13" fill="#55ddec">{escape(langs)}</text>
<text x="28" y="181" font-family="Arial,sans-serif" font-size="11" fill="#a2b2c4">Curated destinations, linked below. Counts describe this selection; they are not live uptime checks.</text></svg>'''
    return '\n'.join(rows),svg

def main():
    # Collect everything before writing: API failure preserves the last good snapshot.
    repos,releases=collect()
    if not repos: raise ValueError('Empty repository response; keeping existing snapshot')
    showcase=json.loads((ROOT/'data/showcase.json').read_text())
    block,svg=render(repos,releases,datetime.now(timezone.utc).strftime('%Y-%m-%d'),showcase)
    readme=ROOT/'README.md'
    updated=replace_block(readme.read_text(),block)
    (ROOT/'assets/activity.svg').write_text(svg)
    readme.write_text(updated)

if __name__=='__main__': main()
