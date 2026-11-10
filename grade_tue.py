#!/usr/bin/env python3
"""Tue Nov 10 2026 10:30 AM: grade Monday Nov 9 (NFL/NBA/NHL/NCAAB/Challenger tennis) from ESPN/ATP finals."""
import json, copy
exec(open('/workspace/csb/build_sat_pm.py').read().split("if os.environ.get('KEEP')")[0])
p=json.load(open('picks.json')); H=p['results']['history']
L={
'Buffalo Bills +6.5':('hit','BUF 23-6 at MIN (won by 17)'),
'San Antonio Spurs +1.5':('hit','SA 122-96 at PHX (won by 26)'),
'New York Islanders +1.5':('hit','SJ 3-2 SO (lost by 1)'),
'Cleveland Cavaliers +1.5':('miss','CHA 124-112 (CLE lost by 12)'),
'Edmonton Oilers +1.5':('hit','EDM 3-1'),
'Golden State Warriors +1.5':('hit','GSW 138-87 (won by 51)'),
'Detroit Pistons +1.5':('hit','DET 122-111 (won by 11)'),
'Ohio State -16.5':('miss','OSU 84-74 (won by 10, needed 17)'),
'Oklahoma -18.5':('miss','OU 81-72 (won by 9, needed 19)'),
'Auburn -15.5':('hit','AUB 75-53 (won by 22)'),
'UIC -10.5':('miss','UIC 82-72 (won by 10, needed 11)'),
'Clemson -13.5':('hit','CLEM 92-77 (won by 15)'),
'Stanford -9.5':('hit','STAN 91-73 (won by 18)'),
'Oregon State -7.5':('hit','ORST 94-84 (won by 10)'),
'Notre Dame -20.5':('hit','ND 94-70 (won by 24)'),
'Alabama -23.5':('hit','BAMA 109-68 (won by 41)'),
'LSU -20.5':('hit','LSU 90-50 (won by 40)'),
'Missouri -22.5':('hit','MIZ 96-58 (won by 38)'),
'Purdue -6.5':('hit','PUR 76-59 (won by 17)'),
'Indiana +3.5':('hit','IND 83-80 (won by 3)'),
'Cincinnati +1.5':('miss','MIN 63-61 at CIN (lost by 2)'),
'Bowling Green ML':('hit','BGSU 95-79'),
'Columbia ML':('hit','Columbia 75-55'),
'Houston Rockets +1.5':('hit','HOU 110-100 (won by 10)'),
'Vancouver Canucks +1.5':('miss','PHI 3-1 at VAN (lost by 2)'),
'Toronto Raptors +4.5':('miss','MEM 118-102 at TOR (lost by 16)'),
'Texas -28.5':('hit','TEX 93-62 (won by 31)'),
'Tennessee -21.5':('hit','TENN 70-47 (won by 23)'),
'UConn -30.5':('hit','UConn 83-41 (won by 42)'),
'Northwestern -5.5':('hit','NU 72-55 (won by 17)'),
'UAB -9.5':('hit','UAB 92-64 (won by 28)'),
'Seton Hall +4.5':('hit','Seton Hall 68-62 (won by 6)'),
'Dallas Mavericks +5.5':('hit','DAL 125-122 (won by 3)'),
'Miami -28.5':('hit','Miami 89-51 (won by 38)'),
'Lakers/Hawks Over 226.5':('hit','LAL 124-114 (238 total)'),
'Georgia ML':('hit','UGA 80-72'),
'Mississippi State ML':('hit','MSST 98-57'),
'DePaul ML':('hit','DePaul 84-47'),
"Christopher O'Connell ML":('hit',"O'Connell d. Bouzige 6-4 6-1"),
'Juncheng Shang ML':('hit','Shang d. Delaney 6-3 3-6 6-4'),
}
WHY={
('10:30 AM','Bills Bought-Down + Spurs Cushion'):('Won: BUF won 23-6 at Minnesota (needed no worse than a 6-point loss) and SA won by 26 at Phoenix.','Fading a backup QB (Wentz) with a bought-down road favorite and giving an elite NBA favorite 10 points of cushion both cashed easily.'),
('10:30 AM','Islanders Road Ice + Cavs Cushion'):('Lost: NYI lost 3-2 in a shootout (+1.5 covered), but Cleveland lost by 12 at Charlotte (+1.5 missed).','An NBA road favorite on a long-ish trip vs a young, fast home team can lose outright; Charlotte had been better at home than its record. NBA road favorites at +1.5 need a healthy, clearly better team AND a check on recent form (CLE had been inconsistent). Road NHL favorites at +1.5 keep covering.'),
('10:30 AM','Oilers Home Ice + Warriors Cushion'):('Won: EDM 3-1 and GSW by 51 over a Pelicans team on a back-to-back.','Back-to-back fade plus home NHL favorite +1.5 both easy.'),
('10:30 AM','Pistons Cushion + Buckeyes Bought-Down'):('Lost: DET won by 11 (+1.5 hit), but Ohio State beat Marshall by only 10 (needed 17).','A Power-4 host vs a decent mid-major (Marshall, Sun Belt) is not the same as vs a SWAC/NEC team. 9 points off a -25.5 line still failed. Against competent mid-majors, cushion must be at least 12-14 points, or skip the alt.'),
('10:30 AM','Sooners + Tigers Bought-Down Hosts'):('Lost: Auburn won by 22 (hit), but Oklahoma beat North Alabama by only 9 (needed 19).','Same as Ohio State: big main spreads (-27.5) vs mid-major visitors with real guards can stay close. The 8-9 point buy-down only works when the visitor is truly bottom-tier (SWAC, NEC, MEAC, D-II-level).'),
('10:30 AM','Flames + Tigers Bought-Down Hosts'):('Lost: Clemson won by 15 (hit), but UIC beat UNC Greensboro by exactly 10 (needed 11).','UIC vs UNCG was a mid-major vs mid-major game; -19.5 was inflated. No bought-down alts in mid-major vs mid-major games.'),
('10:30 AM','West Coast Bought-Down Hosts'):('Won: Stanford by 18 and Oregon State by 10 (needed 8).','Power/strong host vs weak visitor held, though Oregon State was close; keep cushions at 9+.'),
('10:30 AM','Best Shot $500K'):('Lost: 9 of 12 legs hit. Cincinnati +1.5 (lost 63-61 to Minnesota), Canucks +1.5 (lost 3-1 to Philadelphia) and Raptors +4.5 (lost by 16 to Memphis) missed. All seven college favorites and the Rockets covered.','The three misses were the three closest-to-coin-flip legs (-380/-225/-245 on near pick\'em games). Big college favorites bought down vs low-major teams went 7/7. A day-long Best Shot should be built ONLY from the -1000+ college moneylines and big-cushion low-major alts, never pick\'em-game cushions.'),
('3:00 PM','Longhorns + Vols Bought-Down Hosts'):('Won: Texas by 31 (needed 29) and Tennessee by 23 (needed 22).','Both won but by only 2 and 1 points more than needed; the 9-point cushion was nearly all used. vs SWAC/Big South visitors it still held.'),
('3:00 PM','Huskies + Wildcats Bought-Down Hosts'):('Won: UConn by 42 and Northwestern by 17.','Elite host vs NEC team plus Big Ten host vs Patriot League both held comfortably.'),
('3:00 PM','Blazers + Pirates Home Cushions'):('Won: UAB by 28 and Seton Hall by 6.','Big host vs MEAC team and better-team +4.5 both cashed.'),
('3:00 PM','Mavs Cushion + Hurricanes Bought-Down'):('Won: Dallas won by 3 (+5.5) and Miami by 38.','Giving a back-to-back home favorite 9 points of cushion instead of the spread was right: Dallas only won by 3.'),
('3:00 PM','Best Shot $500K'):('Won: all 6 legs hit (Lakers/Hawks went over, Georgia, Mississippi State, DePaul, O\'Connell, Shang). But it was only -125, so it paid $4 on $5.','A short Best Shot of near-certain legs cashes, but the payout is tiny. Plan the morning/afternoon split so the 3 PM Best Shot gets enough strong evening legs to reach +1000.'),
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
