#!/usr/bin/env python3
"""Mon Nov 9, 2026 10:30 AM ET run: grade Sunday (grade_mon.py) then build Monday card."""
import json, copy, os, datetime
src = open('/workspace/csb/build_sun_am.py').read()
src = src.replace("/workspace/sunam/fresh_ev_", "/workspace/mon/fresh_ev_").split("add('Bears Home Cushion")[0]
exec(src)
add('Bills Bought-Down + Spurs Cushion', [
 (36244880, ALT, rn('Buffalo Bills (+6.5)'), 'Buffalo Bills +6.5', 'NFL', 'Buffalo is -3 at Minnesota, and the Vikings start backup QB Carson Wentz (Kyler Murray out, plus RB Claiborne and WR Jennings out). +6.5 is 9.5 points off the main and crosses 3 and 4: the Bills only lose this leg if the Wentz-led Vikings win by 7+. Fade-the-backup-QB and bought-down NFL road favorites (4/4 Sunday) both point here.'),
 (36290201, ALT, rn('San Antonio Spurs +1.5'), 'San Antonio Spurs +1.5', 'NBA', 'Spurs (8-2) are -8.5 at 3-5 Phoenix, which is missing Mark Williams and Jordan Goodwin. +1.5 gives 10 points of cushion; San Antonio only fails if it loses by 2+.'),
], 'Two good teams bought 9.5-10 points off the main against weaker or short-handed opponents.')
add('Islanders Road Ice + Cavs Cushion', [
 (36296139, APL, rn('New York Islanders +1.5'), 'New York Islanders +1.5', 'NHL', 'NYI is the -142 road favorite at San Jose; +1.5 covers any Islanders win or one-goal loss. Road favorites at +1.5 keep cashing (TB lost by 1 Sunday and still covered).'),
 (36290200, ALT, rn('Cleveland Cavaliers +1.5'), 'Cleveland Cavaliers +1.5', 'NBA', 'Cleveland is -8.5 at Charlotte; +1.5 is 10 points of cushion for the better team.'),
], 'Road NHL favorite at +1.5 plus an NBA favorite bought 10 points down.')
add('Oilers Home Ice + Warriors Cushion', [
 (36296137, APL, rn('Edmonton Oilers +1.5'), 'Edmonton Oilers +1.5', 'NHL', 'Edmonton is the -156 home favorite vs the Rangers; +1.5 means the Oilers only lose this leg if they lose by 2+ at home. Lesson: use +1.5 on the better team or the favorite, not a pick\'em home side.'),
 (36290202, ALT, rn('Golden State Warriors +1.5'), 'Golden State Warriors +1.5', 'NBA', 'Warriors are -9.5 at home and New Orleans is on the second night of a back-to-back after losing by 16 at the Clippers Sunday. Golden State is short-handed (Butler, Porzingis, Moody, Richard out), which is why we take 11 points of cushion instead of the spread.'),
], 'Home favorite +1.5 in hockey plus a home NBA favorite bought 11 points down against a tired team.')
add('Pistons Cushion + Buckeyes Bought-Down', [
 (36290198, ALT, rn('Detroit Pistons +1.5'), 'Detroit Pistons +1.5', 'NBA', 'Detroit (6-3) is -10.5 at home vs 4-6 Washington, which is missing Watkins, Vukcevic, Beekman and Champagnie. Detroit is on a back-to-back, so we take +1.5 (12 points of cushion) rather than a bought-down minus line.'),
 (36297638, ALTN, rh('Ohio State', -16.5), 'Ohio State -16.5', 'NCAAB', 'Ohio State is -25.5 at home vs Marshall (ML -20000); -16.5 leaves 9 points of cushion. Bought-down home favorites with 9+ cushion are 5/5.'),
], 'Home NBA favorite with 12 points of cushion plus a big college home favorite bought 9 points down.')
add('Sooners + Tigers Bought-Down Hosts', [
 (36297540, ALTN, rh('Oklahoma', -18.5), 'Oklahoma -18.5', 'NCAAB', 'Oklahoma is -27.5 at home vs North Alabama (ML -50000); -18.5 leaves 9 points of cushion.'),
 (36297581, ALTN, rh('Auburn', -15.5), 'Auburn -15.5', 'NCAAB', 'Auburn is -23.5 at home vs App State (ML -10000); -15.5 leaves 8 points of cushion.'),
], 'Two SEC hosts bought 8-9 points off huge main spreads.')
add('Flames + Tigers Bought-Down Hosts', [
 (36297671, ALTN, rh('UIC', -10.5), 'UIC -10.5', 'NCAAB', 'UIC is -19.5 at home vs UNC Greensboro (ML -4500); -10.5 leaves 9 points of cushion.'),
 (36297656, ALTN, rh('Clemson', -13.5), 'Clemson -13.5', 'NCAAB', 'Clemson is -21.5 at home vs North Dakota (ML -10000); -13.5 leaves 8 points of cushion.'),
], 'Two home favorites bought 8-9 points down.')
add('West Coast Bought-Down Hosts', [
 (36297628, ALTN, rh('Stanford', -9.5), 'Stanford -9.5', 'NCAAB', 'Stanford is -18.5 at home vs Rice (ML -4000); -9.5 leaves 9 points of cushion.'),
 (36297585, ALTN, rh('Oregon State', -7.5), 'Oregon State -7.5', 'NCAAB', 'Oregon State is -16.5 at home vs Eastern Washington (ML -2800); -7.5 leaves 9 points of cushion.'),
], 'Two late home favorites bought 9 points down.')
bs = add('Best Shot $500K', [
 (36297669, ALTN, rh('Notre Dame', -20.5), 'Notre Dame -20.5', 'NCAAB', 'Notre Dame is -28.5 at home vs Eastern Illinois (ML -100000); -20.5 leaves 8 points of cushion.'),
 (36297672, ALTN, rh('Alabama', -23.5), 'Alabama -23.5', 'NCAAB', 'Alabama is -32.5 at home vs Oakland (ML -100000); -23.5 leaves 9 points of cushion.'),
 (36297561, ALTN, rh('LSU', -20.5), 'LSU -20.5', 'NCAAB', 'LSU is -29.5 at home vs Louisiana Tech (ML -100000); -20.5 leaves 9 points of cushion.'),
 (36297570, ALTN, rh('Missouri', -22.5), 'Missouri -22.5', 'NCAAB', 'Missouri is -31.5 at home vs SIU-Edwardsville (ML -100000); -22.5 leaves 9 points of cushion.'),
 (36297571, ALTN, rh('Purdue', -6.5), 'Purdue -6.5', 'NCAAB', 'Purdue is -15.5 at home vs Illinois State (ML -2100); -6.5 leaves 9 points of cushion.'),
 (36297640, ALTN, rh('Indiana', 3.5), 'Indiana +3.5', 'NCAAB', 'Indiana is -5.5 at home vs Syracuse; +3.5 means the Hoosiers only fail if they lose by 4+ at home.'),
 (36297655, ALTN, rh('Cincinnati', 1.5), 'Cincinnati +1.5', 'NCAAB', 'Cincinnati is -6.5 at home vs Minnesota; +1.5 covers any win or a one-point loss.'),
 (36297650, ML, rn('Bowling Green'), 'Bowling Green ML', 'NCAAB', 'Bowling Green is -12.5 at home vs Cleveland State; only needs to win.'),
 (36297663, ML, rn('Columbia'), 'Columbia ML', 'NCAAB', 'Columbia is -12.5 at home vs Stonehill; only needs to win.'),
 (36290203, ALT, rn('Houston Rockets +1.5'), 'Houston Rockets +1.5', 'NBA', 'Houston is -8.5 at home, and Denver lists Jokic, Murray, Gordon, Johnson, DeRozan and Braun as questionable. +1.5 gives 10 points of cushion.'),
 (36296138, APL, rn('Vancouver Canucks +1.5'), 'Vancouver Canucks +1.5', 'NHL', 'Philadelphia played in Calgary last night (OT) and is on a back-to-back; the home Canucks at +1.5 only fail on a 2+ goal loss.'),
 (36290205, ALT, rn('Toronto Raptors +4.5'), 'Toronto Raptors +4.5', 'NBA', 'Toronto is the -3.5 home favorite vs Memphis; +4.5 gives 8 points of cushion.'),
], 'Built from the legs left after the 2-leg card: big college home favorites bought 8-9 points down, home favorites that only need to win, and NBA/NHL home favorites with extra cushion. It stops at 12 legs because the rest of the slate is coin-flip territory, so it lands far short of the $5K target.', stake=5, lst=[])
D, R = '2026-11-09', '10:30 AM'
for t, typ in [(t, 'parlay') for t in new] + [(bs, 'lottery')]:
    if not already_in_history(H, t['name'], D, R):
        H.append({'date': D, 'run': R, 'type': typ, 'name': t['name'], 'odds': t['odds'], 'stake': t['stake'], 'result': 'pending', 'profit': 0,
                  'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'pending'} for l in t['legs']],
                  'whyExplanation': 'Pending.', 'lesson': ''})
