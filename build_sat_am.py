#!/usr/bin/env python3
"""Sat Nov 7, 2026 10:30 AM ET — grade Friday settles + build Saturday morning card."""
import json, copy, datetime, urllib.request, os, re
from datetime import timezone, timedelta

ET = timezone(timedelta(hours=-5))
K = 'FhMFpcPWXMeyZxOx'
UA = {'User-Agent': 'Mozilla/5.0'}
NOW = datetime.datetime.now(timezone.utc)

# EventIds already on pending tickets (Fri PM card + Sun NFL from Thu/Fri) — do not reuse
BURNED = {
    35632913, 36244868, 36244869, 36244871, 36244872, 36244874, 36244875,
    36244876, 36244877, 36244878, 36244879, 36260494, 36260589, 36260623,
    36260645, 36260771, 36285062, 36285069, 36285113, 36285148, 36285161,
    36285198, 36285326, 36285790, 36287945, 36287946, 36287947, 36287956,
    36287958, 36287959, 36287960, 36287969,
}

def get(u):
    try:
        return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25))
    except Exception:
        return {}

def am_odds(r):
    wi = (r.get('winRunnerOdds') or {}).get('americanDisplayOdds') or {}
    return wi.get('americanOddsInt') or wi.get('americanOdds')

def am_to_dec(o):
    return 1 + 100 / abs(o) if o < 0 else 1 + o / 100.0

def combine(odds):
    d = 1.0
    for o in odds:
        d *= am_to_dec(o)
    am = round((d - 1) * 100) if d >= 2 else round(-100 / (d - 1))
    return int(am), d

def profit_for(odds, stake, won=True):
    if not won:
        return -stake
    if odds < 0:
        return round(stake * 100 / abs(odds), 2)
    return round(stake * odds / 100.0, 2)

def start_et(iso):
    t = datetime.datetime.fromisoformat(iso.replace('Z', '+00:00')).astimezone(ET)
    h = t.strftime('%I').lstrip('0') or '12'
    return f"{t.strftime('%a')} {h}:{t.strftime('%M')} {t.strftime('%p')} ET"

def load_event(eid, tabs=('', 'popular', 'alternates')):
    mkts, ev = {}, None
    for tab in tabs:
        path = f'/workspace/ev_{eid}{("_"+tab) if tab else ""}.json'
        o = None
        if os.path.exists(path):
            try:
                o = json.load(open(path))
            except Exception:
                o = None
        if not o or not (o.get('attachments') or {}).get('markets'):
            o = get(f'https://sbapi.pa.sportsbook.fanduel.com/api/event-page?_ak={K}&eventId={eid}' + (f'&tab={tab}' if tab else ''))
            try:
                json.dump(o, open(path, 'w'))
            except Exception:
                pass
        mkts.update((o.get('attachments') or {}).get('markets') or {})
        evs = (o.get('attachments') or {}).get('events') or {}
        if isinstance(evs, dict) and evs:
            ev = list(evs.values())[0]
        elif isinstance(evs, list) and evs:
            ev = evs[0]
    return ev, mkts

def find_runner(mkts, market_pred, runner_pred):
    for mid, m in mkts.items():
        if m.get('marketStatus') != 'OPEN' or m.get('inPlay'):
            continue
        if m.get('sgmMarket') is False:
            continue
        mn = m.get('marketName', '')
        if not market_pred(mn):
            continue
        ctp = m.get('canTurnInPlay')
        mt = m.get('marketType', '')
        prop = any(p in mt for p in ('PLAYER', 'TO_RECORD', 'TO_SCORE')) or 'Shots on Goal' in mn
        if ctp is False and not prop:
            continue
        for r in m.get('runners') or []:
            if r.get('runnerStatus') != 'ACTIVE':
                continue
            if runner_pred(r, m):
                o = am_odds(r)
                if o is None:
                    continue
                return {
                    'marketId': mid,
                    'selectionId': str(r['selectionId']),
                    'odds': int(o),
                    'market': mn,
                    'runnerName': r.get('runnerName'),
                    'handicap': r.get('handicap'),
                    'eventId': int(m['eventId']),
                }
    return None

