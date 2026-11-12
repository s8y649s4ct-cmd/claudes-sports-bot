#!/usr/bin/env python3
"""Thu Nov 12 2026 10:30 AM: grade Wednesday Nov 11 (NBA/NHL/NCAAB) from ESPN finals."""
import json, copy
exec(open('/workspace/csb/build_sat_pm.py').read().split("if os.environ.get('KEEP')")[0])
p=json.load(open('picks.json')); H=p['results']['history']
L={
'Los Angeles Lakers -4.5':('hit','LAL 123-112 at MIL (won by 11)'),
'Tulsa -8.5':('hit','TLSA 80-71 (won by 9, needed 9)'),
'San Antonio Spurs -5.5':('miss','SAS 124-119 at CHI (won by 5, needed 6)'),
'UC Davis -2.5':('hit','UCD 81-69 (won by 12)'),
'New York Knicks +6.5':('miss','CLE 115-107 at NYK (NYK lost by 8)'),
'Furman ML':('hit','FUR 80-67 at Holy Cross'),
'Notre Dame ML':('hit','ND 99-59'),
'South Carolina ML':('hit','SC 77-41'),
'Boise State ML':('hit','BSU 111-79'),
'Colorado State ML':('hit','CSU 87-71'),
'Seattle ML':('miss','UTSA 86-59 at Seattle (Seattle lost by 27)'),
'Edmonton Oilers +1.5':('hit','EDM 3-2 OT'),
'Houston Rockets +3.5':('hit','HOU 115-108 (won by 7)'),
'Vegas Golden Knights +1.5':('hit','VGK 5-3'),
'Boston Celtics +7.5':('hit','BOS 98-93 at TOR (won by 5)'),
'Denver Nuggets +7.5':('hit','DEN 123-118 at MEM (won by 5)'),
'New Orleans Pelicans +7.5':('miss','BKN 145-111 at NO (NO lost by 34)'),
'Grand Canyon ML':('hit','GCU 99-71'),
'Orlando Magic +12.5':('hit','ORL 123-108 at UTA (won by 15)'),
'Anaheim Ducks +2.5':('hit','NSH 4-2 at ANA (lost by 2)'),
}
WHY={
('10:30 AM','Lakers + Golden Hurricane Bought-Down'):('Won: the Lakers won by 11 at Milwaukee (needed 5) and Tulsa beat Oral Roberts by 9 (needed 9, exactly enough).','Both 9-point buy-downs held, but Tulsa covered by zero points: an AAC host projected by 16.5 won by only 9. Model margins vs low-majors run hot in November; Tulsa -8.5 was the thinnest kind of leg.'),
('10:30 AM','Spurs Bought-Down + Aggies Cushion'):('Lost: UC Davis won by 12 (hit), but San Antonio won only 124-119 at Chicago, so Spurs -5.5 missed by half a point. The Bulls led 41-29 after one quarter.','An NBA road favorite bought down to a minus number still has to win by margin. Even an elite 9-2 team on a 10-game win streak won a road game against a 1-8 team by only 5. For NBA 2-leg parlays, put the cushion on the plus side (+1.5 or better) for road favorites, or skip.'),
('10:30 AM','Knicks Home Cushion + Paladins ML'):('Lost: Furman won by 13 (hit), but Cleveland beat the Knicks 115-107 (Knicks +6.5 missed by 1.5). Harden scored a season-high 32. Josh Hart, listed out, actually played 26 minutes.','A -4.5 home favorite on a back-to-back against a talented team (Mitchell, Harden, Mobley, Allen) is close to a coin flip, and 11 points of cushion did not make it a near lock. Cleveland\'s 1-4 road record hid a roster that is better than the Knicks on paper. Small NBA favorites (-3.5 to -4.5) on a back-to-back are out of 2-leg parlays.'),
('10:30 AM','Best Shot $500K'):('Lost: 4 of 5 moneylines hit (Notre Dame, South Carolina, Boise State and Colorado State all won by 16+), but Seattle (-3000) lost 86-59 at home to UTSA.','The first -1800+ college moneyline loss on record (previously 34-0 in lock parlays). UTSA is an AAC team visiting a WAC/WCC-level host; the price came from UTSA\'s weak opener (beat VMI by 2), not from a true tier gap. Near-lock moneylines need a real conference/quality gap: Power or top mid-major host vs a bottom-75 visitor (T-Rank 290+). A visitor from an equal or higher league is never a lock regardless of the price.'),
('3:00 PM','Oilers Home Ice + Rockets Home Cushion'):('Won: Edmonton beat Philadelphia 3-2 in OT and Houston beat Golden State by 7 (needed to lose by no more than 3).','Goalie-edge NHL home favorite at +1.5 plus a rested, healthier NBA home favorite with 10 points of cushion both held.'),
('3:00 PM','Golden Knights Home Ice + Celtics Big Cushion'):('Won: Vegas beat Utah 5-3 and Boston won 98-93 at Toronto (+7.5 was not needed).','Goalie-edge +1.5 (now 6-1 the last three days on favorites with the edge) plus the clearly better NBA team with 13 points of cushion vs a depleted host.'),
('3:00 PM','Nuggets + Pelicans Cushions'):('Lost: Denver won by 5 at Memphis (hit), but Brooklyn routed New Orleans 145-111 (Pelicans +7.5 missed by 26). Egor Demin returned for Brooklyn and the Nets scored 83 in the first half.','The Pelicans were only -3.5 at home vs a 2-8 team: the market was saying these teams were close, and New Orleans itself is a weak team. A small favorite that is not clearly good is not "the better team". NBA cushions need a favorite of -6.5 or more, or a favorite with a proven record, not just a bad opponent. Also check returning players (Demin) the day of the game.'),
('3:00 PM','Best Shot $500K'):('Won: Grand Canyon won by 28, Orlando won by 15 at Utah (+12.5 not needed) and Anaheim lost only 4-2 to Nashville (+2.5 covered). Paid $1.45 on $5 at -345.','The three-leg safety ticket won, but at -345 it pays almost nothing. Nashville\'s second goal margin was the closest call (+2.5 held by half a goal).'),
}
for h in H:
    if h['result']!='pending': continue
    for l in h['legs']:
        if l['result']=='pending' and l['pick'] in L: l['result'],l['actual']=L[l['pick']]
    rs=[l['result'] for l in h['legs']]
    if 'pending' in rs: continue
    won=all(r in('hit','void') for r in rs)
    h['result']='won' if won else 'lost'
    h['profit']=profit_for(h['odds'],h.get('stake') or 10,won)
    h['whyExplanation'],h['lesson']=WHY[(h['run'],h['name'])]
    print(h['date'],h['run'],h['name'],h['result'],h['profit'])
T=recompute_totals(H); p['results']['totals']=T
for k in('singles','parlays','lottery'): p['results'][k]=copy.deepcopy(T[k])
json.dump(p,open('picks.json','w'),indent=1)
print(T['overall'],T['singles'],T['parlays'],T['lottery'],T['legs'])
