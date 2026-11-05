#!/usr/bin/env python3
"""Thu Nov 5, 2026 3:00 PM ET — grade morning + build afternoon card."""
import json, copy, datetime, urllib.request, os
from datetime import timezone, timedelta

ET = timezone(timedelta(hours=-5))
K = 'FhMFpcPWXMeyZxOx'
UA = {'User-Agent': 'Mozilla/5.0'}

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
        o = get(f'https://sbapi.pa.sportsbook.fanduel.com/api/event-page?_ak={K}&eventId={eid}' + (f'&tab={tab}' if tab else ''))
        mkts.update((o.get('attachments') or {}).get('markets') or {})
        evs = (o.get('attachments') or {}).get('events') or {}
        if isinstance(evs, dict) and evs:
            ev = list(evs.values())[0]
        elif isinstance(evs, list) and evs:
            ev = evs[0]
    # also merge cached files
    for suf in ['', '_alternates', '_popular']:
        path = f'/workspace/ev_{eid}{suf}.json'
        if os.path.exists(path):
            try:
                d = json.load(open(path))
                mkts.update((d.get('attachments') or {}).get('markets') or {})
                if not ev:
                    evs = (d.get('attachments') or {}).get('events') or {}
                    if isinstance(evs, dict) and evs:
                        ev = list(evs.values())[0]
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
        # restricted feed check
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

# ---- load morning card ----
p = json.load(open('/workspace/csb/picks.json'))
morning_singles = copy.deepcopy(p['singles'])
morning_parlays = copy.deepcopy(p['parlays'])
morning_lottery = copy.deepcopy(p['lottery'])

# ---- stale pending leg resolution ----
stale = {
    ('Best Shot $500K', 'Sassuolo v Fiorentina Under 3.5 Goals'): ('miss', 'Sassuolo 2-4 Fiorentina (6 goals)'),
    ('Best Shot $500K', 'Lorient v Brest Under 2.5 Goals'): ('hit', 'Lorient 0-2 Brest (2 goals)'),
    ('Best Shot $500K', 'Atalanta ML (90 min)'): ('miss', 'Atalanta 0-3 Parma'),
    ('Best Shot $500K', 'Deportivo v Osasuna Under 2.5 Goals'): ('miss', 'Deportivo 2-1 Osasuna (3 goals)'),
    ('Best Shot $500K', 'Newcastle v Everton Under 3.5 Goals'): ('hit', 'Newcastle 0-1 Everton (1 goal)'),
    ('Best Shot $500K', 'Panthers ML'): ('miss', 'Red Wings 5, Panthers 3'),
    ('Best Shot $500K', 'Bruins +1.5'): ('hit', 'Bruins 3, Golden Knights 2 (SO)'),
    ('Best Shot $500K', 'Avalanche ML'): ('hit', 'Avalanche 5, Blackhawks 2'),
    ('Best Shot $500K', 'Flames +1.5'): ('hit', 'Flames 2, Sharks 1'),
    ('Best Shot $500K', 'Seahawks +1.5 (Alt Spread)'): ('miss', 'Bears 34, Seahawks 17 (lost by 17)'),
    ('Best Shot $500K', 'Iowa State ML'): ('miss', 'Memphis 80, Iowa State 76'),
    ('Best Shot $500K', 'Gonzaga ML'): ('hit', 'Gonzaga 78, Purdue 72'),
    ('Best Shot $500K', 'Florida ML'): ('hit', 'Florida 77, Miami 67'),
    ('Monday Favorites Ladder', 'Seahawks ML'): ('miss', 'Bears 34, Seahawks 17'),
    ('Monday Favorites Ladder', 'Newcastle or Draw'): ('miss', 'Newcastle 0-1 Everton'),
    ('Monday Favorites Ladder', 'Iowa State -6.5 (Alt Spread)'): ('miss', 'Memphis 80, Iowa State 76'),
}
for h in p['results']['history']:
    for leg in h.get('legs') or []:
        if leg.get('result') != 'pending':
            continue
        key = (h.get('name'), leg.get('pick'))
        if key in stale:
            leg['result'], leg['actual'] = stale[key]

