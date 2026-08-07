#!/usr/bin/env python3
"""Generate every catalog view from catalog/resources.json."""
from __future__ import annotations
import argparse, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog/resources.json"
START = "<!-- catalog:start -->"
END = "<!-- catalog:end -->"

def write_lf(path: Path, text: str) -> None:
    """Write generated UTF-8 text with deterministic LF line endings."""
    normalized=text.replace("\r\n","\n").replace("\r","\n")
    path.write_bytes(normalized.encode("utf-8"))

def display(value: str) -> str:
    return value.replace("-", " ").title()

def table(items):
    lines=["| Resource | Best for | Cost | Source | Risk |", "| --- | --- | --- | --- | --- |"]
    for x in items:
        lines.append(f"| [{x['name']}]({x['url']}) | {x['best_for']} | {x['cost']} | {display(x['source_type'])} | {display(x['risk_level'])} |")
    return "\n".join(lines)

def replace_region(path: Path, content: str):
    text=path.read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise RuntimeError(f"missing catalog markers: {path}")
    before, rest=text.split(START,1); _, after=rest.split(END,1)
    return before+START+"\n"+content.rstrip()+"\n"+END+after

def render(data):
    resources=data['resources']; date=data['generated_on']; outputs={}
    by=defaultdict(list)
    for x in resources: by[x['category']].append(x)
    for values in by.values(): values.sort(key=lambda x:x['name'].casefold())

    lines=["# Resource Catalog", "", "The catalog is generated from `catalog/resources.json`; edit the data source rather than generated category pages.", ""]
    for cat in sorted(by):
        lines += [f"## {display(cat)}", "", table(by[cat]), ""]
    outputs[ROOT/'catalog/INDEX.md']="\n".join(lines).rstrip()+"\n"

    dimensions=[('TAGS.md','Tags',Counter(t for x in resources for t in x['tags'])),
                ('AUDIENCES.md','Audiences',Counter(t for x in resources for t in x['audiences'])),
                ('STAGES.md','Lifecycle stages',Counter(t for x in resources for t in x['stages'])),
                ('PLATFORMS.md','Platforms',Counter(t for x in resources for t in x['platforms'])),
                ('RISKS.md','Risk levels',Counter(x['risk_level'] for x in resources)),
                ('COSTS.md','Cost models',Counter(x['cost'] for x in resources)),
                ('SOURCES.md','Source types',Counter(x['source_type'] for x in resources))]
    for filename,title,counts in dimensions:
        body=[f"# {title}","",f"Generated from catalog schema **2.0** on **{date}**.","",f"| {title[:-1] if title.endswith('s') else title} | Entries |","| --- | ---: |"]
        for k,v in sorted(counts.items(), key=lambda kv:(-kv[1],kv[0])): body.append(f"| {display(k)} | {v} |")
        outputs[ROOT/'catalog'/filename]="\n".join(body)+"\n"

    stats=["# Catalog Statistics","",f"Generated on **{date}** from schema **2.0**.","",f"Total resources: **{len(resources)}**","", "| Category | Entries |","| --- | ---: |"]
    for cat in sorted(by): stats.append(f"| {display(cat)} | {len(by[cat])} |")
    outputs[ROOT/'catalog/STATS.md']="\n".join(stats)+"\n"

    fresh=Counter(x['reviewed_on'] for x in resources)
    body=["# Review Freshness","","Active resources must receive editorial review at least every 180 days. Automated link checks do not replace editorial review.","","| Reviewed on | Entries |","| --- | ---: |"]
    for k,v in sorted(fresh.items(), reverse=True): body.append(f"| {k} | {v} |")
    outputs[ROOT/'catalog/FRESHNESS.md']="\n".join(body)+"\n"

    categories={'schema_version':'2.0','generated_on':date,'categories':[]}
    for cat in sorted(by):
        vals=by[cat]
        categories['categories'].append({'id':cat,'name':display(cat),'resource_count':len(vals),'tags':sorted({t for x in vals for t in x['tags']}),'stages':sorted({t for x in vals for t in x['stages']}),'platforms':sorted({t for x in vals for t in x['platforms']})})
    outputs[ROOT/'catalog/categories.json']=json.dumps(categories,indent=2)+"\n"
    search={'schema_version':'2.0','generated_on':date,'resources':resources}
    outputs[ROOT/'catalog/search-index.json']=json.dumps(search,indent=2,ensure_ascii=False)+"\n"

    resource_index=["# Hackathon Resource Library","","This library is generated from the canonical catalog. Edit `catalog/resources.json`, not the generated category pages.","","| Category | Entries | Main stages |","| --- | ---: | --- |"]
    for cat in sorted(by):
        stages=sorted({stage for item in by[cat] for stage in item['stages']})
        resource_index.append(f"| [{display(cat)}]({cat}/) | {len(by[cat])} | {', '.join(display(stage) for stage in stages)} |")
    resource_index += ["","## Focused packs","","Use [`packs/`](packs/) when the project type is known and the full catalog is too broad.","","## Curation","","Resources are selected for practical usefulness, canonical documentation, active maintenance, and a concrete hackathon use case. Inclusion is not an endorsement or a guarantee of pricing, availability, safety, or event eligibility.",""]
    outputs[ROOT/'resources/README.md']="\n".join(resource_index)

    for cat, vals in by.items():
        page=[f"# {display(cat)} Resources","",f"Curated resources for hackathon teams. Last catalog generation: **{date}**.","",table(vals),"","## Selection guidance","","Prefer the smallest tool the team already understands. Confirm current pricing, quotas, regional availability, event eligibility, and data-handling terms before committing the demo to a provider.",""]
        outputs[ROOT/'resources'/cat/'README.md']="\n".join(page)

    # Curated, task-oriented packs. The entries remain catalog records, not duplicated metadata.
    pack_specs={
      'first-hackathon': {'title':'First Hackathon Pack','categories':['hackathons','learning','collaboration','hosting','presentation'],'limit':18},
      'web-app': {'title':'Web Application Pack','categories':['frontend','backend','databases','authentication','hosting','testing'],'limit':24},
      'ai-app': {'title':'AI Application Pack','categories':['ai','vector-databases','datasets','observability','security'],'limit':24},
      'mobile-app': {'title':'Mobile Application Pack','categories':['mobile','backend','authentication','databases','testing'],'limit':20},
      'hardware-iot': {'title':'Hardware and IoT Pack','categories':['hardware','messaging','realtime','cloud','data-visualization'],'limit':20},
      'demo-day': {'title':'Demo Day Pack','categories':['presentation','media','observability','hosting','collaboration'],'limit':18},
      'organizer': {'title':'Organizer Pack','categories':['hackathons','collaboration','communications','presentation','accessibility','security'],'limit':24},
      'privacy-first': {'title':'Privacy-First Pack','categories':['security','authentication','databases','storage','ai'],'limit':20},
    }
    packs_dir=ROOT/'catalog/packs'; pages_dir=ROOT/'resources/packs'; packs_dir.mkdir(parents=True,exist_ok=True); pages_dir.mkdir(parents=True,exist_ok=True)
    for pid,spec in pack_specs.items():
        selected=[]
        for cat in spec['categories']:
            selected.extend(by.get(cat,[]))
        selected=selected[:spec['limit']]
        payload={'schema_version':'1.0','generated_on':date,'id':pid,'name':spec['title'],'resource_ids':[x['id'] for x in selected]}
        outputs[packs_dir/f'{pid}.json']=json.dumps(payload,indent=2)+"\n"
        outputs[pages_dir/f'{pid}.md']="\n".join([f"# {spec['title']}","","A focused subset of the canonical catalog for this delivery scenario.","",table(selected),"","Use this pack as a decision aid, not as a requirement to adopt every listed tool.",""])

    pack_index=["# Focused Resource Packs","","Packs are generated subsets of the canonical resource catalog for common hackathon scenarios.",""]
    for pid,spec in pack_specs.items():
        pack_index.append(f"- [{spec['title']}]({pid}.md)")
    pack_index += ["","A pack reduces decision time; it is not a requirement to use every listed service.",""]
    outputs[pages_dir/'README.md']="\n".join(pack_index)

    # Main README category cards and selected entries.
    category_lines=["<!--lint enable awesome-list-item-->","","## Curated Resources","",f"The canonical catalog currently contains **{len(resources)}** reviewed resources across **{len(by)}** categories. Each category page is generated from the machine-readable catalog.",""]
    for cat in sorted(by):
        category_lines += [f"### {display(cat)}", "", f"[Browse all {len(by[cat])} resources](resources/{cat}/).", ""]
        for x in by[cat][:3]: category_lines.append(f"- [{x['name']}]({x['url']}) - {x['best_for']}.")
        category_lines.append("")
    category_lines += ["<!--lint disable awesome-list-item-->", ""]
    outputs[ROOT/'README.md']=replace_region(ROOT/'README.md',"\n".join(category_lines))
    return outputs

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--check',action='store_true'); args=ap.parse_args()
    data=json.loads(CATALOG.read_text(encoding='utf-8')); outputs=render(data); bad=[]
    for path,content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8')!=content: bad.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True,exist_ok=True); write_lf(path,content)
    if bad:
        print('Generated files are stale:',*bad,sep='\n- '); return 1
    print(f"Catalog views {'verified' if args.check else 'generated'}: {len(outputs)} files")
    return 0
if __name__=='__main__': raise SystemExit(main())
