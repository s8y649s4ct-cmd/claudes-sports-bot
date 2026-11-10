#!/usr/bin/env python3
"""Tue Nov 10, 2026 10:30 AM ET run: grade Monday (grade_tue.py) then build Tuesday card.
Split plan (Mon 3PM lesson): this card builds a DAY-LONG Best Shot and uses the early East tips + NBA/NHL 7-8 PM.
Held back for 3 PM: OKC/POR, ORL/SAC, LAC/PHX; NHL MIN/MTL, WSH/OTT, FLA/CBJ, DET/STL, NSH/LAK;
NCAAB Utah State, New Mexico, Utah, Colorado, San Francisco, Arizona State, Fresno State, K-State/Creighton, Davidson, Dayton, Fordham, Iowa/VT, MTSU, Tulane, Kennesaw."""
import json, copy, os, datetime
src = open('/workspace/csb/build_sun_am.py').read()
src = src.replace("/workspace/sunam/fresh_ev_", "/workspace/tue/fresh_ev_").split("add('Bears Home Cushion")[0]
exec(src)
ALTT = lambda mn: mn == 'Alternate Total Points'
add('Heat Cushion + Avalanche Road Ice', [
 (36295141, ALT, rn('Miami Heat +1.5'), 'Miami Heat +1.5', 'NBA', 'Miami is -8.5 at 1-9 Utah, which has lost 8 straight and is without Keyonte George, Jaren Jackson Jr. and Jusuf Nurkic (Markkanen questionable). Giannis is probable (wrist) and has not missed a game. +1.5 gives 10 points of cushion: the Heat only lose this leg by losing by 2+ to the worst-shorthanded team in the West.'),
 (36300174, APL, rn('Colorado Avalanche +1.5'), 'Colorado Avalanche +1.5', 'NHL', 'Colorado is the -156 road favorite at Toronto, which has lost 3 straight and was shut out 4-0 at home by New Jersey Sunday. Blackwood (9-3-1) starts vs Bobrovsky (3.34 GAA). Road favorites at +1.5 keep covering (NJ, TB, NYI all cashed in the last 3 days).'),
], 'An NBA favorite with 10 points of cushion against a depleted 1-9 team, plus a road NHL favorite at +1.5.')
add('Knicks Bought-Down + Devils Road Ice', [
 (36295139, ALT, rn('New York Knicks -6.5'), 'New York Knicks -6.5', 'NBA', 'NY is -15.5 at home vs 1-9 Milwaukee (6 straight losses, 0-4 on the road, -13 net rating, Herro questionable). -6.5 is 9 points of cushion for the defending champs, who have won 5 of 6.'),
 (36299762, APL, rn('New Jersey Devils +1.5'), 'New Jersey Devils +1.5', 'NHL', 'NJ (13-5, 5 straight wins) is the -154 road favorite at 7-8-3 Winnipeg. Risk: backup Jake Allen starts instead of Hellebuyck and the Jets have won 3 straight, which is why we take +1.5 (covers any win or one-goal loss) and not the moneyline.'),
], 'A home NBA favorite bought 9 points down vs a 1-9 team, plus the hottest road NHL favorite at +1.5.')
add('Cyclones + Musketeers Bought-Down Hosts', [
 (36302978, ALTN, rh('Iowa State', -26.5), 'Iowa State -26.5', 'NCAAB', 'Iowa State is -35.5 at home vs SWAC Southern, which lost by 52 at TCU last week. -26.5 leaves 9 points of cushion against a truly bottom-tier visitor (the only kind of game where big buy-downs held Monday).'),
 (36302599, ALTN, rh('Xavier', -26.5), 'Xavier -26.5', 'NCAAB', 'Xavier is -35.5 at home vs Detroit Mercy, which lost by 61 at Marquette. -26.5 leaves 9 points of cushion.'),
], 'Two Power/Big East hosts bought 9 points down against bottom-tier visitors who have already lost by 52 and 61.')
add('Wolfpack + Rebels Bought-Down Hosts', [
 (36302963, ALTN, rh('NC State', -10.5), 'NC State -10.5', 'NCAAB', 'NC State is -19.5 at home vs Presbyterian (ML -4500), which lost by 14 at Georgia. -10.5 leaves 9 points of cushion.'),
 (36302968, ALTN, rh('Ole Miss', -17.5), 'Ole Miss -17.5', 'NCAAB', 'Ole Miss is -26.5 at home vs SE Louisiana (ML -30000), which lost by 33 at Auburn. -17.5 leaves 9 points of cushion.'),
], 'Two ACC/SEC hosts bought 9 points down vs low-major visitors.')
add('Broncos MACtion + Scarlet Knights', [
 (36280892, ALT, rn('Western Michigan (-4.5)'), 'Western Michigan -4.5', 'NCAAF', 'WMU (6-3, 4-1 MAC, won 4 of 5) is -14.5 at 1-8 Akron (0-5 MAC, 5 straight losses, allowed 25+ in every one) and comes off a bye. Only long-term absences are C Schleicher and DE Bishop. -4.5 is 10 points of cushion; WMU hasn\'t lost to Akron since 2017.'),
 (36302906, ALTN, rh('Rutgers', -14.5), 'Rutgers -14.5', 'NCAAB', 'Rutgers is -23.5 at home vs NJIT (ML -10000), which lost by 23 at Iona. -14.5 leaves 9 points of cushion.'),
], 'A MAC road favorite bought 10 points down vs the worst team in the conference, plus a Big Ten host bought 9 down.')
add('Deacons + Friars Bought-Down Hosts', [
 (36302954, ALTN, rh('Wake Forest', -9.5), 'Wake Forest -9.5', 'NCAAB', 'Wake is -18.5 at home vs Big South Charleston Southern (ML -4000). -9.5 leaves 9 points of cushion.'),
 (36302907, ALTN, rh('Providence', -22.5), 'Providence -22.5', 'NCAAB', 'Providence is -31.5 at home vs 0-2 Bryant, which lost to Quinnipiac and Fairfield. -22.5 leaves 9 points of cushion.'),
], 'Two home favorites bought 9 points down vs visitors that have already lost to mid-majors.')
bs = add('Best Shot $500K', [
 (36302899, ALTN, rh('Georgetown', -19.5), 'Georgetown -19.5', 'NCAAB', 'Georgetown is -27.5 at home vs MEAC Delaware State; -19.5 leaves 8 points of cushion. Hoyas beat Maryland by 12.'),
 (36302560, ALTN, rh('UCF', -4.5), 'UCF -4.5', 'NCAAB', 'UCF is -13.5 at home vs South Alabama (ML -1250); -4.5 leaves 9 points of cushion.'),
 (36302577, ALTN, rh('Georgia Tech', -7.5), 'Georgia Tech -7.5', 'NCAAB', 'Georgia Tech is -16.5 at home vs Eastern Kentucky (ML -2800); -7.5 leaves 9 points of cushion.'),
 (36302571, ALTN, rh('North Carolina', -4.5), 'North Carolina -4.5', 'NCAAB', 'UNC is -13.5 at home vs Wyoming (ML -1200) after beating Wofford by 39; -4.5 leaves 9 points of cushion.'),
 (36302724, ALTN, rh('Saint Louis', -14.5), 'Saint Louis -14.5', 'NCAAB', 'SLU is -23.5 at home vs Northern Kentucky (ML -10000), which lost by 37 at Texas A&M; -14.5 leaves 9 points of cushion.'),
 (36302744, ALTN, rh('Wisconsin', -16.5), 'Wisconsin -16.5', 'NCAAB', 'Wisconsin is -25.5 at home vs Fairfield (ML -20000); -16.5 leaves 9 points of cushion.'),
 (36302591, ALTN, rh('Villanova', -14.5), 'Villanova -14.5', 'NCAAB', 'Villanova is -23.5 at home vs La Salle (ML -10000); -14.5 leaves 9 points of cushion.'),
 (36302270, ML, rn('Florida'), 'Florida ML', 'NCAAB', 'Florida is -9.5 at Florida State (ML -490); moneyline only because it is a road rivalry game.'),
 (36295143, ALTT, rn('Over 204.5'), 'Celtics/76ers Over 204.5', 'NBA', 'Main total 217.5; Over 204.5 is 13 points of cushion. Both teams are healthy and top-5 in the East.'),
 (36302976, ML, rn('SMU'), 'SMU ML', 'NCAAB', 'SMU is -26.5 at home vs SWAC Prairie View (ML -30000).'),
 (36302967, ML, rn('Rhode Island'), 'Rhode Island ML', 'NCAAB', 'URI is -20.5 at home vs Maine (ML -7000); URI won its first two by 44 and 18.'),
 (36302522, ML, rn('GW Revolutionaries'), 'GW ML', 'NCAAB', 'GW is -14.5 at home vs Elon (ML -1700).'),
 (36302779, ALTN, rh('TCU', -25.5), 'TCU -25.5', 'NCAAB', 'TCU is -34.5 at home vs UL Monroe, which lost by 41 at Texas A&M; -25.5 leaves 9 points of cushion.'),
 (36302773, ALTN, rh('Arizona', -27.5), 'Arizona -27.5', 'NCAAB', 'Arizona is -36.5 at home vs Northern Arizona, which lost by 29 at New Mexico and 12 at UNLV; -27.5 leaves 9 points of cushion.'),
 (36302960, ALTN, rh('BYU', -19.5), 'BYU -19.5', 'NCAAB', 'BYU is -28.5 at home vs Queens, which lost by 50 at Oklahoma State; -19.5 leaves 9 points of cushion.'),
], 'Day-long Best Shot (per the Monday split lesson): big college home favorites bought 8-9 points down against low-major visitors, -1200 to -30000 moneylines, and one NBA total with 13 points of cushion. No pick\'em-game cushions (the three Monday misses). It is far short of the $5K target: getting there would mean adding 60-65% legs.', stake=5, lst=[])
D, R = '2026-11-10', '10:30 AM'
for t, typ in [(t, 'parlay') for t in new] + [(bs, 'lottery')]:
    if not already_in_history(H, t['name'], D, R):
        H.append({'date': D, 'run': R, 'type': typ, 'name': t['name'], 'odds': t['odds'], 'stake': t['stake'], 'result': 'pending', 'profit': 0,
                  'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'pending'} for l in t['legs']],
                  'whyExplanation': 'Pending.', 'lesson': ''})