# ---- grade morning Europa + Best Shot ----
new_hist = []
europa = {
    'date': '2026-11-05', 'run': '10:30 AM', 'type': 'parlay', 'name': 'Europa Class-Gap Favorites',
    'odds': -174, 'stake': 10, 'result': 'lost', 'profit': -10,
    'legs': [
        {'pick': 'Crvena Zvezda ML', 'odds': -2000, 'event': 'Crvena Zvezda v Inter Club Escaldes', 'result': 'hit', 'actual': 'Red Star Belgrade 2-1 Inter Escaldes'},
        {'pick': 'Atalanta ML', 'odds': -1100, 'event': 'Atalanta v Kairat Almaty', 'result': 'miss', 'actual': 'Atalanta 1-1 Kairat Almaty (draw)'},
        {'pick': 'Benfica ML', 'odds': -1000, 'event': 'Benfica v Lech Poznan', 'result': 'pending', 'actual': 'in progress at 3 PM grade'},
        {'pick': 'FC Copenhagen ML', 'odds': -900, 'event': 'FC Copenhagen v FC Iberia 1999', 'result': 'pending', 'actual': 'in progress at 3 PM grade'},
        {'pick': 'Lugano ML', 'odds': -800, 'event': 'Lugano v FK Kauno Zalgiris', 'result': 'pending', 'actual': 'in progress at 3 PM grade'},
    ],
    'whyExplanation': 'LOST. Atalanta drew 1-1 at home with Kairat Almaty, so the moneyline missed. Crvena Zvezda won 2-1. Benfica/Copenhagen/Lugano were still in progress but the ticket was already dead.',
    'lesson': "A -1100 home favorite in UEFA Conference League can still draw a supposed mismatch (Atalanta 1-1 Kairat). Class-gap soccer MLs are not locks — prefer double chance unless the opponent is truly amateur-tier."
}
new_hist.append(europa)

known_bs = {
    'AC Milan or Draw': ('miss', 'Ferencvaros won 2-0 at AC Milan'),
    'Anderlecht vs Salzburg Over 1.5 Goals': ('hit', 'Anderlecht 2-0 Salzburg'),
    'Bournemouth to score (Away Over 0.5)': ('hit', 'Bournemouth scored 3 at Sparta Prague'),
    'Crystal Palace to score (Home Over 0.5)': ('hit', 'Crystal Palace 1-1 Hoffenheim'),
    'Hajduk Split or Draw': ('miss', 'Lincoln Red Imps won 1-0 vs Hajduk Split'),
    'Midtjylland vs Ajax Over 1.5 Goals': ('hit', 'Midtjylland 1-6 Ajax'),
    'Real Sociedad to score (Home Over 0.5)': ('hit', 'Real Sociedad 1-1 Lyon'),
    'Thun vs Hearts Over 1.5 Goals': ('hit', 'Thun 3-1 Hearts'),
}
bs = morning_lottery[0]
bs_legs = []
for leg in bs['legs']:
    entry = {'pick': leg['pick'], 'odds': leg['odds'], 'event': leg['event']}
    if leg['pick'] in known_bs:
        entry['result'], entry['actual'] = known_bs[leg['pick']]
    else:
        entry['result'] = 'pending'
        entry['actual'] = 'in progress or plays tonight'
    bs_legs.append(entry)
hits = sum(1 for l in bs_legs if l['result'] == 'hit')
misses = sum(1 for l in bs_legs if l['result'] == 'miss')
new_hist.append({
    'date': '2026-11-05', 'run': '10:30 AM', 'type': 'lottery', 'name': 'Best Shot $500K',
    'odds': bs['odds'], 'stake': 5, 'result': 'lost', 'profit': -5,
    'legs': bs_legs,
    'whyExplanation': f'LOST. Dead on early soccer: AC Milan or Draw missed (Ferencvaros 2-0 in Milan) and Hajduk Split or Draw missed (Lincoln Red Imps 1-0). Settled soccer {hits} hit / {misses} miss; NHL/NBA/NCAAF/NCAAB still pending tonight.',
    'lesson': "Away European 'or Draw' double chances failed twice in one window (Milan home to Ferencvaros; Hajduk at Lincoln Red Imps). Awkward away venues can upset 'class-gap' frames — prefer home double chance or team-to-score."
})

for s in morning_singles:
    new_hist.append({
        'date': '2026-11-05', 'run': '10:30 AM', 'type': 'single', 'name': s['pick'],
        'odds': s['odds'], 'stake': s.get('stake', 10), 'result': 'pending', 'profit': 0,
        'legs': [{'pick': s['pick'], 'odds': s['odds'], 'event': s['event'], 'result': 'pending', 'actual': 'plays tonight'}],
        'whyExplanation': 'Pending — TNF tonight.', 'lesson': ''
    })
