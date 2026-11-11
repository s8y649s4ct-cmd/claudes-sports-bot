#!/usr/bin/env python3
"""Wed Nov 11, 2026 10:30 AM ET run: grade Tuesday (grade_wed.py) then build Wednesday card.
Split plan: this card uses the 2 PM-8 PM East/Central games + a day-long Best Shot of near-lock moneylines.
Held back for 3 PM: NBA GSW/HOU, ORL/UTA, OKC/POR, DEN/MEM, BOS/TOR, BKN/NO, WSH/IND; all 6 NHL games
(EDM/PHI, VGK/UTA, ANA/NSH, SJ/PIT, BUF/TB, CGY/NYR); NCAAB GCU, Cal Baptist, USC/Cal, UCLA, Oregon, Nebraska."""
import json, copy, os, datetime
src = open('/workspace/csb/build_sun_am.py').read()
src = src.replace("/workspace/sunam/fresh_ev_", "/workspace/wed/fresh_ev_").split("add('Bears Home Cushion")[0]
exec(src)
add('Lakers + Golden Hurricane Bought-Down', [
 (36298493, ALT, rn('Los Angeles Lakers -4.5'), 'Los Angeles Lakers -4.5', 'NBA', 'The 10-2 Lakers (6 straight wins, 5-1 on the road) are -13.5 at 1-10 Milwaukee, which has lost 7 straight, is 1-5 at home with a -14.9 point differential, and is on the second night of a back-to-back after losing by 32 at New York. Leading scorer Tyler Herro is out. Luka Doncic (39.3 ppg, 30+ in 8 straight) and Austin Reaves are off the injury report; LA had Tuesday off. -4.5 is 9 points of cushion. Milwaukee has lost by 5+ in 10 of its 11 games.'),
 (36306803, ALTN, rh('Tulsa', -8.5), 'Tulsa -8.5', 'NCAAB', 'Tulsa (2-0, 30 wins and an NIT final last year, 90+ points in both games) is -17.5 at home vs Oral Roberts (Torvik ~270), whose top guard Connor Dow has a fractured wrist. A Torvik-style model projects Tulsa by about 16.5, more than the buy-down number plus 5 (13.5). -8.5 leaves 9 points of cushion.'),
], 'A 10-2 road favorite vs a 1-10 team on a back-to-back, plus a strong AAC host vs a short-handed low-major. Both legs are bought 9 points down from the main line.')
add('Spurs Bought-Down + Aggies Cushion', [
 (36298490, ALT, rn('San Antonio Spurs -5.5'), 'San Antonio Spurs -5.5', 'NBA', 'San Antonio (9-2, 9 straight wins, 5-0 on the road, +11.7 differential, top-4 defense) is -14.5 at 1-8 Chicago (0-3 at home, 7 straight losses, -16.6 differential). Wembanyama (30.1 ppg) is expected to play. Only Tobias Harris is out, and Vassell is questionable. Chicago has Powell, Collins, Awaka and Claxton all questionable. -5.5 is 9 points of cushion. Seven of SA\'s nine wins came by 6+, and Chicago has lost by 6+ in 7 of its 9 games.'),
 (36306908, ALTN, rh('UC Davis', -2.5), 'UC Davis -2.5', 'NCAAB', 'UC Davis is -11.5 at home (12-4 at home last year) vs 0-3 Incarnate Word (Torvik ~346), which lost at home to Chicago State and by 19 at UTEP. UIW has 14 new players and averages 18.3 turnovers. The model projects Davis by about 12, well above the 2.5 + 5 bar. -2.5 is 9 points of cushion.'),
], 'An elite road favorite on a 9-game win streak vs a 1-8 team, plus a home favorite vs a bottom-20 visitor. Each is bought 9 points down.')
add('Knicks Home Cushion + Paladins ML', [
 (36298492, ALT, rn('New York Knicks +6.5'), 'New York Knicks +6.5', 'NBA', 'New York (6-4, 4 straight wins, 4-2 at home) is the -4.5 home favorite vs Cleveland, which is 1-4 on the road, has lost 2 straight and lost by 12 at Charlotte Monday. The Knicks are on a back-to-back but at home with no travel, and starters rested in Tuesday\'s 32-point win. Josh Hart is out. The back-to-back is why we take +6.5 (11 points of cushion) instead of the spread, the same setup that cashed with Dallas +5.5 Monday. It only loses if Cleveland wins by 7+.'),
 (36306690, ML, rn('Furman'), 'Furman ML', 'NCAAB', 'Furman (3-0, two NCAA bids in four years, just beat Missouri Valley champ Northern Iowa by 15, 99 ppg) is -11.5 at 0-2 Holy Cross (Torvik ~352), which lost by 44 at URI and 29 at Villanova. Moneyline only because Furman is on the road and the main line is not huge.'),
], 'A home favorite with 11 points of cushion, plus a strong mid-major road moneyline vs a bottom-15 team.')
bs = add('Best Shot $500K', [
 (36307787, ML, rn('Notre Dame'), 'Notre Dame ML', 'NCAAB', 'Notre Dame is -26.5 (ML -20000) at home vs South Carolina State. Notre Dame beat Mercyhurst by 27 and Eastern Illinois by 24. After Tuesday\'s lesson (buy-downs from -27-type lines went 4/7), mega-spread games get the moneyline, not an alt spread.'),
 (36306393, ML, rn('South Carolina'), 'South Carolina ML', 'NCAAB', 'South Carolina is -22.5 (ML -10000) at home vs Saint Peter\'s, which lost to Binghamton and NJIT. Moneyline only: the Gamecocks beat SEMO by only 10.'),
 (36306828, ML, rn('Boise State'), 'Boise State ML', 'NCAAB', 'Boise State is -16.5 (ML -3000) at home vs Oakland. Boise beat Butler by 19.'),
 (36306827, ML, rn('Colorado State'), 'Colorado State ML', 'NCAAB', 'Colorado State is -16.5 (ML -2800) at home vs Portland State, which lost by 19 at Seattle.'),
 (36306808, ML, rn('Seattle'), 'Seattle ML', 'NCAAB', 'Seattle is -16.5 (ML -3000) at home vs UTSA, which beat VMI by only 2 at home. Seattle beat Portland State by 19.'),
], 'A day-long safety ticket of home moneylines at -2800 or shorter. This is far short of the $5K target. Every leg strong enough to add real price is on a 2-leg parlay (Ferdinand\'s priority) or held back for the 3 PM card (Grand Canyon, Oilers, late NBA/NHL). The only ways to add price are pick\'em cushions or mid-major short favorites, the exact legs that sank the last two big Best Shots. So this stays short instead of being padded.', stake=5, lst=[])
D, R = '2026-11-11', '10:30 AM'
for t, typ in [(t, 'parlay') for t in new] + [(bs, 'lottery')]:
    if not already_in_history(H, t['name'], D, R):
        H.append({'date': D, 'run': R, 'type': typ, 'name': t['name'], 'odds': t['odds'], 'stake': t['stake'], 'result': 'pending', 'profit': 0,
                  'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'pending'} for l in t['legs']],
                  'whyExplanation': 'Pending.', 'lesson': ''})
