#!/usr/bin/env python3
"""Mon Nov 16, 2026 10:30 AM ET run. Fresh FanDuel PA pulls in /workspace/mon16am."""
import json, copy, os, datetime, glob
src = open('/workspace/csb/build_sun_am.py').read()
src = src.replace("/workspace/sunam/fresh_ev_", "/workspace/mon16am/fresh_ev_").split("add('Bears Home Cushion")[0]
exec(src)
MN = lambda name: (lambda mn: mn == name)
ASP = MN('Alternate Spread')
add('Celtics Home Cushion + Nuggets Home Cushion', [
 (36319063, ASP, rn('Boston Celtics +1.5'), 'Boston Celtics +1.5', 'NBA', 'Boston (11-2, 6-0 at home) is the -8.5 home favorite over Orlando (5-7), which is without Paolo Banchero, Jonathan Isaac and Noah Penda. Boston already won by 11 in Orlando this season and has no injuries listed. The Celtics lose this leg only if Orlando wins outright by 2+. Priced at -335, far better value than the -850 we paid for the same leg Sunday. Tips 7:10 PM ET.'),
 (36319062, ASP, rn('Denver Nuggets +4.5'), 'Denver Nuggets +4.5', 'NBA', 'Denver (7-4) is -9.5 at home to Phoenix (5-7, 0-3 on the road: lost at Portland by 41, at OKC by 11, at Golden State by 3). +4.5 is 14 points off the main line. The bigger cushion (not +1.5) is because Denver is only 2-2 at home (lost to Golden State by 20 and Portland by 8). Only Julian Strawther is out for Denver; Phoenix is without Mark Williams. Tips 9:10 PM ET.'),
], 'Two strong home favorites taken on the plus side: the Celtics are unbeaten at home against a Banchero-less Magic, and the Nuggets get a 14-point cushion against a Suns team that has not won on the road.')
add('76ers Road Cushion + Cavs Home Cushion', [
 (36319067, ASP, rn('Philadelphia 76ers +4.5'), 'Philadelphia 76ers +4.5', 'NBA', 'Philadelphia (11-3, 5-1 on the road) is -5.5 at Brooklyn (3-9, 1-3 at home). Home-loss check passes: the Nets lost at home by 7 (Charlotte), 27 (Indiana) and 16 (Detroit). +4.5 is 10 points off the main line. The cushion is +4.5, not +1.5, because Joel Embiid is day-to-day. Tips 7:40 PM ET.'),
 (36319064, ASP, rn('Cleveland Cavaliers +4.5'), 'Cleveland Cavaliers +4.5', 'NBA', 'Cleveland (7-7, 5-2 at home) is -9.5 vs Chicago (3-9, 2-5 on the road, with road losses by 43, 35, 30, 19 and 14). +4.5 is 14 points off the main line. The cushion is sized up because Evan Mobley, Sam Merrill and Nae\'Qwan Tomlin are out. Cleveland\'s two home losses were to OKC (by 5) and New York (by 12). Tips 7:10 PM ET.'),
], 'A clearly better road team against a Nets side that loses at home by 7+, plus a home favorite with a 14-point cushion against a Bulls team that gets blown out on the road. Both cushions are sized to the injury list.')
bs = add('Best Shot $500K', [
 (36326452, ML, rn('UC San Diego'), 'UC San Diego ML', 'NCAAB', 'Tier gap: UC San Diego (T-Rank 129) hosts Texas Southern (T-Rank 335, 1-3). UCSD is -19.5. Tips 10:00 PM ET.'),
 (36319061, ASP, rn('Memphis Grizzlies +7.5'), 'Memphis Grizzlies +7.5', 'NBA', 'Memphis (9-4, 6-0 on the road, winning road games by 3, 5, 11, 16, 21 and 31) is -3.5 at Washington (4-10, 2-4 at home). +7.5 is 11 points off the main line, so the Wizards must win by 8+. The deep cushion is because Memphis is short-handed: Ty Jerome, Scotty Pippen Jr. and Quinten Post are out, and Zach Edey and Isaiah Stewart are day-to-day. Washington lost at home by 10, 15, 28 and 4. Tips 7:10 PM ET.'),
 (36275768, MN('Alternate Total Points'), (lambda r, m: '27.5' in r.get('runnerName', '') and r.get('runnerName', '').startswith('Over')), 'Chargers/Ravens Over 27.5 Points', 'NFL', 'Game-log test: all 8 Chargers games have had 28+ total points (lowest 28, 33), and 8 of 9 Ravens games have too (the exception was 23). Main total is 38.5, so this is 11 points of cushion. Risk: Baltimore starts Jacoby Brissett with Lamar Jackson on IR, and the Chargers (0-8) are without Ladd McConkey. Kicks 8:15 PM ET.'),
], 'The three highest-probability legs left after the two parlays: a bottom-tier college mismatch (the -100000 moneylines were left out because they add nothing), a deep 11-point cushion on an unbeaten road team, and a low NFL alt total that clears the game-log test. Far short of the $5K target; every other leg tonight failed a rule and would be a 60-80% leg, so it is not padded.', stake=5, lst=[])
D, R = '2026-11-16', '10:30 AM'
for t, typ in [(t, 'parlay') for t in new] + [(bs, 'lottery')]:
    if not already_in_history(H, t['name'], D, R):
        H.append({'date': D, 'run': R, 'type': typ, 'name': t['name'], 'odds': t['odds'], 'stake': t['stake'], 'result': 'pending', 'profit': 0,
                  'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'pending'} for l in t['legs']],
                  'whyExplanation': 'Pending.', 'lesson': ''})