for par in morning_parlays:
    if par['name'] == 'Europa Class-Gap Favorites':
        continue
    new_hist.append({
        'date': '2026-11-05', 'run': '10:30 AM', 'type': 'parlay', 'name': par['name'],
        'odds': par['odds'], 'stake': par.get('stake', 10), 'result': 'pending', 'profit': 0,
        'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'plays tonight'} for l in par['legs']],
        'whyExplanation': 'Pending — games tonight.', 'lesson': ''
    })

p['results']['history'].extend(new_hist)

# ---- recount totals from history ----
# Start from previous settled W/L then apply only NEW graded tickets (europa L, BS L)
# Safer: recompute ticket totals from history for won/lost/pending/staked/profit

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
            # pending stake not in staked until settled (existing convention uses settled only)
        elif result == 'void':
            pass
        legs = h.get('legs') or []
        if not legs and h.get('type') == 'single':
            if result == 'won':
                hit += 1
            elif result == 'lost':
                miss += 1
            elif result == 'pending':
                pend += 1
            elif result == 'void':
                void += 1
        for leg in legs:
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

totals = recompute_totals(p['results']['history'])
p['results']['totals'] = totals
p['results']['singles'] = copy.deepcopy(totals['singles'])
p['results']['parlays'] = copy.deepcopy(totals['parlays'])
p['results']['lottery'] = copy.deepcopy(totals['lottery'])
p['results']['updated'] = 'Thu Nov 5, 2026 3:00 PM ET'
p['results']['sources'] = 'ESPN scoreboards/box scores (UEFA Europa/Conference, Serie A, Ligue 1, EPL, NHL, NFL, NCAAB); FanDuel PA public odds feed'

top_lessons = [
    'NHL home +1.5 is 9-0 and college MLs at -1800 or longer are 16-0 — keep building around these.',
    "Away European 'or Draw' / short class-gap MLs failed again (Milan, Hajduk, Atalanta) — prefer home DC or to-score unless the gap is extreme.",
    'No coin-flip lottery legs (~75%+ only); no NBA -12 spreads or -2.5 favorite spreads; no Rockets; no road dogs at Denver.',
    'NBA alt overs need 18+ points of cushion; no college alt spreads of -20 or more vs weak foes; no pick\'em college legs.',
    'Morning slate burned most Thu NHL/NBA/NFL events — afternoon Best Shot leans NCAAB cushions + Friday -1800 MLs and stays short of $5K rather than pad coin-flips.',
]
p['results']['topLessons'] = top_lessons

# ---- build afternoon card ----
EIDS = {
    'jets': 36244871, 'raiders': 36244875, 'cards': 36244878, 'lions': 36244872,
    'utah': 36281115, 'psu': 36280970, 'cha': 36280983, 'tulane': 36281366, 'tulsa': 36281148,
    'msu': 36281162, 'ntx': 36281323, 'merri': 36281338, 'iona': 36281337, 'depaul': 36281173,
    'iw': 36281343, 'usa': 36281169, 'marist': 36281346,
    'oregon': 36285142, 'ncsu': 36285236, 'gt': 36285243, 'purdue': 36285183, 'fsu': 36285203,
    'xavier': 36285273, 'uk': 36285241, 'unc': 36285174, 'osu': 36285153, 'bama': 36285288, 'wisc': 36285309,
    'buf': 36260073, 'cgy': 36260074,
}
cache = {}
for k, eid in EIDS.items():
    tabs = ('', 'popular', 'alternates')
    cache[k] = load_event(eid, tabs)
    assert cache[k][0], f'missing event {k}'

used_events, used_picks = set(), set()

