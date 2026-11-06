#!/usr/bin/env python3
"""Fri Nov 6, 2026 3:00 PM ET — grade pending + build afternoon card.

Morning burned all Fri NBA/NHL and most Power NCAAB MLs. Afternoon uses:
- unused Fri NCAAB (WVU/TAMU bought-down alts, Minnesota/Stanford/etc.)
- Sat NHL home +1.5
- Sat CFB bought-down favorites
- Sun NFL plus-money / cushion legs
"""
import json, copy, datetime, urllib.request, os, re
from datetime import timezone, timedelta

ET = timezone(timedelta(hours=-5))
K = 'FhMFpcPWXMeyZxOx'
UA = {'User-Agent': 'Mozilla/5.0'}
NOW = datetime.datetime.now(timezone.utc)
MORNING_USED = {
    36244602, 36260073, 36260074, 36260085, 36260455, 36260456, 36260458,
    36279168, 36279169, 36279170, 36279171, 36279172, 36279173, 36279174,
    36279175, 36279176, 36285084, 36285100, 36285119, 36285127, 36285142,
    36285153, 36285174, 36285183, 36285203, 36285236, 36285241, 36285243,
    36285273, 36285288, 36285309, 36285628, 36285789, 36285793, 36285809,
    36287413, 36287449,
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

# ---- load ----
p = json.load(open('/workspace/csb/picks.json'))
morning_singles = copy.deepcopy(p['singles'])
morning_parlays = copy.deepcopy(p['parlays'])
morning_lottery = copy.deepcopy(p['lottery'])

# ============================================================
# STEP 1 — pending grades (Fri games not started; Sunday NFL stays pending)
# Europa Benfica/Copenhagen/Lugano already hit in morning build.
# ============================================================
# Nothing new to settle for Friday afternoon — all Fri games pending, Sunday NFL pending.
# Just ensure morning tickets are appended to history as pending.

def already_in_history(name, date, run):
    for h in p['results']['history']:
        if h.get('name') == name and h.get('date') == date and h.get('run') == run:
            return True
    return False

# Append morning (10:30 AM) tickets as pending if missing
for s in morning_singles:
    if already_in_history(s['pick'], '2026-11-06', '10:30 AM'):
        continue
    p['results']['history'].append({
        'date': '2026-11-06', 'run': '10:30 AM', 'type': 'single', 'name': s['pick'],
        'odds': s['odds'], 'stake': s.get('stake', 10), 'result': 'pending', 'profit': 0,
        'legs': [{'pick': s['pick'], 'odds': s['odds'], 'event': s['event'], 'result': 'pending', 'actual': 'plays Friday'}],
        'whyExplanation': 'Pending — Friday night.', 'lesson': ''
    })

for t in morning_parlays:
    if already_in_history(t['name'], '2026-11-06', '10:30 AM'):
        continue
    p['results']['history'].append({
        'date': '2026-11-06', 'run': '10:30 AM', 'type': 'parlay', 'name': t['name'],
        'odds': t['odds'], 'stake': t.get('stake', 10), 'result': 'pending', 'profit': 0,
        'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'plays Friday'} for l in t['legs']],
        'whyExplanation': 'Pending — Friday night.', 'lesson': ''
    })

for t in morning_lottery:
    if already_in_history(t['name'], '2026-11-06', '10:30 AM'):
        continue
    p['results']['history'].append({
        'date': '2026-11-06', 'run': '10:30 AM', 'type': 'lottery', 'name': t['name'],
        'odds': t['odds'], 'stake': t.get('stake', 5), 'result': 'pending', 'profit': 0,
        'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'plays Friday'} for l in t['legs']],
        'whyExplanation': 'Pending — Friday night.', 'lesson': ''
    })

# ============================================================
# STEP 2 — load events for afternoon card
# ============================================================
EIDS = {
    # singles
    'msu': 36260645, 'raiders': 36244875, 'cards': 36244878,
    # home ice sat
    'leafs': 36287956, 'wild': 36287960, 'nyi': 36287945,
    # friday campus
    'wvu_bb': 36285790, 'tamu': 36285161, 'minn': 36285148,
    # sat cfb
    'ttu': 36260771, 'hou': 36260623, 'nd': 35632913,
    # best shot
    'stanford': 36285062, 'kraken': 36287947, 'sens': 36287946,
    'jets': 36244871, 'lions': 36244872, 'osu_fb': 36260589,
    'sf_bb': 36285069, 'ucf': 36285198, 'car': 36287958,
    'edm': 36287969, 'dal': 36287959, 'bucs': 36244879,
    'cowboys': 36244868, 'chargers': 36244874, 'commanders': 36244876,
    'northwestern': 36285326, 'kstate': 36285113,
}

cache = {}
for key, eid in EIDS.items():
    cache[key] = load_event(eid)
    if not cache[key][0]:
        print('WARN missing', key, eid)

used_events, used_picks = set(str(x) for x in MORNING_USED), set()

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
        raise SystemExit(f'no sel for {pick} key={key} opts={opts[:25]}')
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

def mn_startswith(prefix):
    return lambda mn: mn.startswith(prefix) or mn == prefix

def mn_in(*names):
    return lambda mn: mn in names or any(mn.startswith(n) for n in names if n.startswith('Alternate'))

def rn_contains(substr):
    return lambda r, m: substr in (r.get('runnerName') or '')

def rn_hc(name, hc):
    return lambda r, m: r.get('runnerName') == name and r.get('handicap') == hc

def rn_eq(name):
    return lambda r, m: r.get('runnerName') == name

# ---- SINGLES (plus money) ----
singles = []
s1 = make_leg(
    'msu', mn_eq('Alternate Spread'), rn_contains('Michigan State (+13.5)'),
    'Michigan State +13.5', 'NCAAF',
    'MSU gets +13.5 at Michigan at even money (main +14.5). Double-digit cushion at plus money vs a heavy home favorite.',
)
singles.append({**s1, 'stake': 10})
s2 = make_leg(
    'raiders', mn_eq('Alternate Spread'), rn_contains('Raiders (+6.5)'),
    'Las Vegas Raiders +6.5', 'NFL',
    'Raiders +6.5 at SF at +146. Main is +9.5; buying toward the number still leaves a TD+ cushion at real plus money.',
)
singles.append({**s2, 'stake': 10})
s3 = make_leg(
    'cards', mn_eq('Alternate Spread'), rn_contains('Cardinals (+7.5)'),
    'Arizona Cardinals +7.5', 'NFL',
    'Cards +7.5 at Seattle at +102. Main is +8.5; one-score-plus cushion at plus money.',
)
singles.append({**s3, 'stake': 10})

# ---- PARLAYS ----
parlays = []

l_tor = make_leg('leafs', mn_eq('Puck Line'), rn_hc('Toronto Maple Leafs', 1.5),
    'Toronto Maple Leafs +1.5', 'NHL',
    'NHL home +1.5 backbone. Leafs host MTL; average-or-better home club with a goal cushion.')
l_wild = make_leg('wild', mn_eq('Puck Line'), rn_hc('Minnesota Wild', 1.5),
    'Minnesota Wild +1.5', 'NHL',
    'Wild home vs Lightning; +1.5 home ice continues the lesson (prefer average+ home clubs).')
l_nyi = make_leg('nyi', mn_eq('Puck Line'), rn_hc('New York Islanders', 1.5),
    'New York Islanders +1.5', 'NHL',
    'Islanders home vs Devils; +1.5 home cushion even as underdogs on the moneyline.')
odds, _ = combine([l_tor['odds'], l_wild['odds'], l_nyi['odds']])
parlays.append({
    'name': 'Saturday Home Ice +1.5', 'odds': odds, 'stake': 10,
    'legs': [l_tor, l_wild, l_nyi],
    'reason': 'Fri NHL board was fully used at 10:30. Three Saturday home +1.5 cushions (Leafs/Wild/Islanders) — prefer average-or-better home clubs after PIT blowout lesson.',
})

l_wvu = make_leg('wvu_bb', lambda mn: mn.startswith('Alternate Spread') or mn == 'Spread',
    rn_hc('West Virginia', -18.5),
    'West Virginia -18.5', 'NCAAB',
    'WVU -27.5 main vs Stetson; bought down to -18.5 (under the -20 ban) at -420. Huge class gap, high-prob cover.')
l_tamu = make_leg('tamu', lambda mn: mn.startswith('Alternate Spread') or mn == 'Spread',
    rn_hc('Texas A&M', -18.5),
    'Texas A&M -18.5', 'NCAAB',
    'TAMU -27.5 main vs NKU; bought to -18.5 under the -20 ban. Power host mismatch.')
l_minn = make_leg('minn', lambda mn: mn.startswith('Alternate Spread') or mn == 'Spread',
    rn_hc('Minnesota', -11.5),
    'Minnesota -11.5', 'NCAAB',
    'Minnesota -14.5 main vs St. Thomas; -11.5 alt keeps ~75%+ cover without a suspended chalk ML.')
odds, _ = combine([l_wvu['odds'], l_tamu['odds'], l_minn['odds']])
parlays.append({
    'name': 'Friday Campus Cushions', 'odds': odds, 'stake': 10,
    'legs': [l_wvu, l_tamu, l_minn],
    'reason': 'Unused Friday Power hosts. Heavy favorites whose MLs are suspended at -100000 — buy down under the -20 alt ban instead of chalk MLs.',
})

l_ttu = make_leg('ttu', mn_eq('Alternate Spread'), rn_contains('Texas Tech (-13.5)'),
    'Texas Tech -13.5', 'NCAAF',
    'TTU -16.5 main vs WVU; bought to -13.5 for a real cushion at -156.')
l_hou = make_leg('hou', mn_eq('Alternate Spread'), rn_contains('Houston (-8.5)'),
    'Houston -8.5', 'NCAAF',
    'Houston -10.5 main vs Cincinnati; -8.5 keeps a one-score cushion without laying the full number.')
l_nd = make_leg('nd', mn_eq('Alternate Spread'), rn_contains('Notre Dame (-3.5)'),
    'Notre Dame -3.5', 'NCAAF',
    'ND -7.5 main vs Miami; bought to -3.5 so we only need a field-goal win at home.')
odds, _ = combine([l_ttu['odds'], l_hou['odds'], l_nd['odds']])
parlays.append({
    'name': 'Saturday CFB Bought-Down', 'odds': odds, 'stake': 10,
    'legs': [l_ttu, l_hou, l_nd],
    'reason': 'Three Saturday CFB favorites bought below the main number for ~75% covers and a real parlay price — no mid-major chalk.',
})

# ---- BEST SHOT ----
bs_specs = [
    ('stanford', mn_eq('Moneyline'), rn_eq('Stanford'), 'Stanford ML', 'NCAAB',
     'Stanford -1450 home vs Oakland. OPEN ML (not suspended); Power host, win-prob first.'),
    ('northwestern', mn_eq('Moneyline'), rn_eq('Northwestern'), 'Northwestern ML', 'NCAAB',
     'Northwestern -950 home vs Stony Brook. Power host mismatch; OPEN ML.'),
    ('kstate', mn_eq('Moneyline'), rn_eq('Kansas State'), 'Kansas State ML', 'NCAAB',
     'K-State -600 home vs CSUN. Power host; OPEN ML around 75%+.'),
    ('sf_bb', mn_eq('Moneyline'), rn_eq('San Francisco'), 'San Francisco ML', 'NCAAB',
     'USF -465 home vs NDSU. Solid home favorite on an OPEN ML.'),
    ('ucf', mn_eq('Moneyline'), rn_eq('UCF'), 'UCF ML', 'NCAAB',
     'UCF -520 home vs Yale. Home favorite on OPEN ML.'),
    ('kraken', mn_eq('Puck Line'), rn_hc('Seattle Kraken', 1.5), 'Seattle Kraken +1.5', 'NHL',
     'Kraken home +1.5 vs Rangers. Home ice cushion on an average home club.'),
    ('sens', mn_eq('Puck Line'), rn_hc('Ottawa Senators', 1.5), 'Ottawa Senators +1.5', 'NHL',
     'Senators home +1.5 vs Utah. Home ice cushion.'),
    ('car', mn_eq('Moneyline'), rn_eq('Carolina Hurricanes'), 'Carolina Hurricanes ML', 'NHL',
     'Hurricanes -410 home vs Blackhawks. Clear class gap; ~80% implied.'),
    ('edm', mn_eq('Moneyline'), rn_eq('Edmonton Oilers'), 'Edmonton Oilers ML', 'NHL',
     'Oilers -310 home vs Canucks. Home favorite at ~75%+.'),
    ('dal', mn_eq('Moneyline'), rn_eq('Dallas Stars'), 'Dallas Stars ML', 'NHL',
     'Stars -300 home vs Sharks. Home favorite vs a weak visitor.'),
    ('jets', mn_eq('Alternate Spread'), rn_contains('Jets (+14.5)'), 'New York Jets +14.5', 'NFL',
     'Jets +14.5 at KC. Huge cushion (main +9.5); ~75%+ cover aim at -194.'),
    ('lions', mn_eq('Alternate Spread'), rn_contains('Lions (-3.5)'), 'Detroit Lions -3.5', 'NFL',
     'Lions -7 main at Miami; bought to -3.5. Only need a field-goal win.'),
    ('osu_fb', mn_eq('Alternate Spread'), rn_contains('Ohio State (-4.5)'), 'Ohio State -4.5', 'NCAAF',
     'OSU -7.5 main vs Oregon; bought to -4.5 for a one-score cover.'),
    ('bucs', mn_eq('Alternate Spread'), rn_contains('Buccaneers (+10.5)'), 'Tampa Bay Buccaneers +10.5', 'NFL',
     'Bucs +10.5 at Chicago. Double-digit dog cushion.'),
    ('cowboys', mn_eq('Alternate Spread'), rn_contains('Cowboys (-3.5)'), 'Dallas Cowboys -3.5', 'NFL',
     'Cowboys -5.5 main at Indy; bought to -3.5.'),
    ('chargers', mn_eq('Alternate Spread'), rn_contains('Chargers (+9.5)'), 'Los Angeles Chargers +9.5', 'NFL',
     'Chargers +9.5 vs Texans. ≥+9.5 cushion lesson.'),
    ('commanders', mn_eq('Alternate Spread'), rn_contains('Commanders (+9.5)'), 'Washington Commanders +9.5', 'NFL',
     'Commanders +9.5 vs Rams. ≥+9.5 cushion.'),
]

bs_legs = []
for spec in bs_specs:
    key, mp, rp, pick, sport, reason = spec
    try:
        leg = make_leg(key, mp, rp, pick, sport, reason)
        bs_legs.append(leg)
    except SystemExit as e:
        print('BS skip', pick, e)

odds_bs, dec_bs = combine([l['odds'] for l in bs_legs]) if bs_legs else (0, 1.0)
payout_5 = round(5 * dec_bs, 2)
print(f'Best Shot: {len(bs_legs)} legs, odds {odds_bs}, $5 → ${payout_5}')

honesty = (
    f'~$5 → ${payout_5}'
    + ('. Short of the $5K target — morning burned Fri NBA/NHL and most Power NCAAB; remaining slate cannot hit $5K without coin-flip padding.'
       if payout_5 < 5000 else ' (inside $5K–$50K target).')
)

lottery = [{
    'name': 'Best Shot $500K',
    'odds': odds_bs,
    'stake': 5,
    'legs': bs_legs,
    'reason': (
        f'{len(bs_legs)} highest-prob unused legs: Fri Power MLs still OPEN, Sat NHL home +1.5 / heavy MLs, '
        f'Sat CFB/NFL bought-down cushions. Win-prob first, no mid-major short favs, no -20 college alts, no morning event reuse. '
        + honesty
    ),
}]

# Append afternoon tickets to history as pending
for s in singles:
    if already_in_history(s['pick'], '2026-11-06', '3:00 PM'):
        continue
    p['results']['history'].append({
        'date': '2026-11-06', 'run': '3:00 PM', 'type': 'single', 'name': s['pick'],
        'odds': s['odds'], 'stake': s.get('stake', 10), 'result': 'pending', 'profit': 0,
        'legs': [{'pick': s['pick'], 'odds': s['odds'], 'event': s['event'], 'result': 'pending', 'actual': 'pending'}],
        'whyExplanation': 'Pending — afternoon card.', 'lesson': ''
    })
for t in parlays:
    if already_in_history(t['name'], '2026-11-06', '3:00 PM'):
        continue
    p['results']['history'].append({
        'date': '2026-11-06', 'run': '3:00 PM', 'type': 'parlay', 'name': t['name'],
        'odds': t['odds'], 'stake': t.get('stake', 10), 'result': 'pending', 'profit': 0,
        'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'pending'} for l in t['legs']],
        'whyExplanation': 'Pending — afternoon card.', 'lesson': ''
    })
for t in lottery:
    if already_in_history(t['name'], '2026-11-06', '3:00 PM'):
        continue
    p['results']['history'].append({
        'date': '2026-11-06', 'run': '3:00 PM', 'type': 'lottery', 'name': t['name'],
        'odds': t['odds'], 'stake': t.get('stake', 5), 'result': 'pending', 'profit': 0,
        'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'pending'} for l in t['legs']],
        'whyExplanation': 'Pending — afternoon card.', 'lesson': ''
    })

# ---- write card ----
p['updated'] = 'Fri Nov 6, 2026 3:00 PM ET'
p['run'] = (
    '3:00 PM ET Friday. No new settles (Fri slate still pending; Sunday NFL pending). '
    'Morning burned all Fri NBA/NHL and most Power NCAAB. Afternoon: plus-money MSU/Raiders/Cards singles; '
    'Sat Home Ice +1.5; Fri Campus bought-down alts (WVU/TAMU/Minnesota); Sat CFB bought-down (TTU/Hou/ND); '
    f'Best Shot {len(bs_legs)} legs ~${payout_5} on $5'
    + (' — short of $5K, no coin-flip pad.' if payout_5 < 5000 else '.')
    + ' Lessons: win-prob first, college -1800+/bought-down under -20, NHL home +1.5, no mid-major short favs, no morning event reuse.'
)
p['singles'] = singles
p['parlays'] = parlays
p['lottery'] = lottery

totals = recompute_totals(p['results']['history'])
p['results']['totals'] = totals
p['results']['singles'] = copy.deepcopy(totals['singles'])
p['results']['parlays'] = copy.deepcopy(totals['parlays'])
p['results']['lottery'] = copy.deepcopy(totals['lottery'])
p['results']['updated'] = 'Fri Nov 6, 2026 3:00 PM ET'
p['results']['sources'] = (
    'FanDuel PA public odds feed; ESPN scoreboards for prior grades; prior lessons.md (college ML 27-0, NHL home +1.5, no mid-major short favs, no -20 college alts)'
)
p['results']['topLessons'] = [
    'College MLs at -1800+ are 27-0 — when those MLs are suspended, buy Power hosts down under the -20 alt ban instead.',
    'NHL home +1.5 stays elite but failed on PIT blowout; prefer average-or-better home clubs (used Leafs/Wild/Islanders/Kraken/Sens).',
    'Mid-major short favorites / tiny alt spreads are not 75% legs — skipped Elon/UIC and all -20+ college alts.',
    'Morning event burn forces afternoon onto Sat NHL/CFB and Sun NFL cushions; do not reuse any morning eventId.',
    'Best Shot stays short of $5K rather than pad with coin-flip MLs when the remaining slate is thin.',
]

json.dump(p, open('/workspace/csb/picks.json', 'w'), indent=1)
print('Wrote picks.json')
print('TOTALS', json.dumps(totals['overall'], indent=2))
print('Card singles', [(s['pick'], s['odds']) for s in singles])
for t in parlays:
    print('Parlay', t['name'], t['odds'], [(l['pick'], l['odds']) for l in t['legs']])
print('BS', odds_bs, payout_5, [(l['pick'], l['odds']) for l in bs_legs])
print('used events this card', sorted(int(x) for x in used_events if int(x) not in MORNING_USED))
