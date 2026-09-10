import json
from pathlib import Path
import re
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
from scripts import update_activity as activity

ROOT = Path(__file__).resolve().parents[1]

class ActivityTests(unittest.TestCase):
    def test_preserves_editorial_content(self):
        source='intro\n'+activity.START+'\nold\n'+activity.END+'\noutro'
        result=activity.replace_block(source,'new')
        self.assertEqual(result,'intro\n'+activity.START+'\nnew\n'+activity.END+'\noutro')
        for bad in ['no markers',source+activity.START,source+activity.END]:
            with self.assertRaises(ValueError): activity.replace_block(bad,'new')

    def test_public_filter_and_release_scope(self):
        repos=[dict(name=n,private=private,fork=fork,archived=False) for n,private,fork in [('project',False,False),('secret',True,False),('fork',False,True),('phlppgdfry',False,False)]]
        release=dict(draft=False,prerelease=False,published_at='2026-09-01',tag_name='v1',html_url='https://github.com/example')
        def fake(path):
            if path.startswith('users/'):return repos
            if '/ClickTrack/' in path:return [release,dict(release,draft=True),dict(release,prerelease=True)]
            return []
        with patch.object(activity,'api',side_effect=fake):
            found,releases=activity.collect()
        self.assertEqual([r['name'] for r in found],['project'])
        self.assertEqual(len(releases),1)
        self.assertEqual(releases[0]['project'],'ClickTrack')

    def test_curated_counts_and_empty_release_state(self):
        showcase=json.loads((ROOT/'data/showcase.json').read_text())
        block,svg=activity.render([],[],'2026-09-09',showcase)
        ET.fromstring(svg)
        self.assertIn('>2</text>',svg)
        self.assertIn('Browser demo',svg)
        self.assertIn('No stable releases',block)
        for item in showcase:self.assertIn(item['url'],block)
        self.assertEqual(len({x['url'] for x in showcase}),len(showcase))
        self.assertTrue(all(x['url'].startswith('https://') for x in showcase))

    def test_metadata_is_escaped(self):
        release={'project':'test|name','tag_name':'[click]','html_url':'https://github.com/example','published_at':'2026-09-09'}
        block,_=activity.render([], [release], '2026-09-09')
        self.assertIn('test\\|name',block)
        self.assertIn('\\[click\\]',block)

class ContentTests(unittest.TestCase):
    def test_local_links_images_and_svg(self):
        for path in ROOT.glob('*.md'):
            text=path.read_text()
            links=re.findall(r'\]\(([^)]+)\)',text)+re.findall(r'(?:href|src)="([^"]+)"',text)
            for link in links:
                if not link.startswith(('https://','http://','mailto:','#')):
                    self.assertTrue((ROOT/link.split('#')[0]).exists(),f'{path.name}: {link}')
            for image in re.findall(r'<img\b[^>]*>',text):self.assertIn('alt=',image)
            self.assertEqual(text.count('<details>'),text.count('</details>'),path.name)
        for svg in (ROOT/'assets').glob('*.svg'):ET.parse(svg)

    def test_covers_and_harbor_destinations(self):
        text=(ROOT/'README.md').read_text()
        self.assertNotIn('<td width="50%"',text)
        self.assertEqual(len(re.findall(r'src="assets/cover-',text)),6)
        self.assertEqual(len(re.findall(r'<a href="[^"]+"><img src="assets/district-',text)),4)

if __name__=='__main__':unittest.main()
