#!/usr/bin/env python3
"""Sat Nov 14, 2026 3:00 PM ET run: nothing from the 10:30 AM card was final at build time (Carolina/Seattle in the 2nd
intermission, Alabama/Vanderbilt in the 3rd; everything else starts 3:30 PM or later). Build from fresh FanDuel PA pulls
cached in /workspace/sat14pm."""
import json, copy, os, datetime, glob
os.makedirs('/workspace/sat14pm', exist_ok=True)
for f in glob.glob('/workspace/sat14pm/fresh_ev_*.json'): os.remove(f)
src = open('/workspace/csb/build_sun_am.py').read()
src = src.replace("/workspace/sunam/fresh_ev_", "/workspace/sat14pm/fresh_ev_").split("add('Bears Home Cushion")[0]
exec(src)
_le = load_event
load_event = lambda eid, tabs=('', 'popular', 'alternates', 'goals'): _le(eid, tabs)
MN = lambda name: (lambda mn: mn == name)
add('Senators Goalie-Edge + Broncos Backup-QB Fade', [
 (36309162, APL, rn('Ottawa Senators +1.5'), 'Ottawa Senators +1.5', 'NHL', 'Held this morning for goalie confirmations; both are now confirmed (Daily Faceoff). Linus Ullmark (8-1-0, .938) starts for Ottawa vs Sergei Murashov (2-4-1, .889) for Pittsburgh, an edge of .049 with the favorite\'s starter far above the .910 bar. Ottawa is the -137 road favorite. +1.5 loses only if Pittsburgh wins by 2+ against the hottest goalie in the league. Faces off 7:10 PM ET.'),
 (36285357, ALTN, rn('Boise State (-6.5)'), 'Boise State -6.5', 'NCAAF', 'Backup-QB fade: Oregon State QB Braden Atkinson (nation\'s leading passer, 3,169 yards, 25 TD) is OUT with a hand injury (Oregonian, downgraded Friday); Maalik Murphy (5 of 7, 1 INT in relief last week) starts. OSU also lost starting LT Jacob Anderson and OLB Will Haverland, and lost 42-21 at home to Texas State last week. No. 17-24 Boise State (8-1, four straight wins) hosts with College GameDay in town; the line moved from -10 to -16.5. SP+ projects Boise by 12.5 (PRIME 14.1) before the QB news; a ~4.7-point QB adjustment puts it near 17, so -6.5 (10 off the main line) clears the buy-down +7 bar. Risk noted: Boise QB Madsen is questionable, but backup Cutforth led a 64-38 win at Colorado State last week. Clear, 55F. Kicks 6:00 PM ET.'),
], 'The goalie-edge NHL leg held from this morning (Ullmark .938 vs Murashov .889, both confirmed) plus a home favorite bought down 10 points against an opponent missing the nation\'s leading passer.')
add('Falcons + Nittany Lions Bought-Down', [
 (36285381, ALTN, rn('Air Force (-4.5)'), 'Air Force -4.5', 'NCAAF', 'Air Force (7-2) is -13.5 at home vs San Jose State (5-5). SP+ projects Air Force by 14.3 and PRIME by 16.1; the line opened -10.5 and moved 3.5 points toward Air Force (sharp side). Forecast rain at Falcon Stadium favors the triple option and shortens the game, which is why the cushion is 9 points off the main line rather than the main line. Buy-down +7 bar: 14.3 clears -4.5 by 9.8. Air Force beat SJSU 26-16 last year. Kicks 7:00 PM ET.'),
 (36285378, ALTN, rn('Penn State (-2.5)'), 'Penn State -2.5', 'NCAAF', 'Penn State (5-4) is -12.5 at home vs Minnesota (5-4, fourth straight game without a bye). The line opened -7 and moved 5.5 points toward Penn State. SP+ projects Penn State by 10.5 (25-14), PRIME by 7. Matchup: Penn State\'s 3rd-down defense is 4th nationally vs Minnesota\'s 128th-ranked 3rd-down offense, and Minnesota is 131st in yards per play and 127th in EPA per play; Minnesota playmaker Theorin Randle is out. Buy-down +7 bar: SP+ 10.5 clears -2.5 by 8. Risk noted: 39F with NW wind gusting to 32 mph in a 41.5-total game, which is why this is 10 points off the main line. Kicks 7:00 PM ET.'),
], 'Two home favorites bought down 9-10 points, each backed by SP+/PRIME projections and by line movement toward them all week.')
bs = add('Best Shot $500K', [
 (36309167, MN('Alternate Total Goals'), rn('Under 8.5'), 'Wild/Bruins Under 8.5 Goals', 'NHL', 'Main total 6.5 (Under -138). Game-log test: 20 of 21 Minnesota games and 16 of 19 Boston games had 8 or fewer goals (36/40, 90%). Both starters are confirmed and both are good: Jesper Wallstedt (13-2-3, .925) and Jeremy Swayman (.913). Faces off 7:09 PM ET.'),
 (36309164, MN('Alternate Total Goals'), rn('Over 3.5'), 'Red Wings/Lightning Over 3.5 Goals', 'NHL', 'Main total 6.5. Game-log test: 19 of 19 Tampa Bay games and 16 of 20 Detroit games had 4+ goals (35/39, 90%). Vasilevskiy is at .885 this season (likely starter). Faces off 7:10 PM ET.'),
], 'A two-leg safety ticket of the two NHL totals that pass the ~90% game-log test. It is nowhere near +1000 or the $5K target: every other leg tonight is either on the 2-leg parlays or is a coin flip, and this morning\'s card already used the tier-gap college hoops moneylines. Not padded.', stake=5, lst=[])
D, R = '2026-11-14', '3:00 PM'
for t, typ in [(t, 'parlay') for t in new] + [(bs, 'lottery')]:
    if not already_in_history(H, t['name'], D, R):
        H.append({'date': D, 'run': R, 'type': typ, 'name': t['name'], 'odds': t['odds'], 'stake': t['stake'], 'result': 'pending', 'profit': 0,
                  'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'pending'} for l in t['legs']],
                  'whyExplanation': 'Pending.', 'lesson': ''})