def make_leg(key, market_pred, runner_pred, pick, sport, reason):
    ev, mkts = cache[key]
    sel = find_runner(mkts, market_pred, runner_pred)
    if not sel:
        # debug dump
        opts = []
        for mid, m in mkts.items():
            if m.get('marketStatus') != 'OPEN':
                continue
            for r in m.get('runners') or []:
                o = am_odds(r)
                if o is not None and (market_pred(m.get('marketName', '')) or True):
                    if runner_pred(r, m) or pick.split()[0] in str(r.get('runnerName')):
                        opts.append((m.get('marketName'), r.get('runnerName'), r.get('handicap'), o, mid, r.get('selectionId'), m.get('canTurnInPlay')))
        raise SystemExit(f'no sel for {pick} key={key} opts={opts[:12]}')
    eid = str(sel['eventId'])
    if eid in used_events:
        raise SystemExit(f'event reuse {eid} for {pick}')
    if pick in used_picks:
        raise SystemExit(f'pick reuse {pick}')
    used_events.add(eid)
    used_picks.add(pick)
    # verify start > now+1h
    t = datetime.datetime.fromisoformat(ev['openDate'].replace('Z', '+00:00'))
    if t < datetime.datetime.now(timezone.utc) + timedelta(hours=1):
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

rn = lambda name: (lambda r, m: r.get('runnerName') == name)
rn_hc = lambda name, hc: (lambda r, m: r.get('runnerName') == name and r.get('handicap') == hc)
mn_eq = lambda name: (lambda mn: mn == name)
mn_alt = lambda: (lambda mn: mn.startswith('Alternate Spread'))
mn_ml = lambda: (lambda mn: mn == 'Moneyline')
mn_sog = lambda: (lambda mn: mn == '2+ Shots on Goal')

singles = []
singles.append({**make_leg('jets', mn_eq('Alternate Spread'), rn('New York Jets (+8.5)'),
    'New York Jets +8.5', 'NFL',
    'Main is Jets +9.5; buy a half-point to +8.5 at plus money. Public is heavy on Kansas City, so this is a plus-money dog cushion with nearly a TD of cover room.'),
    'stake': 10})
singles.append({**make_leg('raiders', mn_eq('Alternate Spread'), rn('Las Vegas Raiders (+7.5)'),
    'Las Vegas Raiders +7.5', 'NFL',
    'Main is Raiders +9.5; +7.5 still leaves TD+ cushion at plus money at San Francisco without buying past a double-digit number on the favorite.'),
    'stake': 10})
singles.append({**make_leg('cards', mn_eq('Alternate Spread'), rn('Arizona Cardinals (+7.5)'),
    'Arizona Cardinals +7.5', 'NFL',
    'Main is Cardinals +8.5; +7.5 at plus money keeps a one-score road cushion in Seattle.'),
    'stake': 10})

parlays = []
# Parlay 1: Lions + Utah + PSU
legs = [
    make_leg('lions', mn_eq('Alternate Spread'), rn('Detroit Lions (+1.5)'),
        'Detroit Lions +1.5', 'NFL',
        'Lions are about -7 at Miami; +1.5 is a huge cushion that only loses if Detroit loses outright by 2+.'),
    make_leg('utah', mn_alt(), rn_hc('Utah', 1.5),
        'Utah +1.5', 'NCAAB',
        'Utah -7.5-ish favorite vs Towson; +1.5 favorite-getting-points cushion at short juice.'),
    make_leg('psu', mn_alt(), rn_hc('Penn State', -2.5),
        'Penn State -2.5', 'NCAAB',
        'Penn State -12.5 favorite vs Chattanooga; bought down to -2.5 (-620) as a high-probability cover.'),
]
odds, dec = combine([l['odds'] for l in legs])
parlays.append({
    'name': 'Lions Cushion + Campus Favorites',
    'odds': odds, 'stake': 10, 'payout': round(10 * dec, 2),
    'reason': 'Three high-probability cushions: Lions +1.5 vs a -7 market, Utah +1.5 as a home favorite getting points, and Penn State bought down from double digits to -2.5.',
    'legs': legs,
})

# Parlay 2: mid-major MLs
legs = [
    make_leg('tulsa', mn_ml(), rn('Tulsa'),
        'Tulsa ML', 'NCAAB',
        'Tulsa -1450 at home vs Northern Illinois — clear class gap on the moneyline (no -20 alt spread).'),
    make_leg('tulane', mn_ml(), rn('Tulane'),
        'Tulane ML', 'NCAAB',
        'Tulane -950 vs Jackson State at home — moneyline anchor, not a big alt spread.'),
    make_leg('oregon', mn_ml(), rn('Oregon'),
        'Oregon ML', 'NCAAB',
        'Oregon -1700 Friday vs Eastern Washington — meets the -1800-ish college ML ladder standard.'),
]
odds, dec = combine([l['odds'] for l in legs])
parlays.append({
    'name': 'Campus Moneyline Trio',
    'odds': odds, 'stake': 10, 'payout': round(10 * dec, 2),
    'reason': 'Three college moneylines at -950 to -1700 against clear overmatched visitors. Uses MLs (proven 16-0 at -1800+) instead of forbidden -20 alt spreads.',
    'legs': legs,
})