def recompute_totals(history):
    sections = {
        'singles': {'won': 0, 'lost': 0, 'pending': 0, 'staked': 0, 'profit': 0.0},
        'parlays': {'won': 0, 'lost': 0, 'pending': 0, 'staked': 0, 'profit': 0.0},
        'lottery': {'won': 0, 'lost': 0, 'pending': 0, 'staked': 0, 'profit': 0.0},
    }
    type_map = {'single': 'singles', 'parlay': 'parlays', 'lottery': 'lottery'}
    hit = miss = pend = void = 0
    for h in history:
        sec = type_map.get(h.get('type'))
        if not sec:
            continue
        stake = h.get('stake') or 0
        result = h.get('result')
        profit = h.get('profit')
        if profit is None:
            profit = 0
        if result == 'won':
            sections[sec]['won'] += 1
            sections[sec]['staked'] += stake
            sections[sec]['profit'] += profit
        elif result == 'lost':
            sections[sec]['lost'] += 1
            sections[sec]['staked'] += stake
            sections[sec]['profit'] += profit
        elif result == 'pending':
            sections[sec]['pending'] += 1
        for leg in h.get('legs') or []:
            r = leg.get('result')
            if r == 'hit':
                hit += 1
            elif r == 'miss':
                miss += 1
            elif r == 'pending':
                pend += 1
            elif r == 'void':
                void += 1
    out = {}
    for k, v in sections.items():
        decided = v['won'] + v['lost']
        v['winPct'] = round(100 * v['won'] / decided, 1) if decided else 0.0
        v['profit'] = round(v['profit'], 2)
        v['roiPct'] = round(100 * v['profit'] / v['staked'], 1) if v['staked'] else 0.0
        out[k] = v
    overall = {
        'won': sum(out[k]['won'] for k in out),
        'lost': sum(out[k]['lost'] for k in out),
        'pending': sum(out[k]['pending'] for k in out),
        'staked': sum(out[k]['staked'] for k in out),
        'profit': round(sum(out[k]['profit'] for k in out), 2),
    }
    decided = overall['won'] + overall['lost']
    overall['winPct'] = round(100 * overall['won'] / decided, 1) if decided else 0.0
    overall['roiPct'] = round(100 * overall['profit'] / overall['staked'], 1) if overall['staked'] else 0.0
    out['overall'] = overall
    out['legs'] = {'hit': hit, 'miss': miss, 'pending': pend, 'void': void}
    for k in ['won', 'lost', 'pending', 'winPct', 'staked', 'profit', 'roiPct']:
        out[k] = overall[k]
    return out

def already_in_history(history, name, date, run):
    for h in history:
        if h.get('name') == name and h.get('date') == date and h.get('run') == run:
            return True
    return False

# ---- load ----
p = json.load(open('/workspace/csb/picks.json'))

# ============================================================
# STEP 1 — GRADE SETTLED
# ============================================================

# Update leftover pending legs on already-lost tickets
leftover_legs = {
    # 11/5 3PM Campus Moneyline Trio (already lost on Tulane)
    ('Campus Moneyline Trio', 'Oregon ML'): ('hit', 'Oregon 98, Eastern Washington 71'),
    # 11/5 3PM Best Shot (already lost)
    ('Best Shot $500K', 'Purdue ML'): ('miss', 'Valparaiso 83, Purdue 80 (2OT)'),
    ('Best Shot $500K', 'Florida State ML'): ('hit', 'Florida State 91, Troy 68'),
    ('Best Shot $500K', 'Xavier ML'): ('hit', 'Xavier 76, Eastern Michigan 53'),
    ('Best Shot $500K', 'NC State ML'): ('hit', 'NC State 77, East Tennessee State 63'),
    ('Best Shot $500K', 'Georgia Tech ML'): ('hit', 'Georgia Tech 95, Georgia Southern 83'),
    ('Best Shot $500K', 'Wisconsin ML'): ('hit', 'Wisconsin 73, Delaware 64'),
    ('Best Shot $500K', 'Tage Thompson 2+ Shots on Goal'): ('hit', 'Tage Thompson 3 SOG'),
    ('Best Shot $500K', 'Leo Carlsson 1+ Shots on Goal'): ('hit', 'Leo Carlsson 1 SOG'),
}

for h in p['results']['history']:
    if h.get('date') == '2026-11-05' and h.get('run') == '3:00 PM':
        for leg in h.get('legs') or []:
            if leg.get('result') != 'pending':
                continue
            key = (h.get('name'), leg.get('pick'))
            if key in leftover_legs:
                leg['result'], leg['actual'] = leftover_legs[key]

