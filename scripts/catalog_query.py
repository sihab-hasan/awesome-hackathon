#!/usr/bin/env python3
"""Search and filter the local resource catalog without network access."""
from __future__ import annotations
import argparse, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'catalog/resources.json').read_text(encoding='utf-8'))['resources']

def main():
    p=argparse.ArgumentParser()
    p.add_argument('terms',nargs='*'); p.add_argument('--category'); p.add_argument('--tag'); p.add_argument('--source',choices=['official','primary','community'])
    p.add_argument('--audience',choices=['participant','organizer','mentor','judge','educator']); p.add_argument('--stage',choices=['discover','plan','build','test','deploy','demo','submit','organize','maintain'])
    p.add_argument('--platform',choices=['any','web','mobile','desktop','cloud','hardware','data','ai']); p.add_argument('--risk',choices=['low','medium','high']); p.add_argument('--json',action='store_true')
    a=p.parse_args(); terms=[x.casefold() for x in a.terms]; out=[]
    for x in DATA:
        hay=' '.join([x['name'],x['description'],x['best_for'],x['category'],*x['tags'],*x['audiences'],*x['stages'],*x['platforms']]).casefold()
        if terms and not all(t in hay for t in terms): continue
        if a.category and x['category']!=a.category: continue
        if a.tag and a.tag not in x['tags']: continue
        if a.source and x['source_type']!=a.source: continue
        if a.audience and a.audience not in x['audiences']: continue
        if a.stage and a.stage not in x['stages']: continue
        if a.platform and a.platform not in x['platforms']: continue
        if a.risk and x['risk_level']!=a.risk: continue
        out.append(x)
    if a.json: print(json.dumps(out,indent=2,ensure_ascii=False))
    else:
        for x in out: print(f"{x['name']}\n  {x['url']}\n  {x['best_for']} [{x['category']}; risk={x['risk_level']}]\n")
        print(f"{len(out)} result(s)")
if __name__=='__main__': main()