totals = recompute_totals(H)
p['updated'] = p['results']['updated'] = 'Mon Nov 9, 2026 10:30 AM ET'
p['run'] = 'Monday 10:30 AM: Sunday graded (2-leg parlays went 7-3). Seven new 2-leg parlays, every leg 8-12 points or 1.5 goals beyond the main, plus a 12-leg Best Shot. No singles cleared the edge bar.'
p['singles'], p['parlays'], p['lottery'] = [], new, [bs]
p['results']['totals'] = totals
for k in ('singles', 'parlays', 'lottery'): p['results'][k] = copy.deepcopy(totals[k])
p['results']['topLessons'] = [
 'Sunday 2-leg parlays went 7-3; every loss came from a dog cushion on a bad team (Nets, Pelicans, Patriots-as-worse-team) or a home pick\'em +1.5 (Sabres).',
 'Bought-down favorites with 9-10 points of cushion keep cashing: NFL road favorites 4/4 Sunday, college home favorites 5/5.',
 'No dog cushions on losing NBA or NFL teams (Jets, Raiders, Cardinals, Nets, Pelicans all lost by 14+).',
 'NHL +1.5 only on the favorite or better team; road favorites at +1.5 keep covering.',
 'Mid-major short favorites (-385 to -520) lost outright again in the Best Shot (St Thomas, Lehigh).',
]
p['results']['sources'] = 'FanDuel PA public odds (event-page API, pulled at build); ESPN scoreboards 11/8 (NFL/NBA/NHL/NCAAB finals); ESPN NBA injuries, iHeart/FantasyDailies Nov 9 injury reports, Bills/Vikings official injury reports; lessons.md'
json.dump(p, open('/workspace/csb/picks.json', 'w'), indent=1)
print(totals['overall'])
for t in new + [bs]: print(t['name'], t['odds'], [(l['pick'], l['odds'], l['start']) for l in t['legs']])
