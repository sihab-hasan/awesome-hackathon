#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('--days',type=int,default=180);p.add_argument('--strict',action='store_true');a=p.parse_args()
 data=json.loads((ROOT/'catalog/resources.json').read_text())['resources'];today=date.today();due=[]
 for x in data:
  age=(today-date.fromisoformat(x['reviewed_on'])).days
  if x['status']=='active' and age>a.days: due.append((age,x))
 for age,x in sorted(due,reverse=True): print(f"{age:4} days  {x['id']}  {x['url']}")
 print(f"{len(due)} resource(s) exceed {a.days} days")
 return 1 if a.strict and due else 0
if __name__=='__main__': raise SystemExit(main())