# Full grades for pending tickets that settled Friday
grades = {
    # ---- 11/5 3PM ----
    ('2026-11-05', '3:00 PM', 'Friday College Locks'): {
        'result': 'won',
        'legs': {
            'Alabama ML': ('hit', 'Alabama 101, Arkansas State 86'),
            'North Carolina ML': ('hit', 'North Carolina 109, Wofford 70'),
            'Ohio State ML': ('hit', 'Ohio State 89, Youngstown State 65'),
            'Kentucky ML': ('hit', 'Kentucky 89, James Madison 80'),
        },
        'why': 'WON at -2821. All four Power hosts at -10000/-20000 hit: Alabama 101-86, UNC 109-70, Ohio State 89-65, Kentucky 89-80.',
        'lesson': 'College MLs at -1800+ continue to cash as lock-parlay backbone (now 31-0 on dedicated lock tickets).',
    },
    # ---- 11/6 10:30 AM singles ----
    ('2026-11-06', '10:30 AM', 'Sacramento Kings +15.5'): {
        'result': 'won',
        'legs': {'Sacramento Kings +15.5': ('hit', 'Spurs 124, Kings 109 (lost by 15 — covered +15.5)')},
        'why': 'WON. Spurs 124 Kings 109 — Sacramento lost by 15 and covered +15.5 by half a point.',
        'lesson': 'Extreme NBA dog cushions (≥+15.5) can still cash in competitive losses. Keep ≥+9.5 minimum; bigger is safer vs elite.',
    },
    ('2026-11-06', '10:30 AM', 'Virginia Tech +4.5'): {
        'result': 'lost',
        'legs': {'Virginia Tech +4.5': ('miss', 'SMU 51, Virginia Tech 28 (lost by 23)')},
        'why': 'LOST. SMU 51 VT 28 — Hokies got blown out on the road and never threatened +4.5.',
        'lesson': 'Small CFB road cushions (+4.5) are not high-prob when the home side is motivated and healthy. Prefer ≥+9.5 for dog singles.',
    },
    ('2026-11-06', '10:30 AM', 'Nevada +8.5'): {
        'result': 'lost',
        'legs': {'Nevada +8.5': ('miss', 'New Mexico 31, Nevada 3 (lost by 28)')},
        'why': 'LOST. New Mexico 31 Nevada 3 — home dog got crushed; +8.5 never had a chance.',
        'lesson': 'Mountain West home dogs can still get run. +8.5 was under the ≥+9.5 cushion rule spirit — need more points or skip soft home dogs.',
    },
    # ---- 11/6 10:30 AM parlays ----
    ('2026-11-06', '10:30 AM', 'Home Ice +1.5 Trio'): {
        'result': 'lost',
        'legs': {
            'Buffalo Sabres +1.5': ('hit', 'Sabres 5, Blue Jackets 2'),
            'Minnesota Wild +1.5': ('hit', 'Wild 4, Sharks 1'),
            'Calgary Flames +1.5': ('miss', 'Ducks 5, Flames 3 (lost by 2)'),
        },
        'why': 'LOST. Buffalo and Minnesota covered easily; Calgary lost 5-3 (by 2) and missed +1.5.',
        'lesson': 'NHL home +1.5 remains strong (2/3) but struggling home clubs (CGY) can lose by 2+. Prefer average-or-better home teams only.',
    },
    ('2026-11-06', '10:30 AM', 'Friday College Locks'): {
        'result': 'won',
        'legs': {
            'Ohio State ML': ('hit', 'Ohio State 89, Youngstown State 65'),
            'Alabama ML': ('hit', 'Alabama 101, Arkansas State 86'),
            'Wisconsin ML': ('hit', 'Wisconsin 73, Delaware 64'),
        },
        'why': 'WON at -5425. All three Power MLs hit. Wisconsin was the closest (73-64).',
        'lesson': 'College MLs at -1800+ on dedicated lock parlays are now 34-0. Keep as the safest backbone.',
    },
    ('2026-11-06', '10:30 AM', 'Campus Alt Favorites'): {
        'result': 'lost',
        'legs': {
            'Kentucky -19.5': ('miss', 'Kentucky 89, James Madison 80 (won by 9)'),
            'Purdue -13.5': ('miss', 'Valparaiso 83, Purdue 80 2OT (lost outright)'),
            'UAB -10.5': ('miss', 'UAB 70, Nicholls 63 (won by 7)'),
        },
        'why': 'LOST 0/3. Purdue fell in 2OT to Valpo; Kentucky won by only 9 vs JMU; UAB won by only 7 vs Nicholls. No leg covered.',
        'lesson': 'Even bought-down Power/campus alts under the -20 ban (‑19.5/‑13.5/‑10.5) failed in one night — early-season hosts can lose outright or fail mid spreads. Prefer -1800+ MLs over campus alt favorites.',
    },
}

# Best Shot 11/6 10:30 — grade all legs
bs_am_legs = {
    'Charlotte Hornets +11.5': ('miss', 'Celtics 119, Hornets 80 (lost by 39)'),
    'Washington Wizards +11.5': ('hit', 'Hawks 139, Wizards 132 (lost by 7)'),
    'Milwaukee Bucks +10.5': ('miss', 'Raptors 121, Bucks 107 (lost by 14)'),
    'Utah Jazz +10.5': ('miss', 'Mavericks 112, Jazz 100 (lost by 12)'),
    'Memphis Grizzlies +9.5': ('miss', 'Thunder 128, Grizzlies 97 (lost by 31)'),
    'New Orleans Pelicans +9.5': ('hit', 'Timberwolves 115, Pelicans 109 (lost by 6)'),
    'Cleveland Cavaliers +9.5': ('hit', 'Cavaliers 119, 76ers 95'),
    'Portland Trail Blazers +9.5': ('hit', 'Lakers 124, Blazers 118 (lost by 6)'),
    'Florida State ML': ('hit', 'Florida State 91, Troy 68'),
    'Xavier ML': ('hit', 'Xavier 76, Eastern Michigan 53'),
    'Georgia ML': ('hit', 'Georgia 91, Presbyterian 77'),
    'Rutgers ML': ('hit', 'Rutgers 81, New Haven 54'),
    'North Carolina ML': ('hit', 'North Carolina 109, Wofford 70'),
    'Georgia Tech ML': ('hit', 'Georgia Tech 95, Georgia Southern 83'),
    'NC State ML': ('hit', 'NC State 77, East Tennessee State 63'),
    'Clemson ML': ('hit', 'Clemson 82, American 73'),
    'Oregon ML': ('hit', 'Oregon 98, Eastern Washington 71'),
    'TCU ML': ('hit', 'TCU 106, Southern 54'),
    'Ole Miss ML': ('hit', 'Ole Miss 92, Central Arkansas 60'),
    'Arizona State ML': ('hit', 'Arizona State 90, Northern Colorado 63'),
    'Oklahoma State ML': ('hit', 'Oklahoma State 118, Queens 68'),
    'Oregon State ML': ('hit', 'Oregon State 96, California Baptist 68'),
    'Colorado State ML': ('hit', 'Colorado State 78, Idaho 67'),
    'TCU +9.5': ('hit', 'Arizona 29, TCU 28 (lost by 1)'),
    'Illinois +8.5': ('hit', 'Illinois 24, Nebraska 13'),
}

