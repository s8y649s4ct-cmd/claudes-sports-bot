#!/usr/bin/env python3
"""Fri Nov 6, 2026 10:30 AM ET — grade pending + build morning card."""
import json, copy, datetime, urllib.request, os, re, glob
from datetime import timezone, timedelta

ET = timezone(timedelta(hours=-5))
K = 'FhMFpcPWXMeyZxOx'
UA = {'User-Agent': 'Mozilla/5.0'}
NOW = datetime.datetime.now(timezone.utc)

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
        if not o:
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
    # merge sport pages
    for pg in ['nba', 'nhl', 'ncaab', 'ncaaf', 'nfl']:
        path = f'/workspace/fd_{pg}.json'
        if not os.path.exists(path):
            continue
        try:
            d = json.load(open(path))
            for mid, m in ((d.get('attachments') or {}).get('markets') or {}).items():
                if str(m.get('eventId')) == str(eid):
                    mkts[mid] = m
            for eid2, e in ((d.get('attachments') or {}).get('events') or {}).items():
                if str(eid2) == str(eid) and isinstance(e, dict):
                    ev = e
        except Exception:
            pass
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

def payout_profit(odds, stake, won):
    if not won:
        return -stake
    if odds < 0:
        return round(stake * (100 / abs(odds)), 2)
    return round(stake * (odds / 100.0), 2)

# ---- load ----
p = json.load(open('/workspace/csb/picks.json'))
afternoon_singles = copy.deepcopy(p['singles'])
afternoon_parlays = copy.deepcopy(p['parlays'])
afternoon_lottery = copy.deepcopy(p['lottery'])

# ============================================================
# STEP 1 — grade pending legs in history + afternoon card
# ============================================================
stale = {
    # Nov 1 Best Shot leftover tennis/NCAAB
    ('Best Shot $500K', 'Basavareddy ML'): ('hit', 'Basavareddy def. Karol 6-3, 6-3 (Bratislava Challenger)'),
    ('Best Shot $500K', 'Shevchenko ML'): ('miss', 'Pavlovic def. Shevchenko 6-3, 4-6, 6-4'),
    ('Best Shot $500K', 'VCU ML'): ('hit', 'VCU 82, Little Rock 72'),
    # Nov 3 Ice & Pitch
    ('Ice & Pitch Cushion Ladder', 'Lyngby vs Randers Under 4.5'): ('hit', 'Lyngby 1-0 Randers (1 goal)'),
    # Nov 5 Europa leftovers
    ('Europa Class-Gap Favorites', 'Benfica ML'): ('hit', 'Benfica 3-1 Lech Poznan'),
    ('Europa Class-Gap Favorites', 'FC Copenhagen ML'): ('hit', 'Copenhagen 2-1 Iberia 1999'),
    ('Europa Class-Gap Favorites', 'Lugano ML'): ('hit', 'Lugano 3-0 Kauno Zalgiris'),
    # Nov 5 morning Best Shot pending
    ('Best Shot $500K', 'New York Rangers +1.5'): ('hit', 'Rangers 3, Flyers 2'),
    ('Best Shot $500K', 'New York Islanders +2.5'): ('hit', 'Hurricanes 5, Islanders 3 (lost by 2)'),
    ('Best Shot $500K', 'New Jersey Devils +1.5'): ('hit', 'Devils 5, Blues 4 (OT)'),
    ('Best Shot $500K', 'Detroit Red Wings +2.5'): ('hit', 'Golden Knights 2, Red Wings 1 (lost by 1)'),
    ('Best Shot $500K', 'Tampa Bay Lightning +1.5'): ('hit', 'Lightning 4, Blackhawks 1'),
    ('Best Shot $500K', 'Winnipeg Jets +1.5'): ('hit', 'Jets 6, Canucks 2'),
    ('Best Shot $500K', 'Magic @ Suns Over 205.5'): ('hit', 'Magic 104, Suns 117 (221)'),
    ('Best Shot $500K', 'UTSA +3.5'): ('miss', 'FAU 60, UTSA 29 (lost by 31)'),
    ('Best Shot $500K', 'James Madison +1.5'): ('hit', 'JMU 54, Southern Miss 23'),
    ('Best Shot $500K', 'Panathinaikos or Draw'): ('hit', 'Panathinaikos 2-1 CSKA Sofia'),
    ('Best Shot $500K', 'Leverkusen or Draw'): ('miss', 'Leverkusen 0-1 Marseille'),
    ('Best Shot $500K', 'Universitatea Craiova or Draw'): ('hit', 'CSU Craiova 2-0 Egnatia'),
    ('Best Shot $500K', 'Sunderland or Draw'): ('miss', 'Sunderland 0-2 Dinamo Zagreb'),
    ('Best Shot $500K', 'Monaco or Draw'): ('hit', 'Monaco 2-0 Nordsjaelland'),
    ('Best Shot $500K', 'Brighton or Draw'): ('hit', 'Brighton 1-0 Getafe'),
    ('Best Shot $500K', 'Sint Truiden vs Brann Over 1.5 Goals'): ('hit', 'Sint-Truiden 1-1 Brann (2 goals)'),
    ('Best Shot $500K', 'Celtic vs Besiktas Over 1.5 Goals'): ('hit', 'Celtic 3-2 Besiktas'),
}

