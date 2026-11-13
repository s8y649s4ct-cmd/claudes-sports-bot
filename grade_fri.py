#!/usr/bin/env python3
"""Fri Nov 13 2026 10:30 AM: grade Thursday Nov 12 (NBA/NHL/NCAAB/NCAAF) from ESPN finals."""
import json, copy
exec(open('/workspace/csb/build_sat_pm.py').read().split("if os.environ.get('KEEP')")[0])
p=json.load(open('picks.json')); H=p['results']['history']
L={
'Detroit Pistons +1.5':('hit','DET 144-140 at WSH in 2OT (won by 4)'),
'George Mason -7.5':('hit','GMU 76-68 vs UMKC (won by 8, needed 8)'),
'Minnesota Wild +1.5':('hit','MIN 5-2 at TOR'),
'Towson ML':('hit','TOW 90-60 vs Loyola MD'),
'Rhode Island ML':('hit','URI 67-47 vs UMES'),
'Indiana ML':('hit','IU 90-66 vs Tennessee Tech'),
'Minnesota ML':('hit','MINN 91-61 vs Southern'),
'High Point ML':('hit','HPU 88-59 vs Southern Utah'),
'Penn State ML':('hit','PSU 72-57 vs Mercyhurst'),
'Bowling Green ML':('hit','BGSU 88-76 vs Niagara'),
'New Jersey Devils +1.5':('hit','NJ 5-2 vs WSH'),
'Ottawa Senators +1.5':('hit','OTT 4-3 OT vs COL'),
'New York Islanders +1.5':('hit','NYI 5-2 at LA'),
'St. Louis Blues +1.5':('hit','STL 1-0 SO at UTA'),
'Dallas Stars +1.5':('miss','WPG 8-3 at DAL (Oettinger 6 GA on 27 shots, pulled)'),
'Phoenix Suns +4.5':('hit','PHX 101-96 vs CHA (won by 5)'),
'West Virginia ML':('hit','WVU 75-61 vs Mercer'),
'Florida Panthers +1.5':('hit','FLA 5-4 vs DET'),
'Louisiana +3.5':('hit','UL 42-21 at ULM (won by 21)'),
}
WHY={
('10:30 AM','Pistons Road Cushion + Patriots Bought-Down'):('Won: Detroit won 144-140 in double overtime at Washington (+1.5 not needed, but it was a coin flip late in regulation), and George Mason beat UMKC 76-68, covering -7.5 by half a point.','Both legs cashed but both were close. Washington on a back-to-back still pushed Detroit to 2OT, so +1.5 on a road favorite was the right side of the number. George Mason (projected by ~16.5) won by only 8: low-major buy-downs keep landing right at the number in November (Tulsa covered by zero Wednesday). Raise the projection bar to buy-down + 7, or use the moneyline.'),
('10:30 AM','Wild Road Ice + Tigers ML'):('Won: Minnesota won 5-2 at Toronto and Towson beat Loyola Maryland 90-60.','A goalie-edge road favorite at +1.5 against a slumping home team, plus a CAA host vs a bottom-25 visitor (true tier gap). Both won comfortably. Keep this template.'),
('10:30 AM','Best Shot $500K'):('Won: all six home moneylines hit (Rhode Island by 20, Indiana by 24, Minnesota by 30, High Point by 29, Penn State by 15, Bowling Green by 12). Paid $0.51 on $5 at -971.','The tier-gap rule (lower-league, T-Rank ~200+ visitors) went 6/6 one day after the Seattle loss. It is a safety ticket, not a $5K ticket; at -971 it pays almost nothing.'),
('3:00 PM','Devils + Senators Goalie-Edge Ice'):('Won: New Jersey beat Washington 5-2 and Ottawa beat Colorado 4-3 in overtime.','Waiting for the confirmed starter (Hellebuyck) before using the Devils was right. Ullmark .945 vs Wedgewood .867, the biggest goalie edge on the board, won in OT; +1.5 was the right protection in a pick\'em.'),
('3:00 PM','Islanders + Blues Goalie-Edge Ice'):('Won: the Islanders won 5-2 at Los Angeles and St. Louis won 1-0 in a shootout at Utah (on a back-to-back).','Goalie edge plus a tired or struggling host. Hofer pitched a shutout against a Utah team on the second night of a back-to-back.'),
('3:00 PM','Stars Home Ice + Suns Big Cushion'):('Lost: Phoenix beat Charlotte 101-96 (+4.5 not needed), but Winnipeg routed Dallas 8-3. Jake Oettinger allowed 6 goals on 27 shots and was pulled.','Dallas had the smallest goalie edge of the five NHL +1.5 legs (Oettinger .906 vs Skinner .883, about .023), and Oettinger is not an elite-form starter this year. The NHL +1.5 legs that won had a wider gap or a tired opponent. Rule: goalie edge of about .025+ and the favorite\'s starter at .910+, or an opponent on a back-to-back. The Suns leg was also closer than it should have been (won by 5 vs a team missing three starters), so the 11-point cushion was justified.'),
('3:00 PM','Best Shot $500K'):('Won: West Virginia beat Mercer by 14, Florida beat Detroit 5-4 (+1.5 not needed) and Louisiana won by 21 at UL Monroe. Paid $1.68 on $5 at -297.','A three-leg safety ticket that cashed but pays very little. Florida (Schmid .886) was the shakiest leg and won by one goal.'),
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