totals = recompute_totals(H)
p['updated'] = p['results']['updated'] = 'Sat Nov 14, 2026 3:00 PM ET'
p['run'] = ("Saturday 3:00 PM: nothing from this morning's card was final at build time (Carolina led Seattle 4-1 after two periods; "
 "Alabama led Vanderbilt 21-6 in the 3rd), so the record is unchanged and all six morning tickets stay pending. Two new 2-leg parlays: "
 "Ottawa +1.5 (Ullmark .938 vs Murashov .889, both confirmed) with Boise State -6.5 (Oregon State's starting QB, the nation's leading passer, is out), "
 "and Air Force -4.5 with Penn State -2.5 (home favorites bought down 9-10 points, SP+ by 14.3 and 10.5, lines moved toward both). "
 "Best Shot is two NHL totals that pass the 90% game-log test, far short of $5K and not padded. No singles and no +1000 lottery: "
 "nothing tonight clears the bar without coin-flip legs. The Islanders leg held this morning was dropped (Sorokin is not starting).")
p['singles'], p['parlays'], p['lottery'] = [], new, [bs]
p['results']['totals'] = totals
for k in ('singles', 'parlays', 'lottery'): p['results'][k] = copy.deepcopy(totals[k])
p['results']['topLessons'] = [
 'Held legs are re-checked at 3 PM, not pre-approved: Ottawa went in (Ullmark .938 and Murashov .889 both confirmed). The Islanders were dropped: Varlamov (.891), not Sorokin, is the likely starter, which fails the .910 bar.',
 'Goalie-edge rule (.025+ with the favorite\'s starter .910+) kept every other NHL +1.5 off: Colorado (Blackwood .901), Minnesota/Boston (.012 edge), Florida/St. Louis (pick\'em, exactly .025) and Detroit (an underdog) all failed.',
 'Backup-QB fade: Boise State -6.5 against an Oregon State team without the nation\'s leading passer (Atkinson out).',
 'Buy-down +7 bar on SP+: Air Force -4.5 (SP+ 14.3, PRIME 16.1) and Penn State -2.5 (SP+ 10.5). BYU (SP+ 5.4 vs -7.5), Washington State (SP+ has CSU by 1), Texas State (SP+ 3.4) and Tulsa (4.9) failed.',
 'NBA road favorites failed the home-loss check or have lineup risk: Dallas at a 4-2-at-home Cleveland team (Mitchell, Harden and Allen questionable on a back-to-back) and Detroit at Miami were skipped; Brooklyn/Memphis is a pick\'em.',
 'Totals only with the ~90% game-log test: Wild/Bruins Under 8.5 (36/40) and Red Wings/Lightning Over 3.5 (35/39) passed; Pistons/Heat and Nets/Grizzlies alt overs failed (Detroit and Brooklyn had several games near 186-204).',
 'College hoops buy-downs were skipped: Villanova -26.5 vs Rider and Grand Canyon -22.5 vs UL Monroe are the deepest alt lines offered and neither team has shown a 27-point margin against comparable opponents; the -100000 moneylines add nothing.',
]
p['results']['sources'] = ('FanDuel PA public odds (event-page API, pulled ~3:00-3:15 PM ET and refreshed at build); ESPN scoreboards 11/14 (grading check: nothing final from the morning card); '
 'Daily Faceoff starting goalies 11/14 (17 of 28 confirmed at pull); NBA official injury report 11/14 2:15 PM ET; SI/CBS (Cavaliers back-to-back after FAA ground stop); '
 'collegefootballcharts.com SP+/PRIME/Elo and line history (Week 11); Early Downs (Minnesota-Penn State); Oregonian, Idaho Statesman, TheSpread, Sharp Wire (Oregon State QB Atkinson out, Boise line move); '
 'ESPN NHL/NBA team schedules (game totals for the game-log test); Barttorvik 2027 T-Rank (team ranks).')
json.dump(p, open('/workspace/csb/picks.json', 'w'), indent=1)
print(totals['overall'], totals['singles'], totals['parlays'], totals['lottery'], totals['legs'])
for t in new + [bs]: print(t['name'], t['odds'], t['stake'], round(t['stake']*combine([l['odds'] for l in t['legs']])[1],2), [(l['pick'], l['odds'], l['start'], l['marketId'], l['selectionId']) for l in t['legs']])