# morning tickets by exact name+date for singles/parlays that need full grade
morning_grades = {
    'Jaguars @ Ravens Under 38.5': {
        'result': 'lost', 'profit': -10,
        'legs': [('Jaguars @ Ravens Under 38.5', 'miss', 'Jaguars 33, Ravens 10 (43 total)')],
        'why': 'LOST. JAX 33 BAL 10 — 43 total cleared 38.5. Backup QB game still went over as Jacksonville scored freely.',
        'lesson': 'TNF unders with a backup QB need more than a soft total if the other offense is healthy and motivated.',
    },
    'Joe Fagnano Under 0.5 Passing TDs': {
        'result': 'won', 'profit': 9.8,  # -102 on $10 ≈ 9.80
        'legs': [('Joe Fagnano Under 0.5 Passing TDs', 'hit', 'Fagnano 0 passing TDs (10/18, 60 yds, 2 INT)')],
        'why': 'WON. Joe Fagnano threw 0 TD passes (10/18, 60 yards, 2 INT) in Baltimore\'s 33-10 loss.',
        'lesson': 'Backup QB under 0.5 pass TD held when the offense was overmatched. Keep for true backups in bad matchups.',
    },
    'Home Ice +1.5 Trio': {
        'result': 'lost', 'profit': -10,
        'legs': [
            ('Pittsburgh Penguins +1.5', 'miss', 'Bruins 6, Penguins 2 (lost by 4)'),
            ('Montreal Canadiens +1.5', 'hit', 'Canadiens 5, Mammoth 4 (OT)'),
            ('Columbus Blue Jackets +1.5', 'hit', 'Blue Jackets 2, Stars 1 (SO)'),
        ],
        'why': 'LOST. Penguins got blown out 6-2 by Boston; Canadiens and Blue Jackets both covered +1.5.',
        'lesson': 'NHL home +1.5 remains strong (2/3 here) but a true mismatch/home team in freefall (PIT) can still get run. Prefer +1.5 when the home side is at least average.',
    },
    'Prime-Time Cushions': {
        'result': 'won', 'profit': 10.8,
        'legs': [
            ('Jacksonville Jaguars -2.5', 'hit', 'Jaguars 33, Ravens 10 (won by 23)'),
            ('Golden State Warriors +4.5', 'hit', 'Warriors 120, Heat 100'),
            ('Colorado Avalanche +1.5', 'hit', 'Predators 3, Avalanche 2 (OT) — covered +1.5'),
            ('Edmonton Oilers +1.5', 'hit', 'Ducks 5, Oilers 4 — covered +1.5'),
        ],
        'why': 'WON at +108. All four cushions hit: JAX -2.5 by 23, GS +4.5 win, COL +1.5 and EDM +1.5 each lost by 1.',
        'lesson': 'Mixed-sport cushion parlays with real points (NFL -2.5 mismatch, NBA +4.5, NHL +1.5) paid. NHL +1.5 home/road cushions continue to cash.',
    },
    'College Locks Ladder': {
        'result': 'won', 'profit': 2.11,  # -473 on $10
        'legs': [
            ('Vanderbilt ML', 'hit', 'Vanderbilt 74, Wake Forest 51'),
            ('Seton Hall ML', 'hit', 'Seton Hall 67, LIU 60'),
            ('Virginia Tech ML', 'hit', 'Virginia Tech 96, Mercer 67'),
            ('Notre Dame ML', 'hit', 'Notre Dame 83, Mercyhurst 56'),
            ('Cincinnati ML', 'hit', 'Cincinnati 81, Green Bay 64'),
            ('Syracuse ML', 'hit', 'Syracuse 102, Central Connecticut 49'),
            ('Pittsburgh ML', 'hit', 'Pittsburgh 80, Buffalo 61'),
            ('Fordham ML', 'hit', 'Fordham 83, Stonehill 63'),
            ('Mississippi State ML', 'hit', 'Mississippi State 82, Northwestern State 44'),
            ('Loyola Chicago ML', 'hit', 'Loyola Chicago 76, West Georgia 53'),
            ('SMU ML', 'hit', 'SMU 95, VMI 70'),
        ],
        'why': 'WON at -473. All 11 college moneylines at -3500 or longer hit. Seton Hall was the closest (67-60).',
        'lesson': 'College MLs at -1800 or longer are now 27-0 when followed. Keep as the Best Shot / ladder backbone.',
    },
}

