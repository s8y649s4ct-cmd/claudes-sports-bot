#!/usr/bin/env python3
"""Sun Nov 8, 2026 10:30 AM ET run: no new settlements since 7:30 AM; add 2-leg-focused card + Best Shot."""
import json, copy, os, datetime
src = open('/workspace/csb/build_sat_pm.py').read().split("if os.environ.get('KEEP')")[0]
src = src.replace("/workspace/satpm/fresh_ev_", "/workspace/sunam/fresh_ev_")
exec(src)
p = json.load(open('/workspace/csb/picks.json')); H = p['results']['history']
used_events, used_picks = set(), set()
pend_events = set()
for x in H:
    if x.get('result') == 'pending':
        for l in x.get('legs') or []:
            used_picks.add(l['pick']); pend_events.add(l['event'])
def make_leg(eid, market_pred, runner_pred, pick, sport, reason):
    ev, mkts = load_event(eid)
    sel = find_runner(mkts, market_pred, runner_pred)
    if not sel: raise SystemExit(f'no selection {pick}')
    if eid in used_events or pick in used_picks or ev['name'] in pend_events: raise SystemExit(f'reuse {pick}')
    t = datetime.datetime.fromisoformat(ev['openDate'].replace('Z', '+00:00'))
    if t < NOW + timedelta(minutes=60): raise SystemExit(f'too soon {pick}')
    used_events.add(eid); used_picks.add(pick)
    return {'pick': pick, 'market': sel['market'], 'odds': sel['odds'], 'sport': sport, 'event': ev['name'],
            'start': start_et(ev['openDate']), 'reason': reason, 'marketId': sel['marketId'],
            'selectionId': sel['selectionId'], 'eventId': sel['eventId']}
ALT = lambda mn: mn == 'Alternate Spread'
ALTN = lambda mn: mn.startswith('Alternate Spread')
APL = lambda mn: mn == 'Alternate Puck Line'
ML = lambda mn: mn == 'Moneyline'
rn = lambda n: (lambda r, m: r.get('runnerName') == n)
rh = lambda n, h: (lambda r, m: r.get('runnerName') == n and float(r.get('handicap') or 0) == h)
new = []
def add(name, specs, reason, stake=10, lst=None):
    legs = [make_leg(*s) for s in specs]
    o, _ = combine([l['odds'] for l in legs])
    t = {'name': name, 'odds': o, 'stake': stake, 'legs': legs, 'reason': reason}
    (lst if lst is not None else new).append(t); return t
