#!/usr/bin/env python3
"""Tue Nov 10, 2026 3:00 PM ET run: nothing settled since 10:30 AM (whole morning card plays tonight).
Build from events held back by the morning card. Fresh FanDuel PA pulls cached in /workspace/tue3."""
import json, copy, os, datetime
src = open('/workspace/csb/build_sun_am.py').read()
src = src.replace("/workspace/sunam/fresh_ev_", "/workspace/tue3/fresh_ev_").split("add('Bears Home Cushion")[0]
exec(src)
ALTT = lambda mn: mn == 'Alternate Total Points'
add('Wild + Blues Ice Cushions', [
 (36299761, APL, rn('Minnesota Wild +1.5'), 'Minnesota Wild +1.5', 'NHL', 'Minnesota (12-3-4, leads the Central, 7-3-2 on the road) is the -128 road favorite at Montreal. Jesper Wallstedt (11-2-3, 1.99 GAA, .922) is confirmed. Montreal is good (11-3-3) with Jacob Fowler in net, which is exactly why this is +1.5 and not the moneyline: the Wild cash on any win or any one-goal loss, including every overtime/shootout loss. Road favorites at +1.5 have cashed in NJ, TB and NYI spots this week.'),
 (36299764, APL, rn('St. Louis Blues +1.5'), 'St. Louis Blues +1.5', 'NHL', 'St. Louis is the -144 home favorite vs Detroit, which has lost 3 straight while scoring 3 goals total. Detroit starts John Gibson in his first game back from a lower-body injury (.860 SV%, 3.46 GAA); Joel Hofer (.919) starts for the Blues. +1.5 only loses if the Red Wings win by 2+.'),
], 'Two NHL favorites at +1.5 with the goalie edge (Wallstedt; Hofer vs a rusty Gibson). Each leg survives a one-goal loss.')
add('Cavaliers Bought-Down + Magic/Kings Over', [
 (36302964, ALTN, rh('Virginia', -29.5), 'Virginia -29.5', 'NCAAB', 'No. 6 Virginia (3-0; beat Drexel by 29, Northeastern by 25 and No. 12 Arkansas by 19) is -38.5 at home vs Bucknell, KenPom No. 344, which lost by 29 at Maryland and by 20 at home to Old Dominion. No injuries on either side. -29.5 is 9 points of cushion against a true bottom-tier visitor (the only buy-down spot that has held up). Previews project 98-65 and 105-67.'),
 (36295138, ALTT, rn('Over 209.5'), 'Magic/Kings Over 209.5', 'NBA', 'Main total 222.5, so Over 209.5 is 13 points of cushion. Sacramento has gone over 214 in all 10 of its games (215-252) and gives up 117+ a night. Orlando is short-handed (Banchero, Suggs, Isaac out), so it has gone under 210 in 3 of 9 games, which is why the cushion is 13 and not a smaller alt.'),
], 'A top-10 host bought 9 points down vs a KenPom 300+ team, plus an NBA total with 13 points of cushion in a game where Sacramento has topped 214 every time.')
add('Commodores ML + Clippers/Suns Over', [
 (36302669, ML, rn('Vanderbilt'), 'Vanderbilt ML', 'NCAAB', 'Vanderbilt is -14.5 (ML -1600) at home vs Memphis. Vandy beat Wake Forest by 23. Memphis is competent (beat VCU by 1), so we take the moneyline only, no buy-down.'),
 (36295142, ALTT, rn('Over 210.5'), 'Clippers/Suns Over 210.5', 'NBA', 'Main total 224.5, so Over 210.5 is 14 points of cushion. 14 of 18 combined Clippers and Suns games went over 210 this year. We fade Phoenix on a back-to-back (lost by 26 at home to the Spurs last night) and avoid both sides here; a tired defense helps the over.'),
], 'An SEC home moneyline plus an NBA total with 14 points of cushion. Lower payout, but both legs avoid the spread.')
bs = add('Best Shot $500K', [
 (36302722, ML, rn('Baylor'), 'Baylor ML', 'NCAAB', 'Baylor is -19.5 (ML -4500) at home vs Yale. Baylor beat Arkansas-Pine Bluff by 56; Yale lost by 12 at UCF. Yale is a good Ivy team, so moneyline only, no buy-down.'),
 (36302772, ML, rn('Arizona State'), 'Arizona State ML', 'NCAAB', 'ASU is -18.5 (ML -4000) at home vs Hofstra after beating Northern Colorado by 27. Hofstra is a competent CAA team (lost by 2 at Princeton), so moneyline only.'),
 (36302769, ML, rn('Utah'), 'Utah ML', 'NCAAB', 'Utah is -16.5 (ML -3000) at home vs Weber State, which lost at home to Utah Valley. Moneyline only (Utah beat Towson by just 10).'),
 (36302748, ML, rn('Colorado'), 'Colorado ML', 'NCAAB', 'Colorado is -12.5 (ML -1000) at home at altitude vs San Diego (a bottom-half WCC team). Colorado lost at home to a good San Diego State team, so moneyline only.'),
 (36302783, ML, rn('New Mexico'), 'New Mexico ML', 'NCAAB', 'New Mexico is -22.5 (ML -10000) at home vs 0-2 Little Rock (lost at home to SE Louisiana). Models project an 18-point margin. Little Rock is KenPom ~217 (lost by just 10 at VCU), not bottom-tier, so no buy-down.'),
], 'Built only from Power-conference home moneylines at -1000 or shorter. Every stronger leg is already on the morning card or the three 2-leg parlays above, and we never repeat an event. The only other options are coin-flip legs: Panthers/Kings +1.5, Utah State or New Mexico buy-downs vs competent mid-majors, and pick\'em games. So this is a short-priced safety ticket, nowhere near +1000 or the $5K target.', stake=5, lst=[])
D, R = '2026-11-10', '3:00 PM'
for t, typ in [(t, 'parlay') for t in new] + [(bs, 'lottery')]:
    if not already_in_history(H, t['name'], D, R):
        H.append({'date': D, 'run': R, 'type': typ, 'name': t['name'], 'odds': t['odds'], 'stake': t['stake'], 'result': 'pending', 'profit': 0,
                  'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'pending'} for l in t['legs']],
                  'whyExplanation': 'Pending.', 'lesson': ''})