for h in p['results']['history']:
    # stale pending cleanup
    for leg in h.get('legs') or []:
        if leg.get('result') != 'pending':
            continue
        key = (h.get('name'), leg.get('pick'))
        if key in stale:
            leg['result'], leg['actual'] = stale[key]
    # full morning ticket grades
    if h.get('date') == '2026-11-05' and h.get('run') == '10:30 AM' and h.get('name') in morning_grades:
        g = morning_grades[h['name']]
        if h.get('result') == 'pending':
            h['result'] = g['result']
            h['profit'] = g['profit']
            h['whyExplanation'] = g['why']
            h['lesson'] = g['lesson']
            by_pick = {x[0]: (x[1], x[2]) for x in g['legs']}
            for leg in h.get('legs') or []:
                if leg.get('pick') in by_pick:
                    leg['result'], leg['actual'] = by_pick[leg['pick']]

# Fix Fagnano profit precisely: odds -102, stake 10 → profit = 10*100/102 ≈ 9.80
for h in p['results']['history']:
    if h.get('name') == 'Joe Fagnano Under 0.5 Passing TDs' and h.get('result') == 'won':
        h['profit'] = round(10 * 100 / 102, 2)
    if h.get('name') == 'College Locks Ladder' and h.get('result') == 'won':
        h['profit'] = round(10 * 100 / 473, 2)
    if h.get('name') == 'Prime-Time Cushions' and h.get('result') == 'won':
        h['profit'] = round(10 * 108 / 100, 2)

# ---- grade afternoon card into history ----
# Afternoon tickets already may not be in history — add them
def already_in_history(name, date, run):
    for h in p['results']['history']:
        if h.get('name') == name and h.get('date') == date and h.get('run') == run:
            return True
    return False

# Singles (Sunday NFL) — pending
for s in afternoon_singles:
    if already_in_history(s['pick'], '2026-11-05', '3:00 PM'):
        continue
    p['results']['history'].append({
        'date': '2026-11-05', 'run': '3:00 PM', 'type': 'single', 'name': s['pick'],
        'odds': s['odds'], 'stake': s.get('stake', 10), 'result': 'pending', 'profit': 0,
        'legs': [{'pick': s['pick'], 'odds': s['odds'], 'event': s['event'], 'result': 'pending', 'actual': 'plays Sunday'}],
        'whyExplanation': 'Pending — Sunday NFL.', 'lesson': ''
    })

# Campus Moneyline Trio — LOST (Tulane)
if not already_in_history('Campus Moneyline Trio', '2026-11-05', '3:00 PM'):
    p['results']['history'].append({
        'date': '2026-11-05', 'run': '3:00 PM', 'type': 'parlay', 'name': 'Campus Moneyline Trio',
        'odds': -398, 'stake': 10, 'result': 'lost', 'profit': -10,
        'legs': [
            {'pick': 'Tulsa ML', 'odds': -1450, 'event': 'Northern Illinois @ Tulsa', 'result': 'hit', 'actual': 'Tulsa 94, Northern Illinois 75'},
            {'pick': 'Tulane ML', 'odds': -950, 'event': 'Jackson State @ Tulane', 'result': 'miss', 'actual': 'Jackson State 87, Tulane 85'},
            {'pick': 'Oregon ML', 'odds': -1700, 'event': 'Eastern Washington @ Oregon', 'result': 'pending', 'actual': 'plays Friday'},
        ],
        'whyExplanation': 'LOST. Tulane fell 87-85 at home to Jackson State. Tulsa won 94-75; Oregon still plays Friday.',
        'lesson': 'Even -950 college home favorites can lose opening-week games to mid-majors. Prefer -1800+ only, and be wary of G5 hosts vs motivated SWAC/MEAC visitors.'
    })

# Sunday Cushions + Utah — Utah hit, NFL pending
if not already_in_history('Sunday Cushions + Utah', '2026-11-05', '3:00 PM'):
    p['results']['history'].append({
        'date': '2026-11-05', 'run': '3:00 PM', 'type': 'parlay', 'name': 'Sunday Cushions + Utah',
        'odds': 204, 'stake': 10, 'result': 'pending', 'profit': 0,
        'legs': [
            {'pick': 'Arizona Cardinals +7.5', 'odds': 102, 'event': 'Arizona Cardinals @ Seattle Seahawks', 'result': 'pending', 'actual': 'plays Sunday'},
            {'pick': 'Detroit Lions +1.5', 'odds': -430, 'event': 'Detroit Lions @ Miami Dolphins', 'result': 'pending', 'actual': 'plays Sunday'},
            {'pick': 'Utah +1.5', 'odds': -450, 'event': 'Towson @ Utah', 'result': 'hit', 'actual': 'Utah 67, Towson 57'},
        ],
        'whyExplanation': 'Pending — Utah hit (67-57); Cardinals and Lions play Sunday.', 'lesson': ''
    })

