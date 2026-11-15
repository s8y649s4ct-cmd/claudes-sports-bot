#!/usr/bin/env python3
"""Sun Nov 15, 2026 10:30 AM ET run: graded Saturday Nov 14 (grade_sun.py), build Sunday card from fresh FanDuel PA pulls."""
import json, copy, os, datetime, glob
os.makedirs('/workspace/sun15am', exist_ok=True)
for f in glob.glob('/workspace/sun15am/fresh_ev_*.json'): os.remove(f)
src = open('/workspace/csb/build_sun_am.py').read()
src = src.replace("/workspace/sunam/fresh_ev_", "/workspace/sun15am/fresh_ev_").split("add('Bears Home Cushion")[0]
exec(src)
MN = lambda name: (lambda mn: mn == name)
ASP = MN('Alternate Spread')
add('Celtics Home Cushion + Chiefs Big Cushion', [
 (36314666, ASP, rn('Boston Celtics +1.5'), 'Boston Celtics +1.5', 'NBA', 'Boston (10-2, 5-0 at home, +11.2 point differential, five straight wins) is the -13.5 home favorite. Dallas (2-4 on the road) is missing both starting-caliber centers, Daniel Gafford and Dereck Lively II, plus Max Christie (ESPN injury report). +1.5 only loses if Dallas wins outright by 2+. Passes the NBA rule (plus-side cushion on a clearly better home team; no favorite-side NBA buy-downs after Saturday\'s Wolves miss). Tips 6:10 PM ET.'),
 (36275759, ASP, rn('Kansas City Chiefs (+7.5)'), 'Kansas City Chiefs +7.5', 'NFL', 'Kansas City (6-2) is the -3.5 road favorite at 3-6 Atlanta; +7.5 is 11 points off the main line and crosses both 3 and 7, so the Chiefs lose this leg only if Atlanta wins by 8+. Mahomes practiced fully. The Falcons have lost at home by 31 (Carolina), 7, 8 and 17 (Cincinnati last week). Risk noted: Xavier Worthy is out and KC lost by 17 at Seattle. Kicks 1:00 PM ET.'),
], 'A clearly better NBA home team at +1.5 against a short-handed visitor, plus an NFL road favorite bought 11 points to the far side of 7. Both legs need an upset by more than a possession to lose.')
bs = add('Best Shot $500K', [
 (36275762, ASP, rn('Jacksonville Jaguars (+2.5)'), 'Jacksonville Jaguars +2.5', 'NFL', 'Jacksonville (6-2, 3-1 on the road incl. a 33-10 win at Baltimore) is -10.5 at 1-7 Tennessee; +2.5 is 13 points off the main line, so the Jaguars lose this leg only if the Titans win by 3+. Home-loss check is split (Titans lost at home by 13 and 23, but by 4 and 3 to Philadelphia and Cleveland), which is why this is a 13-point cushion and not a bought line. Kicks 1:00 PM ET.'),
 (36314673, ASP, rn('San Antonio Spurs +1.5'), 'San Antonio Spurs +1.5', 'NBA', 'San Antonio (11-2, 6-0 on the road, 11 straight wins, +13.3 differential) is -16.5 at Utah (1-12, 11 straight losses). The Jazz are without Lauri Markkanen, Jaren Jackson Jr., Jusuf Nurkic and Jaxson Hayes. +1.5 loses only on an outright Utah win by 2+. Tips 5:10 PM ET.'),
 (36320594, ML, rn('Charleston'), 'Charleston ML', 'NCAAB', 'Tier-gap rule (host T-Rank top ~150 vs a bottom-tier visitor): Charleston (T-Rank 139, 3-0) hosts South Carolina State (318). -17.5 main line. Tips 2:00 PM ET.'),
 (36320520, ML, rn('Boston College'), 'Boston College ML', 'NCAAB', 'Tier gap: Boston College (T-Rank 104, 3-0) hosts New Hampshire (308). -22.5 main line. Tips 1:30 PM ET.'),
 (36321889, ML, rn('Penn State'), 'Penn State ML', 'NCAAB', 'Tier gap: Penn State (T-Rank 94) hosts New Haven (339, second-year Division I program). -23.5 main line. Tips 4:30 PM ET.'),
 (36320708, ML, rn('Loyola Marymount'), 'Loyola Marymount ML', 'NCAAB', 'Tier gap: Loyola Marymount (T-Rank 144) hosts Chicago State (335). -18.5 main line. Risk noted: LMU is 1-3 so far, so this is the weakest of the five college hosts. Tips 4:00 PM ET.'),
 (36320707, ML, rn('James Madison'), 'James Madison ML', 'NCAAB', 'Tier gap: James Madison (T-Rank 137) hosts Mercyhurst (306, 1-3). -14.5 main line. Tips 4:00 PM ET.'),
], 'The highest-probability legs left after the parlay: an NFL road favorite with a 13-point cushion, the 11-2 Spurs at +1.5 against a gutted Jazz team, and five tier-gap college hosts (host T-Rank top 150 vs visitor 300+). Nowhere near the $5K target: every other leg today failed a rule (see notes) and would be a 60-80% leg. Not padded.', stake=5, lst=[])
D, R = '2026-11-15', '10:30 AM'
for t, typ in [(t, 'parlay') for t in new] + [(bs, 'lottery')]:
    if not already_in_history(H, t['name'], D, R):
        H.append({'date': D, 'run': R, 'type': typ, 'name': t['name'], 'odds': t['odds'], 'stake': t['stake'], 'result': 'pending', 'profit': 0,
                  'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'pending'} for l in t['legs']],
                  'whyExplanation': 'Pending.', 'lesson': ''})