# Parlay 3: Friday heavy locks
legs = [
    make_leg('bama', mn_ml(), rn('Alabama'),
        'Alabama ML', 'NCAAB',
        'Alabama -20000 Friday vs Arkansas State — classic -1800+ college lock.'),
    make_leg('unc', mn_ml(), rn('North Carolina'),
        'North Carolina ML', 'NCAAB',
        'UNC -10000 Friday vs Wofford.'),
    make_leg('osu', mn_ml(), rn('Ohio State'),
        'Ohio State ML', 'NCAAB',
        'Ohio State -10000 Friday vs Youngstown State.'),
    make_leg('uk', mn_ml(), rn('Kentucky'),
        'Kentucky ML', 'NCAAB',
        'Kentucky -10000 Friday vs James Madison.'),
]
odds, dec = combine([l['odds'] for l in legs])
parlays.append({
    'name': 'Friday College Locks',
    'odds': odds, 'stake': 10, 'payout': round(10 * dec, 2),
    'reason': 'Lesson applied: college MLs at -1800 or longer are 16-0. Four Friday home/power-conference locks vs overmatched visitors.',
    'legs': legs,
})

# ---- Best Shot ----
bs_specs = [
    ('cha', mn_alt(), rn_hc('Charlotte', -5.5), 'Charlotte -5.5', 'NCAAB',
     'Charlotte -11.5 favorite vs Georgia State; bought down to -5.5.'),
    ('msu', mn_alt(), rn_hc('Michigan State', -17.5), 'Michigan State -17.5', 'NCAAB',
     'No. 6 MSU vs Toledo; -17.5 is under the -20 alt-spread ban and still a massive expected margin (KenPom ~98% ML).'),
    ('ntx', mn_alt(), rn_hc('North Texas', 8.5), 'North Texas +8.5', 'NCAAB',
     'McNeese is a slight favorite on the road; North Texas +8.5 is a double-digit-ish cushion at -310.'),
    ('merri', mn_alt(), rn_hc('Merrimack', -3.5), 'Merrimack -3.5', 'NCAAB',
     'Merrimack -9.5-ish favorite vs UMass Lowell; bought down to -3.5.'),
    ('iona', mn_alt(), rn_hc('Iona', -3.5), 'Iona -3.5', 'NCAAB',
     'Iona -9.5 favorite vs NJIT; bought down to -3.5.'),
    ('depaul', mn_alt(), rn_hc('DePaul', -0.5), 'DePaul -0.5', 'NCAAB',
     'DePaul -6.5 favorite vs USF; -0.5 is essentially a moneyline with a half-point.'),
    ('iw', mn_alt(), rn_hc('Incarnate Word', -2.5), 'Incarnate Word -2.5', 'NCAAB',
     'Incarnate Word -8.5 favorite vs Chicago State; bought down to -2.5.'),
    ('usa', mn_alt(), rn_hc('South Alabama', 3.5), 'South Alabama +3.5', 'NCAAB',
     'South Alabama -4.5 favorite vs Jacksonville State; +3.5 favorite-getting-points.'),
    ('marist', mn_alt(), rn_hc('Marist', 4.5), 'Marist +4.5', 'NCAAB',
     'Marist -4.5 favorite vs UMBC; +4.5 is a full touchdown of favorite cushion.'),
    ('purdue', mn_ml(), rn('Purdue'), 'Purdue ML', 'NCAAB',
     'Purdue -4000 Friday vs Valparaiso — -1800+ college lock.'),
    ('fsu', mn_ml(), rn('Florida State'), 'Florida State ML', 'NCAAB',
     'Florida State -4000 Friday vs Troy.'),
    ('xavier', mn_ml(), rn('Xavier'), 'Xavier ML', 'NCAAB',
     'Xavier -4500 Friday vs Eastern Michigan.'),
    ('ncsu', mn_ml(), rn('NC State'), 'NC State ML', 'NCAAB',
     'NC State -1800 Friday vs East Tennessee State.'),
    ('gt', mn_ml(), rn('Georgia Tech'), 'Georgia Tech ML', 'NCAAB',
     'Georgia Tech -1800 Friday vs Georgia Southern.'),
    ('wisc', mn_ml(), rn('Wisconsin'), 'Wisconsin ML', 'NCAAB',
     'Wisconsin -10000 Friday vs Delaware.'),
    ('buf', mn_sog(), rn('Tage Thompson'), 'Tage Thompson 2+ Shots on Goal', 'NHL',
     'Thompson is a high-volume Buffalo shooter; 2+ SOG at short price on a restricted main feed is allowed as a player prop (canTurnInPlay exception).'),
    ('cgy', lambda mn: mn == '1+ Shots on Goal', rn('Leo Carlsson'), 'Leo Carlsson 1+ Shots on Goal', 'NHL',
     'Carlsson 1+ SOG at about -2000 — high-volume Duck on the road in Calgary; player-prop exception to restricted feed.'),
]

