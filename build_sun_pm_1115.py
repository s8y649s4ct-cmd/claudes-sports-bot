#!/usr/bin/env python3
"""Sun Nov 15, 2026 3:00 PM ET run: nothing from the 10:30 AM card was final at build time. Fresh FanDuel PA pulls in /workspace/sun15pm."""
import json, copy, os, datetime, glob
os.makedirs('/workspace/sun15pm', exist_ok=True)
for f in glob.glob('/workspace/sun15pm/fresh_ev_*.json'): os.remove(f)
src = open('/workspace/csb/build_sun_am.py').read()
src = src.replace("/workspace/sunam/fresh_ev_", "/workspace/sun15pm/fresh_ev_").split("add('Bears Home Cushion")[0]
exec(src)
MN = lambda name: (lambda mn: mn == name)
ASP = MN('Alternate Spread')
add('Hawks Road Cushion + Rams Big Cushion', [
 (36314670, ASP, rn('Atlanta Hawks +1.5'), 'Atlanta Hawks +1.5', 'NBA', 'Atlanta (7-6, 4-3 on the road with wins at Orlando, Charlotte, Indiana and Washington) is the -7.5 road favorite at Milwaukee (1-12). Home-loss check passes clearly: the Bucks lost at home by 32 (Houston), 25 (Cleveland), 20 (Boston), 14 (Toronto), 11 (Lakers) and 7 (Chicago), so 5 of 6 home losses were by 10+; their only home win is over Indiana. Hawks are without rookie Kingston Flemings (back); Jock Landale is questionable. Milwaukee\'s Ryan Rollins is questionable and Ousmane Dieng is out (ESPN injury report). +1.5 loses only if Milwaukee wins outright by 2+. Tips 8:10 PM ET.'),
 (36275766, ASP, rn('Los Angeles Rams (+3.5)'), 'Los Angeles Rams +3.5', 'NFL', 'The Rams (5-4) are -9.5 at Arizona (3-6); +3.5 is 13 points off the main line and crosses the key number 3, so the Rams lose this leg only if Arizona wins by 4+. Arizona is 0-3 at home, losing by 24 (Seattle), 24 (Detroit) and 14 (Denver), so the home-loss check passes. Arizona\'s QB room is gutted: Gardner Minshew is on IR (season-ending UCL tear) and Joey Aguilar is inactive, and center Hjalte Froholdt and guard Jon Gaines are inactive (ESPN injury report). Risk noted: Puka Nacua and Davante Adams are on IR, Arizona won 18-16 at the Rams in Week 6, and Myles Garrett is questionable. Kicks 4:05 PM ET.'),
], 'Two plus-side cushions on clearly better road favorites whose hosts have been getting blown out at home (Bucks 1-12, five home losses by 10+; Cardinals 0-3 at home, all by 14+, and down to a backup QB).')
bs = add('Best Shot $500K', [
 (36314671, ASP, rn('Houston Rockets +4.5'), 'Houston Rockets +4.5', 'NBA', 'Houston (10-3) is -8.5 at Washington (4-9); +4.5 is 13 points off the main line, so the Rockets lose this leg only if the Wizards win by 5+. The bigger cushion (instead of +1.5) is because Houston is without Fred VanVleet, Clint Capela and the suspended Marcus Smart. Washington\'s home losses were by 15 (Atlanta), 10 (Toronto) and 4 (Detroit, 144-140), and Alex Sarr, Tre Johnson and Bub Carrington are all questionable. Tips 7:10 PM ET.'),
 (36314669, ASP, rn('Oklahoma City Thunder +4.5'), 'Oklahoma City Thunder +4.5', 'NBA', 'Oklahoma City (8-5) is -11.5 at Sacramento (1-12, 0-7 at home); +4.5 is 16 points off the main line, so the Thunder lose this leg only if the Kings get their first home win by 5+. The deep cushion is deliberate: OKC is without Chet Holmgren, Jalen Williams and Cason Wallace and is 3-5 on the road. Sacramento is without Maxime Raynaud and Ben Simmons, with Keegan Murray and Precious Achiuwa questionable. Tips 9:10 PM ET.'),
], 'The two highest-probability legs left after the parlay: deep plus-side cushions (13 and 16 points off the main line) on short-handed but much better road teams. Nowhere near the $5K target. Every other leg tonight failed a rule (see notes) and would be a 60-80% leg, so it is not padded.', stake=5, lst=[])
D, R = '2026-11-15', '3:00 PM'
for t, typ in [(t, 'parlay') for t in new] + [(bs, 'lottery')]:
    if not already_in_history(H, t['name'], D, R):
        H.append({'date': D, 'run': R, 'type': typ, 'name': t['name'], 'odds': t['odds'], 'stake': t['stake'], 'result': 'pending', 'profit': 0,
                  'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'pending'} for l in t['legs']],
                  'whyExplanation': 'Pending.', 'lesson': ''})
