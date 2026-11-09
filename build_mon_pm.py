#!/usr/bin/env python3
"""Mon Nov 9, 2026 3:00 PM ET run: nothing settled since 10:30 AM (whole morning card plays tonight).
Build afternoon card from the events NOT on the morning card (morning used 8/10 NBA, 3/3 NHL, MNF, 19 NCAAB)."""
import json, copy, os, datetime
src = open('/workspace/csb/build_sun_am.py').read()
src = src.replace("/workspace/sunam/fresh_ev_", "/workspace/monpm/fresh_ev_").split("add('Bears Home Cushion")[0]
exec(src)
rs = lambda pre, h: (lambda r, m: r.get('runnerName', '').startswith(pre) and float(r.get('handicap') or 0) == h)
TEN = lambda mn: mn == 'Moneyline'
ALTT = lambda mn: mn == 'Alternate Total Points'
add('Longhorns + Vols Bought-Down Hosts', [
 (36297648, ALTN, rh('Texas', -28.5), 'Texas -28.5', 'NCAAB', 'Texas is -37.5 at home vs Grambling (ML -100000) and has won its first two games by 50 (Chicago State) and 48 (Gardner-Webb). -28.5 leaves 9 points of cushion against a SWAC team.'),
 (36297645, ALTN, rh('Tennessee', -21.5), 'Tennessee -21.5', 'NCAAB', 'Tennessee is -30.5 at home vs Radford (ML -100000); the Vols beat Wofford by 31, and Radford already lost by 14 at San Francisco and by 14 at Cal. -21.5 leaves 9 points of cushion.'),
], 'Two elite home favorites bought 9 points off huge main spreads; both have been winning openers by 30-50.')
add('Huskies + Wildcats Bought-Down Hosts', [
 (36297665, ALTN, rh('Connecticut', -30.5), 'UConn -30.5', 'NCAAB', 'UConn is -39.5 at home vs Wagner (ML -100000). UConn beat Gardner-Webb by 40 and won at Michigan; Wagner lost by 26 at Boston College and by 26 at Miami. -30.5 leaves 9 points of cushion.'),
 (36297560, ALTN, rh('Northwestern', -5.5), 'Northwestern -5.5', 'NCAAB', 'Northwestern is -14.5 at home vs Boston University (ML -1600) after wins by 26 and 13. -5.5 leaves 9 points of cushion for the Big Ten host over a Patriot League visitor.'),
], 'A national-title-level host and a Big Ten host, each bought 9 points down.')
add('Blazers + Pirates Home Cushions', [
 (36297535, ALTN, rh('UAB', -9.5), 'UAB -9.5', 'NCAAB', 'UAB is -18.5 at home vs Florida A&M (ML -4000). FAMU lost by 43 at Florida State and lost at home to Division II Fort Valley State. -9.5 leaves 9 points of cushion.'),
 (36297591, ALTN, rh('Seton Hall', 4.5), 'Seton Hall +4.5', 'NCAAB', 'Seton Hall is the -205 home favorite (-4.5) vs Charlotte and is 2-0 (beat Saint Peter\'s by 24). +4.5 gives 9 points of cushion: the Pirates only fail by losing at home by 5+. Better team, home, favorite: the profile that has kept cashing.'),
], 'A big home favorite bought 9 down plus a Big East home favorite moved to +4.5.')
add('Mavs Cushion + Hurricanes Bought-Down', [
 (36290199, ALT, rn('Dallas Mavericks +5.5'), 'Dallas Mavericks +5.5', 'NBA', 'Dallas (6-4) is -3.5 at home vs 3-7 Indiana, which is without Tyrese Haliburton, Sheppard and Furphy (McConnell questionable). Kyrie Irving and Cooper Flagg are both off the injury report. Dallas is on a back-to-back but played at home last night (no travel, beat Brooklyn by 37 with starters resting in the 4th). That back-to-back is why we take +5.5 (9 points of cushion) instead of the spread.'),
 (36297682, ALTN, rh('Miami', -28.5), 'Miami -28.5', 'NCAAB', 'Miami is -36.5 at home vs North Florida (ML -100000). UNF lost by 51 at UCLA; Miami beat Wagner by 26. -28.5 leaves 8 points of cushion, and FanDuel prices Miami\'s team total at 100.5.'),
], 'Better NBA team at home with 9 points of cushion, plus a big college host bought 8 points down.')
bs = add('Best Shot $500K', [
 (36290204, ALTT, rn('Over 226.5'), 'Lakers/Hawks Over 226.5', 'NBA', 'The main total is 235.5; 226.5 leaves 9 points of cushion. Atlanta leads the NBA in shot volume and has scored 120+ three straight games; the Lakers are No. 1 in offense, Luka Doncic (40.1 ppg) returns, and LA is on the second night of a back-to-back with a No. 18 defense. A total instead of a side because Luka\'s return makes the spread a coin flip.'),
 (36297644, ML, rn('Georgia'), 'Georgia ML', 'NCAAB', 'Georgia is -22.5 at home vs FGCU (ML -10000) and is 2-0. Moneyline only: Georgia has won by just 14 and 16 so far, so the -13.5 alt was not safe enough.'),
 (36297673, ML, rn('Mississippi State'), 'Mississippi State ML', 'NCAAB', 'Mississippi State is -23.5 at home vs Jackson State (ML -10000) after wins by 18 and 38; no alt spreads offered, so moneyline only.'),
 (36297573, ML, rn('DePaul'), 'DePaul ML', 'NCAAB', 'DePaul is -24.5 at home vs Alabama A&M (ML -20000); 2-0 including a win over South Florida.'),
 (36298123, TEN, rn("Christopher O'Connell"), "Christopher O'Connell ML", 'Tennis', "ATP Challenger Brisbane R32: O'Connell (ATP No. 117, career-high 53) vs Moerani Bouzige (No. 461), who needed three sets to beat a No. 986 player in qualifying."),
 (36291165, TEN, rn('Juncheng Shang'), 'Juncheng Shang ML', 'Tennis', 'ATP Challenger Brisbane R32: Shang (career-high top 50 on the ATP Tour) is -580 against Australian Jake Delaney, ranked far below him.'),
], 'Every high-probability evening event was already used by the morning card or by the four 2-leg parlays above, and we do not repeat events across tickets. What is left: one NBA total with 9 points of cushion, three college moneylines at -10000 or shorter, and two Challenger favorites. Adding anything else would mean coin-flip legs, so this Best Shot is far short of +1000 and of the $5K target.', stake=5, lst=[])
D, R = '2026-11-09', '3:00 PM'
for t, typ in [(t, 'parlay') for t in new] + [(bs, 'lottery')]:
    if not already_in_history(H, t['name'], D, R):
        H.append({'date': D, 'run': R, 'type': typ, 'name': t['name'], 'odds': t['odds'], 'stake': t['stake'], 'result': 'pending', 'profit': 0,
                  'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'pending'} for l in t['legs']],
                  'whyExplanation': 'Pending.', 'lesson': ''})
totals = recompute_totals(H)
p['updated'] = p['results']['updated'] = 'Mon Nov 9, 2026 3:00 PM ET'
p['run'] = 'Monday 3:00 PM: nothing new settled (the whole 10:30 AM card plays tonight). Four new 2-leg parlays from the events the morning card did not use, every leg 8-9 points beyond the main, plus a short Best Shot. No singles cleared the edge bar. The morning tickets are still live; see the record below.'
p['singles'], p['lottery'] = [], [bs]
p['parlays'] = new
p['results']['totals'] = totals
for k in ('singles', 'parlays', 'lottery'): p['results'][k] = copy.deepcopy(totals[k])
p['results']['sources'] = 'FanDuel PA public odds (event-page API, pulled ~3:15 PM ET); ESPN scoreboards Nov 2-8 (NBA/NCAAB results), ESPN NBA injuries, NBA 2 PM injury report via Heavy/Lakers Nation/Yahoo/VSiN, Tennis.com/Sportradar (Brisbane Challenger); lessons.md'
json.dump(p, open('/workspace/csb/picks.json', 'w'), indent=1)
print(totals['overall'])
for t in new + [bs]: print(t['name'], t['odds'], [(l['pick'], l['odds'], l['start']) for l in t['legs']])
