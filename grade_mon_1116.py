#!/usr/bin/env python3
"""Mon Nov 16 2026 10:30 AM: grade Sunday Nov 15 tickets from ESPN finals."""
import json, copy
exec(open('/workspace/csb/build_sat_pm.py').read().split("if os.environ.get('KEEP')")[0])
p=json.load(open('picks.json')); H=p['results']['history']
L={
'Boston Celtics +1.5':('hit','BOS 131-94 vs DAL (won by 37)'),
'Kansas City Chiefs +7.5':('hit','KC 35-13 at ATL (won by 22)'),
'Jacksonville Jaguars +2.5':('hit','JAX 40-23 at TEN (won by 17)'),
'San Antonio Spurs +1.5':('hit','SA 110-102 at UTAH (won by 8)'),
'Charleston ML':('hit','COFC 90-66 vs SC State'),
'Boston College ML':('hit','BC 67-55 vs New Hampshire'),
'Penn State ML':('hit','PSU 86-52 vs New Haven'),
'Loyola Marymount ML':('hit','LMU 86-49 vs Chicago State'),
'James Madison ML':('hit','JMU 80-71 vs Mercyhurst (by 9)'),
'Atlanta Hawks +1.5':('hit','ATL 113-106 at MIL (won by 7)'),
'Los Angeles Rams +3.5':('hit','LAR 34-6 at ARI (won by 28)'),
'Houston Rockets +4.5':('hit','HOU 147-119 at WSH (won by 28)'),
'Oklahoma City Thunder +4.5':('hit','OKC 125-103 at SAC (won by 22)'),
}
WHY={
('10:30 AM','Celtics Home Cushion + Chiefs Big Cushion'):('Won: Boston beat Dallas 131-94 and Kansas City won 35-13 at Atlanta. Both cushions were never in danger.','Plus-side cushions on clearly better teams went 2/2; the Chiefs +7.5 (15 points off the main) was never needed. Keep this leg type as the backbone.'),
('10:30 AM','Best Shot $500K'):('Won 7/7: Jaguars won by 17 at Tennessee, Spurs by 8 at Utah, and all five college hosts won (Charleston by 24, BC by 12, Penn State by 34, LMU by 37, JMU by 9).','Tier gaps vs bottom-tier visitors went 5/5 (JMU vs Mercyhurst the closest at 9). Plus-side NFL/NBA cushions held. The rule set (bottom-tier visitors only, plus-side cushions, home-loss check) produced a clean sweep.'),
('3:00 PM','Hawks Road Cushion + Rams Big Cushion'):('Won: Atlanta won 113-106 at Milwaukee and the Rams won 34-6 at Arizona.','The home-loss check (Bucks 5 of 6 home losses by 10+, Cardinals 0-3 at home by 14+) picked two hosts that lost again. Arizona\'s backup-QB situation was the decisive factor. Backup-QB fade on the plus side works.'),
('3:00 PM','Best Shot $500K'):('Won 2/2: Houston won 147-119 at Washington and OKC won 125-103 at Sacramento.','Short-handed but much better road teams still won by 20+; the +4.5 injury-sized cushions were never tested. Keep sizing cushions to the injury list; the approach went 2/2 in its first test.'),
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
