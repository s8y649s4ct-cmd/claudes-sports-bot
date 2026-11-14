#!/usr/bin/env python3
"""Sat Nov 14 2026 10:30 AM: grade Friday Nov 13 (NBA/NHL/NCAAB/NCAAF) from ESPN finals."""
import json, copy
exec(open('/workspace/csb/build_sat_pm.py').read().split("if os.environ.get('KEEP')")[0])
p=json.load(open('picks.json')); H=p['results']['history']
L={
'Portland Trail Blazers +1.5':('hit','POR 120-107 at SAC (won by 13)'),
'Houston Rockets -6.5':('hit','HOU 125-118 vs UTA (won by 7, needed 7)'),
'New York Knicks +1.5':('miss','IND 106-104 vs NYK (Knicks lost by 2; needed to lose by 1 or less)'),
'Rutgers -13.5':('hit','RUTG 72-51 vs Bryant (won by 21)'),
'Houston +3.5':('miss','COLO 42-32 vs HOU (Houston lost by 10)'),
'Atlanta Hawks +4.5':('miss','CHI 125-117 OT vs ATL (110-110 after regulation; Bulls won OT 15-7, Hawks lost by 8)'),
'Florida State ML':('hit','FSU 84-60 vs TAMU-CC'),
'NC State ML':('hit','NCSU 81-62 vs Troy'),
'UCF ML':('hit','UCF 84-70 vs Georgia Southern'),
'TCU ML':('hit','TCU 76-64 vs Milwaukee'),
'Arkansas ML':('hit','ARK 79-66 vs Central Arkansas'),
'SMU ML':('hit','SMU 90-65 vs Ball State'),
'Liberty ML':('hit','LIB 74-66 vs NC Central'),
'Tarleton State ML':('hit','TAR 73-69 vs Alcorn State (by 4)'),
'San Antonio Spurs +1.5':('hit','SA 123-85 vs GSW (won by 38)'),
'Orlando Magic +1.5':('hit','ORL 107-99 vs MIL (won by 8)'),
'Memphis Grizzlies +7.5':('hit','MEM 142-111 at NOP (won by 31)'),
'Illinois +20.5':('hit','UCLA 22-14 vs ILL (Illinois lost by 8)'),
'Vancouver Canucks Under 3.5 Goals':('hit','NYR 5-1 at VAN (Canucks scored 1)'),
'Drake ML':('hit','DRKE 81-72 vs South Dakota'),
'Cavaliers/Heat Over 213.5':('hit','MIA 133-121 (254 total)'),
'Predators/Golden Knights Under 8.5 Goals':('hit','NSH 3-2 SO at VGK (5 total goals incl. shootout goal)'),
}
WHY={
('10:30 AM','Blazers Road Cushion + Rockets Bought-Down'):('Won: Portland won 120-107 at Sacramento (+1.5 not needed) and Houston beat Utah 125-118, covering -6.5 by half a point.','Blazers +1.5 was the model road-favorite leg: the Kings\' home losses were by 11, 13, 15, 6, 7 and 27 (blowouts), and they lost by 13 again. Rockets -6.5 needed Sengun\'s 43 to clear by half a point vs an 11-straight-loss Jazz team; NBA buy-downs of ~10 points still land near the number, so buy-downs of NBA spreads should keep 10+ points off the main line.'),
('10:30 AM','Knicks Road Cushion + Scarlet Knights Bought-Down'):('Lost: Rutgers beat Bryant 72-51 (covered -13.5 by 7.5), but Indiana beat New York 106-104 in an NBA Cup game; Knicks +1.5 missed by half a point.','The Pacers\' home losses before Friday were by 5, 8, 4 and 12, so they were a competitive home team despite 1-4. Brunson scored 33 but the Knicks lost the second quarter 32-22. Rule: a road favorite on the plus side needs a home team that has been getting blown out at home (most home losses by 10+, like Sacramento). If the bad home team\'s losses are mostly within 8, skip it. Also, NBA Cup games produced two outright wins by struggling home teams on Friday (Indiana, Chicago).'),
('10:30 AM','Cougars Road Cushion + Hawks Big Cushion'):('Lost both legs: Colorado beat No. 14 Houston 42-32 (Houston +3.5 lost by 10), and Chicago beat Atlanta 125-117 in overtime (110-110 after regulation, so Hawks +4.5 lost when the Bulls won OT 15-7).','Two road favorites against struggling home teams both lost outright. Colorado ran for 67-, 38- and 32-yard touchdowns at home at night with a coach on the hot seat. College road favorites under two touchdowns carry upset risk that +3.5 does not cover. Chicago\'s home losses were all by 4-6, which was the warning; we added cushion when we should have skipped. Rules: (1) no CFB road favorite of less than -14 on any side; (2) skip NBA road favorites when the home team keeps losing close at home (same as the Knicks lesson).'),
('10:30 AM','Best Shot $500K'):('Won 8/8: Florida State by 24, NC State by 19, UCF by 14, TCU by 12, Arkansas by 13, SMU by 25, Liberty by 8 and Tarleton State by 4. Paid $0.65 on $5 at -767.','The tier-gap rule went 8/8 again (23/23 over three Best Shots), but Tarleton (-2800) beat SWAC Alcorn by only 4 and Liberty (-3000) by 8. When the host is itself a low-major (T-Rank 150+), the tier gap is smaller than the price suggests. Tier-gap moneylines now need a host in the top ~150.'),
('3:00 PM','Spurs + Magic Home Cushions'):('Won: San Antonio beat Golden State 123-85 and Orlando beat Milwaukee 107-99.','Both clearly-better home favorites cashed. Orlando was 0-4 at home but won by 8 against a 0-5-on-the-road Bucks team. The watch rule is resolved: no tightening needed when the visitor is also winless on the road and point differential favors the home team by 9+.'),
('3:00 PM','Grizzlies Road Cushion + Illini Big Cushion'):('Won: Memphis won 142-111 at New Orleans, and UCLA beat Illinois 22-14 (+20.5 covered by 12.5).','Road favorite with a 5-0 road record vs a home team that had been blown out at home: an easy cover, the opposite of Chicago/Indiana. The backup-QB fade (points against UCLA\'s third-string QB in a 47.5-total game) cashed comfortably.'),
('3:00 PM','Canucks Team Under + Bulldogs ML'):('Won: the Rangers beat Vancouver 5-1 (Canucks scored once), and Drake beat South Dakota 81-72.','A team-total under on the NHL\'s worst offense instead of a failed goalie-edge +1.5 worked as designed. Drake won by 9 against an 87.5-ppg visitor; moneyline (not a buy-down) was right.'),
('3:00 PM','Best Shot $500K'):('Won: Heat 133, Cavaliers 121 (254, Over 213.5 by 40.5), and Nashville won 3-2 in a shootout at Vegas (5 goals, Under 8.5). Paid $1.25 on $5 at -400.','The ~90% game-log totals test went 2/2. Short, safe, low payout, as stated.'),
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
