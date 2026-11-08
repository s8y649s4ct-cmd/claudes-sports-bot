#!/usr/bin/env python3
"""Sun Nov 8, 2026 special: grade Sat tickets + 2-leg parlay card."""
import json, copy, os, datetime
src = open('/workspace/csb/build_sat_pm.py').read().split("if os.environ.get('KEEP')")[0]
src = src.replace("/workspace/satpm/fresh_ev_", "/workspace/sun/fresh_ev_")
exec(src)
p = json.load(open('/workspace/csb/picks.json')); H = p['results']['history']
G = {  # idx: (result or None, {pick:(res,actual)}, why, lesson)
107: ('won', {'Michigan State +13.5': ('hit', 'MSU won 15-6')}, 'Michigan State won outright 15-6 at Michigan.', 'Healthy quality dog with 13.5 cushion cashed.'),
110: ('lost', {'Toronto Maple Leafs +1.5': ('miss', 'MTL 4-2'), 'Minnesota Wild +1.5': ('hit', 'lost 4-3 OT'), 'New York Islanders +1.5': ('hit', 'lost 5-4 OT')}, 'Toronto lost 4-2 at home to Montreal; Wild and Isles both covered +1.5 in OT losses.', 'Home +1.5 vs a strong rival can still lose by 2 (empty-net).'),
112: ('lost', {'Texas Tech -13.5': ('miss', 'won 53-48'), 'Houston -8.5': ('miss', 'won 31-24'), 'Notre Dame -3.5': ('hit', 'won 31-24')}, 'Texas Tech won by only 5 and Houston by 7.', 'Double-digit CFB spreads in shootouts are not safe legs.'),
113: ('lost', {'Ohio State -4.5': ('miss', 'Oregon won 41-28'), 'Seattle Kraken +1.5': ('hit', 'lost 4-3'), 'Ottawa Senators +1.5': ('hit', 'won 4-2'), 'Carolina Hurricanes ML': ('hit', 'won 9-2'), 'Edmonton Oilers ML': ('hit', 'won 4-2'), 'Dallas Stars ML': ('hit', 'won 4-3'), 'Navy ML': ('hit', 'won 42-35')}, 'Ohio State lost 41-28 at home to Oregon.', 'Top-10 vs top-10 CFB favorites are coin flips, not Best Shot legs.'),
114: ('won', {'Arkansas +9.5': ('hit', 'lost 26-23')}, 'Arkansas lost by 3, well inside +9.5.', ''),
117: ('lost', {"Saint Joseph's ML": ('hit', 'won 67-57 OT'), 'Miami (OH) ML': ('hit', 'won 80-73'), 'Dayton ML': ('miss', 'lost 81-76 OT')}, 'Dayton lost at home in OT to Northern Illinois.', 'Early-season college locks can still lose; SJU also needed OT.'),
118: ('lost', {'Washington Wizards +14.5': ('miss', 'lost 114-75'), 'Indiana Pacers +12.5': ('hit', 'lost by 12'), 'Brooklyn Nets +12.5': ('hit', 'lost by 3')}, 'Wizards lost by 39 at OKC (second night of back-to-back).', 'No dog cushions vs OKC, and none for teams on a back-to-back.'),
121: ('won', {'Iowa -3.5': ('hit', 'won 24-10')}, 'Iowa won by 14 vs the backup-QB Wildcats.', 'Fade-the-backup-QB worked.'),
122: ('won', {'Oklahoma @ Florida Under 43.5': ('hit', '30 total')}, 'OU won 23-7; 30 total.', ''),
123: ('lost', {'Air Force @ Army Under 42.5': ('miss', '45 total')}, 'Air Force won 24-21; 45 total.', 'Service-academy unders are not automatic.'),
124: ('lost', {'San Diego FC v Sporting KC Over 2.5 Goals': ('miss', '0-1'), 'Minnesota Utd v San Jose Over 1.5 Goals': ('hit', '3-1'), 'Real Salt Lake v LA Galaxy Over 1.5 Goals': ('hit', '2-1')}, 'San Diego v SKC ended 0-1.', 'Over 2.5 even at -420 failed with nothing at stake for either side.'),
125: ('lost', {'Kentucky +14.5': ('miss', 'lost 34-6'), 'Georgia +7.5': ('hit', 'won 42-7'), 'Texas State +14.5': ('hit', 'won 42-21')}, 'Kentucky lost by 28 at Tennessee.', 'Road SEC dogs can get blown out even with two-score cushions.'),
126: ('won', {'Davidson -2.5': ('hit', 'won 88-76'), 'UC San Diego -1.5': ('hit', 'won 81-65'), 'High Point ML': ('hit', 'won 83-71')}, 'All three home favorites won by 12+.', 'Bought-down home favorites (9+ points of cushion) went 3/3.'),
127: ('lost', {'Wisconsin -7.5': ('hit', '31-10'), 'Mississippi State +6.5': ('hit', 'lost 25-23'), 'Louisiana +1.5': ('hit', 'won 28-26'), 'Boise State -6.5': ('hit', '64-38'), 'Jacksonville State -7.5': ('hit', '47-14'), 'Louisville -5.5': ('hit', '44-17'), 'Liberty -6.5': ('hit', '30-14'), 'Arizona State +4.5': ('hit', 'won 20-10'), 'Utah State +7.5': ('hit', 'won 17-10'), 'Hawaii +1.5': ('hit', 'won 17-14'), 'UNLV +5.5': ('miss', 'lost 41-35'), 'Austin FC v Portland Over 2.5 Goals': ('miss', '0-2'), 'Seattle v LAFC Over 1.5 Goals': ('hit', '2-1'), 'FC Dallas v Colorado Over 1.5 Goals': ('hit', '3-1'), 'Furman +4.5': ('hit', 'won 98-83'), 'Providence +11.5': ('hit', 'lost by 9'), 'Georgetown +12.5': ('hit', 'won 86-74'), 'UC Irvine -1.5': ('hit', 'won by 12'), 'Seokhyeon Ko ML': ('hit', 'UD'), 'Austin Bashi ML': ('hit', 'R1 sub'), 'Keiichiro Nakamura ML': ('miss', 'lost UD'), 'Lucas Fernando ML': ('hit', 'UD'), 'Lipscomb ML': ('hit', 'won 78-77')}, 'Hit 20 of 23: UNLV +5.5 (lost by 6), Austin/Portland Over 2.5 (0-2) and Nakamura (lost decision) missed.', 'Close again; soccer Over 2.5 and UFC near-pick favorites are the weak links.'),
128: ('lost', {'Elijah Smith ML': ('hit', 'R1 KO'), 'Nina Milosevic ML': ('hit', 'R2 TKO'), 'Kondratavicius v Petroski: Fight Does Not Go the Distance': ('hit', 'R2 TKO'), 'Cortes Acosta v Walker: Fight Does Not Go the Distance': ('hit', 'R3 KO'), 'Suarez v Jandiroba: Fight Goes the Distance': ('hit', 'UD'), 'Marcos Degli ML': ('miss', 'lost UD to Raposo'), 'Jose Souza ML': ('hit', 'R1 TKO'), 'Karine Silva ML': ('hit', 'UD'), 'Thomas Petersen ML': ('hit', 'R3 TKO')}, 'Hit 8 of 9; only Marcos Degli (-225) lost a decision.', 'UFC -225 favorites are the ladder weak spot.'),
}
for i, (res, legs, why, lesson) in G.items():
    h = H[i]
    assert h['result'] == 'pending', i
    for l in h['legs']:
        if l['pick'] in legs and l['result'] == 'pending':
            l['result'], l['actual'] = legs[l['pick']]
    h['result'] = res; h['whyExplanation'] = why; h['lesson'] = lesson
    h['profit'] = profit_for(h['odds'], h.get('stake') or 10, res == 'won')

