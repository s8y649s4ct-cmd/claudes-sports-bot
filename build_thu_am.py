#!/usr/bin/env python3
"""Thu Nov 12, 2026 10:30 AM ET run: grade Wednesday (grade_thu.py) then build Thursday card.
Split plan: this card uses 3 PM-7:10 PM East games + a day-long Best Shot of near-lock home moneylines.
Held back for 3 PM: NBA TOR/PHI (Embiid/LeBron day-to-day), DAL/MIN, CHA/PHX; NHL WSH/NJ (Devils starter unconfirmed),
WPG/DAL, STL/UTA, NYI/LA, plus BUF/CHI etc.; NCAAB BYU, UTEP, SJSU, A&M; TNF WSH/NYG; CFB Memphis/USF, Louisiana/ULM.
FanDuel PA pulls (~10:25 AM ET) cached in /workspace/thu."""
import json, copy, os, datetime
src = open('/workspace/csb/build_sun_am.py').read()
src = src.replace("/workspace/sunam/fresh_ev_", "/workspace/thu/fresh_ev_").split("add('Bears Home Cushion")[0]
exec(src)
add('Pistons Road Cushion + Patriots Bought-Down', [
 (36303942, ALT, rn('Detroit Pistons +1.5'), 'Detroit Pistons +1.5', 'NBA', 'Detroit (7-3, 4-1 on the road, +8.1 differential) is the -10.5 favorite at Washington (4-8, 5 straight losses, -5.9 differential). The Wizards are on the second night of a back-to-back after losing by 13 at Indiana last night; Detroit is rested and beat this same Wizards team by 11 on Monday. Cade Cunningham is active; Detroit is without Jalen Duren and Isaiah Joe (both also out Monday). Washington is missing Vukcevic, Beekman, Champagnie and Watkins. +1.5 is 12 points of cushion: Detroit only loses this leg if Washington wins by 2+. Passes the road-favorite form/rest check (rested, 4-1 away, clearly better team, favorite by 10+).'),
 (36309891, ALTN, rh('George Mason', -7.5), 'George Mason -7.5', 'NCAAB', 'George Mason (T-Rank ~81, 2-0) is -15.5 (ML -2500) at home vs UMKC (T-Rank ~274), which is playing its third game in five days after a Tuesday night trip to Florida A&M and lost by 18 at Jacksonville. A Torvik-style model projects Mason by about 16.5, clearing the buy-down rule (needs 7.5 + 5 = 12.5). -7.5 is 8 points off the main. UMKC is a Summit League visitor, not a competent mid-major in the ~165 range that sank Tuesday buy-downs. Tips 3:00 PM ET.'),
], 'A rested, clearly better NBA road favorite with 12 points of cushion vs a team on a back-to-back, plus a strong A-10 host bought 8 points down vs a tired low-major whose projection clears the buy-down rule by 4.')
add('Wild Road Ice + Tigers ML', [
 (36309087, APL, rn('Minnesota Wild +1.5'), 'Minnesota Wild +1.5', 'NHL', 'Minnesota (13-3-4, 7-1-2 last 10, 8-3-2 on the road) is the -176 favorite at Toronto (8-10-2, 4 straight losses, 4-7-1 at home; lost 4-0 to New Jersey and 6-3 to Colorado at home this week). Goalie edge, including the favorite\'s own starter: Jesper Wallstedt (.924, 1.93 GAA, 12-2-3, Minnesota\'s clear No. 1) vs Anthony Stolarz (.907, 2.71). Neither team played last night. +1.5 only loses if Toronto wins by 2+.'),
 (36309905, ML, rn('Towson'), 'Towson ML', 'NCAAB', 'Towson (T-Rank ~176) is -13.5 (ML -1250) at home vs Loyola Maryland (T-Rank ~344), which lost by 11 at Mount St. Mary\'s. Towson beat LIU by 20 at home and lost only by 10 at Utah. The model projects Towson by about 13. A CAA host vs a bottom-25 Patriot League visitor is a real tier gap (the Seattle/UTSA lesson). Moneyline only, no buy-down.'),
], 'A road NHL favorite at +1.5 with the goalie edge against a slumping home team, plus a home moneyline vs a bottom-25 visitor.')
bs = add('Best Shot $500K', [
 (36309925, ML, rn('Rhode Island'), 'Rhode Island ML', 'NCAAB', 'Rhode Island (3-0, beat Holy Cross by 44) is -25.5 (ML -30000) at home vs Maryland-Eastern Shore, T-Rank 365 (last in Division I), which lost by 28 at Boston College last night (second road game in two nights). Mega-spread games get the moneyline only.'),
 (36309899, ML, rn('Indiana'), 'Indiana ML', 'NCAAB', 'Indiana (3-0, T-Rank ~29, beat Syracuse) is -24.5 (ML -20000) at home vs Tennessee Tech (T-Rank ~209). Moneyline only: Tennessee Tech beat Western Kentucky, so it is a competent OVC team and a buy-down is not safe.'),
 (36309926, ML, rn('Minnesota'), 'Minnesota ML', 'NCAAB', 'Minnesota (3-0, won at Cincinnati) is -25.5 (ML -20000) at home vs 0-4 Southern (T-Rank ~299), which lost by 52 at TCU and 37 at Iowa State. The projection (~20) does not clear the buy-down rule for -16.5, so moneyline only.'),
 (36309912, ML, rn('High Point'), 'High Point ML', 'NCAAB', 'High Point (3-0, T-Rank ~75, beat Washington State by 12) is -22.5 (ML -10000) at home vs Southern Utah (T-Rank ~240), whose two wins came against non-Division I teams. Projection about 17. Moneyline only.'),
 (36309897, ML, rn('Penn State'), 'Penn State ML', 'NCAAB', 'Penn State is -20.5 (ML -7000) at home vs Mercyhurst (T-Rank ~308, second-year D-I program), which lost by 27 at Notre Dame. Projection about 18. Moneyline only: Penn State\'s defense allowed 93 to Chattanooga and it lost to Pitt, so no buy-down.'),
 (36309915, ML, rn('Bowling Green'), 'Bowling Green ML', 'NCAAB', 'Bowling Green (2-0, beat Cleveland State by 16) is -14.5 (ML -1600) at home vs Niagara (T-Rank ~324, lost its opener to Morgan State). Projection about 13. MAC host vs a bottom-40 MAAC visitor.'),
], 'A day-long safety ticket of six home moneylines from -1600 to -30000, each against a visitor from a lower conference tier (the Seattle/UTSA lesson). It is far short of the $5K target: the strongest legs with real price are on the 2-leg parlays (Ferdinand\'s priority), and the late games are held for 3 PM. Reaching $5K would need coin-flip legs (pick\'em NHL games without a goalie edge, TNF Commanders/Giants at -132, Memphis -3.5, mega-line buy-downs like West Virginia -27.5 with no moneyline offered). So it stays short instead of being padded.', stake=5, lst=[])
D, R = '2026-11-12', '10:30 AM'
for t, typ in [(t, 'parlay') for t in new] + [(bs, 'lottery')]:
    if not already_in_history(H, t['name'], D, R):
        H.append({'date': D, 'run': R, 'type': typ, 'name': t['name'], 'odds': t['odds'], 'stake': t['stake'], 'result': 'pending', 'profit': 0,
                  'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'pending'} for l in t['legs']],
                  'whyExplanation': 'Pending.', 'lesson': ''})