grades[('2026-11-06', '10:30 AM', 'Best Shot $500K')] = {
    'result': 'lost',
    'legs': bs_am_legs,
    'why': 'LOST. NBA dog cushions went 4/8 — Charlotte (by 39), Milwaukee (by 14), Utah (by 12) and Memphis (by 31) blew through ≥+9.5. All 15 college MLs and both CFB cushions hit.',
    'lesson': 'NBA ≥+9.5 cushions still fail in true mismatches (OKC/BOS blowouts). College -1800+ MLs on the same ticket went 15/15 — lean harder on those and skip the softest NBA dogs vs elite.',
}

# 11/6 3PM Friday Campus Cushions — WON
grades[('2026-11-06', '3:00 PM', 'Friday Campus Cushions')] = {
    'result': 'won',
    'legs': {
        'West Virginia -18.5': ('hit', 'West Virginia 91, Stetson 53 (won by 38)'),
        'Texas A&M -18.5': ('hit', 'Texas A&M 104, Northern Kentucky 67 (won by 37)'),
        'Minnesota -11.5': ('hit', 'Minnesota 76, St. Thomas 62 (won by 14)'),
    },
    'why': 'WON at +135. WVU -18.5 by 38, TAMU -18.5 by 37, Minnesota -11.5 by 14 — all covered the bought-down alts under the -20 ban.',
    'lesson': 'When chalk MLs are suspended, buying Power hosts down under -20 can still cash in true mismatches (contrast with Campus Alt Favorites 0-3 the same night).',
}

# 11/6 3PM Best Shot — update Friday college legs; keep ticket pending (NHL/CFB/NFL remain)
bs_pm_fri = {
    'Stanford ML': ('hit', 'Stanford 81, Oakland 63'),
    'Northwestern ML': ('hit', 'Northwestern 78, Stony Brook 65'),
    'Kansas State ML': ('hit', 'Kansas State 95, CSUN 78'),
    'San Francisco ML': ('hit', 'San Francisco 79, North Dakota State 70'),
    'UCF ML': ('hit', 'UCF 87, Yale 75'),
}

for h in p['results']['history']:
    key = (h.get('date'), h.get('run'), h.get('name'))
    if key in grades and h.get('result') == 'pending':
        g = grades[key]
        h['result'] = g['result']
        h['whyExplanation'] = g['why']
        h['lesson'] = g['lesson']
        by_pick = g['legs']
        for leg in h.get('legs') or []:
            if leg.get('pick') in by_pick:
                leg['result'], leg['actual'] = by_pick[leg['pick']]
        if g['result'] == 'won':
            h['profit'] = profit_for(h['odds'], h.get('stake') or 10, True)
        elif g['result'] == 'lost':
            h['profit'] = profit_for(h['odds'], h.get('stake') or 10, False)
    # Partial update afternoon Best Shot Friday legs
    if h.get('date') == '2026-11-06' and h.get('run') == '3:00 PM' and h.get('name') == 'Best Shot $500K':
        for leg in h.get('legs') or []:
            if leg.get('pick') in bs_pm_fri and leg.get('result') == 'pending':
                leg['result'], leg['actual'] = bs_pm_fri[leg['pick']]
        hits = sum(1 for l in h['legs'] if l.get('result') == 'hit')
        misses = sum(1 for l in h['legs'] if l.get('result') == 'miss')
        pend = sum(1 for l in h['legs'] if l.get('result') == 'pending')
        h['whyExplanation'] = (
            f'Pending — Friday college MLs went {hits} hit / {misses} miss so far; '
            f'{pend} Sat NHL / Sat CFB / Sun NFL legs still open. Ticket stays pending.'
        )

# Sunday NFL / Sat games still pending — leave alone:
# Jets, Raiders, Cards singles; Sunday Cushions; MSU; Sat Home Ice; Sat CFB Bought-Down; remaining BS legs

print('Graded pending → settled where finals exist')

# ============================================================
# STEP 2 — BUILD TODAY'S CARD
# ============================================================
EIDS = {
    # singles
    'arkansas': 36260590, 'broncos': 36244867, 'clemson': 36260624,
    # parlays
    'sju': 36289107, 'miami_oh': 36289981, 'dayton': 36288999,
    'wizards': 36282777, 'pacers': 36282776, 'nets': 36282778,
    'auburn': 36260590,  # WAIT — arkansas uses same event as auburn! conflict
}
# Fix: Arkansas single uses Auburn@Arkansas game — cannot also use Auburn in parlay
# Remap singles away from Auburn game if we want Auburn in CFB parlay

EIDS = {
    # singles (unique events)
    'isu': 36260639,          # Iowa State +13.5 plus-ish
    'broncos': 36244867,      # Broncos -3.5 +116
    'clemson': 36260624,      # Clemson -3.5 +124
    # college locks parlay
    'sju': 36289107,
    'miami_oh': 36289981,
    'dayton': 36288999,
    # NBA dog cushions parlay
    'wizards': 36282777,
    'pacers': 36282776,
    'nets': 36282778,
    # CFB bought-down parlay
    'auburn': 36260590,
    'baylor': 36260639,  # CONFLICT with isu single — fix
    'utah': 36244174,
}

