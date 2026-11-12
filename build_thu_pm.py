#!/usr/bin/env python3
"""Thu Nov 12, 2026 3:00 PM ET run: nothing settled since 10:30 AM (all morning tickets finish tonight).
Build from events held back by the morning card. Fresh FanDuel PA pulls (~2:58 PM ET) cached in /workspace/thu3."""
import json, copy, os, datetime
src = open('/workspace/csb/build_sun_am.py').read()
src = src.replace("/workspace/sunam/fresh_ev_", "/workspace/thu3/fresh_ev_").split("add('Bears Home Cushion")[0]
exec(src)
add('Devils + Senators Goalie-Edge Ice', [
 (36309084, APL, rn('New Jersey Devils +1.5'), 'New Jersey Devils +1.5', 'NHL', 'New Jersey (13-6-0, 8-2-0 at home) is the -154 home favorite vs Washington (10-6-0, 3-2-0 on the road). This is the leg held this morning pending the goalie: Connor Hellebuyck (.913) is now confirmed by the Devils vs Logan Thompson (.891, not yet confirmed). Neither team played last night. +1.5 only loses if the Capitals win by 2+ in Newark, where the Devils have lost only twice all season.'),
 (36309077, APL, rn('Ottawa Senators +1.5'), 'Ottawa Senators +1.5', 'NHL', 'A pick\'em (-110 each) with the biggest goalie edge on the board: Linus Ullmark (.945, confirmed) for Ottawa vs Scott Wedgewood (.867, confirmed) for Colorado. Ottawa is 6-2-1 at home; Colorado is 4-5-0 on the road. Neither team played last night. Same setup as Vegas (-128, Hart over Cossa), which covered +1.5 Wednesday. Only loses if Colorado wins by 2+.'),
], 'Two NHL home teams at +1.5, each with a confirmed starting goalie edge (Hellebuyck over Thompson, Ullmark .945 over Wedgewood .867), against rested but weaker road teams.')
add('Islanders + Blues Goalie-Edge Ice', [
 (36309081, APL, rn('New York Islanders +1.5'), 'New York Islanders +1.5', 'NHL', 'Near pick\'em (+102) at Los Angeles, which is 5-9-2 overall and 2-6-0 at home. Goalie edge: Ilya Sorokin (.914, likely) vs Darcy Kuemper (.877, likely). Neither team played last night. +1.5 only loses if the Kings win by 2+; they have won only two home games all season. Sorokin\'s Islanders covered +1.5 in a shootout loss Monday.'),
 (36309082, APL, rn('St. Louis Blues +1.5'), 'St. Louis Blues +1.5', 'NHL', 'St. Louis is the -126 road favorite at Utah. Utah is on the second night of a back-to-back (lost 5-3 at Vegas last night) and travels home; St. Louis is rested. Goalie edge: Joel Hofer (.920, confirmed) vs Karel Vejmelka (.866, likely). Road favorites go on the plus side (lesson), so +1.5, not the moneyline. The Blues are only 3-6-1 on the road, which is why this is +1.5: Utah must win by 2+ on tired legs.'),
], 'Two NHL +1.5 legs with a clear goalie edge: Sorokin vs a Kings team that is 2-6 at home, and a rested Blues team with Hofer vs a Utah team on a back-to-back.')
add('Stars Home Ice + Suns Big Cushion', [
 (36309083, APL, rn('Dallas Stars +1.5'), 'Dallas Stars +1.5', 'NHL', 'Dallas (10-5-2) is the -172 home favorite vs Winnipeg (8-8-3, 3-4-2 on the road). Goalie edge: Jake Oettinger (.906, confirmed) vs Stuart Skinner (.883, confirmed). Both teams are rested. +1.5 only loses if the Jets win by 2+ in Dallas.'),
 (36303939, ALT, rn('Phoenix Suns +4.5'), 'Phoenix Suns +4.5', 'NBA', 'Phoenix is the -6.5 home favorite (held this morning for injury news). Charlotte (4-7, -11.6 differential, 1-3 on the road, 98.8 points per game) is confirmed without Brandon Miller, Kon Knueppel and Dennis Schroder, three of its top four guards and wings. Phoenix (4-3 at home, -5.3 differential) is without only Mark Williams and just beat the Clippers by 23. Neither team played last night. +4.5 is 11 points of cushion: Charlotte must win by 5+ in Phoenix. Not a smaller cushion because Phoenix\'s defense ranks 28th.'),
], 'A home NHL favorite at +1.5 with the goalie edge, plus an NBA home favorite with 11 points of cushion against a Hornets team missing three starters.')
bs = add('Best Shot $500K', [
 (36309919, ML, rn('West Virginia'), 'West Virginia ML', 'NCAAB', 'West Virginia (2-0, T-Rank ~43, Big 12) is -24.5 (ML -20000) at home vs Mercer (T-Rank ~244), which lost by 29 at Virginia Tech. A Power-conference, top-50 host vs a sub-200 visitor passes the tier-gap rule. Model projects WVU by ~20, which does not clear the buy-down rule, so moneyline only. Tips 7:00 PM ET.'),
 (36309089, APL, rn('Florida Panthers +1.5'), 'Florida Panthers +1.5', 'NHL', 'Florida is the -172 home favorite vs Detroit (7-9-3, 3-4-2 on the road). Goalie edge: Akira Schmid (.886, confirmed) vs John Gibson (.866, confirmed). Both teams are rested. +1.5 only loses if Detroit wins by 2+.'),
 (36285247, ALT, rn('Louisiana (+3.5)'), 'Louisiana +3.5', 'NCAAF', 'Louisiana (6-3) is the -10.5 road favorite at UL Monroe (2-7, 0-4 at home, home losses by 3, 28, 24 and 14, including to FCS SE Louisiana). Road favorites go on the plus side: +3.5 means ULM must win by 4+. Louisiana\'s road losses were at USC and at Southern Miss (by 4) and Louisiana Tech (by 1); it beat Charlotte by 27 on the road.'),
], 'A short-priced safety ticket, far short of +1000 and the $5K target. The strongest legs tonight are on the three 2-leg parlays (Ferdinand\'s priority), and we never repeat an event, including the morning\'s pending tickets. Reaching $5K on $5 would need roughly ten coin-flip legs (TNF Commanders/Giants, Memphis -3.5, Bruins/Canadiens and Lightning/Blue Jackets with no goalie edge, a Sabres team on a back-to-back with a backup, 76ers without LeBron and maybe Embiid, small NBA favorites). So it stays short instead of being padded. The morning\'s day-long Best Shot is still live.', stake=5, lst=[])
D, R = '2026-11-12', '3:00 PM'
for t, typ in [(t, 'parlay') for t in new] + [(bs, 'lottery')]:
    if not already_in_history(H, t['name'], D, R):
        H.append({'date': D, 'run': R, 'type': typ, 'name': t['name'], 'odds': t['odds'], 'stake': t['stake'], 'result': 'pending', 'profit': 0,
                  'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'pending'} for l in t['legs']],
                  'whyExplanation': 'Pending.', 'lesson': ''})
