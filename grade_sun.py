#!/usr/bin/env python3
"""Sun Nov 15 2026 10:30 AM: grade Saturday Nov 14 (NBA/NHL/NCAAB/NCAAF) from ESPN finals."""
import json, copy
exec(open('/workspace/csb/build_sat_pm.py').read().split("if os.environ.get('KEEP')")[0])
p=json.load(open('picks.json')); H=p['results']['history']
L={
'Denver Nuggets +1.5':('hit','DEN 116-108 at NO (won by 8)'),
'Minnesota Timberwolves -4.5':('miss','CHI 117-106 at MIN (Wolves lost by 11)'),
'Liberty -10.5':('miss','LIB 28-23 vs MTSU (won by 5, needed 11)'),
'Iowa -7.5':('hit','IOWA 28-7 vs Purdue (won by 21)'),
'Notre Dame -17.5':('hit','ND 41-7 vs BC (won by 34)'),
'Virginia Tech -5.5':('miss','STAN 40-22 at VT (Hokies lost by 18)'),
'Louisiana Tech -7.5':('hit','LT 63-31 vs USM (won by 32)'),
'New Mexico -7.5':('miss','UNLV 21-17 at UNM (Lobos lost by 4)'),
'New Jersey Devils +1.5':('hit','NJ 7-4 at WSH (won by 3)'),
'Carolina Hurricanes +1.5':('hit','CAR 5-1 vs SEA (won by 4)'),
'Georgia Tech ML':('hit','GT 75-74 vs UNC Asheville (by 1)'),
'Wake Forest ML':('hit','WAKE 89-51 vs Southern Utah'),
'St. Bonaventure ML':('hit','SBU 81-58 vs Lafayette'),
'California ML':('hit','CAL 79-73 vs Utah Tech (by 6)'),
'Duquesne ML':('hit','DUQ 71-58 vs Binghamton'),
'Alabama +1.5':('hit','ALA 21-6 at Vanderbilt'),
'Ottawa Senators +1.5':('hit','OTT 4-1 at PIT (won by 3)'),
'Boise State -6.5':('miss','BOIS 46-41 vs ORST (won by 5, needed 7)'),
'Air Force -4.5':('hit','AFA 24-3 vs SJSU (won by 21)'),
'Penn State -2.5':('hit','PSU 42-14 vs MINN (won by 28)'),
'Wild/Bruins Under 8.5 Goals':('hit','MIN 6-2 at BOS (8 goals; under by 0.5)'),
'Red Wings/Lightning Over 3.5 Goals':('miss','DET 2-0 at TB (2 goals)'),
}
WHY={
('10:30 AM','Nuggets Road Cushion + Wolves Bought-Down'):('Lost: Denver won 116-108 at New Orleans (hit), but Chicago beat Minnesota 117-106; Wolves -4.5 lost outright by 11.','The "opponent on a back-to-back after OT" premise for an NBA buy-down failed badly: the tired Bulls won by 11 on the road. This is the second straight day an NBA buy-down nearly or fully failed (Rockets covered by 0.5 Friday). NBA spreads, even bought down 10 points, are not near-locks. Rule: no NBA alt-spread buy-downs on the favorite side; NBA legs only as +1.5 cushions on clearly better teams that pass the home-loss check.'),
('10:30 AM','Flames + Hawkeyes Bought-Down'):('Lost: Iowa beat Purdue 28-7 (hit), but Liberty beat Middle Tennessee only 28-23; -10.5 missed by 6.','Liberty was -20.5 main and SP+ cleared the +7 bar, but a Group-of-5 favorite beat a bad conference rival by 5. CFB buy-downs went 4/7 on Saturday (Iowa, Notre Dame, Louisiana Tech, Air Force, Penn State hit; Liberty, Virginia Tech, New Mexico, Boise missed). Model margin projections of 12-18 points have too much variance for a single bought line.'),
('10:30 AM','Irish + Hokies Bought-Down'):('Lost: Notre Dame beat Boston College 41-7 (hit), but Stanford won 40-22 at Virginia Tech; Hokies -5.5 lost outright by 18.','Virginia Tech was a modest -12.5 home favorite; SP+ cleared the +7 bar but the Hokies lost by 18. Mid-sized CFB favorites (main line under -14) lose outright too often for a buy-down to be near-certain. Rule: CFB buy-downs only on main-line favorites of -17 or more (Notre Dame, Louisiana Tech, Penn State-type spots), home only.'),
('10:30 AM','Bulldogs + Lobos Bought-Down'):('Lost: Louisiana Tech beat Southern Miss 63-31 (hit), but UNLV won 21-17 at New Mexico; Lobos -7.5 lost outright.','New Mexico was -14.5 main vs a UNLV team that is a stronger program than its record; model edge alone was not enough. Same rule: home favorites of -17+ only for CFB buy-downs.'),
('10:30 AM','Devils + Canes Goalie-Edge Ice'):('Won: New Jersey won 7-4 at Washington and Carolina beat Seattle 5-1.','The goalie-edge +1.5 rule (favorite starter .910+, edge .025+, confirmed) went 3/3 Saturday incl. Ottawa. It is the most reliable leg type on the card. Paid $4.13 on $10.'),
('10:30 AM','Best Shot $500K'):('Won 6/6: Georgia Tech by 1 (75-74 vs UNC Asheville), Wake Forest by 38, St. Bonaventure by 23, Cal by 6, Duquesne by 13, Alabama 21-6 at Vanderbilt. Paid $1.77 on $5.','The tier-gap rule is now 29/29, but Georgia Tech (-3500) survived by one point and Cal (-1600) by six. Early-season ACC/high-major hosts vs decent mid-majors are not true locks; keep tier gaps to bottom-tier (SWAC/MEAC/NEC-type, T-Rank 300+) visitors.'),
('3:00 PM','Senators Goalie-Edge + Broncos Backup-QB Fade'):('Lost: Ottawa won 4-1 at Pittsburgh (hit), but Boise State beat Oregon State only 46-41; -6.5 missed by 2.','The backup-QB fade failed: Oregon State\'s backup scored 41 points. The adjustment for a missing QB was overestimated, and Boise had its own QB question. Rule: the backup-QB fade works on the underdog side (points against a bad backup, like Illinois +20.5), not by buying down the favorite.'),
('3:00 PM','Falcons + Nittany Lions Bought-Down'):('Won: Air Force beat San Jose State 24-3 and Penn State beat Minnesota 42-14.','Both home favorites in the -12.5 to -13.5 range covered big, backed by strong line movement toward them. Watch rule (require both SP+ and PRIME) is moot: Penn State won by 28. Line movement of 3.5+ points toward the favorite was the common thread in the winning CFB buy-downs. Paid $5.75 on $10.'),
('3:00 PM','Best Shot $500K'):('Lost: Minnesota won 6-2 at Boston (8 goals, Under 8.5 hit by half a goal), but Detroit beat Tampa Bay 2-0; Over 3.5 missed with only 2 goals.','The ~90% game-log totals test went 1/2 and the hit was a half-goal sweat. Low NHL alt overs are exposed to a hot goalie (Detroit shutout). Rule: NHL alt overs only when both starting goalies are below .900 and confirmed; game-log rate alone is not enough.'),
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