# Resolve conflicts: ISU single conflicts with Baylor parlay (same game)
# Use Arkansas +9.5 as single (Auburn game) and Baylor/Utah/FSU for CFB parlay instead
EIDS = {
    'arkansas': 36260590,   # single Arkansas +9.5
    'broncos': 36244867,    # single Broncos -3.5
    'texas': 36244185,      # single Texas -3.5 +106 (plus money bought down)
    'sju': 36289107,
    'miami_oh': 36289981,
    'dayton': 36288999,
    'wizards': 36282777,
    'pacers': 36282776,
    'nets': 36282778,
    'baylor': 36260639,
    'utah': 36244174,
    'fsu': 36260632,
    # Best Shot extras
    'avs': 36287957,
    'caps': 36287949,  # Florida +1.5
    'preds': 36287950, # STL +1.5
    'kings_nhl': 36287970, # PIT +1.5
    'gcu': 36289019,
    'murray': 36290050,
    'santa_clara': 36289036,
    'magic': 36282775,
    'cavs': 36282780,
    'blazers': 36282779,
    'suns': 36282781,
    'purdue_fb': 36260644,  # Maryland +9.5
    'okst_fb': 36260728,    # KSU +11.5
    'tulane': 36260760,     # Tulane +10.5
    'ucla': 36244623,       # Minnesota +10.5
    'morehead': 36288901,   # Morehead +41.5
    'nmsu': 36288992,       # NMSU +32.5
    'clemson': 36260624,
    'ncsu_fb': 36260631,
    'coastal': 36260730,
    'uconn': 36260474,
    'bengals': 35603243,    # Bengals -3.5
    'eagles': 36244873,     # Eagles +10.5 / Giants side
}

cache = {}
for key, eid in EIDS.items():
    tabs = ('', 'popular', 'alternates')
    if key in ('morehead', 'nmsu'):
        tabs = ('', 'popular', 'alternates', 'spreads')
    cache[key] = load_event(eid, tabs)
    if not cache[key][0]:
        print('WARN missing', key, eid)

used_events, used_picks = set(str(x) for x in BURNED), set()

def make_leg(key, market_pred, runner_pred, pick, sport, reason):
    ev, mkts = cache[key]
    sel = find_runner(mkts, market_pred, runner_pred)
    if not sel:
        opts = []
        for mid, m in mkts.items():
            if m.get('marketStatus') != 'OPEN':
                continue
            mn = m.get('marketName', '')
            if not market_pred(mn):
                continue
            for r in m.get('runners') or []:
                o = am_odds(r)
                opts.append((mn, r.get('runnerName'), r.get('handicap'), o, mid, r.get('selectionId'), m.get('canTurnInPlay'), m.get('sgmMarket')))
        raise SystemExit(f'no sel for {pick} key={key} opts={opts[:30]}')
    eid = str(sel['eventId'])
    if eid in used_events:
        raise SystemExit(f'event reuse {eid} for {pick}')
    if pick in used_picks:
        raise SystemExit(f'pick reuse {pick}')
    used_events.add(eid)
    used_picks.add(pick)
    t = datetime.datetime.fromisoformat(ev['openDate'].replace('Z', '+00:00'))
    if t < NOW + timedelta(hours=1):
        raise SystemExit(f'start too soon {pick} {ev["openDate"]}')
    return {
        'pick': pick,
        'market': sel['market'],
        'odds': sel['odds'],
        'sport': sport,
        'event': ev['name'],
        'start': start_et(ev['openDate']),
        'reason': reason,
        'marketId': sel['marketId'],
        'selectionId': sel['selectionId'],
        'eventId': sel['eventId'],
    }

def mn_eq(name):
    return lambda mn: mn == name

def mn_alt_spread():
    return lambda mn: mn == 'Alternate Spread' or mn.startswith('Alternate Spread')

def rn_contains(substr):
    return lambda r, m: substr in (r.get('runnerName') or '')

def rn_hc(name, hc):
    return lambda r, m: r.get('runnerName') == name and r.get('handicap') == hc

def rn_eq(name):
    return lambda r, m: r.get('runnerName') == name

# ---- SINGLES (plus money) ----
singles = []
s1 = make_leg(
    'arkansas', mn_eq('Alternate Spread'), rn_contains('Arkansas (+9.5)'),
    'Arkansas +9.5', 'NCAAF',
    'Arkansas +9.5 at Auburn at +100 (main +10.5). Double-digit-minus-one CFB dog cushion at true plus money — win-prob first with a real payout.',
)
singles.append({**s1, 'stake': 10})
s2 = make_leg(
    'broncos', mn_eq('Alternate Spread'), rn_contains('Broncos (-3.5)'),
    'Denver Broncos -3.5', 'NFL',
    'Broncos -2.5 main at Carolina; bought to -3.5 at +116. Only need a field-goal win on the road at plus money.',
)
singles.append({**s2, 'stake': 10})
s3 = make_leg(
    'texas', mn_eq('Alternate Spread'), rn_contains('Texas (-3.5)'),
    'Texas -3.5', 'NCAAF',
    'Texas -2.5 main at Missouri; bought to -3.5 at +106. Plus-money bought-down favorite — need a field-goal win.',
)
singles.append({**s3, 'stake': 10})

# ---- PARLAYS ----
parlays = []

