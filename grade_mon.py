#!/usr/bin/env python3
"""Mon Nov 9 2026 10:30 AM: grade Sunday Nov 8 (NFL/NBA/NHL/NCAAB) from ESPN finals."""
import json
exec(open('/workspace/csb/build_sat_pm.py').read().split("if os.environ.get('KEEP')")[0])
p=json.load(open('picks.json')); H=p['results']['history']
L={ # pick: (result, actual)
'New York Jets +8.5':('miss','KC 35-12 (lost by 23)'),
'Las Vegas Raiders +7.5':('miss','SF 38-17 (lost by 21)'),
'Las Vegas Raiders +6.5':('miss','SF 38-17 (lost by 21)'),
'Arizona Cardinals +7.5':('miss','SEA 17-3 (lost by 14)'),
'Detroit Lions +1.5':('hit','DET 19-9 (won by 10)'),
'Denver Broncos -3.5':('hit','DEN 26-21 (won by 5)'),
'Philadelphia 76ers +1.5':('hit','PHI 127-121 (won by 6)'),
'Boston Bruins +1.5':('hit','BOS 4-1'),
'Boston Celtics -2.5':('hit','BOS 117-97 (won by 20)'),
'Anaheim Ducks +1.5':('hit','ANA 5-2'),
'Miami Heat +1.5':('hit','MIA 114-108 (won by 6)'),
'Utah Jazz +21.5':('hit','MIN 115-100 (lost by 15)'),
'Brooklyn Nets +18.5':('miss','DAL 130-93 (lost by 37)'),
'New Orleans Pelicans +10.5':('miss','LAC 139-123 (lost by 16)'),
'Chicago Bears +3.5':('hit','CHI 27-24 (won by 3)'),
'New Jersey Devils +1.5':('hit','NJ 4-0'),
'Houston Texans +4.5':('hit','HOU 44-22 (won by 22)'),
'Buffalo Sabres +1.5':('miss','VGK 4-1 (lost by 3)'),
'Philadelphia Eagles +13.5':('hit','NYG 19-11 (lost by 8)'),
'New Orleans Saints +6.5':('hit','NO 23-22 OT (won by 1)'),
'New England Patriots +6.5':('miss','GB 45-27 (lost by 18)'),
'Los Angeles Rams +5.5':('hit','LAR 20-13 (won by 7)'),
'Dallas Cowboys +5.5':('hit','DAL 27-23 (won by 4)'),
'Tampa Bay Lightning +1.5':('hit','WPG 4-3 (lost by 1)'),
'South Carolina -8.5':('hit','SC 78-68 (won by 10)'),
'Drake -4.5':('hit','Drake 75-68 (won by 7)'),
'Houston -10.5':('hit','Houston 86-68 (won by 18)'),
'William & Mary -3.5':('hit','W&M 104-73 (won by 31)'),
'St Thomas -2.5':('miss','Green Bay 76-67 (St Thomas lost by 9)'),
"Hawai'i -2.5":('hit',"Hawai'i 71-62 (won by 9)"),
'Air Force ML (-0.5)':('hit','Air Force 89-82'),
'Western Michigan +0.5':('hit','WMU 87-71'),
'Lehigh +0.5':('miss','Brown 65-55 (Lehigh lost by 10)'),
'Pittsburgh +7.5':('hit','Pitt 82-76 (won by 6)'),
'Philadelphia Flyers +1.5':('hit','CGY 4-3 OT (lost by 1)'),
}
WHY={
'New York Jets +8.5':('Lost: KC won 35-12, so the 8.5-point cushion was gone by halftime.','A road dog cushion against an elite home team (KC) is not a safe leg; mismatches like this run away, the same as the NBA mismatch lesson.'),
'Las Vegas Raiders +7.5':('Lost: SF won 38-17 by 21.','Bad road dogs at elite hosts lose big; don\'t take dog cushions on bad teams in NFL either.'),
'Las Vegas Raiders +6.5':('Lost: SF won 38-17 by 21.','Same as above: no dog cushions on bad road teams.'),
'Arizona Cardinals +7.5':('Lost: SEA won 17-3 by 14; Arizona scored 3 points.','Low-scoring offenses can\'t keep games close against good defenses; a dog cushion needs a functional offense.'),
'Sunday Cushions + Utah':('Lost: Utah +1.5 and Detroit +1.5 hit, but Arizona +7.5 missed (lost 17-3).','Same Cardinals lesson: dog cushions on a weak offense are the leak. Bought-down favorites (Detroit) cashed again.'),
'Denver Broncos -3.5':('Won: DEN 26-21, covered -3.5 by 1.5.','Buying a road favorite down to -3.5 at plus money works (Texas -3.5 and Denver -3.5 both cashed).'),
'Sixers Cushion + Bruins Home Ice':('Won: PHI won by 6 and BOS won 4-1, both legs hit.','Healthy favorite at +1.5 vs a depleted team, plus home favorite +1.5, both easy.'),
'Celtics Bought-Down + Ducks Home Ice':('Won: BOS by 20 and ANA 5-2.','Elite team bought down 10 points vs a bad team was never in doubt.'),
'Heat Cushion + Jazz Big Dog':('Won: MIA by 6 and Utah lost by only 15 (needed under 22).','10-point extra cushion on a dog vs a short-handed favorite held.'),
'Nets + Pelicans Big Cushions':('Lost: both legs missed. BKN lost by 37 (+18.5) and NOP by 16 (+10.5).','NBA dog cushions on bad teams keep failing (now WAS, CHA, MEM, BKN, NOP). Stop taking NBA dog cushions on losing teams entirely; use favorites bought down instead.'),
'Bears Home Cushion + Devils Road Ice':('Won: CHI 27-24 (needed no worse than -3 loss) and NJ 4-0.','Bought-down home favorite crossing 3 cashed, and fading a back-to-back team (TOR) worked again.'),
'Texans Bought-Down + Sabres Home Ice':('Lost: HOU won by 22, but Buffalo lost 4-1 at home to Vegas.','NHL home pick\'em +1.5 is not a lock against a stronger visitor; only use +1.5 on the better team or the favorite.'),
'Eagles Big Home Cushion + Saints Home Cushion':('Won: PHI lost by 8 (+13.5 covered) and NO won 23-22 in OT.','Big cushions in low-total divisional games held. Note the Eagles lost outright as a favorite, so the extra 10 points mattered.'),
'Patriots Home Cushion + Rams Bought-Down':('Lost: LAR won by 7, but GB won 45-27 at NE (Patriots +6.5 missed by 12).','A short-handed opponent (GB missing Parsons) can still blow you out; the 9.5-point cushion leg on a -3 home favorite failed when the favorite was the worse team. Check that the bought-down side is actually the better team.'),
'Cowboys Bought-Down + Lightning Road Ice':('Won: DAL won by 4 (+5.5) and TB lost by 1 in Winnipeg (+1.5).','Road favorite +1.5 in NHL keeps cashing; bought-down NFL road favorites with 10 points cushion went 4/4 Sunday (DAL, LAR, HOU, DET).'),
'Hoops Bought-Down Hosts II':('Won: SC by 10 (-8.5) and Drake by 7 (-4.5), though both games were closer than the main spread.','Bought-down home favorites now 5/5, but these were tight; keep the 9-point cushion and don\'t shrink it.'),
'Best Shot $500K':('Lost: 7 of 9 legs hit. St Thomas -2.5 (lost 76-67 to Green Bay) and Lehigh +0.5 (lost 65-55 to Brown) missed.','Small-conference home favorites at -385 to -520 (St Thomas, Lehigh) lost outright; mid-major short favorites are not high-probability legs, which repeats an earlier lesson. Only use college favorites -1000 or shorter in the Best Shot.'),
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
    w=WHY.get(h['name']) or WHY.get(h['legs'][0]['pick'])
    h['whyExplanation'],h['lesson']=w
    print(h['date'],h['name'],h['result'],h['profit'])
T=recompute_totals(H); p['results']['totals']=T
import copy
for k in('singles','parlays','lottery'): p['results'][k]=copy.deepcopy(T[k])
json.dump(p,open('picks.json','w'),indent=1)
print(T['overall'],T['singles'],T['parlays'],T['lottery'],T['legs'])