totals = recompute_totals(H)
p['updated'] = p['results']['updated'] = 'Wed Nov 11, 2026 10:30 AM ET'
p['run'] = 'Wednesday 10:30 AM: Tuesday graded. 2-leg parlays went 7-2 (the misses were the Devils with a backup goalie and Magic/Kings Over by 3 points). The day-long Best Shot went 12/15 and lost; the 3 PM Best Shot won. Today: three 2-leg parlays, every leg 9-11 points off the main or a moneyline vs a bottom-20 team, plus a short day-long Best Shot. No singles cleared the edge bar. No +1000 lottery was possible without coin-flip legs. Late NBA/NHL and West college games are held for 3 PM.'
p['singles'], p['parlays'], p['lottery'] = [], new, [bs]
p['results']['totals'] = totals
for k in ('singles', 'parlays', 'lottery'): p['results'][k] = copy.deepcopy(totals[k])
p['results']['topLessons'] = [
 'Tuesday 2-leg parlays went 7-2: buy-downs vs bottom-tier visitors from -19.5 to -38.5 main lines went 9/9 on 2-legs. Keep using them only after a model check.',
 'Mega-spread buy-downs (main -27.5 or bigger) are high-variance: Georgetown, TCU (2OT) and BYU missed in the Best Shot. Use the moneyline in those games.',
 'NHL +1.5 needs the goalie edge. A favorite starting its backup (Devils/Jake Allen) does not qualify.',
 'Big-cushion NBA totals fail when a team is missing 2+ scorers and has already gone under the alt (Orlando, 207 vs 209.5). Require ~90% of both teams\' games to clear the number.',
 'NBA road favorites at +1.5 or bought-down only with form plus rest edges: Lakers and Spurs both face 1-win teams (Milwaukee on a back-to-back).',
]
p['results']['sources'] = 'FanDuel PA public odds (event-page API, pulled ~10:30 AM ET); ESPN scoreboards 11/10 (NBA/NHL/NCAAB/CFB finals) and 11/3-11/10 NCAAB results; ESPN NBA standings, injuries and team game logs; Barttorvik 2027 T-Rank ratings (projected margins); Daily Faceoff starting goalies 11/11; Lakers Wire/Heavy/Sports Mole (LAL-MIL); SI/Pounding The Rock/Sports Mole (SAS-CHI); Tulsa & ORU athletics/Tulsa World (Mayor\'s Cup); Furman & Holy Cross athletics; UC Davis athletics/AP (UIW-UCD); lessons.md'
json.dump(p, open('/workspace/csb/picks.json', 'w'), indent=1)
print(totals['overall'])
for t in new + [bs]: print(t['name'], t['odds'], t['stake'], [(l['pick'], l['odds'], l['start']) for l in t['legs']])
