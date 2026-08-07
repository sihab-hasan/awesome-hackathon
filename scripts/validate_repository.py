#!/usr/bin/env python3
"""Validate catalog semantics, generated views, repository structure, workflows, and links."""
from __future__ import annotations
from datetime import date, datetime, timedelta, timezone
import json, re, subprocess, sys, tomllib, urllib.parse

try:
    import yaml
except ImportError:
    yaml = None
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; CATALOG=ROOT/'catalog/resources.json'
SLUG=re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$'); LINK=re.compile(r'!?\[[^\]]*\]\(([^)]+)\)'); BAD_PLACEHOLDER=re.compile(r'\b(TODO|TBD|FIXME|COMING SOON|LOREM IPSUM)\b',re.I)
REQUIRED={'README.md','docs/README.md','docs/getting-started/quickstart.md','LICENSE','CONTRIBUTING.md','CODE_OF_CONDUCT.md','SECURITY.md','docs/maintainers/curation.md','docs/maintainers/governance.md','docs/maintainers/maintenance.md','docs/maintainers/releasing.md','docs/maintainers/quality-standard.md','docs/maintainers/resource-lifecycle.md','docs/repository/architecture.md','docs/maintainers/playbook.md','docs/maintainers/editorial-checklist.md','catalog/resources.json','catalog/schema.json','scripts/generate_catalog.py','scripts/catalog_query.py','scripts/validate_repository.py','scripts/validate_structured_files.py','requirements-validation.txt','tests/test_repository.py','.github/workflows/ci.yml','.github/workflows/link-check.yml','.github/workflows/pages.yml','.github/workflows/release.yml'}
ENUM={'source_type':{'official','primary','community'},'status':{'active','deprecated','archived'},'risk_level':{'low','medium','high'}}
ARRAY_ENUM={'audiences':{'participant','organizer','mentor','judge','educator'},'stages':{'discover','plan','build','test','deploy','demo','submit','organize','maintain'},'platforms':{'any','web','mobile','desktop','cloud','hardware','data','ai'}}
KEYS={'id','category','name','url','description','tags','cost','official','source_type','status','best_for','reviewed_on','audiences','stages','platforms','risk_level'}

def fail(errors,msg): errors.append(msg)
def parse_iso(v,label,errors):
    try:return date.fromisoformat(v)
    except Exception: fail(errors,f'{label}: invalid ISO date {v!r}')

LOCAL_TOP_LEVEL_DIRS={'.git','.venv','venv','site','.pytest_cache','.mypy_cache','.ruff_cache'}