# Friday College Locks — all Friday pending
if not already_in_history('Friday College Locks', '2026-11-05', '3:00 PM'):
    p['results']['history'].append({
        'date': '2026-11-05', 'run': '3:00 PM', 'type': 'parlay', 'name': 'Friday College Locks',
        'odds': -2821, 'stake': 10, 'result': 'pending', 'profit': 0,
        'legs': [
            {'pick': 'Alabama ML', 'odds': -20000, 'event': 'Arkansas State @ Alabama', 'result': 'pending', 'actual': 'plays Friday'},
            {'pick': 'North Carolina ML', 'odds': -10000, 'event': 'Wofford @ North Carolina', 'result': 'pending', 'actual': 'plays Friday'},
            {'pick': 'Ohio State ML', 'odds': -10000, 'event': 'Youngstown St @ Ohio State', 'result': 'pending', 'actual': 'plays Friday'},
            {'pick': 'Kentucky ML', 'odds': -10000, 'event': 'James Madison @ Kentucky', 'result': 'pending', 'actual': 'plays Friday'},
        ],
        'whyExplanation': 'Pending — all four play Friday night.', 'lesson': ''
    })

# Afternoon Best Shot — LOST on Thu legs
bs_thu = {
    'Penn State -5.5': ('miss', 'Penn State 97, Chattanooga 93 (won by 4)'),
    'Charlotte -5.5': ('hit', 'Charlotte 77, Georgia State 67 (won by 10)'),
    'Michigan State -17.5': ('hit', 'Michigan State 91, Toledo 61 (won by 30)'),
    'North Texas +8.5': ('hit', 'North Texas 77, McNeese 67'),
    'Merrimack -3.5': ('miss', 'UMass Lowell 71, Merrimack 61'),
    'Iona -3.5': ('hit', 'Iona 72, NJIT 49'),
    'DePaul -0.5': ('hit', 'DePaul 82, South Florida 80'),
    'Incarnate Word -2.5': ('miss', 'Chicago State 66, Incarnate Word 54'),
    'South Alabama +3.5': ('hit', 'South Alabama 83, Jacksonville State 80 (2OT)'),
    'Marist +4.5': ('hit', 'Marist 88, UMBC 80'),
    'Quinnipiac ML': ('hit', 'Quinnipiac 66, Bryant 56'),
    "Saint Peter's ML": ('miss', "Binghamton 58, Saint Peter's 55"),
    'Purdue ML': ('pending', 'plays Friday'),
    'Florida State ML': ('pending', 'plays Friday'),
    'Xavier ML': ('pending', 'plays Friday'),
    'NC State ML': ('pending', 'plays Friday'),
    'Georgia Tech ML': ('pending', 'plays Friday'),
    'Wisconsin ML': ('pending', 'plays Friday'),
    'Tage Thompson 2+ Shots on Goal': ('pending', 'plays Friday'),
    'Leo Carlsson 1+ Shots on Goal': ('pending', 'plays Friday'),
}
if not already_in_history('Best Shot $500K', '2026-11-05', '3:00 PM'):
    legs = []
    for leg in afternoon_lottery[0]['legs']:
        res, act = bs_thu.get(leg['pick'], ('pending', 'unknown'))
        legs.append({'pick': leg['pick'], 'odds': leg['odds'], 'event': leg['event'], 'result': res, 'actual': act})
    hits = sum(1 for l in legs if l['result'] == 'hit')
    misses = sum(1 for l in legs if l['result'] == 'miss')
    p['results']['history'].append({
        'date': '2026-11-05', 'run': '3:00 PM', 'type': 'lottery', 'name': 'Best Shot $500K',
        'odds': afternoon_lottery[0]['odds'], 'stake': 5, 'result': 'lost', 'profit': -5,
        'legs': legs,
        'whyExplanation': f'LOST. Thursday NCAAB killed it: Penn State -5.5 won by only 4, Merrimack lost outright, Incarnate Word lost outright, Saint Peter\'s lost at home. Settled {hits} hit / {misses} miss; Friday legs moot.',
        'lesson': 'Small-school / mid-major alt spreads and short home MLs (Merrimack -3.5, IW -2.5, Saint Peter\'s ML, PSU -5.5) are not 75% legs. Stick to Power-conference -1800+ MLs and big cushions only.'
    })

# Update morning Best Shot why with more settled legs (ticket already lost)
for h in p['results']['history']:
    if h.get('date') == '2026-11-05' and h.get('run') == '10:30 AM' and h.get('name') == 'Best Shot $500K':
        hits = sum(1 for l in h['legs'] if l.get('result') == 'hit')
        misses = sum(1 for l in h['legs'] if l.get('result') == 'miss')
        h['whyExplanation'] = (
            f'LOST. Dead early on AC Milan or Draw and Hajduk Split or Draw. Final settled soccer/NHL/NBA/NCAAF: '
            f'{hits} hit / {misses} miss. Late misses also included Leverkusen or Draw (0-1 Marseille), '
            f'Sunderland or Draw (0-2 Dinamo Zagreb), and UTSA +3.5 (lost by 31).'
        )

