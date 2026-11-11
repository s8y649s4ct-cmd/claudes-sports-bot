#!/usr/bin/env python3
"""Wed Nov 11, 2026 3:00 PM ET run: nothing settled since 10:30 AM (every morning ticket finishes tonight).
Build from events held back by the morning card. Fresh FanDuel PA pulls (~2:55 PM ET) cached in /workspace/wed3."""
import json, copy, os, datetime
src = open('/workspace/csb/build_sun_am.py').read()
src = src.replace("/workspace/sunam/fresh_ev_", "/workspace/wed3/fresh_ev_").split("add('Bears Home Cushion")[0]
exec(src)
add('Oilers Home Ice + Rockets Home Cushion', [
 (36305493, APL, rn('Edmonton Oilers +1.5'), 'Edmonton Oilers +1.5', 'NHL', 'Edmonton (13-3-3, 6-2-2 last 10, won 2 straight) is the -188 home favorite vs Philadelphia (5-10-5, 2-6-2 on the road, -1.0 goal differential). Goalie edge: Tristan Jarry (.898) is confirmed for Edmonton vs Dan Vladar (.880, 3.27 GAA) for Philly. Both teams are rested. +1.5 only loses if the Flyers win by 2+ in Edmonton; only one of the Oilers\' home games this year was a loss by 2+ (7-2 vs Toronto).'),
 (36298494, ALT, rn('Houston Rockets +3.5'), 'Houston Rockets +3.5', 'NBA', 'Houston (8-3, 5-1 at home, +9.1 differential) is the -6.5 home favorite. Home wins: Dallas by 18, Atlanta by 10, OKC by 21, Boston by 16 and Denver by 10. Golden State has won 8 straight but did it on a 6-game homestand (2-2 on the road). Tonight starts a 5-game trip without Payton II, Williams, Porzingis, Butler and Moody. Houston is missing only centers Capela and Adams. +3.5 is 10 points of cushion: the Warriors must win by 4+ in Houston. Last season\'s three meetings were all decided by 4 or fewer.'),
], 'A strong NHL home favorite at +1.5 with the goalie edge, plus the better-rested, healthier NBA home favorite bought 10 points down.')
add('Golden Knights Home Ice + Celtics Big Cushion', [
 (36305489, APL, rn('Vegas Golden Knights +1.5'), 'Vegas Golden Knights +1.5', 'NHL', 'Vegas (12-5-2, won 3 straight) is the -128 home favorite vs Utah (10-7-1, lost 2 straight). Goalie edge: Carter Hart (.900, 2.48 GAA) is confirmed vs Sebastian Cossa (.873, 3.38). It is a near pick\'em, which is exactly why this is +1.5 and not the moneyline. The Wild had the same -128 goalie-edge setup Tuesday and covered. +1.5 only loses if Utah wins by 2+.'),
 (36298487, ALT, rn('Boston Celtics +7.5'), 'Boston Celtics +7.5', 'NBA', 'Boston (9-2, 4 straight wins, +11.7 differential) is -5.5 at Toronto. Boston is on a road back-to-back (beat Philadelphia by 22 last night, so starters sat late) and Paul George is out. That is why this is +7.5, 13 points of cushion, and not the spread (the back-to-back rule). Toronto (5-5, 2-2 at home) is without Scottie Barnes, Trayce Jackson-Davis and Kawhi Leonard, and Quickley and Murray-Boyles are questionable. Only loses if the short-handed Raptors win by 8+.'),
], 'A near pick\'em NHL favorite with the goalie edge at +1.5, plus the clearly better NBA team with 13 points of cushion against a depleted host.')
add('Nuggets + Pelicans Cushions', [
 (36298491, ALT, rn('Denver Nuggets +7.5'), 'Denver Nuggets +7.5', 'NBA', 'Denver is the -3.5 road favorite at Memphis. Both teams last played Monday, so no back-to-back. Memphis is without Scotty Pippen Jr. and Quinten Post, Isaiah Stewart is questionable, and the Grizzlies are 2-3 at home. Denver is missing only Julian Strawther. +7.5 is 11 points of cushion: Memphis must win by 8+. Road-favorite form check: Denver\'s 4 losses were to OKC, Golden State, Portland and Houston, all playoff-level teams.'),
 (36298486, ALT, rn('New Orleans Pelicans +7.5'), 'New Orleans Pelicans +7.5', 'NBA', 'New Orleans is the -3.5 home favorite vs 2-8 Brooklyn (1-5 on the road, -9.0 differential, lost by 37 at Dallas last time out). Both teams are rested. +7.5 is 11 points of cushion: the Nets would have to win by 8+ in New Orleans. Brooklyn\'s two wins this year came by 10 and 8.'),
], 'Two NBA favorites, each with 11 points of cushion and no back-to-back, against weaker or short-handed opponents.')
bs = add('Best Shot $500K', [
 (36306806, ML, rn('Grand Canyon'), 'Grand Canyon ML', 'NCAAB', 'Grand Canyon is -18.5 (ML -4000) at home vs Cal Poly. A Torvik-style model projects GCU by ~17, and GCU beat Bethune-Cookman by 18. Cal Poly (T-Rank ~165) scored 84 at Arizona, so it is a competent mid-major. Under Tuesday\'s lesson (8-9 point buy-downs vs competent mid-majors failed 3 times), that means moneyline only. The -9.5 buy-down held back this morning was dropped.'),
 (36298488, ALT, rn('Orlando Magic +12.5'), 'Orlando Magic +12.5', 'NBA', 'Orlando is the -4.5 favorite at 1-10 Utah (9 straight losses, 1-5 at home, -11.1 differential, without Markkanen, Jaren Jackson Jr. and Nurkic). Both teams are on the second night of a back-to-back. Orlando is depleted (Banchero, Suggs, Isaac out), which is why the cushion is 17 points. Utah has not beaten anyone by more than 1 point this year.'),
 (36305488, APL, rn('Anaheim Ducks +2.5'), 'Anaheim Ducks +2.5', 'NHL', 'Anaheim (won 5 straight) is the -137 home favorite vs Nashville, which is on the second night of a back-to-back (won 3-0 at LA last night) and starts backup Justus Annunen (.874). Only one of the Ducks\' 8 home games was a loss by 3+. +2.5 only loses on a Nashville win by 3+ goals. Not +1.5: Brossoit (.877) is no goalie edge.'),
], 'A short-priced safety ticket, far short of +1000 and the $5K target. Every stronger leg tonight is on one of the three 2-leg parlays (Ferdinand\'s priority), and we never repeat an event. Getting to +1000 would mean adding coin-flip legs: Penguins/Rangers with weak or backup goalies, Lightning/Sabres with no goalie edge, Cal Baptist (0-2 under a new coach, lost at home to North Florida; BetMGM model only 79%), USC at Cal (model projects USC by only ~4), or buy-downs from -29.5 to -46.5 mega lines. So it stays short instead of being padded. The morning\'s day-long Best Shot is still live.', stake=5, lst=[])
D, R = '2026-11-11', '3:00 PM'
for t, typ in [(t, 'parlay') for t in new] + [(bs, 'lottery')]:
    if not already_in_history(H, t['name'], D, R):
        H.append({'date': D, 'run': R, 'type': typ, 'name': t['name'], 'odds': t['odds'], 'stake': t['stake'], 'result': 'pending', 'profit': 0,
                  'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'pending'} for l in t['legs']],
                  'whyExplanation': 'Pending.', 'lesson': ''})