l_sju = make_leg('sju', mn_eq('Moneyline'), rn_eq("Saint Joseph's"),
    "Saint Joseph's ML", 'NCAAB',
    "Saint Joseph's -3000 home vs Lafayette. OPEN Power-host-caliber ML past the -1800 floor.")
l_mia = make_leg('miami_oh', mn_eq('Moneyline'), rn_eq('Miami (OH)'),
    'Miami (OH) ML', 'NCAAB',
    'Miami (OH) -4500 home vs Bellarmine. Clear class gap; OPEN ML at -1800+.')
l_day = make_leg('dayton', mn_eq('Moneyline'), rn_eq('Dayton'),
    'Dayton ML', 'NCAAB',
    'Dayton -4500 home vs Northern Illinois. OPEN ML well past -1800.')
odds, _ = combine([l_sju['odds'], l_mia['odds'], l_day['odds']])
parlays.append({
    'name': 'Saturday College Locks', 'odds': odds, 'stake': 10,
    'legs': [l_sju, l_mia, l_day],
    'reason': 'Three OPEN college MLs at -3000/-4500/-4500. College -1800+ lock parlays are 34-0 — keep as the safest 3-leg backbone.',
})

l_wsh = make_leg('wizards', mn_eq('Alternate Spread'), rn_contains('Wizards +14.5'),
    'Washington Wizards +14.5', 'NBA',
    'Wizards +11.5 main at OKC; bought OUT to +14.5 (-166). Extra cushion vs the league elite after Friday blowout misses.')
l_ind = make_leg('pacers', mn_eq('Alternate Spread'), rn_contains('Pacers +12.5'),
    'Indiana Pacers +12.5', 'NBA',
    'Pacers +7.5 main vs Denver; +12.5 alt (-230) adds 5 points of cushion — no Denver road-dog fade, just a fat home cushion.')
l_bkn = make_leg('nets', mn_eq('Alternate Spread'), rn_contains('Nets +12.5'),
    'Brooklyn Nets +12.5', 'NBA',
    'Nets +6.5 main at Atlanta; +12.5 (-255) is a ≥+9.5-style cushion with room after Friday mismatch lessons.')
odds, _ = combine([l_wsh['odds'], l_ind['odds'], l_bkn['odds']])
parlays.append({
    'name': 'NBA Big Cushions', 'odds': odds, 'stake': 10,
    'legs': [l_wsh, l_ind, l_bkn],
    'reason': 'Three NBA dog cushions bought well past the main number (≥+12.5) after Friday ≥+9.5 misses in true mismatches. Win-prob first.',
})

l_bay = make_leg('baylor', mn_eq('Alternate Spread'), rn_contains('Baylor (-7.5)'),
    'Baylor -7.5', 'NCAAF',
    'Baylor -9.5 main vs Iowa State; bought to -7.5 (-142) for a one-score cover.')
l_utah = make_leg('utah', mn_eq('Alternate Spread'), rn_contains('Utah (-3.5)'),
    'Utah -3.5', 'NCAAF',
    'Utah -4.5 main vs BYU; bought to -3.5 (-122). Only need a field-goal win at home.')
l_fsu = make_leg('fsu', mn_eq('Alternate Spread'), rn_contains('Florida State (-3.5)'),
    'Florida State -3.5', 'NCAAF',
    'FSU -5.5 main at BC; bought to -3.5 (-154). Field-goal cover on a road favorite.')
odds, _ = combine([l_bay['odds'], l_utah['odds'], l_fsu['odds']])
parlays.append({
    'name': 'Saturday CFB Bought-Down', 'odds': odds, 'stake': 10,
    'legs': [l_bay, l_utah, l_fsu],
    'reason': 'Three Saturday CFB favorites bought below the main number for ~75% covers and a real parlay price. No mid-major chalk; no event reuse with pending Fri PM CFB ticket.',
})

