"""Render TOOLBOX.md from data/toolbox.json. No dependencies."""
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
OWNER = 'phlppgdfry'
INTRO = '''# Toolbox

[← Profile](README.md) · [Professional](PROFESSIONAL.md) · [Projects](PROJECTS.md)

Tools and technologies from my projects. This is a toolbox, not a proficiency ranking. A linked badge opens a public repository that uses the tool; an unlinked badge is used in private app repositories or day-to-day work. **Explored** lists learning paths that have not produced a working project yet.
'''
OUTRO = '''
---

Generated from [`data/toolbox.json`](data/toolbox.json) by `scripts/build_toolbox.py`. `scripts/scan_toolbox.py` checks every entry against all repositories and reports tools that are no longer used, evidence links that stopped matching and frequently used packages without an entry.
'''

def badge(tool):
    label = quote(tool['name'].replace('-', '--').replace(' ', '_'), safe='_.')
    url = f"https://img.shields.io/badge/{label}-{tool['color']}?style=flat-square"
    if tool.get('logo'):
        url += f"&logo={tool['logo']}&logoColor={tool.get('logo_color', 'white')}"
    image = f"![{tool['name']}]({url})"
    return f"[{image}](https://github.com/{OWNER}/{tool['repo']})" if tool.get('repo') else image

def render(registry):
    sections = ['### ' + s['title'] + '\n' + '\n'.join(badge(t) for t in s['tools']) for s in registry['sections']]
    return INTRO + '\n' + '\n\n'.join(sections) + '\n' + OUTRO

if __name__ == '__main__':
    registry = json.loads((ROOT / 'data/toolbox.json').read_text())
    (ROOT / 'TOOLBOX.md').write_text(render(registry))
