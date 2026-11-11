#!/usr/bin/env python3
"""Wed Nov 11 2026 10:30 AM: grade Tuesday Nov 10 (NBA/NHL/NCAAB/CFB) from ESPN finals."""
import json, copy
exec(open('/workspace/csb/build_sat_pm.py').read().split("if os.environ.get('KEEP')")[0])
p=json.load(open('picks.json')); H=p['results']['history']
L={
'Miami Heat +1.5':('hit','MIA 115-109 at UTA (won by 6)'),
'Colorado Avalanche +1.5':('hit','COL 6-3 at TOR'),
'New York Knicks -6.5':('hit','NYK 117-85 (won by 32)'),
'New Jersey Devils +1.5':('miss','WPG 4-2 (NJ lost by 2)'),
'Iowa State -26.5':('hit','ISU 84-47 (won by 37)'),
'Xavier -26.5':('hit','XAV 100-55 (won by 45)'),
'NC State -10.5':('hit','NCSU 94-60 (won by 34)'),
'Ole Miss -17.5':('hit','MISS 91-51 (won by 40)'),
'Western Michigan -4.5':('hit','WMU 42-14 at Akron (won by 28)'),
'Rutgers -14.5':('hit','RU 101-64 (won by 37)'),
'Wake Forest -9.5':('hit','WAKE 82-64 (won by 18)'),
'Providence -22.5':('hit','PROV 78-55 (won by 23)'),
'Georgetown -19.5':('miss','GU 83-78 (won by 5, needed 20)'),
'UCF -4.5':('hit','UCF 76-69 (won by 7)'),
'Georgia Tech -7.5':('hit','GT 85-71 (won by 14)'),
'North Carolina -4.5':('hit','UNC 76-63 (won by 13)'),
'Saint Louis -14.5':('hit','SLU 125-63 (won by 62)'),
'Wisconsin -16.5':('hit','WIS 89-42 (won by 47)'),
'Villanova -14.5':('hit','NOVA 80-59 (won by 21)'),
'Florida ML':('hit','UF 81-72 at FSU'),
'Celtics/76ers Over 204.5':('hit','BOS 123-101 (224 total)'),
'SMU ML':('hit','SMU 98-63'),
'Rhode Island ML':('hit','URI 71-65'),
'GW ML':('hit','GW 69-50'),
'TCU -25.5':('miss','TCU 100-92 in 2OT (won by 8, needed 26)'),
'Arizona -27.5':('hit','ARIZ 90-59 (won by 31)'),
'BYU -19.5':('miss','BYU 98-82 (won by 16, needed 20)'),
'Minnesota Wild +1.5':('hit','MIN 2-1 OT at MTL'),
'St. Louis Blues +1.5':('hit','STL 3-2'),
'Virginia -29.5':('hit','UVA 95-61 (won by 34)'),
'Magic/Kings Over 209.5':('miss','ORL 107-100 (207 total, needed 210)'),
'Vanderbilt ML':('hit','VAN 105-81'),
'Clippers/Suns Over 210.5':('hit','PHX 133-110 (243 total)'),
'Baylor ML':('hit','BAY 90-61'),
'Arizona State ML':('hit','ASU 85-63'),
'Utah ML':('hit','UTAH 85-64'),
'Colorado ML':('hit','COLO 83-75'),
'New Mexico ML':('hit','UNM 94-69'),
}
WHY={
('10:30 AM','Heat Cushion + Avalanche Road Ice'):('Won: Miami won by 6 at depleted 1-9 Utah (+1.5) and Colorado won 6-3 at Toronto.','Favorite vs a depleted bottom team with 10 points of cushion plus a road NHL favorite at +1.5 both held. Note Miami only won by 6 as an 8.5 favorite: the cushion, not the spread, is what made it safe.'),
('10:30 AM','Knicks Bought-Down + Devils Road Ice'):('Lost: Knicks won by 32 (hit), but the Devils lost 4-2 at Winnipeg with backup Jake Allen in net (+1.5 missed by one goal; the second Jets goal was decisive).','We flagged the backup goalie and still used the leg. An NHL road favorite starting its backup goalie against its opponent\'s starter has no goalie edge, so it fails our own "+1.5 only with the goalie edge" rule. Skip those.'),
('10:30 AM','Cyclones + Musketeers Bought-Down Hosts'):('Won: Iowa State by 37 (needed 27) and Xavier by 45 (needed 27).','Buy-downs vs visitors that already lost by 50+ (SWAC Southern, Detroit Mercy) were comfortable.'),
('10:30 AM','Wolfpack + Rebels Bought-Down Hosts'):('Won: NC State by 34 (needed 11) and Ole Miss by 40 (needed 18).','Power host vs low-major visitor at a moderate main line (-19.5 to -26.5) held easily.'),
('10:30 AM','Broncos MACtion + Scarlet Knights'):('Won: Western Michigan won 42-14 at Akron and Rutgers by 37.','MAC road favorite bought 10 down vs the worst conference team plus a Big Ten host vs NJIT: both easy.'),
('10:30 AM','Deacons + Friars Bought-Down Hosts'):('Won: Wake by 18 (needed 10) and Providence by 23 (needed 23, covered by half a point).','Providence -22.5 covered by just 0.5. Main lines above -30 swing a lot; a 9-point buy-down from -31.5 is thinner than it looks.'),
('10:30 AM','Best Shot $500K'):('Lost: 12 of 15 legs hit. Georgetown -19.5 (won by only 5 vs Delaware State), TCU -25.5 (won by 8 in 2OT vs UL Monroe) and BYU -19.5 (won by 16 vs Queens) missed. All moneylines, the Celtics/76ers total and the other buy-downs hit.','All three misses were buy-downs from mega-spreads (-27.5 to -34.5 main lines). Those games are high-variance: starters sit, benches play, and the margin can collapse. Buy-downs from a -20 to -26 main held 10/10 Tuesday, but from -27.5 and up went 4/7 (Georgetown, TCU and BYU missed; Iowa State, Xavier, Arizona and UVA hit). In a 15-leg ticket, use moneylines for mega-spread games, not alt spreads.'),
('3:00 PM','Wild + Blues Ice Cushions'):('Won: Minnesota won 2-1 in OT at Montreal and St. Louis beat Detroit 3-2.','Both legs were +1.5 on favorites with the starting-goalie edge; both games were one-goal games, so the moneyline would also have won but the +1.5 removed the OT risk.'),
('3:00 PM','Cavaliers Bought-Down + Magic/Kings Over'):('Lost: Virginia won by 34 (hit), but Orlando-Sacramento finished 107-100, 207 total (Over 209.5 missed by 3).','A short-handed team (Orlando without Banchero, Suggs and Isaac) can drag even a 13-point alt total under; Orlando had already gone under 210 in 3 of 9 games. A team that misses the alt total in 30%+ of its games is not a big-cushion total. Require both teams to clear it in roughly 90%+ of games, and avoid totals involving teams missing 2+ primary scorers.'),
('3:00 PM','Commodores ML + Clippers/Suns Over'):('Won: Vanderbilt won by 24 and Clippers/Suns scored 243 (needed 211).','A 14-point total cushion where 14 of 18 combined games cleared it held easily; moneyline vs a competent mid-major was correct.'),
('3:00 PM','Best Shot $500K'):('Won: all 5 home moneylines hit (Baylor, Arizona State, Utah, Colorado, New Mexico), but at -493 it paid only $1.01 on $5.','Near-lock moneylines win but pay almost nothing. Plan the day so the stronger card has the price.'),
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