add('Bears Home Cushion + Devils Road Ice', [
 (36244879, ALT, rn('Chicago Bears (+3.5)'), 'Chicago Bears +3.5', 'NFL', 'Chicago is the -6.5 home favorite on Sunday Night Football; +3.5 is 10 points of cushion and crosses the key number 3, so the Bears only lose this leg if Tampa wins by 4+ in Chicago. Bucs are without edge rusher Yaya Diaby; Chicago has no inactives of note.'),
 (36291491, APL, rn('New Jersey Devils +1.5'), 'New Jersey Devils +1.5', 'NHL', 'NJ is the -154 road favorite at Toronto, and the Leafs are on the second night of a back-to-back after losing 4-2 at home to Montreal Saturday. +1.5 covers any Devils win or one-goal loss.'),
], 'Home NFL favorite bought to +3.5 plus a road NHL favorite at +1.5 against a tired team. Both legs need a multi-score upset to lose.')
add('Texans Bought-Down + Sabres Home Ice', [
 (36244874, ALT, rn('Houston Texans (+4.5)'), 'Houston Texans +4.5', 'NFL', 'Houston is -5.5 at the Chargers, whose offensive line is gutted (Slater, Pipkins, Biadasz, Penning on IR) and whose secondary is missing Derwin James, Deane Leonard and Kendall Williamson. +4.5 is 10 points off the main: Houston can lose by up to 4.'),
 (36291493, APL, rn('Buffalo Sabres +1.5'), 'Buffalo Sabres +1.5', 'NHL', 'Pick\'em game (-106) at home; +1.5 means Buffalo only fails if it loses by 2+ on home ice. Lessons say pick\'em +1.5 legs hold up far better than coin-flip MLs.'),
], 'Bought-down road favorite against a depleted roster plus home pick\'em +1.5.')
add('Eagles Big Home Cushion + Saints Home Cushion', [
 (36244873, ALT, rn('Philadelphia Eagles (+13.5)'), 'Philadelphia Eagles +13.5', 'NFL', 'Eagles are only +3 at home vs the Giants (total 38.5, a low-scoring script), so +13.5 is 10.5 points beyond the main and past both 7 and 10. Philly is missing DeVonta Smith, but a 14+ point home loss in a 38.5-total divisional game is rare.'),
 (36244869, ALT, rn('New Orleans Saints (+6.5)'), 'New Orleans Saints +6.5', 'NFL', 'Saints are -3.5 home favorites vs Cleveland in a 42.5-total game; +6.5 gives 10 points of cushion. Lesson: bought-down home favorites with 9+ points of cushion keep cashing.'),
], 'Two home NFL teams with 10+ points of cushion in low-total games.')
add('Patriots Home Cushion + Rams Bought-Down', [
 (36244877, ALT, rn('New England Patriots (+6.5)'), 'New England Patriots +6.5', 'NFL', 'NE is -3 at home and Green Bay is short-handed: Micah Parsons, Zaire Franklin, starting OL Rhyan and Glover all out. +6.5 is 9.5 points of cushion (A.J. Brown out for NE is the risk).'),
 (36244876, ALT, rn('Los Angeles Rams (+5.5)'), 'Los Angeles Rams +5.5', 'NFL', 'Rams are -4.5 at 2-4-1 Washington, which is missing WRs Dyami Brown and Treylon Burks. +5.5 is 10 points of cushion: the Rams can lose by up to 5.'),
], 'Home favorite and road favorite, both bought 9.5-10 points off the main.')
add('Cowboys Bought-Down + Lightning Road Ice', [
 (36244868, ALT, rn('Dallas Cowboys (+5.5)'), 'Dallas Cowboys +5.5', 'NFL', 'Dallas is -4.5 at 2-6 Indianapolis; +5.5 is 10 points of cushion. Colts are missing LB Davis-Gaither, CB Walley and S Haulcy.'),
 (36291492, APL, rn('Tampa Bay Lightning +1.5'), 'Tampa Bay Lightning +1.5', 'NHL', 'TB is the -142 road favorite at Winnipeg; +1.5 covers any win or one-goal loss.'),
], 'Bought-down road favorite plus road NHL favorite at +1.5.')
add('Hoops Bought-Down Hosts II', [
 (36293099, ALTN, rh('South Carolina', -8.5), 'South Carolina -8.5', 'NCAAB', 'SEC host is -17.5 vs SE Missouri State (ML -3500); -8.5 leaves 9 points of cushion. Bought-down home favorites with 9+ cushion went 3/3 Saturday.'),
 (36293113, ALTN, rh('Drake', -4.5), 'Drake -4.5', 'NCAAB', 'Drake is -13.5 at home vs SWAC Southern (ML -1250); -4.5 leaves 9 points of cushion.'),
], 'Repeat of Saturday\'s winning pattern: big home favorites bought down 9 points.')
# Best Shot
bs = add('Best Shot $500K', [
 (36293174, ALTN, rh('Houston', -10.5), 'Houston -10.5', 'NCAAB', 'Houston (ML -4500) is -19.5 at Cal; -10.5 gives 9 points of cushion for an elite defense.'),
 (36293164, ALTN, rh('William & Mary', -3.5), 'William & Mary -3.5', 'NCAAB', 'W&M is -9.5 at home vs Norfolk State (ML -520); -3.5 leaves 6 points of cushion.'),
 (36293109, ALTN, rh('St Thomas', -2.5), 'St Thomas -2.5', 'NCAAB', 'St Thomas is -8.5 at home vs Green Bay (ML -385); -2.5 leaves 6 points of cushion.'),
 (36293175, ALTN, rh("Hawai'i", -2.5), "Hawai'i -2.5", 'NCAAB', 'Hawaii is -8.5 at home (ML -360) and UT Arlington makes the long trip; -2.5 leaves 6 points of cushion.'),
 (36293112, ALTN, rh('Air Force', -0.5), 'Air Force ML (-0.5)', 'NCAAB', 'Air Force -6.5 at home at altitude vs Idaho State.'),
 (36293106, ALTN, rh('Western Michigan', 0.5), 'Western Michigan +0.5', 'NCAAB', 'WMU -5.5 at home vs Campbell; needs a win.'),
 (36293108, ALTN, rh('Lehigh', 0.5), 'Lehigh +0.5', 'NCAAB', 'Lehigh -5.5 at home vs Brown; needs a win.'),
 (36293171, ALTN, rh('Pittsburgh', 7.5), 'Pittsburgh +7.5', 'NCAAB', 'Pitt is -2.5 at Penn State; +7.5 is 10 points of cushion.'),
 (36291490, APL, rn('Philadelphia Flyers +1.5'), 'Philadelphia Flyers +1.5', 'NHL', 'Road pick\'em +1.5 (lessons: road +1.5 in a pick\'em holds up; avoid the struggling-Calgary home side).'),
], 'Highest-probability legs left after the 2-leg card: home college favorites (mostly just needing to win), one 10-point road cushion plus one pick\'em +1.5. Stops at 9 legs (four more home favorites are on a restricted FanDuel feed that cannot be parlayed): adding more would mean 60-65% legs, so it is far short of the $5K target.', stake=5, lst=[])
bs = bs
# keep this morning's still-pending 2-leg special tickets on the card
parlays = p['parlays'] + new
D, R = '2026-11-08', '10:30 AM'
for t, typ in [(t, 'parlay') for t in new] + [(bs, 'lottery')]:
    if not already_in_history(H, t['name'], D, R):
        H.append({'date': D, 'run': R, 'type': typ, 'name': t['name'], 'odds': t['odds'], 'stake': t['stake'], 'result': 'pending', 'profit': 0,
                  'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'pending'} for l in t['legs']],
                  'whyExplanation': 'Pending.', 'lesson': ''})
totals = recompute_totals(H)
p['updated'] = p['results']['updated'] = 'Sun Nov 8, 2026 10:30 AM ET'
p['run'] = 'Sunday 10:30 AM: six new 2-leg parlays (every leg 9-10+ points or 1.5 goals beyond the main) added to this morning\'s four, plus a 12-leg Best Shot. No singles cleared the edge bar. Nothing new settled since 7:30 AM.'
p['singles'], p['parlays'], p['lottery'] = [], parlays, [bs]
p['results']['totals'] = totals
for k in ('singles', 'parlays', 'lottery'): p['results'][k] = copy.deepcopy(totals[k])
json.dump(p, open('/workspace/csb/picks.json', 'w'), indent=1)
print(totals['overall'], totals['legs'])
for t in new + [bs]: print(t['name'], t['odds'], [(l['pick'], l['odds'], l['start']) for l in t['legs']])
