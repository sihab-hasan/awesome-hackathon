from __future__ import annotations
import json, subprocess, sys, unittest

import yaml
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class RepositoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog=json.loads((ROOT/'catalog/resources.json').read_text())
        cls.resources=cls.catalog['resources']

    def test_catalog_has_unique_ids_urls_and_names(self):
        self.assertEqual(len(self.resources),len({x['id'] for x in self.resources}))
        self.assertEqual(len(self.resources),len({x['url'] for x in self.resources}))
        self.assertEqual(len(self.resources),len({x['name'].casefold() for x in self.resources}))

    def test_every_category_has_generated_page(self):
        for category in {x['category'] for x in self.resources}:
            self.assertTrue((ROOT/'resources'/category/'README.md').is_file(),category)

    def test_catalog_cli_filters(self):
        result=subprocess.run([sys.executable,str(ROOT/'scripts/catalog_query.py'),'--category','observability','--json'],capture_output=True,text=True,check=True)
        items=json.loads(result.stdout)
        self.assertGreaterEqual(len(items),4)
        self.assertTrue(all(x['category']=='observability' for x in items))

    def test_generator_is_idempotent(self):
        subprocess.run([sys.executable,str(ROOT/'scripts/generate_catalog.py'),'--check'],check=True)

    def test_main_readme_contents_first(self):
        text=(ROOT/'README.md').read_text()
        headings=[line for line in text.splitlines() if line.startswith('## ')]
        self.assertTrue(headings and headings[0]=='## Contents')

    def test_no_duplicate_legacy_directories(self):
        for name in ('awesome','templates','starter-kits','examples'):
            self.assertFalse((ROOT/name).exists(),name)

    def test_documentation_navigation_is_complete(self):
        config=yaml.safe_load((ROOT/'mkdocs.yml').read_text())
        docs_root=ROOT/config.get('docs_dir','docs')
        actual={str(p.relative_to(docs_root)).replace('\\','/') for p in docs_root.rglob('*.md')}
        def flatten(value):
            if isinstance(value,str): return [value]
            if isinstance(value,list): return [path for item in value for path in flatten(item)]
            if isinstance(value,dict): return [path for item in value.values() for path in flatten(item)]
            return []
        self.assertEqual(actual,set(flatten(config['nav'])))

    def test_documentation_theme_toggle(self):
        for config_name in ('mkdocs-site.yml', 'mkdocs.yml'):
            config=yaml.safe_load((ROOT/config_name).read_text())
            palettes=config['theme'].get('palette',[])
            self.assertEqual(len(palettes),3,config_name)
            self.assertEqual(
                [item.get('scheme') for item in palettes],
                [None,'default','slate'],
                config_name,
            )
            self.assertEqual(
                [item.get('media') for item in palettes],
                [
                    '(prefers-color-scheme)',
                    '(prefers-color-scheme: light)',
                    '(prefers-color-scheme: dark)',
                ],
                config_name,
            )
            self.assertEqual(
                [item['toggle']['icon'] for item in palettes],
                ['lucide/sun-moon','lucide/sun','lucide/moon'],
                config_name,
            )

    def test_resource_issue_categories_follow_catalog(self):
        form=yaml.safe_load((ROOT/'.github/ISSUE_TEMPLATE/resource-request.yml').read_text())
        field=next(x for x in form['body'] if x.get('id')=='category')
        options=set(field['attributes']['options'])
        self.assertEqual(options,{x['category'] for x in self.resources}|{'other'})

    def test_complete_organizer_and_judge_operations_exist(self):
        required=[
            'organizers/budget-and-sponsorship.md','organizers/challenge-design.md',
            'organizers/venue-and-logistics.md','organizers/virtual-and-hybrid.md',
            'organizers/accessibility-and-inclusion.md','organizers/post-event.md',
            'organizers/templates/incident-record.md','judges/calibration.md',
            'judges/conflicts.md','judges/feedback.md'
        ]
        for path in required:
            self.assertTrue((ROOT/path).is_file(),path)

if __name__=='__main__': unittest.main()