totals = recompute_totals(H)
p['updated'] = p['results']['updated'] = 'Sun Nov 15, 2026 3:00 PM ET'
p['run'] = ("Sunday 3:00 PM: nothing from the 10:30 AM card was final at build time (Chiefs up 14-3 and Jaguars up 16-10 in the 1 PM games; "
 "Boston College and Charleston leading). Tonight's card is small: one 2-leg parlay (Hawks +1.5, Rams +3.5) and a 2-leg Best Shot "
 "(Rockets +4.5, Thunder +4.5). No singles and no +1000 lottery: no other leg passed the rules. NHL goalie-edge legs were skipped because "
 "no qualifying starter was confirmed by build time.")
p['singles'], p['parlays'], p['lottery'] = [], new, [bs]
p['results']['totals'] = totals
for k in ('singles', 'parlays', 'lottery'): p['results'][k] = copy.deepcopy(totals[k])
p['results']['topLessons'] = [
 'Plus-side cushions on clearly better teams are the main leg type. Tonight that means Hawks +1.5, Rams +3.5, Rockets +4.5 and Thunder +4.5. Favorite-side buy-downs stay paused.',
 'Home-loss check decided the NBA and NFL picks. Bucks (5 of 6 home losses by 10+) and Cardinals (0-3 at home, all by 14+) pass. Raptors (lost at home by 5, 7 and 16; Knicks -5.5), Suns (5-3 at home) and Raiders (lost at home by 3, 3 and 14; Seattle without Darnold) fail.',
 'The cushion grows with injury risk: Houston (no VanVleet, Capela or Smart) gets +4.5, not +1.5. OKC (no Holmgren, J. Williams or Wallace; 3-5 on the road) gets +4.5 against a Kings team that is 0-7 at home.',
 'Goalie-edge NHL +1.5 only with a confirmed starter. Saros (.922) vs Nedeljkovic (.895) qualifies on paper, but it was only projected at build time, so Nashville +1.5 was left off. Calgary (Cooley .913, confirmed) is an underdog, so it was skipped too. Edmonton (Jarry .903) and Vegas (Hart .896) fall below .910.',
 'Tier-gap moneylines: none tonight. USC vs Arkansas-Pine Bluff is -100000, which adds nothing. The other hosts are below the top 150 (Seattle 152, SJSU 183, Buffalo 220) or the visitors are above 300 (Coastal 239, Alabama State 253).',
 'Women\'s college moneylines (UConn -1600, UCLA -8000) are on a restricted FanDuel feed (sgmMarket=false) and cannot be parlayed, so they were not used.',
]
p['results']['sources'] = ('FanDuel PA public odds (content-managed pages and event-page API, pulled ~2:45-3:00 PM ET); ESPN scoreboards 11/15; '
 'ESPN NBA and NFL injury reports 11/15; ESPN team schedules (home-loss check); Daily Faceoff starting goalies 11/15; Barttorvik T-Rank.')
json.dump(p, open('/workspace/csb/picks.json', 'w'), indent=1)
print(totals['overall'], totals['legs'])
for t in new + [bs]: print(t['name'], t['odds'], t['stake'], round(t['stake']*(combine([l['odds'] for l in t['legs']])[1]-1),2), [(l['pick'], l['odds'], l['start'], l['marketId'], l['selectionId']) for l in t['legs']])