def tracked_files():
    """Return tracked files in a live Git checkout, otherwise None."""
    if not (ROOT/'.git').exists():
        return None
    try:
        result=subprocess.run(
            ['git','ls-files','-z'],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    paths=[]
    for raw in result.stdout.split(b'\0'):
        if not raw:
            continue
        try:
            rel=Path(raw.decode('utf-8'))
        except UnicodeDecodeError:
            continue
        path=ROOT/rel
        if path.is_file() or path.is_symlink():
            paths.append(path)
    return paths

def repository_paths():
    """Yield maintained repository paths, excluding local checkout/build metadata."""
    tracked=tracked_files()
    if tracked is not None:
        yield from tracked
        return
    for path in ROOT.rglob('*'):
        rel=path.relative_to(ROOT)
        if rel.parts and rel.parts[0] in LOCAL_TOP_LEVEL_DIRS:
            continue
        yield path

def repository_files():
    for path in repository_paths():
        if path.is_file():
            yield path

def validate_catalog(errors):
    data=json.loads(CATALOG.read_text(encoding='utf-8'))
    if set(data)!={'schema_version','generated_on','resources'}: fail(errors,'catalog root keys invalid')
    if data.get('schema_version')!='2.0': fail(errors,'catalog schema_version must be 2.0')
    today=datetime.now(timezone(timedelta(hours=6))).date(); generated=parse_iso(data.get('generated_on'),'generated_on',errors)
    if generated and generated>today: fail(errors,'generated_on is future dated')
    ids=set(); urls=set(); names=set(); categories=set()
    for i,x in enumerate(data.get('resources',[]),1):
        label=f'resource {i}'
        if set(x)!=KEYS: fail(errors,f'{label}: keys differ; missing={sorted(KEYS-set(x))}, extra={sorted(set(x)-KEYS)}')
        if not SLUG.fullmatch(str(x.get('id',''))): fail(errors,f'{label}: invalid id')
        if x.get('id') in ids: fail(errors,f'{label}: duplicate id {x.get("id")}')
        ids.add(x.get('id'))
        cat=x.get('category'); categories.add(cat)
        if not SLUG.fullmatch(str(cat or '')): fail(errors,f'{label}: invalid category')
        name=x.get('name',''); key=name.casefold()
        if key in names: fail(errors,f'{label}: duplicate global resource name')
        names.add(key)
        url=x.get('url','')
        if not isinstance(url,str) or not url.startswith('https://') or not urllib.parse.urlparse(url).netloc: fail(errors,f'{label}: URL must be valid HTTPS')
        if url in urls: fail(errors,f'{label}: duplicate URL')
        urls.add(url)
        if any(k.lower().startswith('utm_') for k in urllib.parse.parse_qs(urllib.parse.urlparse(url).query)): fail(errors,f'{label}: tracking parameters forbidden')
        if not (20<=len(x.get('description',''))<=240): fail(errors,f'{label}: description length')
        if not (8<=len(x.get('best_for',''))<=160): fail(errors,f'{label}: best_for length')
        tags=x.get('tags');
        if not isinstance(tags,list) or not tags or len(tags)!=len(set(tags)) or any(not SLUG.fullmatch(str(t)) for t in tags): fail(errors,f'{label}: invalid tags')
        if not isinstance(x.get('official'),bool): fail(errors,f'{label}: official must be boolean')
        for field,allowed in ENUM.items():
            if x.get(field) not in allowed: fail(errors,f'{label}: invalid {field}')
        if isinstance(x.get('official'),bool) and x.get('official')!=(x.get('source_type')=='official'): fail(errors,f'{label}: official/source_type mismatch')
        for field,allowed in ARRAY_ENUM.items():
            vals=x.get(field)
            if not isinstance(vals,list) or not vals or len(vals)!=len(set(vals)) or any(v not in allowed for v in vals): fail(errors,f'{label}: invalid {field}')
        reviewed=parse_iso(x.get('reviewed_on'),f'{label} reviewed_on',errors)
        if reviewed:
            if reviewed>today: fail(errors,f'{label}: future review date')
            if x.get('status')=='active' and (today-reviewed).days>180: fail(errors,f'{label}: review older than 180 days')
    if len(categories)<30: fail(errors,'catalog should retain broad category coverage')
    return data

def validate_files(errors):
    for path in REQUIRED:
        if not (ROOT/path).exists(): fail(errors,f'missing required path: {path}')
    for p in repository_paths():
        if p.is_symlink():
            try:p.resolve().relative_to(ROOT.resolve())
            except ValueError: fail(errors,f'escaping symlink: {p.relative_to(ROOT)}')
        if not p.is_file(): continue
        rel=p.relative_to(ROOT)
        if '__pycache__' in p.parts or p.suffix in {'.pyc','.pyo'}: fail(errors,f'generated Python cache committed: {rel}')
        if p.stat().st_size==0: fail(errors,f'empty file: {rel}')
        if p.suffix.lower() in {'.md','.py','.json','.yml','.yaml','.toml','.txt','.cff','.svg'} or p.name in {'Makefile','VERSION','LICENSE'}:
            try:
                raw=p.read_bytes()
                if b'\r\n' in raw: fail(errors,f'CRLF line endings: {rel}')
                text_value=raw.decode('utf-8')
                if any(line.endswith((' ','\t')) for line in text_value.splitlines()): fail(errors,f'trailing whitespace: {rel}')
            except UnicodeDecodeError:
                fail(errors,f'non-UTF-8 maintained text file: {rel}')
        if '.git' in rel.parts: fail(errors,f'embedded git metadata: {rel}')
        if p.suffix=='.json':
            try:json.loads(p.read_text(encoding='utf-8'))
            except Exception as e: fail(errors,f'invalid JSON {rel}: {e}')
        if p.suffix=='.md':
            text=p.read_text(encoding='utf-8')
            if not text.startswith('#'): fail(errors,f'missing top heading: {rel}')
            if '/mnt/data/' in text or 'C:\\' in text: fail(errors,f'environment path: {rel}')
            if BAD_PLACEHOLDER.search(text) and rel.as_posix() != 'docs/project/roadmap.md': fail(errors,f'unresolved placeholder: {rel}')
            for raw in LINK.findall(text):
                target=raw.strip().split()[0].strip('<>')
                if target.startswith(('http://','https://','mailto:','#')): continue
                target=target.split('#',1)[0]
                if not target: continue
                dest=(p.parent/urllib.parse.unquote(target)).resolve()
                try:dest.relative_to(ROOT.resolve())
                except ValueError: fail(errors,f'link escapes repository: {rel} -> {target}'); continue
                if not dest.exists(): fail(errors,f'broken internal link: {rel} -> {target}')

def _flatten_nav(value):
    paths=[]
    if isinstance(value,str): paths.append(value)
    elif isinstance(value,list):
        for item in value: paths.extend(_flatten_nav(item))
    elif isinstance(value,dict):
        for item in value.values(): paths.extend(_flatten_nav(item))
    return paths

def validate_documentation_navigation(errors):
    if yaml is None:
        fail(errors,'PyYAML is required for documentation navigation validation')
        return
    try:
        config=yaml.safe_load((ROOT/'mkdocs.yml').read_text(encoding='utf-8')) or {}
    except Exception as exc:
        fail(errors,f'mkdocs.yml parse failure: {exc}')
        return
    docs_dir=config.get('docs_dir','docs')
    handbook=(ROOT/docs_dir).resolve()
    if not handbook.is_dir():
        fail(errors,f'mkdocs docs_dir does not exist: {docs_dir}')
        return
    actual={str(p.relative_to(handbook)).replace('\\','/') for p in handbook.rglob('*.md')}
    nav=set(_flatten_nav(config.get('nav',[])))
    missing=sorted(actual-nav)
    unknown=sorted(x for x in nav if x.endswith('.md') and x not in actual)
    if missing: fail(errors,f'mkdocs nav missing pages: {missing}')
    if unknown: fail(errors,f'mkdocs nav references missing pages: {unknown}')

def validate_generated_views(errors,data):
    categories={x['category'] for x in data.get('resources',[])}
    for category in categories:
        page=ROOT/'resources'/category/'README.md'
        if not page.is_file(): fail(errors,f'missing generated category page: {category}')
    try:
        index=json.loads((ROOT/'catalog/search-index.json').read_text(encoding='utf-8'))
        indexed=index.get('resources',index) if isinstance(index,dict) else index
        if not isinstance(indexed,list) or len(indexed)!=len(data.get('resources',[])):
            fail(errors,'search index resource count mismatch')
    except Exception as exc:
        fail(errors,f'search index validation failure: {exc}')

def validate_issue_forms(errors,data):
    if yaml is None: return
    path=ROOT/'.github/ISSUE_TEMPLATE/resource-request.yml'
    try:
        form=yaml.safe_load(path.read_text(encoding='utf-8'))
        category_field=next(x for x in form.get('body',[]) if x.get('id')=='category')
        options=set(category_field.get('attributes',{}).get('options',[]))
        expected={x['category'] for x in data.get('resources',[])}|{'other'}
        if options!=expected: fail(errors,f'resource issue categories out of sync: missing={sorted(expected-options)}, extra={sorted(options-expected)}')
    except Exception as exc:
        fail(errors,f'resource issue form validation failure: {exc}')

def validate_workflows(errors):
    required={'ci.yml','link-check.yml','pages.yml','release.yml','codeql.yml','dependency-review.yml','awesome-lint.yml','markdown-lint.yml','spell-check.yml','catalog-review.yml'}
    present={p.name for p in (ROOT/'.github/workflows').glob('*.yml')}
    for name in sorted(required-present): fail(errors,f'missing workflow: {name}')
    for p in (ROOT/'.github/workflows').glob('*.yml'):
        text=p.read_text(encoding='utf-8')
        if 'pull_request_target:' in text: fail(errors,f'unsafe pull_request_target: {p.name}')
        if re.search(r'permissions:\s*write-all',text): fail(errors,f'overbroad write-all: {p.name}')
        if 'actions/checkout@v6' in text: fail(errors,f'outdated checkout major in {p.name}; use v7')
        if 'github/codeql-action/' in text and '@v3' in text: fail(errors,f'outdated CodeQL major in {p.name}; use v4')

def validate_versions(errors,data):
    version=(ROOT/'VERSION').read_text().strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+',version): fail(errors,'VERSION is not semantic')
    py=tomllib.loads((ROOT/'pyproject.toml').read_text())
    if py.get('project',{}).get('version')!=version: fail(errors,'pyproject version mismatch')
    c=(ROOT/'CITATION.cff').read_text()
    if f'version: {version}' not in c: fail(errors,'CITATION version mismatch')
    readme=(ROOT/'README.md').read_text()
    count=len(data['resources'])
    if f'resources-{count}-' not in readme: fail(errors,'README resource badge/count stale')

def main():
    errors=[]
    try:data=validate_catalog(errors)
    except Exception as e: errors.append(f'catalog parse failure: {e}'); data={'resources':[]}
    validate_files(errors)
    validate_generated_views(errors,data)
    validate_documentation_navigation(errors)
    validate_issue_forms(errors,data)
    validate_workflows(errors)
    validate_versions(errors,data)
    if errors:
        print('VALIDATION FAILED'); print('\n'.join(f'- {e}' for e in errors)); return 1
    files_list=list(repository_files()); md=sum(1 for p in files_list if p.suffix.lower()=='.md'); files=len(files_list)
    print(f'VALIDATION PASSED: {len(data["resources"])} resources, {md} Markdown files, {files} total files')
    return 0
if __name__=='__main__': raise SystemExit(main())