# ---- BEST SHOT ----
bs_specs = [
    ('gcu', mn_eq('Moneyline'), rn_eq('Grand Canyon'), 'Grand Canyon ML', 'NCAAB',
     'Grand Canyon -10000 home vs Bethune-Cookman. OPEN ML far past -1800.'),
    ('murray', mn_eq('Moneyline'), rn_eq('Murray State'), 'Murray State ML', 'NCAAB',
     'Murray State -10000 home vs Northwestern State. OPEN -1800+ ML.'),
    ('santa_clara', mn_eq('Moneyline'), rn_eq('Santa Clara'), 'Santa Clara ML', 'NCAAB',
     'Santa Clara -10000 home vs Sacramento State. OPEN -1800+ ML.'),
    ('avs', mn_eq('Moneyline'), rn_eq('Colorado Avalanche'), 'Colorado Avalanche ML', 'NHL',
     'Avalanche -230/-245 home vs Detroit. Clear home favorite; average+ club (home +1.5 lesson).'),
    ('caps', mn_eq('Puck Line'), rn_hc('Florida Panthers', 1.5), 'Florida Panthers +1.5', 'NHL',
     'Panthers +1.5 at Washington (-280). Goal cushion in a pick\'em; avoid coin-flip Caps ML.'),
    ('preds', mn_eq('Puck Line'), rn_hc('St. Louis Blues', 1.5), 'St. Louis Blues +1.5', 'NHL',
     'Blues +1.5 at Nashville (-290). Goal cushion in a true pick\'em.'),
    ('kings_nhl', mn_eq('Puck Line'), rn_hc('Pittsburgh Penguins', 1.5), 'Pittsburgh Penguins +1.5', 'NHL',
     'Penguins +1.5 at LA (-230). Goal cushion rather than a coin-flip Kings ML.'),
    ('magic', mn_eq('Alternate Spread'), rn_contains('Magic +11.5'), 'Orlando Magic +11.5', 'NBA',
     'Magic +5.5 main at Golden State; +11.5 (-255) adds 6 points of cushion.'),
    ('cavs', mn_eq('Alternate Spread'), rn_contains('Cavaliers +10.5'), 'Cleveland Cavaliers +10.5', 'NBA',
     'Cavs +4.5 main vs Knicks; +10.5 (-240) is a ≥+9.5 cushion at home.'),
    ('blazers', mn_eq('Alternate Spread'), rn_contains('Blazers +11.5'), 'Portland Trail Blazers +11.5', 'NBA',
     'Blazers +5.5 main vs Spurs; +11.5 (-260) buys past the ≥+9.5 floor.'),
    ('suns', mn_eq('Alternate Spread'), rn_contains('Suns +11.5'), 'Phoenix Suns +11.5', 'NBA',
     'Suns +6.5-ish main vs Houston; +11.5 (-225) cushion. Not a Rockets favorite lay.'),
    ('morehead', lambda mn: mn.startswith('Alternate Spread'), rn_hc('Morehead State', 41.5),
     'Morehead State +41.5', 'NCAAB',
     'Louisville -38.5 main (ML suspended). Morehead +41.5 (-170) is a high-prob dog cushion — no -20+ favorite alt.'),
    ('nmsu', lambda mn: mn.startswith('Alternate Spread'), rn_hc('New Mexico State', 32.5),
     'New Mexico State +32.5', 'NCAAB',
     'Gonzaga -29.5 main (ML suspended). NMSU +32.5 (-168) under the favorite -20 ban — dog cushion instead.'),
    ('purdue_fb', mn_eq('Alternate Spread'), rn_contains('Maryland (+9.5)'), 'Maryland +9.5', 'NCAAF',
     'Maryland +5.5 main at Purdue; +9.5 (-196) reaches the ≥+9.5 CFB dog cushion.'),
    ('okst_fb', mn_eq('Alternate Spread'), rn_contains('Kansas State (+11.5)'), 'Kansas State +11.5', 'NCAAF',
     'K-State +6.5 main vs Oklahoma State; +11.5 (-188) double-digit cushion.'),
    ('tulane', mn_eq('Alternate Spread'), rn_contains('Tulane (+10.5)'), 'Tulane +10.5', 'NCAAF',
     'Tulane +2.5 main vs Tulsa; +10.5 (-340) big home cushion after the mid-major ML lesson.'),
    ('ucla', mn_eq('Alternate Spread'), rn_contains('Minnesota (+10.5)'), 'Minnesota +10.5', 'NCAAF',
     'Minnesota +3.5 main vs UCLA; +10.5 (-290) ≥+9.5 dog cushion.'),
    ('bengals', mn_eq('Alternate Spread'), rn_contains('Bengals (-3.5)'), 'Cincinnati Bengals -3.5', 'NFL',
     'Bengals -3 main at Atlanta; -3.5 at +100. Plus-money bought-down favorite.'),
    ('eagles', mn_eq('Alternate Spread'), rn_contains('Eagles (+10.5)'), 'Philadelphia Eagles +10.5', 'NFL',
     'Eagles +3 main vs Giants; +10.5 (-360) double-digit home cushion.'),
    ('clemson', mn_eq('Alternate Spread'), rn_contains('Clemson (+1.5)'), 'Clemson +1.5', 'NCAAF',
     'Clemson -2.5 main at Syracuse; +1.5 alt (-142) is a soft cover if they win or lose by 1.'),
    ('ncsu_fb', mn_eq('Alternate Spread'), rn_contains('NC State (+10.5)'), 'NC State +10.5', 'NCAAF',
     'NC State +4.5 main vs Duke; +10.5 (-250) ≥+9.5 dog cushion.'),
    ('coastal', mn_eq('Alternate Spread'), rn_contains('Old Dominion (+11.5)'), 'Old Dominion +11.5', 'NCAAF',
     'ODU +6.5 main at Coastal; +11.5 (-188) double-digit cushion.'),
    ('uconn', mn_eq('Alternate Spread'), rn_contains('Connecticut (+11.5)'), 'Connecticut +11.5', 'NCAAF',
     'UConn +7.5 main vs UNC; +11.5 (-154) ≥+9.5 home cushion.'),
]

bs_legs = []
for spec in bs_specs:
    key, mp, rp, pick, sport, reason = spec
    try:
        leg = make_leg(key, mp, rp, pick, sport, reason)
        bs_legs.append(leg)
        print('BS OK', pick, leg['odds'])
    except SystemExit as e:
        print('BS skip', pick, e)

odds_bs, dec_bs = combine([l['odds'] for l in bs_legs]) if bs_legs else (0, 1.0)
payout_5 = round(5 * dec_bs, 2)
print(f'Best Shot: {len(bs_legs)} legs, odds {odds_bs}, $5 → ${payout_5}')