# ============================================================
# STEP 2/3 — build Friday 10:30 AM card
# ============================================================
EIDS = {
    'kings': 36279170, 'hornets': 36279168, 'wizards': 36279175, 'bucks': 36279176,
    'buf': 36260073, 'cgy': 36260074, 'min': 36260085,
    'oregon': 36285142, 'osu': 36285153, 'purdue': 36285183, 'unc': 36285174,
    'fsu': 36285203, 'ncsu': 36285236, 'uk': 36285241, 'gt': 36285243,
    'xavier': 36285273, 'clemson': 36285628, 'uga': 36285789, 'rutgers': 36287449,
    'bama': 36285288, 'wisc': 36285309, 'uab': 36285793, 'tcu_bb': 36287413,
    'olemiss': 36285127, 'csu': 36285100, 'asu': 36285119, 'okst': 36285809,
    'orst': 36285084, 'uva': 36285126, 'stanford': 36285062, 'minn': 36285148,
    'spurs': 36279170,  # same as kings event
    'vt': 36244602, 'nevada': 36260456, 'arizona_fb': 36260458,
}

cache = {}
for key, eid in EIDS.items():
    tabs = ('', 'popular', 'alternates')
    if key in ('buf', 'cgy', 'min'):
        tabs = ('', 'popular', 'alternates', 'shots')
    cache[key] = load_event(eid, tabs)
    if not cache[key][0]:
        print('WARN missing event', key, eid)

used_events, used_picks = set(), set()

def make_leg(key, market_pred, runner_pred, pick, sport, reason):
    ev, mkts = cache[key]
    sel = find_runner(mkts, market_pred, runner_pred)
    if not sel:
        # debug
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
        raise SystemExit(f'no sel for {pick} key={key} opts={opts[:20]}')
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
    if t > NOW + timedelta(hours=12):
        print(f'WARN start >12h {pick} {ev["openDate"]}')
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

def rn_eq(name):
    return lambda r, m: r.get('runnerName') == name

def rn_contains(substr):
    return lambda r, m: substr in (r.get('runnerName') or '')

def rn_hc(name, hc):
    return lambda r, m: r.get('runnerName') == name and r.get('handicap') == hc

def mn_eq(name):
    return lambda mn: mn == name

def mn_in(*names):
    return lambda mn: mn in names

# ---- SINGLES ----
singles = []
s1 = make_leg(
    'kings', mn_eq('Alternate Spread'), rn_eq('Sacramento Kings +15.5'),
    'Sacramento Kings +15.5', 'NBA',
    'Kings missing Murray/Simmons/Raynaud but +15.5 is near-main cushion at plus money vs Spurs. Lessons want ≥+9.5; this is +15.5 at +102.',
)
singles.append({**s1, 'stake': 10})
s2 = make_leg(
    'vt', mn_eq('Alternate Spread'), rn_contains('Virginia Tech (+4.5)'),
    'Virginia Tech +4.5', 'NCAAF',
    'VT gets 4.5 on the road at SMU at plus money. Main is +6.5; buying down 2 keeps a real cushion without juice.',
)
singles.append({**s2, 'stake': 10})
s3 = make_leg(
    'nevada', mn_eq('Alternate Spread'), rn_contains('Nevada (+8.5)'),
    'Nevada +8.5', 'NCAAF',
    'Nevada home vs New Mexico with +8.5 at even money. Main is +10.5; one-score-plus cushion at +100.',
)
singles.append({**s3, 'stake': 10})

# ---- helper: best college favorite alt spread near target odds ----
def best_fav_alt(key, team, target=-320, lo=-550, hi=-200):
    """Pick favorite alt spread closest to target odds in [lo, hi]."""
    ev, mkts = cache[key]
    cands = []
    for mid, m in mkts.items():
        if m.get('marketStatus') != 'OPEN' or m.get('inPlay'):
            continue
        if m.get('sgmMarket') is False:
            continue
        if m.get('canTurnInPlay') is False:
            continue
        mn = m.get('marketName', '')
        if not (mn == 'Spread' or mn.startswith('Alternate Spread')):
            continue
        for r in m.get('runners') or []:
            if r.get('runnerStatus') != 'ACTIVE':
                continue
            if r.get('runnerName') != team:
                continue
            hc = r.get('handicap')
            o = am_odds(r)
            if o is None or hc is None:
                continue
            o = int(o)
            if hc >= 0:
                continue  # need favorite laying points
            if not (lo <= o <= hi):
                continue
            # ban college alt spreads of -20 or more (lessons)
            if hc <= -20:
                continue
            cands.append((abs(o - target), o, hc, mid, str(r['selectionId']), mn))
    if not cands:
        return None
    cands.sort()
    _, o, hc, mid, sid, mn = cands[0]
    return {
        'marketId': mid, 'selectionId': sid, 'odds': o, 'market': mn,
        'runnerName': team, 'handicap': hc, 'eventId': int(cache[key][1][mid]['eventId']) if mid in cache[key][1] else int(list(cache[key][1].values())[0]['eventId']),
        'pick': f'{team} {hc}', 'hc': hc,
    }