totals = recompute_totals(H)
p['updated'] = p['results']['updated'] = 'Tue Nov 10, 2026 3:00 PM ET'
p['run'] = 'Tuesday 3:00 PM: nothing new settled since 10:30 AM, and the whole morning card plays tonight (still pending, see the record). Three new 2-leg parlays from the events held back for this run, plus a short-priced Best Shot of home moneylines. No singles cleared the edge bar. No +1000 lottery was possible without weak legs.'
p['singles'], p['parlays'], p['lottery'] = [], new, [bs]
p['results']['totals'] = totals
for k in ('singles', 'parlays', 'lottery'): p['results'][k] = copy.deepcopy(totals[k])
p['results']['topLessons'] = [
 'Buy down only vs truly bottom-tier visitors (KenPom 300+, SWAC/MEAC/NEC, teams already blown out). Utah Tech and Little Rock (KenPom ~200s, close losses to good teams) got moneylines or nothing, not 9-point buy-downs.',
 'Mid-major vs mid-major and mid-major short favorites stay off tickets (Davidson, MTSU, Tulane, Kennesaw, Fordham, SF skipped).',
 'NHL +1.5 only on favorites with the goalie edge; skip near pick\'em favorites in bad form (Panthers with a struggling Markstrom, Kings 2-5 at home).',
 'Fade NBA back-to-backs and road favorites that fail a form check (Orlando lost by 30 and 13 on the road; Phoenix played last night). Use big-cushion totals instead of sides.',
 'Plan the day: when the morning card builds a day-long Best Shot, the 3 PM Best Shot will be short-priced. Say so rather than pad it.',
]
p['results']['sources'] = 'FanDuel PA public odds (event-page API, pulled ~3:00 PM ET); ESPN NCAAB scoreboards Nov 3-9, ESPN NBA team schedules/injuries (Nov 10), ESPN NHL/NBA scoreboards Nov 8-10; Daily Faceoff starting goalies (Nov 10); Streaking The Lawn/SI/TeamRankings (UVA-Bucknell); The Pit Press/GoLobos/The Breakdown (UNM-Little Rock); USU Athletics/HJ News/The Low Post (USU-Utah Tech); lessons.md'
json.dump(p, open('/workspace/csb/picks.json', 'w'), indent=1)
print(totals['overall'], totals['parlays'], totals['lottery'], totals['singles'])
for t in new + [bs]: print(t['name'], t['odds'], t['stake'], [(l['pick'], l['odds'], l['start']) for l in t['legs']])