totals = recompute_totals(H)
p['updated'] = p['results']['updated'] = 'Mon Nov 16, 2026 10:30 AM ET'
p['run'] = ("Monday 10:30 AM: Sunday went 4-0 (both parlays and both Best Shots won, 13/13 legs). Today's card: two 2-leg NBA cushion parlays "
 "(Celtics +1.5 / Nuggets +4.5 and 76ers +4.5 / Cavs +4.5) and a 3-leg Best Shot (UC San Diego ML, Grizzlies +7.5, Chargers/Ravens Over 27.5). "
 "No singles (no real plus-money edge) and no +1000 lottery (it would need coin-flip legs). NHL legs were skipped because no starting goalie was confirmed at build time.")
p['singles'], p['parlays'], p['lottery'] = [], new, [bs]
p['results']['totals'] = totals
for k in ('singles', 'parlays', 'lottery'): p['results'][k] = copy.deepcopy(totals[k])
p['results']['topLessons'] = [
 'Sunday went 4-0 and 13/13 legs with plus-side cushions, the home-loss check and bottom-tier tier gaps. Today\'s card uses only those leg types.',
 'Size the cushion to the injury list: Celtics (healthy, opponent missing Banchero) get +1.5. Sixers (Embiid day-to-day) and Cavs (no Mobley) get +4.5. Memphis (four rotation players out or doubtful) gets +7.5.',
 'Home-loss check: Nets (home losses by 7, 27, 16) and Wizards (by 10, 15, 28, 4) pass. Miami/Houston, New Orleans/Golden State (Curry, Butler, Porzingis out) and Minnesota/Portland (Edwards out) failed and were skipped.',
 'Tier gaps only vs T-Rank 300+ visitors with a top-150 host: UCSD vs Texas Southern (335) passes. Clemson vs The Citadel (346) also passed, but FanDuel flags that moneyline as not parlay-safe (no in-play market), so it was left off. UTEP (162) vs FAMU failed the host test. The -100000 moneylines (Maryland, Ohio State, Kentucky, Minnesota, Texas A&M, UCLA) add nothing.',
 'No MNF side: the Ravens are 1-3 at home with Brissett at QB, and the 0-8 Chargers are not a clearly better team. Only the alt total passed (game-log test 16/17).',
 'NHL goalie-edge +1.5 legs need a confirmed starter. None was confirmed at 10:30 AM, so none were used.',
]
p['results']['sources'] = ('FanDuel PA public odds (content-managed pages and event-page API, pulled ~10:30 AM ET 11/16); ESPN scoreboards 11/15 (grading) and 11/16; '
 'ESPN NBA and NFL injury reports 11/16; ESPN team schedules (home-loss check, game-log totals); Barttorvik T-Rank 2027.')
json.dump(p, open('/workspace/csb/picks.json', 'w'), indent=1)
print(totals['overall'], totals['legs'])
for t in new + [bs]: print(t['name'], t['odds'], t['stake'], round(t['stake']*(combine([l['odds'] for l in t['legs']])[1]-1),2), [(l['pick'], l['odds'], l['start'], l['marketId'], l['selectionId']) for l in t['legs']])