totals = recompute_totals(H)
o = totals['overall']
p['updated'] = p['results']['updated'] = 'Sun Nov 15, 2026 10:30 AM ET'
p['run'] = ("Sunday 10:30 AM: Saturday graded 3-6 (Devils/Canes goalie-edge, Air Force/Penn State and the morning Best Shot won; four CFB/NBA buy-down parlays, "
 "the Senators/Boise parlay and the totals Best Shot lost). Today's card is deliberately small after a bad buy-down day: one 2-leg parlay "
 "(Celtics +1.5 and Chiefs +7.5) and a 7-leg Best Shot (Jaguars +2.5, Spurs +1.5, five tier-gap college hosts). No favorite-side buy-downs, "
 "no singles, no +1000 lottery. NHL, Sunday Night Football and late NBA are held for the 3 PM run (goalie confirmations, inactives).")
p['singles'], p['parlays'], p['lottery'] = [], new, [bs]
p['results']['totals'] = totals
for k in ('singles', 'parlays', 'lottery'): p['results'][k] = copy.deepcopy(totals[k])
p['results']['topLessons'] = [
 'Favorite-side buy-downs are paused: Saturday they went 6/11 (Liberty, Virginia Tech, New Mexico, Boise State, Wolves missed; VT, UNM and the Wolves lost outright). Today every spread leg is a plus-side cushion on the clearly better team.',
 'CFB buy-downs only on home favorites of -17 or more with line movement toward them (the winners: Notre Dame, Louisiana Tech, Iowa, Air Force, Penn State).',
 'Goalie-edge NHL +1.5 is 3/3 Saturday and the best leg type on the card; tonight\'s NHL games are held for 3 PM starting-goalie confirmations.',
 'Home-loss check applied to NFL road favorites: Bills at the Jets (Jets lost at home by 3, 3 and 5) and 49ers at Dallas (Cowboys lost at home by 3, 8 and 3) were skipped. Jaguars at Tennessee is split, so it got a 13-point cushion.',
 'Packers +7.5 was skipped: Green Bay is without Josh Jacobs and Micah Parsons against the NFL\'s top defense, and Kirk Cousins starts for Minnesota. Seattle (Darnold and Smith-Njigba out) and Rams (Nacua out, lost to Arizona at home in Week 6) were skipped.',
 'Tier-gap moneylines tightened to visitors ranked 300+: Charleston, Boston College, Penn State, LMU and James Madison qualify. Seattle (host 152), Buffalo, San Jose State, Georgia State and San Diego State vs NMSU (161) do not.',
 'NHL alt overs need two sub-.900 confirmed goalies (Detroit shut out Tampa Bay 2-0 to sink the 3 PM Best Shot).',
]
p['results']['sources'] = ('FanDuel PA public odds (event-page API, pulled ~10:35-11:00 AM ET and refreshed at build); ESPN scoreboards 11/14 (grading); '
 'NFL.com official injury report (Week 11 final statuses); Vikings.com / NFL.com / Kalshi News (Cousins starting for Minnesota, Packers inactives); '
 'ESPN NBA injury report and standings 11/15; ESPN NFL team schedules (home-loss check); Barttorvik 2027 T-Rank.')
json.dump(p, open('/workspace/csb/picks.json', 'w'), indent=1)
print(totals['overall'], totals['singles'], totals['parlays'], totals['lottery'], totals['legs'])
for t in new + [bs]: print(t['name'], t['odds'], t['stake'], round(t['stake']*combine([l['odds'] for l in t['legs']])[1],2), [(l['pick'], l['odds'], l['start'], l['marketId'], l['selectionId']) for l in t['legs']])