# Need 25 legs - add more from remaining: Seahawks -2.5? SEA event free. SF -2.5 free. KC -3.5 free.
# jets/raiders/cards events used by singles. lions used by parlay. 
# Free NFL: none of the 4 if all used... jets,raiders,cards singles; lions parlay. All 4 NFL used!
# Need more NCAAB. Add Quinnipiac etc - fetch if needed.

# Currently 17 specs. Need 8 more high-prob from unused events.
# Load more events
extra = {
    'qui': 36281334,  # Bryant @ Quinnipiac
    'stp': 36281335,  # Binghamton @ Saint Peter's
    'fair': 36281331, # Vermont @ Fairfield - skip pick'em
    'sacred': 36281356, # Maine @ Sacred Heart
    'mani': 36281361, # Albany @ Manhattan
    'hof': 36281346, # wait marist used
}
# Fetch a few more
for k, eid in [('qui', 36281334), ('stp', 36281335), ('sacred', 36281356), ('mani', 36281361),
               ('sea', 36244878), # USED by cards single - skip
               ('sf', 36244875), # USED
               ]:
    pass

for k, eid in [('qui', 36281334), ('stp', 36281335), ('sacred', 36281356), ('mani', 36281361),
               ('creigh', 36281377), ('duke', 36280956), ('florida', 36281368), ('texas', 36281369),
               ('ill', 36281134), ('ariz', 36281108), ('tech', 36281378), ('ind', 36281325)]:
    cache[k] = load_event(eid)
    print('extra', k, cache[k][0]['name'] if cache[k][0] else None, len(cache[k][1]))

# Add safe extras: Quinnipiac -6.5 or ML, Saint Peter's ML, Sacred Heart ML, Manhattan ML
# For Duke/Florida etc only if ML exists or alt under -20

extra_specs = []
# Quinnipiac
sel = find_runner(cache['qui'][1], mn_ml(), rn('Quinnipiac'))
if sel and sel['odds'] <= -250:
    extra_specs.append(('qui', mn_ml(), rn('Quinnipiac'), 'Quinnipiac ML', 'NCAAB',
        'Quinnipiac home favorite vs Bryant.'))
sel = find_runner(cache['stp'][1], mn_ml(), rn("Saint Peter's"))
if sel and sel['odds'] <= -250:
    extra_specs.append(('stp', mn_ml(), rn("Saint Peter's"), "Saint Peter's ML", 'NCAAB',
        "Saint Peter's home favorite vs Binghamton."))
sel = find_runner(cache['sacred'][1], mn_ml(), rn('Sacred Heart'))
if sel and sel['odds'] <= -250:
    extra_specs.append(('sacred', mn_ml(), rn('Sacred Heart'), 'Sacred Heart ML', 'NCAAB',
        'Sacred Heart home favorite vs Maine.'))
sel = find_runner(cache['mani'][1], mn_ml(), rn('Manhattan'))
if sel and sel['odds'] <= -250:
    extra_specs.append(('mani', mn_ml(), rn('Manhattan'), 'Manhattan ML', 'NCAAB',
        'Manhattan home favorite vs Albany.'))

