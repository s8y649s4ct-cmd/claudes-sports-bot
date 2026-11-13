#!/usr/bin/env python3
"""Fri Nov 13, 2026 10:30 AM ET run: grade Thursday (grade_fri.py) then build Friday card.
Split plan: this card uses NYK/IND, UTA/HOU, POR/SAC, ATL/CHI, Bryant/Rutgers, Houston/Colorado + a day-long Best Shot
of tier-gap college moneylines. Held back for 3 PM (injury/goalie news): NBA GSW/SAS (Fox, Vassell questionable),
MIL/ORL (Suggs, da Silva), OKC/LAC, CLE/MIA, MEM/NO; NHL NYR/VAN, NSH/VGK; NCAAB Drake, Utah State, late West games.
FanDuel PA pulls (~10:25 AM ET, refreshed at build) cached in /workspace/fri13."""
import json, copy, os, datetime
src = open('/workspace/csb/build_sun_am.py').read()
src = src.replace("/workspace/sunam/fresh_ev_", "/workspace/fri13/fresh_ev_").split("add('Bears Home Cushion")[0]
exec(src)
add('Blazers Road Cushion + Rockets Bought-Down', [
 (36307626, ALT, rn('Portland Trail Blazers +1.5'), 'Portland Trail Blazers +1.5', 'NBA', 'Portland (8-3, +7.2 differential, 5-1 on the road) is the -10.5 road favorite at Sacramento (1-10, -12.7, 0-6 at home, 4 straight losses). The Kings\' home losses: by 11, 13, 15, 6, 7 and 27. Portland beat OKC twice this week and has won road games by 7, 22, 8 and 13 without Morant and Sharpe. Sacramento is without Simmons and Raynaud (Achiuwa questionable). Neither team played last night. Road favorites go on the plus side (Thursday lesson): +1.5 is 12 points of cushion, so the Kings must win by 2+ for the first home win of the season.'),
 (36307622, ALT, rn('Houston Rockets -6.5'), 'Houston Rockets -6.5', 'NBA', 'Houston (9-3, +8.9, 6-1 at home with home wins by 10, 21, 16, 10 and 7) is -16.5 vs Utah (1-11, 0-10 in its last 10, -11.5, 0-5 on the road with road losses by 22, 7, 12, 15 and 22). Utah is without Lauri Markkanen (hand fracture), Jaren Jackson Jr. (MCL) and Nurkic. Houston is missing Smart (suspended), Capela and Adams, which is why this is bought 10 points down rather than played near the main line. A home favorite that is clearly the better team with 10 points of cushion (the 9-10 point buy-down lesson). Neither team played last night.'),
], 'Two NBA favorites from the clearly-better side with 10-12 points of cushion: a road favorite on the plus side against the winless-at-home Kings, and the Rockets bought down 10 against a 0-10 Jazz team missing its two best players.')
add('Knicks Road Cushion + Scarlet Knights Bought-Down', [
 (36307624, ALT, rn('New York Knicks +1.5'), 'New York Knicks +1.5', 'NBA', 'New York (6-5, +6.8 differential, no one on the injury report) is the -8.5 road favorite at Indiana (4-8, -2.4, 1-4 at home). Tyrese Haliburton is out at least 10 more days and Aaron Nesmith is questionable. The Pacers\' home losses were by 5, 8, 4 and 12. New York beat Cleveland on the road by 12 and Milwaukee by 32 last week. Both teams are rested (neither played Thursday). Road favorite on the plus side: +1.5 is 10 points of cushion, so Indiana must win by 2+.'),
 (36313109, ALTN, rh('Rutgers', -13.5), 'Rutgers -13.5', 'NCAAB', 'Rutgers (2-0, T-Rank ~77, beat NJIT by 37 and New Haven by 27) is -22.5 (ML -10000) at home vs Bryant (1-3, T-Rank ~335), which lost by 10 at Quinnipiac, by 9 at home to Fairfield and by 23 at Providence. The T-Rank-style projection is Rutgers by ~22.5, which clears the buy-down rule with room (needs 13.5 + 5 = 18.5; we now want +7 = 20.5 after George Mason covered by half a point). A main line of -22.5 is inside the -15 to -26 range where 9-point buy-downs went 10/10. Tips 6:00 PM ET.'),
], 'A rested, healthy road favorite with 10 points of cushion against a Pacers team without Haliburton, plus a Big Ten host bought 9 points down against a bottom-30 visitor whose projection clears the buy-down bar by 9.')
add('Cougars Road Cushion + Hawks Big Cushion', [
 (36285252, ALT, rn('Houston (+3.5)'), 'Houston +3.5', 'NCAAF', 'No. 14 Houston (7-2, QB Conner Weigman active, no significant injuries) is the -9.5 road favorite at Colorado (3-6, 1-5 Big 12, 19.8 points per game; scored 7, 13, 7, 24, 24, 27 and 10 vs FBS teams). Colorado is missing WRs Kaleb Mathis and Danny Scudero, RB Micah Welch and S Naeten Mitchell. Houston has allowed 30+ only once and has the toughest past schedule in the Big 12; its two losses were at Texas Tech by 2 and at Utah by 8. Road favorites go on the plus side: +3.5 is 13 points of cushion, so Colorado must win by 4+. Kicks 10:15 PM ET.'),
 (36307623, ALT, rn('Atlanta Hawks +4.5'), 'Atlanta Hawks +4.5', 'NBA', 'Atlanta (7-5, +2.1, 4-2 on the road) is the -6.5 favorite at Chicago (1-9, -15.5 differential, 8 straight losses, 0-4 at home). Chicago\'s home losses were all close (by 4, 6, 6 and 5), which is why this gets 11 points of cushion rather than +1.5: the Bulls must win by 5+ for their first home win. Chicago is without Caleb Wilson (4-6 weeks) and Tobe Awaka, with Norman Powell questionable; Atlanta is without Gilbert and Newell (Flemings questionable). Neither team played last night. The Hawks are not a -6.5+ "clearly better" juggernaut, so the cushion is bigger than the usual 9-10.'),
], 'A healthy top-15 college road favorite at +3.5 (13 points of cushion) against a weak Colorado offense, plus an NBA road favorite with 11 points of cushion against a 1-9 Bulls team that has not won at home.')
bs = add('Best Shot $500K', [
 (36313108, ML, rn('Florida State'), 'Florida State ML', 'NCAAB', 'Florida State (T-Rank ~52, ACC) is -23.5 (ML -10000) at home vs Texas A&M-Corpus Christi (T-Rank ~194). Power host vs sub-200 visitor passes the tier-gap rule. Moneyline only: TAMU-CC won at Louisiana, so it is competent enough that a buy-down is not safe. FSU beat Troy by 23. Tips 5:00 PM ET.'),
 (36313212, ML, rn('NC State'), 'NC State ML', 'NCAAB', 'NC State (3-0, T-Rank ~34) is -22.5 (ML -10000) at home vs Troy (T-Rank ~164), which lost by 23 at Florida State. Moneyline only (Troy is a competent Sun Belt team).'),
 (36313232, ML, rn('UCF'), 'UCF ML', 'NCAAB', 'UCF (2-0, T-Rank ~72, Big 12) is -22.5 (ML -10000) at home vs Georgia Southern (T-Rank ~309), which lost at Georgia Tech and at home to Mercer.'),
 (36313233, ML, rn('TCU'), 'TCU ML', 'NCAAB', 'TCU (T-Rank ~59, Big 12) is -23.5 (ML -10000) at home vs Milwaukee (T-Rank ~246), which lost by 23 at Santa Clara. Moneyline only: TCU beat UL Monroe by only 8.'),
 (36313235, ML, rn('Arkansas'), 'Arkansas ML', 'NCAAB', 'Arkansas (T-Rank ~28, SEC) is -24.5 (ML -20000) at home vs Central Arkansas (T-Rank ~172), which lost by 32 at Ole Miss. Projection ~18, so moneyline only.'),
 (36313246, ML, rn('SMU'), 'SMU ML', 'NCAAB', 'SMU (2-0, T-Rank ~53, ACC; beat VMI by 25 and Prairie View by 35) is -22.5 (ML -10000) at home vs Ball State (T-Rank ~292).'),
 (36313220, ML, rn('Liberty'), 'Liberty ML', 'NCAAB', 'Liberty (T-Rank ~143, CUSA) is -17.5 (ML -3000) at home vs North Carolina Central (T-Rank ~353, MEAC), which lost by 14 at VMI. Lower-league visitor ranked 290+ passes the tier-gap rule.'),
 (36313236, ML, rn('Tarleton State'), 'Tarleton State ML', 'NCAAB', 'Tarleton State (T-Rank ~142, WAC) is -15.5 (ML -2800) at home vs 0-3 Alcorn State (T-Rank ~358, SWAC), which lost by 37 at Murray State. Projection ~17.5.'),
], 'A day-long safety ticket of eight home moneylines (-2800 to -20000), each against a lower-tier visitor (the Seattle/UTSA tier-gap rule). It is nowhere near the $5K target. The strongest priced legs are on the three 2-leg parlays (Ferdinand\'s priority), and the late NBA/NHL games are held for 3 PM injury and goalie news. Reaching $5K on $5 would need about ten coin-flip legs (pick\'em NBA games like Cavs/Heat and Grizzlies/Pelicans, FSU/Pitt CFB at -3.5, UCLA with a third-string QB, Xavier/Mississippi State, Stanford/UNLV). So it stays short instead of being padded. Skipped despite big prices: Purdue (-4500, lost at home to Valparaiso), California Baptist (lost at home to North Florida), mega-spread games with no moneyline (Duke -44.5, Vanderbilt -40.5, Florida -37.5, Illinois -36.5).', stake=5, lst=[])
D, R = '2026-11-13', '10:30 AM'
for t, typ in [(t, 'parlay') for t in new] + [(bs, 'lottery')]:
    if not already_in_history(H, t['name'], D, R):
        H.append({'date': D, 'run': R, 'type': typ, 'name': t['name'], 'odds': t['odds'], 'stake': t['stake'], 'result': 'pending', 'profit': 0,
                  'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'pending'} for l in t['legs']],
                  'whyExplanation': 'Pending.', 'lesson': ''})
