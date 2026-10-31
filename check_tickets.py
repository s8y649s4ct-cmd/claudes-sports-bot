#!/usr/bin/env python3
"""Fail (exit 1) if any parlay/lottery ticket can't be placed as one FanDuel parlay:
two legs from the same event, a market that is not OPEN / already in play / started,
a selection that is not ACTIVE, or a market on a restricted feed (main-line markets with
canTurnInPlay=false such as FCS, or non-standard markets with sgmMarket=false).
Stores each leg's eventId in picks.json so later runs are faster."""
import json,sys,glob,os,urllib.request,datetime
K='FhMFpcPWXMeyZxOx'
def get(u):
  try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=25))
  except Exception: return {}
d=json.load(open('picks.json'))
tickets=d['parlays']+d['lottery']
legs=[l for t in tickets for l in t['legs']]
need={l['marketId'] for l in legs}
info={}
def scan(o):
  for m in ((o.get('attachments') or {}).get('markets') or {}).values():
    if m.get('marketId') in need: info[m['marketId']]=m
evs={l['eventId'] for l in legs if l.get('eventId')}
for f in sorted(glob.glob('/workspace/*.json'),key=os.path.getmtime):   # cached feeds give eventIds
  try:
    for m in json.load(open(f))['attachments']['markets'].values():
      if m.get('marketId') in need: evs.add(m['eventId'])
  except Exception: pass
if need-{m for m in info}:
  for pg in ['nba','nhl','ncaaf','nfl','soccer','tennis','cfl','ncaab','mlb']:
    o=get(f'https://sbapi.pa.sportsbook.fanduel.com/api/content-managed-page?page=CUSTOM&customPageId={pg}&_ak={K}&timezone=America/New_York')
    for m in ((o.get('attachments') or {}).get('markets') or {}).values():
      if m.get('marketId') in need: evs.add(m['eventId'])
for e in evs:   # live state comes from the event pages
  for tab in ['','popular','alternates','goals','shots','player-props','team-props','points','player-points','player-rebounds','player-assists','player-threes','player-combos','quarters','1st-quarter']:
    scan(get(f'https://sbapi.pa.sportsbook.fanduel.com/api/event-page?_ak={K}&eventId={e}'+(f'&tab={tab}' if tab else '')))
    if not (need-set(info)): break
now=datetime.datetime.now(datetime.timezone.utc).isoformat()[:19]
PROPS=('PLAYER','TO_RECORD','TO_SCORE')
bad=[]
for t in tickets:
  seen={}
  for l in t['legs']:
    m=info.get(l['marketId']); tag=f"[{t['name']}] {l['pick']}"
    if not m: bad.append(tag+': market not found on FanDuel (closed or removed)'); continue
    l['eventId']=m['eventId']
    if m['eventId'] in seen: bad.append(f"{tag}: same event as {seen[m['eventId']]}")
    seen[m['eventId']]=l['pick']
    if m.get('marketStatus')!='OPEN' or m.get('inPlay'): bad.append(tag+f": market {m.get('marketStatus')} inPlay={m.get('inPlay')}")
    if m.get('marketTime','9')[:19]<=now: bad.append(tag+': already started')
    r=[x for x in m.get('runners',[]) if str(x['selectionId'])==str(l['selectionId'])]
    if not r or r[0].get('runnerStatus')!='ACTIVE': bad.append(tag+': selection not active')
    if m.get('sgmMarket') is False: bad.append(tag+f": non-standard market ({m.get('marketType')}, sgmMarket=false)")
    if m.get('canTurnInPlay') is False and not any(p in m.get('marketType','') for p in PROPS): bad.append(tag+': restricted feed (canTurnInPlay=false, e.g. FCS)')
json.dump(d,open('picks.json','w'),indent=1)
if bad: print('check_tickets FAILED:\n  '+'\n  '.join(bad)); sys.exit(1)
print(f'check_tickets: OK ({len(tickets)} tickets, {len(legs)} legs, one leg per event, all open)')