# Heavy favorites with ML if any
for k, team in [('ind', 'Indiana'), ('duke', 'Duke'), ('florida', 'Florida'), ('texas', 'Texas'),
                ('ill', 'Illinois'), ('creigh', 'Creighton'), ('ariz', 'Arizona'), ('tech', 'Texas Tech')]:
    sel = find_runner(cache[k][1], mn_ml(), rn(team))
    if sel and sel['odds'] <= -800:
        extra_specs.append((k, mn_ml(), rn(team), f'{team} ML', 'NCAAB',
            f'{team} heavy favorite moneyline (no -20 alt spread).'))
    else:
        # try alt under -20: e.g. -17.5 style only
        sel = find_runner(cache[k][1], mn_alt(), lambda r, m, t=team: r.get('runnerName') == t and isinstance(r.get('handicap'), (int, float)) and -20 < r.get('handicap') <= -10 and (am_odds(r) or 0) <= -300)
        if sel:
            hc = sel['handicap']
            extra_specs.append((k, mn_alt(), rn_hc(team, hc), f'{team} {hc}', 'NCAAB',
                f'{team} alt spread {hc} (under the -20 ban) vs an overmatched visitor.'))

print('extra_specs', [(e[0], e[3]) for e in extra_specs])

bs_legs = []
for spec in bs_specs + extra_specs:
    if len(bs_legs) >= 25:
        break
    key, mp, rp, pick, sport, reason = spec
    if str(EIDS.get(key, cache[key][0] and list((get(f'x')).keys()) if False else '')):
        pass
    # skip if event already used
    ev = cache[key][0]
    eid = None
    # peek event id from markets
    for m in cache[key][1].values():
        eid = str(m.get('eventId'))
        break
    if eid in used_events:
        print('skip used', pick)
        continue
    try:
        bs_legs.append(make_leg(key, mp, rp, pick, sport, reason))
    except SystemExit as e:
        print('skip fail', pick, e)
        used_events.discard(eid)
        used_picks.discard(pick)

# If still short of 25, stop at what we have (honesty > padding)
print('Best Shot legs', len(bs_legs))
for i, l in enumerate(bs_legs, 1):
    print(f"  {i}. {l['pick']} {l['odds']:+d} eid={l['eventId']}")

odds, dec = combine([l['odds'] for l in bs_legs])
payout = round(5 * dec, 2)
bs_ticket = {
    'name': 'Best Shot $500K',
    'odds': odds,
    'stake': 5,
    'payout': payout,
    'reason': (
        f'{len(bs_legs)} high-probability legs (NCAAB bought-down cushions around -300 to -480, Friday college MLs at -1800 or longer, and two NHL SOG props). '
        f'Target was $5K–$50K on $5; this slate pays about ${payout:.0f} on $5 ({odds:+d}) after morning tickets burned Thu NHL/NBA/NFL events. '
        f'We stay short of $5K rather than add coin-flip legs. Nothing guaranteed.'
    ),
    'legs': bs_legs,
}

# Sport lottery if we can make +1000 without reuse - skip if not enough events
lottery = [bs_ticket]

# Optional second lottery from leftover heavy MLs - check leftovers
leftover = []
# none required

p['singles'] = singles
p['parlays'] = parlays
p['lottery'] = lottery
p['updated'] = 'Thu Nov 5, 2026 3:00 PM ET'
p['run'] = (
    '3:00 PM ET run (Thursday). Graded Europa Class-Gap Favorites L (Atalanta 1-1 Kairat) and morning Best Shot L '
    '(Milan lost at home; Hajduk lost at Lincoln Red Imps); other morning tickets pending tonight. '
    'Afternoon card: plus-money NFL dog cushions; Lions/Utah/PSU cushions; campus MLs; Friday -1800+ college locks. '
    f'Best Shot ({len(bs_legs)} legs, {odds:+d}, ~${payout:.0f} on $5) stays short of the $5K target because most Thu NHL/NBA events were already used this morning — no coin-flip padding. '
    'Lessons enforced: no -20 college alt spreads, no event reuse, 75%+ lottery legs only.'
)

json.dump(p, open('/workspace/csb/picks.json', 'w'), indent=1)
print('\nWROTE picks.json')
print('singles', len(singles), 'parlays', len(parlays), 'lottery', len(lottery), 'bs legs', len(bs_legs))
print('Best Shot', odds, payout)
print('used events', len(used_events))
print('record', totals['won'], '-', totals['lost'], 'pending', totals['pending'], 'profit', totals['profit'])