used_events, used_picks = set(), set()
for x in H:
    for l in x.get('legs') or []:
        if l.get('result') == 'pending': used_picks.add(l['pick'])
def make_leg(eid, market_pred, runner_pred, pick, sport, reason):
    ev, mkts = load_event(eid)
    sel = find_runner(mkts, market_pred, runner_pred)
    if not sel: raise SystemExit(f'no selection {pick}')
    if eid in used_events or pick in used_picks: raise SystemExit(f'reuse {pick}')
    t = datetime.datetime.fromisoformat(ev['openDate'].replace('Z', '+00:00'))
    if t < NOW + timedelta(minutes=60): raise SystemExit(f'too soon {pick}')
    used_events.add(eid); used_picks.add(pick)
    return {'pick': pick, 'market': sel['market'], 'odds': sel['odds'], 'sport': sport, 'event': ev['name'],
            'start': start_et(ev['openDate']), 'reason': reason, 'marketId': sel['marketId'],
            'selectionId': sel['selectionId'], 'eventId': sel['eventId']}
ALT = lambda mn: mn == 'Alternate Spread'
APL = lambda mn: mn == 'Alternate Puck Line'
rn = lambda n: (lambda r, m: r.get('runnerName') == n)
parlays = []
def add(name, specs, reason):
    legs = [make_leg(*s) for s in specs]
    o, _ = combine([l['odds'] for l in legs])
    parlays.append({'name': name, 'odds': o, 'stake': 10, 'legs': legs, 'reason': reason})