def commit_sel(key, sel, pick, sport, reason):
    ev, mkts = cache[key]
    # fix eventId from markets
    mid = sel['marketId']
    m = mkts.get(mid) or next(m for m in mkts.values() if m.get('marketId') == mid or str(m.get('marketId')) == str(mid))
    eid = int(m['eventId'])
    if str(eid) in used_events:
        raise SystemExit(f'event reuse {eid} for {pick}')
    if pick in used_picks:
        raise SystemExit(f'pick reuse {pick}')
    used_events.add(str(eid))
    used_picks.add(pick)
    t = datetime.datetime.fromisoformat(ev['openDate'].replace('Z', '+00:00'))
    if t < NOW + timedelta(hours=1):
        raise SystemExit(f'start too soon {pick}')
    return {
        'pick': pick, 'market': sel['market'], 'odds': sel['odds'], 'sport': sport,
        'event': ev['name'], 'start': start_et(ev['openDate']), 'reason': reason,
        'marketId': sel['marketId'], 'selectionId': sel['selectionId'], 'eventId': eid,
    }

# ---- PARLAYS ----
parlays = []

l_buf = make_leg('buf', mn_eq('Alternate Puck Line'), rn_eq('Buffalo Sabres +1.5'), 'Buffalo Sabres +1.5', 'NHL',
    'NHL home +1.5 backbone. Sabres are favorites; +1.5 is a heavy home cushion.')
l_min = make_leg('min', mn_eq('Alternate Puck Line'), rn_eq('Minnesota Wild +1.5'), 'Minnesota Wild +1.5', 'NHL',
    'Wild home vs Sharks; +1.5 home ice continues the lesson.')
l_cgy = make_leg('cgy', mn_eq('Alternate Puck Line'), rn_eq('Calgary Flames +1.5'), 'Calgary Flames +1.5', 'NHL',
    'Flames home vs Ducks; +1.5 home cushion.')
odds, _ = combine([l_buf['odds'], l_min['odds'], l_cgy['odds']])
parlays.append({
    'name': 'Home Ice +1.5 Trio', 'odds': odds, 'stake': 10,
    'legs': [l_buf, l_min, l_cgy],
    'reason': 'NHL home +1.5 is our strongest recurring angle. All three Friday home sides get +1.5.',
})

# College alt-spread ladder (bought down, not -20+) for meaningful payout
college_alt_parlay_keys = [
    ('uk', 'Kentucky'), ('purdue', 'Purdue'), ('fsu', 'Florida State'),
]
college_legs = []
for key, team in college_alt_parlay_keys:
    sel = best_fav_alt(key, team, target=-300, lo=-500, hi=-200)
    if not sel:
        # fall back to ML if -1800+
        leg = make_leg(key, mn_eq('Moneyline'), rn_eq(team), f'{team} ML', 'NCAAB',
            f'{team} home ML at -1800+ only.')
        college_legs.append(leg)
        continue
    pick = f'{team} {sel["hc"]}'
    leg = commit_sel(key, sel, pick, 'NCAAB',
        f'{team} bought down from a huge main spread to {sel["hc"]} (no -20+ alts). High-prob cover around {sel["odds"]}.')
    college_legs.append(leg)
odds, _ = combine([l['odds'] for l in college_legs])
parlays.append({
    'name': 'Campus Alt Favorites', 'odds': odds, 'stake': 10,
    'legs': college_legs,
    'reason': 'Three Power hosts bought down below the main number (and under the -20 alt ban) instead of a -4000 chalk ML parlay.',
})

l_hor = make_leg('hornets', mn_eq('Alternate Spread'), rn_eq('Charlotte Hornets +9.5'), 'Charlotte Hornets +9.5', 'NBA',
    'Hornets +9.5 (≥+9.5 cushion) vs Celtics.')
l_buck = make_leg('bucks', mn_eq('Alternate Spread'), rn_eq('Milwaukee Bucks +9.5'), 'Milwaukee Bucks +9.5', 'NBA',
    'Bucks +9.5 at home vs Raptors missing Kawhi.')
l_wiz = make_leg('wizards', mn_eq('Alternate Spread'), rn_eq('Washington Wizards +9.5'), 'Washington Wizards +9.5', 'NBA',
    'Wizards +9.5 on the road at Atlanta.')