totals = recompute_totals(H)
p['updated'] = p['results']['updated'] = 'Wed Nov 11, 2026 3:00 PM ET'
p['run'] = 'Wednesday 3:00 PM: nothing new settled since 10:30 AM. Every morning ticket finishes tonight (still pending, see the record). Three new 2-leg parlays from the events held back this morning: two NHL favorites at +1.5 with the goalie edge, NBA favorites with 10-13 points of cushion, plus a short-priced Best Shot. No singles cleared the edge bar. No +1000 lottery was possible without coin-flip legs.'
p['singles'], p['parlays'], p['lottery'] = [], new, [bs]
p['results']['totals'] = totals
for k in ('singles', 'parlays', 'lottery'): p['results'][k] = copy.deepcopy(totals[k])
p['results']['topLessons'] = [
 'NHL +1.5 only with the goalie edge, including the favorite\'s own starter: Jarry over Vladar (Oilers) and Hart over Cossa (Vegas) qualified. Penguins (Murashov .878), Rangers (backup Korpisalo) and Lightning/Sabres (no edge) were skipped.',
 'Back-to-back rule: Boston is on a road back-to-back, so it gets +7.5 (13 of cushion) instead of the spread, and only because Toronto is missing Barnes, Jackson-Davis and Leonard.',
 'Buy-downs vs competent mid-majors stay out: GCU vs Cal Poly (T-Rank ~165) is moneyline only, and the morning\'s held-back GCU -9.5 was dropped.',
 'NBA totals need ~90% of both teams\' games to clear the alt: DEN/MEM, WSH/IND, BKN/NO, BOS/TOR, ORL/UTA and OKC/POR all failed the game-log check.',
 'Don\'t pad the Best Shot: Cal Baptist (0-2, lost at home to UNF), USC at Cal (projected by ~4) and -29.5+ mega-line buy-downs were all skipped.',
]
p['results']['sources'] = 'FanDuel PA public odds (event-page API, pulled ~2:55 PM ET); ESPN NBA/NHL standings, injuries, team schedules and scoreboards (Nov 9-10); Daily Faceoff starting goalies 11/11; NBA.com/SI/CBS Sports Warriors-Rockets previews; CBU Athletics/BetMGM/FOX Sports (Chicago State-Cal Baptist); Barttorvik 2027 T-Rank ratings (projected margins); ESPN NCAAB results Nov 3-10; lessons.md'
json.dump(p, open('/workspace/csb/picks.json', 'w'), indent=1)
print(totals['overall'], totals['parlays'], totals['lottery'], totals['singles'])
for t in new + [bs]: print(t['name'], t['odds'], t['stake'], [(l['pick'], l['odds'], l['start'], l['marketId'], l['selectionId']) for l in t['legs']])