add('Sixers Cushion + Bruins Home Ice', [
 (36286506, ALT, rn('Philadelphia 76ers +1.5'), 'Philadelphia 76ers +1.5', 'NBA', 'PHI (8-2) is -9.5 at 1-7 Chicago, which is missing Claxton and Collins; +1.5 gives 11 points of cushion — Philly only has to not lose by 2+.'),
 (36291494, APL, rn('Boston Bruins +1.5'), 'Boston Bruins +1.5', 'NHL', 'Home favorite (-137) at +1.5: Boston only fails if it loses by 2+ at home (NHL home +1.5 lesson).'),
], 'Two legs with big cushions off the main line; win-probability first.')
add('Celtics Bought-Down + Ducks Home Ice', [
 (36286504, ALT, rn('Boston Celtics -2.5'), 'Boston Celtics -2.5', 'NBA', 'BOS (7-2) is -12.5 at 1-8 Milwaukee with no starters out; -2.5 leaves 10 points of cushion.'),
 (36291489, APL, rn('Anaheim Ducks +1.5'), 'Anaheim Ducks +1.5', 'NHL', 'Ducks are the -122 home favorite; +1.5 covers any win or one-goal loss.'),
], 'Bought-down elite road favorite plus home +1.5.')
add('Heat Cushion + Jazz Big Dog', [
 (36286505, ALT, rn('Miami Heat +1.5'), 'Miami Heat +1.5', 'NBA', 'MIA is -7.5 at Sacramento, which is missing Murray, Raynaud and Simmons; +1.5 gives 9 points of cushion.'),
 (36286510, ALT, rn('Utah Jazz +21.5'), 'Utah Jazz +21.5', 'NBA', 'MIN is -11.5 but without Edwards (33 ppg) and DiVincenzo; +21.5 is 10 points beyond the main.'),
], 'Two NBA legs with 9-10 points of cushion; Minnesota is short-handed so a 22+ blowout is unlikely.')
add('Nets + Pelicans Big Cushions', [
 (36286507, ALT, rn('Brooklyn Nets +18.5'), 'Brooklyn Nets +18.5', 'NBA', 'DAL -9.5 without Lively; +18.5 is 9 points of extra cushion. Nets lost by just 3 at Atlanta last night.'),
 (36286509, ALT, rn('New Orleans Pelicans +10.5'), 'New Orleans Pelicans +10.5', 'NBA', 'NOP is actually a slight favorite (-118) at the Clippers; +10.5 needs them to avoid a double-digit loss.'),
], 'Big NBA dog cushions (lesson: +9.5 off the main or more), no elite opponents.')

D, R = '2026-11-08', 'Sun 2-Leg Special'
for t in parlays:
    if not already_in_history(H, t['name'], D, R):
        H.append({'date': D, 'run': R, 'type': 'parlay', 'name': t['name'], 'odds': t['odds'], 'stake': 10, 'result': 'pending', 'profit': 0,
                  'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'pending'} for l in t['legs']],
                  'whyExplanation': 'Pending — Sunday 2-leg special.', 'lesson': ''})
totals = recompute_totals(H)
p['updated'] = p['results']['updated'] = 'Sun Nov 8, 2026 7:30 AM ET'
p['run'] = 'Sunday 2-leg special at Ferdinand\'s request: four 2-leg parlays, every leg 9-11 points (or 1.5 goals at home) beyond the main. Graded Saturday: Hoops Bought-Down, Iowa -3.5, OU/UF Under, Arkansas +9.5, MSU +13.5 won; Best Shot hit 20/23.'
p['singles'], p['parlays'], p['lottery'] = [], parlays, []
p['results']['totals'] = totals
for k in ('singles', 'parlays', 'lottery'): p['results'][k] = copy.deepcopy(totals[k])
json.dump(p, open('/workspace/csb/picks.json', 'w'), indent=1)
print(json.dumps(totals['overall']), totals['legs'])
for k in ('singles','parlays','lottery'): print(k, totals[k])
for t in parlays: print(t['name'], t['odds'], [(l['pick'], l['odds'], l['start'], l['marketId'], l['selectionId']) for l in t['legs']])
