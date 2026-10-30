#!/usr/bin/env python3
"""Fill marketIdMD (FanDuel Maryland, 724.x) for every leg in picks.json that has a PA marketId (742.x).
Same method as King Ferdinand's md.py: find the PA market's eventId/marketType/marketName, fetch the MD
event page for that event, and match on same marketType+marketName with a shared (selectionId,handicap)."""
import json,re,glob,urllib.request
K='FhMFpcPWXMeyZxOx'
def get(u):
  try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=20))
  except Exception as e: return {}
d=json.load(open('picks.json'))
legs=d['singles']+[l for p in d['parlays']+d['lottery'] for l in p['legs']]
need={l['marketId'] for l in legs if l.get('marketId')}
info={}
def scan(o):
  for m in ((o.get('attachments') or {}).get('markets') or {}).values():
    if m.get('marketId') in need: info[m['marketId']]=m
for f in glob.glob('/workspace/*.json')+glob.glob('/workspace/kfsp/.cache/*'):
  try: scan(json.load(open(f)))
  except Exception: pass
if need-set(info):
  for pg in ['nba','nhl','ncaaf','nfl','soccer','tennis','ncaab','mlb']:
    scan(get(f'https://sbapi.pa.sportsbook.fanduel.com/api/content-managed-page?page=CUSTOM&customPageId={pg}&_ak={K}&timezone=America/New_York'))
# event pages on PA for leftovers need eventIds; take them from MD tabs below
evs={}
for m in info.values(): evs.setdefault(m['eventId'],set())
mdm={}
for ev in evs:
  for tab in ['','popular','player-points','player-props','quarters','goals','alternates','1st-quarter','points']:
    o=get(f'https://sbapi.md.sportsbook.fanduel.com/api/event-page?_ak={K}&eventId={ev}'+(f'&tab={tab}' if tab else ''))
    for m in ((o.get('attachments') or {}).get('markets') or {}).values():
      mdm.setdefault((m['eventId'],m.get('marketType'),m.get('marketName')),[]).append(m)
sig=lambda m:{(r['selectionId'],r.get('handicap',0)) for r in m.get('runners',[])}
mp={}
for pid,m in info.items():
  for c in mdm.get((m['eventId'],m.get('marketType'),m.get('marketName')),[]):
    if sig(m)&sig(c): mp[pid]=c['marketId']; break
n=0
for l in legs:
  if l.get('marketId') in mp: l['marketIdMD']=mp[l['marketId']]; n+=1
  else: l.pop('marketIdMD',None)
json.dump(d,open('picks.json','w'),indent=1)
print(f'md_map: {n}/{len(legs)} legs got marketIdMD ({len(info)}/{len(need)} PA markets found)')