totals = recompute_totals(H)
p['updated'] = p['results']['updated'] = 'Tue Nov 10, 2026 10:30 AM ET'
p['run'] = 'Tuesday 10:30 AM: Monday graded (2-leg parlays 7-4; the 3 PM Best Shot won). Six new 2-leg parlays, every leg 9-10 points or 1.5 goals beyond the main against bottom-tier or depleted opponents, plus a day-long 15-leg Best Shot. No singles cleared the edge bar. Late West games and several NBA/NHL games are held back for 3 PM.'
p['singles'], p['parlays'], p['lottery'] = [], new, [bs]
p['results']['totals'] = totals
for k in ('singles', 'parlays', 'lottery'): p['results'][k] = copy.deepcopy(totals[k])
p['results']['topLessons'] = [
 'Monday 2-leg parlays went 7-4; three of the four losses were 8-9 point college buy-downs against competent mid-majors (Marshall, North Alabama, UNC Greensboro). Buy down only vs truly bottom-tier visitors.',
 'Mid-major vs mid-major games are not buy-down spots, even with a -19.5 main line (UIC won by exactly 10).',
 'Road NHL favorites at +1.5 keep covering (NYI lost in a shootout and still cashed); NBA road favorites at +1.5 need form checks (CLE lost by 12 at CHA).',
 'Best Shot misses came only from pick\'em-game cushions (Cincinnati, Canucks, Raptors); the 7 college buy-downs vs low-majors all hit.',
 'Plan the day: build a day-long Best Shot at 10:30 AM and hold back late games for the 3 PM card.',
]
p['results']['sources'] = 'FanDuel PA public odds (event-page API, pulled at build ~10:45 AM ET); ESPN scoreboards 11/9 (NFL/NBA/NHL/NCAAB finals) and 11/3-11/9 NCAAB results; ATP/Tennis Foresight (Brisbane Challenger results); NBA official injury report 11/10 8 AM, SI/Talkbasket/Heat Nation (Giannis probable), Sports Mole/SI (Bucks-Knicks), Daily Faceoff/AOL (NHL goalies), WMU athletics/Winners&Whiners (WMU-Akron); ESPN NBA/NHL/MAC standings; lessons.md'
json.dump(p, open('/workspace/csb/picks.json', 'w'), indent=1)
print(totals['overall'])
for t in new + [bs]: print(t['name'], t['odds'], [(l['pick'], l['odds'], l['start']) for l in t['legs']])