totals = recompute_totals(H)
p['updated'] = p['results']['updated'] = 'Thu Nov 12, 2026 10:30 AM ET'
p['run'] = 'Thursday 10:30 AM: Wednesday graded. 2-leg parlays went 3-3 (misses: Spurs -5.5 by half a point, Knicks +6.5 by 1.5, Pelicans +7.5 in a 34-point Nets rout). The morning Best Shot lost on Seattle (-3000) falling to UTSA; the 3 PM Best Shot won. Today: two 2-leg parlays (Pistons +1.5 / George Mason -7.5, Wild +1.5 / Towson ML) and a short day-long Best Shot of six home moneylines. No singles cleared the edge bar. No +1000 lottery was possible without coin-flip legs. Late NBA/NHL, BYU, TNF and Thursday CFB are held for 3 PM.'
p['singles'], p['parlays'], p['lottery'] = [], new, [bs]
p['results']['totals'] = totals
for k in ('singles', 'parlays', 'lottery'): p['results'][k] = copy.deepcopy(totals[k])
p['results']['topLessons'] = [
 'Near-lock moneylines need a real tier gap: Seattle (-3000) lost by 27 to UTSA, an AAC visitor. Only back -1500+ moneylines when the visitor is from a lower league tier and ranks ~290+ (or the host is a Power/top-100 team vs a sub-200 visitor).',
 'NBA cushions need a favorite of -6.5 or more that is clearly the better team: the Pelicans (-3.5 vs 2-8 Brooklyn) lost by 34 and the Knicks (-4.5 on a back-to-back vs Cleveland) lost by 8. Small NBA favorites stay out of 2-leg parlays.',
 'NBA road favorites go on the plus side: Spurs -5.5 (from -14.5) missed by half a point at 1-8 Chicago. Road favorites get +1.5 or more, not a minus alt line (Pistons +1.5 today).',
 'NHL +1.5 with the goalie edge, including the favorite\'s own starter, went 2-0 again (Oilers, Vegas): Wild +1.5 (Wallstedt over Stolarz) today. Devils are held for 3 PM until their starter is confirmed.',
 'Don\'t pad the Best Shot: no pick\'em NHL, TNF coin flips or mega-line buy-downs; it stays short-priced and says so.',
]
p['results']['sources'] = 'FanDuel PA public odds (event-page API, pulled ~10:25 AM ET); ESPN scoreboards and box scores 11/11 (NBA/NHL/NCAAB finals) and 11/3-11/11 NCAAB results; ESPN NBA/NHL standings, injuries and team schedules; Daily Faceoff starting goalies 11/12; DariMarket/SportCrow/Yahoo Pistons-Wizards injury reports; Barttorvik 2027 T-Rank ratings (projected margins); lessons.md'
json.dump(p, open('/workspace/csb/picks.json', 'w'), indent=1)
print(totals['overall'])
for t in new + [bs]: print(t['name'], t['odds'], t['stake'], [(l['pick'], l['odds'], l['start'], l['marketId'], l['selectionId']) for l in t['legs']])