odds, _ = combine([l_hor['odds'], l_buck['odds'], l_wiz['odds']])
parlays.append({
    'name': 'NBA +9.5 Cushions', 'odds': odds, 'stake': 10,
    'legs': [l_hor, l_buck, l_wiz],
    'reason': 'Three NBA dog cushions at +9.5 — the minimum that held up when we stuck to it.',
})

# ---- BEST SHOT ----
# Prefer alt spreads ~-250 to -450 (moves payout); fall back to -1800+ MLs when no alts.
bs_candidates = [
    ('osu', 'Ohio State'), ('bama', 'Alabama'), ('wisc', 'Wisconsin'),
    ('xavier', 'Xavier'), ('uga', 'Georgia'), ('rutgers', 'Rutgers'),
    ('unc', 'North Carolina'), ('gt', 'Georgia Tech'), ('ncsu', 'NC State'),
    ('clemson', 'Clemson'), ('oregon', 'Oregon'), ('tcu_bb', 'TCU'),
    ('olemiss', 'Ole Miss'), ('asu', 'Arizona State'), ('okst', 'Oklahoma State'),
    ('orst', 'Oregon State'), ('csu', 'Colorado State'), ('uab', 'UAB'),
    ('uva', 'Virginia'), ('olemiss2', None),  # placeholder removed below
]
# add more events that may have alts only
extra = [
    ('stanford', 'Stanford'), ('minn', 'Minnesota'),
]
# Ensure extras in cache / EIDS - stanford and minn already in EIDS

bs_legs = []
for key, team in [
    ('osu', 'Ohio State'), ('bama', 'Alabama'), ('wisc', 'Wisconsin'),
    ('xavier', 'Xavier'), ('uga', 'Georgia'), ('rutgers', 'Rutgers'),
    ('unc', 'North Carolina'), ('gt', 'Georgia Tech'), ('ncsu', 'NC State'),
    ('clemson', 'Clemson'), ('oregon', 'Oregon'), ('tcu_bb', 'TCU'),
    ('olemiss', 'Ole Miss'), ('asu', 'Arizona State'), ('okst', 'Oklahoma State'),
    ('orst', 'Oregon State'), ('csu', 'Colorado State'), ('uab', 'UAB'),
    ('uva', 'Virginia'), ('stanford', 'Stanford'), ('minn', 'Minnesota'),
]:
    if key not in cache or not cache[key][0]:
        print('no cache', key); continue
    if str(cache[key][0].get('eventId', EIDS[key])) in used_events or str(EIDS[key]) in used_events:
        # check properly
        pass
    eid = str(EIDS[key])
    if eid in used_events:
        print('event used', key); continue
    sel = best_fav_alt(key, team, target=-300, lo=-550, hi=-200)
    if sel:
        pick = f'{team} {sel["hc"]}'
        try:
            leg = commit_sel(key, sel, pick, 'NCAAB',
                f'{team} alt spread {sel["hc"]} bought under the main number; ~75%+ cover aim at {sel["odds"]}. No -20+ alts.')
            bs_legs.append(leg)
            continue
        except SystemExit as e:
            print('commit fail', e); continue
    # ML fallback only at -1800 or longer
    try:
        leg = make_leg(key, mn_eq('Moneyline'), rn_eq(team), f'{team} ML', 'NCAAB',
            f'{team} heavy ML (-1800+ only) when alt board thin.')
        if leg['odds'] > -1800:
            used_events.discard(str(leg['eventId']))
            used_picks.discard(leg['pick'])
            print('skip ML short', team, leg['odds'])
            continue
        bs_legs.append(leg)
    except SystemExit as e:
        print('skip', team, e)

# NCAAF cushion
if str(EIDS['arizona_fb']) not in used_events:
    try:
        leg = make_leg('arizona_fb', mn_eq('Alternate Spread'), rn_contains('TCU (+9.5)'), 'TCU +9.5', 'NCAAF',
            'TCU road at Arizona with +9.5 cushion.')
        bs_legs.append(leg)
    except SystemExit as e:
        print('skip TCU fb', e)