totals = recompute_totals(H)
p['updated'] = p['results']['updated'] = 'Fri Nov 13, 2026 10:30 AM ET'
p['run'] = 'Friday 10:30 AM: graded Thursday 6-1 (all three 10:30 AM tickets and three of four 3:00 PM tickets won; Stars/Suns lost when Winnipeg beat Dallas 8-3). Three new 2-leg parlays: NBA favorites with 10-12 points of cushion (Blazers +1.5, Rockets -6.5, Knicks +1.5, Hawks +4.5), Rutgers bought 9 down vs a bottom-30 visitor, and No. 14 Houston +3.5 at Colorado, plus a day-long Best Shot of eight tier-gap college moneylines (short-priced, stated rather than padded). Spurs/Warriors, Magic/Bucks, Thunder/Clippers and both NHL games are held for 3 PM injury and goalie news. No singles cleared the edge bar. No +1000 lottery was possible without coin-flip legs.'
p['singles'], p['parlays'], p['lottery'] = [], new, [bs]
p['results']['totals'] = totals
for k in ('singles', 'parlays', 'lottery'): p['results'][k] = copy.deepcopy(totals[k])
p['results']['topLessons'] = [
 'Thursday went 6-1. The only loss was the smallest goalie edge on the board (Oettinger .906 vs Skinner .883): NHL +1.5 now needs an edge of about .025+ with the favorite\'s starter at .910+, or an opponent on a back-to-back.',
 'Buy-downs vs low-majors land close to the number in November (George Mason by 8 on -7.5, Tulsa by 9 on -8.5): the projection must now clear the buy-down by about 7 (Rutgers -13.5, projected ~22.5).',
 'NBA road favorites go on the plus side (Pistons +1.5 survived a 2OT game): Blazers +1.5, Knicks +1.5, Hawks +4.5 today.',
 'NBA cushions only on clearly better favorites with point-differential support; bigger cushion (11) when the home dog keeps games close (Bulls home losses by 4-6).',
 'Fade backup-QB teams rather than back them: UCLA (third-string QB, short week, vs an Illinois defense on a 4-game win streak) was skipped despite 9-0.',
 'Tier-gap rule for big college moneylines went 6/6 Thursday; today\'s eight Best Shot moneylines all pass it. Purdue (lost at home to Valparaiso) and Cal Baptist were skipped.',
]
p['results']['sources'] = 'FanDuel PA public odds (event-page API, pulled ~10:25 AM ET and refreshed at build); ESPN NBA/NHL/NCAAB/CFB scoreboards 10/20-11/12 (finals, back-to-backs, margins), ESPN NBA standings and injuries 11/13, ESPN CFB schedules; Daily Faceoff starting goalies 11/13; SI, CollegeFFB, UH Athletics (Houston-Colorado); VC Star, AP, CBS, Writing Illini (Illinois-UCLA); Barttorvik 2027 T-Rank ratings; lessons.md'
json.dump(p, open('/workspace/csb/picks.json', 'w'), indent=1)
print(totals['overall'], totals['legs'])
for t in new + [bs]: print(t['name'], t['odds'], t['stake'], [(l['pick'], l['odds'], l['start'], l['marketId'], l['selectionId']) for l in t['legs']])