honesty = (
    f'~$5 → ${payout_5}'
    + ('. Short of the $5K target — would need coin-flip padding to stretch further.'
       if payout_5 < 5000 else
       ('. Inside the $5K–$50K target on $5.' if payout_5 <= 50000 else
        '. Above $50K on $5 — trimmed to highest-prob legs only; payout is a byproduct.'))
)

lottery = [{
    'name': 'Best Shot $500K',
    'odds': odds_bs,
    'stake': 5,
    'legs': bs_legs,
    'reason': (
        f'{len(bs_legs)} highest-prob unused legs: college -1800+ MLs, NHL +1.5 / Avs ML, NBA dog cushions ≥+10.5, '
        f'CFB/NFL bought-down cushions, campus dog cushions (no -20 fav alts). Win-prob first. '
        + honesty
    ),
}]

# Optional second lottery if we want sport-lottery — only if Best Shot is first and we have room
# Skip second lottery to avoid burning more high-prob legs; Best Shot is the focus.

def upsert_pending(entry):
    for i, h in enumerate(p['results']['history']):
        if h.get('name') == entry['name'] and h.get('date') == entry['date'] and h.get('run') == entry['run'] and h.get('result') == 'pending':
            p['results']['history'][i] = entry
            return
    p['results']['history'].append(entry)

for s in singles:
    upsert_pending({
        'date': '2026-11-07', 'run': '10:30 AM', 'type': 'single', 'name': s['pick'],
        'odds': s['odds'], 'stake': s.get('stake', 10), 'result': 'pending', 'profit': 0,
        'legs': [{'pick': s['pick'], 'odds': s['odds'], 'event': s['event'], 'result': 'pending', 'actual': 'plays Saturday/Sunday'}],
        'whyExplanation': 'Pending — Saturday 10:30 AM card.', 'lesson': ''
    })
for t in parlays:
    upsert_pending({
        'date': '2026-11-07', 'run': '10:30 AM', 'type': 'parlay', 'name': t['name'],
        'odds': t['odds'], 'stake': t.get('stake', 10), 'result': 'pending', 'profit': 0,
        'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'pending'} for l in t['legs']],
        'whyExplanation': 'Pending — Saturday 10:30 AM card.', 'lesson': ''
    })
for t in lottery:
    upsert_pending({
        'date': '2026-11-07', 'run': '10:30 AM', 'type': 'lottery', 'name': t['name'],
        'odds': t['odds'], 'stake': t.get('stake', 5), 'result': 'pending', 'profit': 0,
        'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'pending'} for l in t['legs']],
        'whyExplanation': 'Pending — Saturday 10:30 AM card.', 'lesson': ''
    })

# ---- write card ----
p['updated'] = 'Sat Nov 7, 2026 10:30 AM ET'
p['run'] = (
    '10:30 AM ET Saturday. Graded Fri: College Locks W (x2), Kings +15.5 W, Campus Cushions W; '
    'VT +4.5 L, Nevada +8.5 L, Home Ice L (CGY), Campus Alt Favorites 0-3 L, Best Shot AM L (NBA cushions). '
    'Lessons shaped card: college -1800+ MLs over campus alts; NHL +1.5 only with real cushion/avg+ clubs; '
    f'NBA dogs bought to +10.5–+14.5; no pending-event reuse. Best Shot {len(bs_legs)} legs ~${payout_5} on $5'
    + (' — short of $5K, no coin-flip pad.' if payout_5 < 5000 else '.')
)
p['singles'] = singles
p['parlays'] = parlays
p['lottery'] = lottery

totals = recompute_totals(p['results']['history'])
p['results']['totals'] = totals
p['results']['singles'] = copy.deepcopy(totals['singles'])
p['results']['parlays'] = copy.deepcopy(totals['parlays'])
p['results']['lottery'] = copy.deepcopy(totals['lottery'])
p['results']['updated'] = 'Sat Nov 7, 2026 10:30 AM ET'
p['results']['sources'] = (
    'FanDuel PA public odds; ESPN scoreboards (NBA/NHL/NCAAB/NCAAF 11/6); lessons.md '
    '(college ML locks, NHL home +1.5, no mid-major short favs, no -20 college alts, NBA ≥+9.5 cushions)'
)
p['results']['topLessons'] = [
    'College MLs at -1800+ are 34-0 on lock parlays — prefer those over any campus alt favorite.',
    'Campus alt favorites went 0-3 Friday (Purdue lost outright; UK/UAB failed mid spreads) — even under the -20 ban, early-season hosts are not automatic.',
    'NBA ≥+9.5 cushions still fail in true mismatches (CHA/MEM blowouts) — buy EXTRA points vs elite (used +12.5/+14.5 today).',
    'NHL home +1.5 missed on CGY (lost by 2); prefer average-or-better homes or take the +1.5 on the pick\'em dog instead of a coin-flip ML.',
    'Do not reuse eventIds from pending Fri PM / Sunday NFL tickets — morning burn is real.',
]

json.dump(p, open('/workspace/csb/picks.json', 'w'), indent=1)
print('Wrote picks.json')
print('TOTALS', json.dumps(totals['overall'], indent=2))
print('Card singles', [(s['pick'], s['odds']) for s in singles])
for t in parlays:
    print('Parlay', t['name'], t['odds'], [(l['pick'], l['odds']) for l in t['legs']])
print('BS', odds_bs, payout_5, [(l['pick'], l['odds']) for l in bs_legs])