totals = recompute_totals(H)
p['updated'] = p['results']['updated'] = 'Thu Nov 12, 2026 3:00 PM ET'
p['run'] = 'Thursday 3:00 PM: nothing new settled since 10:30 AM. Every morning ticket finishes tonight (still pending, see the record). Three new 2-leg parlays from the events held back this morning: five NHL +1.5 legs with a confirmed or likely goalie edge (Devils with Hellebuyck now confirmed) and Suns +4.5 vs a Charlotte team missing three starters, plus a short-priced Best Shot. The held 76ers leg was dropped (LeBron out, Embiid questionable, Philly only +1.0 point differential). No singles cleared the edge bar. No +1000 lottery was possible without coin-flip legs.'
p['singles'], p['parlays'], p['lottery'] = [], new, [bs]
p['results']['totals'] = totals
for k in ('singles', 'parlays', 'lottery'): p['results'][k] = copy.deepcopy(totals[k])
p['results']['topLessons'] = [
 'Held legs are re-checked, not pre-approved: Devils +1.5 went in once Hellebuyck was confirmed; 76ers -7.5 was dropped (LeBron out, Embiid questionable, line fell from -10.5 to -7.5, and Philly\'s +1.0 differential is not "clearly better").',
 'NHL +1.5 only with the goalie edge, including the favorite\'s own starter: Hellebuyck, Ullmark (.945), Sorokin, Hofer, Oettinger and Schmid qualified. Bruins/Canadiens (Swayman vs Fowler) and Lightning/Blue Jackets had no edge and were skipped.',
 'Back-to-back check from last night\'s scoreboard: Utah (lost at Vegas), Tampa Bay and Buffalo all play the second night; Blues +1.5 targets the tired Utah team; Buffalo (backup Lyon) was skipped.',
 'Road favorites go on the plus side: Blues +1.5 and Louisiana +3.5, not the moneyline or spread.',
 'Tier-gap rule for big moneylines: West Virginia (top-50 Big 12) vs Mercer (~244) passes; BYU vs Montana State (~126) and Bradley (1-2, lost at home to Pacific) do not.',
 'Don\'t pad the Best Shot: no TNF coin flip, no pick\'em NHL without a goalie edge, no small NBA favorites.',
]
p['results']['sources'] = 'FanDuel PA public odds (event-page API, pulled ~2:58 PM ET); ESPN NBA/NHL scoreboards 11/11 (back-to-backs) and 11/12, ESPN NBA injuries and standings; NBA official injury report 11/12 8 AM; ESPN/Inquirer/NBA.com (Embiid, LeBron); Fadeaway World/TotalApex (Hornets-Suns); Daily Faceoff starting goalies 11/12; ESPN college football schedules (Louisiana, ULM); Barttorvik 2027 T-Rank ratings; lessons.md'
json.dump(p, open('/workspace/csb/picks.json', 'w'), indent=1)
print(totals['overall'], totals['legs'])
for t in new + [bs]: print(t['name'], t['odds'], t['stake'], [(l['pick'], l['odds'], l['start'], l['marketId'], l['selectionId']) for l in t['legs']])