# Add Baylor/Kansas/etc if we load them — extend EIDS on the fly
for eid, team, key in [
    (36285542, 'Baylor', 'baylor'),
    (36285088, 'Kansas', 'kansas'),
    (36285117, 'BYU', 'byu'),
    (36285804, 'Miami', 'miami'),
    (36287402, 'Oklahoma', 'oklahoma'),
    (36287414, 'LSU', 'lsu'),
    (36285121, 'Iowa', 'iowa'),
    (36285788, 'Villanova', 'villanova'),
    (36285790, 'West Virginia', 'wvu'),
    (36285161, 'Texas A&M', 'tamu'),
]:
    if len(bs_legs) >= 25:
        break
    if str(eid) in used_events:
        continue
    EIDS[key] = eid
    cache[key] = load_event(eid, ('', 'popular', 'alternates'))
    if not cache[key][0]:
        continue
    sel = best_fav_alt(key, team, target=-300, lo=-550, hi=-200)
    if sel:
        pick = f'{team} {sel["hc"]}'
        try:
            leg = commit_sel(key, sel, pick, 'NCAAB',
                f'{team} alt {sel["hc"]} bought under main; high-prob cover, no -20+ ban breach.')
            bs_legs.append(leg)
        except SystemExit as e:
            print('skip extra', e)
            continue
    else:
        try:
            leg = make_leg(key, mn_eq('Moneyline'), rn_eq(team), f'{team} ML', 'NCAAB',
                f'{team} ML -1800+ fallback.')
            if leg['odds'] > -1800:
                used_events.discard(str(leg['eventId']))
                used_picks.discard(leg['pick'])
                continue
            bs_legs.append(leg)
        except SystemExit:
            continue

# Cap at 25
bs_legs = bs_legs[:25]
odds_bs, dec_bs = combine([l['odds'] for l in bs_legs]) if bs_legs else (0, 1)
payout_5 = round(5 * dec_bs, 2)
print(f'Best Shot: {len(bs_legs)} legs, odds {odds_bs}, $5 payout ~${payout_5}')

lottery = [{
    'name': 'Best Shot $500K',
    'odds': odds_bs,
    'stake': 5,
    'legs': bs_legs,
    'reason': (
        f'{len(bs_legs)} highest-prob legs — mostly college favorites bought down to ~-250/-500 alts '
        f'(no -20+ spreads), plus any -1800+ MLs where the alt board is thin, plus one NCAAF cushion. '
        f'~$5 → ${payout_5}'
        + ('. Short of the $5K target after skipping coin-flips and reusing no events from safer tickets.'
           if payout_5 < 5000 else ' (inside $5K–$50K target).')
    ),
}]

# ---- write card ----
p['updated'] = 'Fri Nov 6, 2026 10:30 AM ET'
p['run'] = (
    '10:30 AM ET run (Friday). Graded Thu night: Fagnano U0.5 TD W, Prime-Time Cushions W (+108), '
    'College Locks Ladder W (11/11), JAX/BAL Under L, Home Ice Trio L (PIT blown out), Campus Moneyline Trio L (Tulane), '
    'afternoon Best Shot L (PSU -5.5 / Merrimack / IW / Saint Peter\'s). Cleaned morning Best Shot leftovers '
    '(Leverkusen/Sunderland/UTSA misses; most NHL/soccer hit). Today: NHL home +1.5 trio; campus alt favorites; '
    'NBA +9.5 cushions; plus-money Kings/VT/Nevada singles; Best Shot built from bought-down college alts '
    '(win-prob first, no coin-flip pad). Lessons: college ML -1800+ now 27-0; no mid-major short favs; '
    'NBA cushions ≥+9.5; NHL home +1.5 backbone; no -20 college alts; no event reuse.'
)
p['singles'] = singles
p['parlays'] = parlays
p['lottery'] = lottery

totals = recompute_totals(p['results']['history'])
p['results']['totals'] = totals
p['results']['singles'] = copy.deepcopy(totals['singles'])
p['results']['parlays'] = copy.deepcopy(totals['parlays'])
p['results']['lottery'] = copy.deepcopy(totals['lottery'])
p['results']['updated'] = 'Fri Nov 6, 2026 10:30 AM ET'
p['results']['sources'] = (
    'ESPN scoreboards/box scores (NFL TNF, NHL, NBA, NCAAB, UEFA Europa/Conference); '
    'BenchScout/VCU Athletics/tennis.com/Danish press for leftover Nov 1–3 legs; FanDuel PA public odds feed'
)
p['results']['topLessons'] = [
    'College MLs at -1800 or longer are now 27-0 (11/11 Thursday) — keep as ladder/Best Shot core when alts are thin.',
    'NHL home +1.5 stays elite but failed when PIT was blown out 6-2; prefer average-or-better home clubs.',
    'Mid-major short favorites and tiny alt spreads (Merrimack -3.5, IW -2.5, Saint Peter\'s ML, Tulane -950) are not 75% legs.',
    'Away European or Draw failed again (Leverkusen, Sunderland); prefer home DC / team-to-score.',
    'Buy college favorites down to ~-10.5/-16.5 alts (never -20+) to keep ~75% covers and real Best Shot payout.',
]

json.dump(p, open('/workspace/csb/picks.json', 'w'), indent=1)
print('Wrote picks.json')
print('TOTALS', json.dumps(totals['overall'], indent=2))
print('Card singles', [(s['pick'], s['odds']) for s in singles])
for t in parlays:
    print('Parlay', t['name'], t['odds'], [(l['pick'], l['odds']) for l in t['legs']])
print('BS', odds_bs, payout_5, [(l['pick'], l['odds']) for l in bs_legs])
