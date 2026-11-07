#!/usr/bin/env python3
"""Sat Nov 7, 2026 3:00 PM ET — grade settled pending tickets + build Saturday afternoon/night card.
Morning card + Fri PM card burned all Sat NBA/NHL events, Mich St/Mich, ND/Miami, WVU/TTU.
Afternoon pool: Sat-night CFB (FBS main feed only), MLS Decision Day (7 PM ET), UFC Vegas card, NCAAB evening."""
import json, copy, datetime, urllib.request, os, sys
from datetime import timezone, timedelta

ET = timezone(timedelta(hours=-5))
K = 'FhMFpcPWXMeyZxOx'
UA = {'User-Agent': 'Mozilla/5.0'}
NOW = datetime.datetime.now(timezone.utc)
CACHE = '/workspace/satpm'
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
        path = f'/workspace/satpm/fresh_ev_{eid}{("_"+tab) if tab else ""}.json'
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
    return any(h.get('name') == name and h.get('date') == date and h.get('run') == run for h in history)

if os.environ.get('KEEP') != '1':
    for f in os.listdir(CACHE):
        if f.startswith('fresh_ev_'):
            os.remove(os.path.join(CACHE, f))

p = json.load(open('/workspace/csb/picks.json'))
H = p['results']['history']

# ============================================================
# STEP 1 — GRADE (finals verified on ESPN scoreboards)
# ============================================================
# key: (date, run, name) -> {'legs': {pick: (result, actual)}, optional 'result','why','lesson'}
GRADES = json.load(open(os.path.join(CACHE, 'grades.json')))

for h in H:
    key = f"{h.get('date')}|{h.get('run')}|{h.get('name')}"
    if key not in GRADES:
        continue
    g = GRADES[key]
    for leg in h.get('legs') or []:
        if leg.get('result') == 'pending' and leg.get('pick') in g.get('legs', {}):
            leg['result'], leg['actual'] = g['legs'][leg['pick']]
    if h.get('result') == 'pending' and g.get('result') in ('won', 'lost'):
        h['result'] = g['result']
        h['whyExplanation'] = g['why']
        h['lesson'] = g['lesson']
        h['profit'] = profit_for(h['odds'], h.get('stake') or 10, g['result'] == 'won')
    elif h.get('result') == 'pending' and g.get('why'):
        h['whyExplanation'] = g['why']

# ============================================================
# STEP 2 — BUILD
# ============================================================
BURNED = set(json.load(open(os.path.join(CACHE, 'burned.json'))))
used_events, used_picks = set(BURNED), set()

def mn_eq(name):
    return lambda mn: mn == name
def mn_pre(prefix):
    return lambda mn: mn.startswith(prefix)
def rn_eq(name):
    return lambda r, m: r.get('runnerName') == name
def rn_hc(name, hc):
    return lambda r, m: r.get('runnerName') == name and float(r.get('handicap') or 0) == hc

def make_leg(eid, market_pred, runner_pred, pick, sport, reason, min_lead_min=60):
    ev, mkts = load_event(eid)
    if not ev:
        raise SystemExit(f'no event {eid} for {pick}')
    sel = find_runner(mkts, market_pred, runner_pred)
    if not sel:
        raise SystemExit(f'no selection for {pick} ({eid})')
    if int(sel['eventId']) in used_events:
        raise SystemExit(f'event reuse {eid} for {pick}')
    if pick in used_picks:
        raise SystemExit(f'pick reuse {pick}')
    t = datetime.datetime.fromisoformat(ev['openDate'].replace('Z', '+00:00'))
    if t < NOW + timedelta(minutes=min_lead_min):
        raise SystemExit(f'start too soon {pick} {ev["openDate"]}')
    used_events.add(int(sel['eventId'])); used_picks.add(pick)
    return {'pick': pick, 'market': sel['market'], 'odds': sel['odds'], 'sport': sport,
            'event': ev['name'], 'start': start_et(ev['openDate']), 'reason': reason,
            'marketId': sel['marketId'], 'selectionId': sel['selectionId'], 'eventId': sel['eventId']}

ALT, ALTT = mn_eq('Alternate Spread'), mn_eq('Alternate Total Points')
ML, DIST = mn_eq('Moneyline'), mn_eq('Will the fight go the distance?')
O15, O25 = mn_eq('Over/Under 1.5 Goals'), mn_eq('Over/Under 2.5 Goals')

# ---------------- SINGLES ----------------
singles = []
for spec in [
    (36260584, ALT, rn_eq('Iowa (-3.5)'), 'Iowa -3.5', 'NCAAF',
     'Northwestern QB Aidan Chiles (100% of NU pass attempts this season, 23 total TDs) is out (ESPN/Thamel), so NU starts a QB with zero 2026 throws vs No. 19 Iowa\'s defense. Main is only Iowa -2.5; buying one point to -3.5 still pays +money and needs just a 4+ point win.'),
    (36260573, ALTT, rn_eq('Under (43.5)'), 'Oklahoma @ Florida Under 43.5', 'NCAAF',
     'Both offenses are broken: OU averages 22 ppg (15th in SEC) and just fired its OC (TE coach Jason Witten calls plays for the first time); Florida switches to QB Tramell Jones Jr. behind a leaky line after 4 turnovers vs UGA, and both lose WRs (Trell Harris, Vernell Brown III out). Under in a game where BOTH offenses are weak is the CFB-under pattern lessons.md allows; one point below the 44.5 main at plus money.'),
    (36260541, ALTT, rn_eq('Under (42.5)'), 'Air Force @ Army Under 42.5', 'NCAAF',
     'Service-academy option offenses shorten the game (lessons.md: ball-control drives limit possessions). Main total 43.5; Under 42.5 at even money in a rivalry where both triple-option teams run clock and defenses know the scheme.'),
]:
    leg = make_leg(*spec); leg['stake'] = 10; singles.append(leg)

# ---------------- PARLAYS ----------------
parlays = []
def add_parlay(name, specs, reason, stake=10):
    legs = [make_leg(*s) for s in specs]
    odds, _ = combine([l['odds'] for l in legs])
    parlays.append({'name': name, 'odds': odds, 'stake': stake, 'legs': legs, 'reason': reason})

add_parlay('MLS Decision Day Goals', [
    (36265602, O25, rn_eq('Over 2.5 Goals'), 'San Diego FC v Sporting KC Over 2.5 Goals', 'Soccer',
     'Sporting KC have conceded 81 goals in 33 (2.45/match, worst in MLS); San Diego score 1.7/match and both are eliminated, so Decision Day is wide open. Market prices O2.5 at -420 (~3.5 expected goals).'),
    (36270445, O15, rn_eq('Over 1.5 Goals'), 'Minnesota Utd v San Jose Over 1.5 Goals', 'Soccer',
     'Minnesota (53 GF/57 GA) must win to keep playoff hopes alive; San Jose (56 GF/48 GA) can climb to 2nd with a win. Both need goals; 2+ goals needed.'),
    (36265603, O15, rn_eq('Over 1.5 Goals'), 'Real Salt Lake v LA Galaxy Over 1.5 Goals', 'Soccer',
     'Win-and-in for the Galaxy (55 GA, leaky) and RSL out with a loss — both must chase. 2+ goals needed.'),
], 'Three Decision Day goals legs where at least one side MUST win and the defenses leak. Goals markets instead of 90-minute MLs (soccer ML lesson). Win-prob first; ~-190 price.')

add_parlay('Night SEC & Pac Cushions', [
    (36244180, ALT, rn_eq('Kentucky (+14.5)'), 'Kentucky +14.5', 'NCAAF',
     'No. 6 Kentucky (7-1, six straight wins, SEC-best turnover margin, least-penalized) gets RB CJ Baxter, WR Nic Anderson and RT Malachi Wood back. Main +5.5; +14.5 is a two-score cushion — would need a 15+ point Tennessee blowout to lose.'),
    (36244152, ALT, rn_eq('Georgia (+7.5)'), 'Georgia +7.5', 'NCAAF',
     'No. 2 Georgia (41 ppg, allows 86 rush yds/g) is the -3.5 favorite; Ole Miss is without RB Kewan Lacy and possibly LB Keaton Thomas/DE Kam Franklin. Georgia +7.5 wins if UGA wins or loses by a TD or less.'),
    (36260556, ALT, rn_eq('Texas State (+14.5)'), 'Texas State +14.5', 'NCAAF',
     'Texas State QB Brad Jackson leads an elite offense that just lost 46-45 to No. 20 Boise. Main +5.5 in a 71.5-total shootout; +14.5 adds 9 points of cushion (≥+9.5 dog-cushion rule).'),
], 'Three dog cushions of ≥+7.5 beyond the main (two-score for KY/TXST) on healthy, high-quality dogs. Lessons: small dog cushions fail; buy to two scores.')

add_parlay('Hoops Bought-Down Hosts', [
    (36289008, mn_pre('Alternate Spread'), rn_hc('Davidson', -2.5), 'Davidson -2.5', 'NCAAB',
     'Davidson -11.5 main / -780 ML at home vs Mercer; -2.5 alt just needs a 3+ point home win (9 points of cushion off the main).'),
    (36289039, mn_pre('Alternate Spread'), rn_hc('UC San Diego', -1.5), 'UC San Diego -1.5', 'NCAAB',
     'UCSD -10.5 main / -610 ML at home vs Fresno State; -1.5 = any home win by 2+.'),
    (36288986, ML, rn_eq('High Point'), 'High Point ML', 'NCAAB',
     'High Point -12.5 / -1100 at home vs Washington State. Clear home class favorite; ML only (no alt market).'),
], 'Three home college favorites bought far below the main (9–10 points of cushion) or on the ML — avoids the -20 alt ban and the mid-major short-fav trap.')

# ---------------- BEST SHOT ----------------
bs_specs = [
    (36260757, ALT, rn_eq('Wisconsin (-7.5)'), 'Wisconsin -7.5', 'NCAAF',
     'Wisconsin -18.5 main / -1250 ML at home; Rutgers lost leading scrimmage threat KJ Duff (26% of yards). -7.5 keeps 11 points of cushion.', 20),
    (36260767, ALT, rn_eq('Mississippi State (+6.5)'), 'Mississippi State +6.5', 'NCAAF',
     'MSU is the -2.5 home favorite (QB Kamario Taylor 17-4 TD-INT, 9.2 YPA); Vanderbilt is down QB Blaze Berlowitz. +6.5 covers any MSU win or a loss by 6 or fewer.', 20),
    (36260759, ALT, rn_eq('Louisiana (+1.5)'), 'Louisiana +1.5', 'NCAAF',
     'Louisiana -7.5 / -285 at home vs South Alabama; +1.5 = Ragin\' Cajuns win (or lose by 1).'),
    (36260531, ALT, rn_eq('Boise State (-6.5)'), 'Boise State -6.5', 'NCAAF',
     'Colorado State has the worst scoring defense in FBS (42.4 ppg) and worst run D per play (258 rush yds/g). Boise (7-1, 35.9 ppg) is without QB Madsen and RB Gaines, but main is still -16.5 — -6.5 leaves 10 points of cushion.'),
    (36260540, ALT, rn_eq('Jacksonville State (-7.5)'), 'Jacksonville State -7.5', 'NCAAF',
     'Jax State (6-2) hosts Sam Houston (1-7). Main -16.5; -7.5 keeps 9 points of cushion.'),
    (36260586, ALT, rn_eq('Louisville (-5.5)'), 'Louisville -5.5', 'NCAAF',
     'Louisville (top-10 offense, 3 straight wins, beat Stanford 52-24) at Georgia Tech (2-6, 3 straight losses, four OL out, 111th in sacks allowed). Main -14.5; -5.5 = 9 points of cushion.'),
    (36260530, ALT, rn_eq('Liberty (-6.5)'), 'Liberty -6.5', 'NCAAF',
     'Liberty (7-1, no injuries listed) at New Mexico State (3-5). Main -15.5; -6.5 = 9 points of cushion.'),
    (36260627, ALT, rn_eq('Arizona State (+4.5)'), 'Arizona State +4.5', 'NCAAF',
     'ASU is the -3.5 home favorite; Colorado is missing WRs Kaleb Mathis and Danny Scudero, RB Micah Welch and DB Braylon Edwards. +4.5 covers an ASU win or a loss by 4 or fewer.'),
    (36260549, ALT, rn_eq('Utah State (+7.5)'), 'Utah State +7.5', 'NCAAF',
     'Pick\'em game at Utah State (strong defense, offense improved with QB McCae Hillstead). +7.5 covers unless Fresno wins by 8+.'),
    (36260638, ALT, rn_eq('Hawaii (+1.5)'), 'Hawaii +1.5', 'NCAAF',
     'UTEP has lost six straight with severe offensive struggles; other books have Hawaii -9.5 vs FanDuel -7.5. +1.5 = Hawaii win.'),
    (36260558, ALT, rn_eq('UNLV (+5.5)'), 'UNLV +5.5', 'NCAAF',
     'UNLV is -3.5 here but -7.5 at other books — FanDuel is short. +5.5 covers a UNLV win or a loss by 5 or fewer at home.'),
    (36270131, O25, rn_eq('Over 2.5 Goals'), 'Austin FC v Portland Over 2.5 Goals', 'Soccer',
     'Portland (60 GF/61 GA) is win-and-in; Austin (42 GF/63 GA) concedes freely and has nothing to play for. Market expects ~3.5 goals.'),
    (36270330, O15, rn_eq('Over 1.5 Goals'), 'Seattle v LAFC Over 1.5 Goals', 'Soccer',
     'Seattle must win to have a playoff chance; LAFC are locked into 6th and can rotate. 2+ goals.'),
    (36265957, O15, rn_eq('Over 1.5 Goals'), 'FC Dallas v Colorado Over 1.5 Goals', 'Soccer',
     'Colorado must win to qualify; Dallas (59 GF/50 GA) need a point. Rapids must open up late. 2+ goals.'),
    (36288990, mn_pre('Alternate Spread'), rn_hc('Furman', 4.5), 'Furman +4.5', 'NCAAB',
     'Furman is the -4.5 home favorite vs Northern Iowa; +4.5 covers any Furman win or a loss by 4 or fewer (9 points of cushion).'),
    (36288737, mn_pre('Alternate Spread'), rn_hc('Providence', 11.5), 'Providence +11.5', 'NCAAB',
     'Providence is only +2.5 at Nebraska; +11.5 is 9 extra points (NBA/NCAAB cushion rule).'),
    (36288757, mn_pre('Alternate Spread'), rn_hc('Georgetown', 12.5), 'Georgetown +12.5', 'NCAAB',
     'Georgetown is +3.5 at home vs Maryland; +12.5 adds 9 points of cushion.'),
    (36289035, mn_pre('Alternate Spread'), rn_hc('UC Irvine', -1.5), 'UC Irvine -1.5', 'NCAAB',
     'UC Irvine -7.5 / -360 at home vs San Jose State; -1.5 = home win by 2+.'),
    (36273712, ML, rn_eq('Seokhyeon Ko'), 'Seokhyeon Ko ML', 'UFC',
     'Ko is -720/-750 everywhere vs Wellington Turman (CBS card). UFC 64%+ favorite filter (ladder 1-0 at +1426).'),
    (36281795, ML, rn_eq('Austin Bashi'), 'Austin Bashi ML', 'UFC',
     'Bashi -590 vs Carlos Calderon; heavy favorite well past the 64% filter.'),
    (36273676, ML, rn_eq('Keiichiro Nakamura'), 'Keiichiro Nakamura ML', 'UFC',
     'Nakamura -360 vs Ollie Schmid (~78% implied).'),
    (36273711, ML, rn_eq('Lucas Fernando'), 'Lucas Fernando ML', 'UFC',
     'Fernando (14-3) -340 vs Billy Elekana; consensus -325 to -340 across books.'),
    (36290047, ML, rn_eq('Lipscomb'), 'Lipscomb ML', 'NCAAB',
     'Lipscomb -8.5 / -385 at home vs SIU-Edwardsville — not a short mid-major favorite (lessons flagged -150 to -300 types); established home program vs OVC visitor.'),
]
bs_legs, bs_skipped = [], []
for spec in bs_specs:
    lead = spec[6] if len(spec) > 6 else 60
    try:
        bs_legs.append(make_leg(*spec[:6], min_lead_min=lead))
    except SystemExit as e:
        bs_skipped.append(f'{spec[3]}: {e}')
print('BS skipped:', bs_skipped)
odds_bs, dec_bs = combine([l['odds'] for l in bs_legs])
payout_5 = round(5 * dec_bs, 2)

# ---------------- SPORT LOTTERY: UFC ----------------
ufc_specs = [
    (36273717, ML, rn_eq('Elijah Smith'), 'Elijah Smith ML', 'UFC',
     'Unbeaten-in-UFC Elijah Smith (10-1, 3-0 UFC) -330 vs 18-8 veteran Davey Grant.'),
    (36273671, ML, rn_eq('Nina Milosevic'), 'Nina Milosevic ML', 'UFC',
     'Milosevic (9-1) -500 vs Priscila Cachoeira (5-9 UFC).'),
    (36273698, DIST, rn_eq('No'), 'Kondratavicius v Petroski: Fight Does Not Go the Distance', 'UFC',
     'Market prices "No" at -590: Kondratavicius is -295 with -220 to win by finish. Safer than his ML.'),
    (36273720, DIST, rn_eq('No'), 'Cortes Acosta v Walker: Fight Does Not Go the Distance', 'UFC',
     'Heavyweights; Walker just won by first-round flying knee and is a KO-or-get-KO\'d fighter, Cortes Acosta has 10 finishes. Over 1.5 rounds is -220, but a finish at some point is -430.'),
    (36273719, DIST, rn_eq('Yes'), 'Suarez v Jandiroba: Fight Goes the Distance', 'UFC',
     'Two elite grapplers who neutralize each other (books: over 2.5 rounds -370); Jandiroba went the distance vs Dern and Ricci.'),
    (36273681, ML, rn_eq('Marcos Degli'), 'Marcos Degli ML', 'UFC',
     'Degli (15-3) -225/-238 vs Mitch Raposo (2-2 UFC). 64%+ filter.'),
    (36273654, ML, rn_eq('Jose Souza'), 'Jose Souza ML', 'UFC',
     'Souza -225 vs Jonny Parsons. 64%+ filter.'),
    (36273684, ML, rn_eq('Karine Silva'), 'Karine Silva ML', 'UFC',
     'Karine Silva -220 vs Gabriella Fernandes; submission threat (-170 to win by sub or points).'),
    (36273688, ML, rn_eq('Thomas Petersen'), 'Thomas Petersen ML', 'UFC',
     'Petersen -164 vs Gabriel Lorenco. Weakest leg on the ticket (62%) — included only to reach the +1000 lottery floor.'),
]
ufc_legs = [make_leg(*s) for s in ufc_specs]
odds_ufc, _ = combine([l['odds'] for l in ufc_legs])

honesty = (f'$5 pays ${payout_5:,.0f}. ' + (
    'SHORT of the $5K target — the 7 PM-onward slate (all NBA/NHL burned by pending tickets) cannot reach $5K without -150 to -250 coin-flip-type legs, so it stops here.'
    if payout_5 < 5000 else 'Inside the $5K–$50K target.'))
lottery = [
    {'name': 'Best Shot $500K', 'odds': odds_bs, 'stake': 5, 'legs': bs_legs,
     'reason': f'{len(bs_legs)} legs, one per event, from unused Sat-night CFB (bought-down favorites / home +points with 9+ points of cushion), MLS Decision Day goals, NCAAB 9-point cushions and UFC heavy favorites (-330 or shorter). No coin-flip MLs, no -20 college alts, no NHL/NBA reuse. ' + honesty},
    {'name': 'UFC Vegas Fight Night Ladder', 'odds': odds_ufc, 'stake': 5, 'legs': ufc_legs,
     'reason': 'UFC 64%+ favorites plus "distance" props where the market is stronger than the ML (UFC ladder pattern 1-0). Sport lottery at +1000 or longer.'},
]

# ---------------- HISTORY APPEND ----------------
D, R = '2026-11-07', '3:00 PM'
def append(entry):
    if not already_in_history(H, entry['name'], D, R):
        H.append(entry)
for s in singles:
    append({'date': D, 'run': R, 'type': 'single', 'name': s['pick'], 'odds': s['odds'], 'stake': 10,
            'result': 'pending', 'profit': 0,
            'legs': [{'pick': s['pick'], 'odds': s['odds'], 'event': s['event'], 'result': 'pending', 'actual': 'plays Saturday night'}],
            'whyExplanation': 'Pending — Saturday 3:00 PM card.', 'lesson': ''})
for t, typ in [(x, 'parlay') for x in parlays] + [(x, 'lottery') for x in lottery]:
    append({'date': D, 'run': R, 'type': typ, 'name': t['name'], 'odds': t['odds'], 'stake': t['stake'],
            'result': 'pending', 'profit': 0,
            'legs': [{'pick': l['pick'], 'odds': l['odds'], 'event': l['event'], 'result': 'pending', 'actual': 'pending'} for l in t['legs']],
            'whyExplanation': 'Pending — Saturday 3:00 PM card.', 'lesson': ''})

totals = recompute_totals(H)
o = totals['overall']
p['updated'] = 'Sat Nov 7, 2026 3:00 PM ET'
p['results']['updated'] = 'Sat Nov 7, 2026 3:00 PM ET'
p['run'] = GRADES.get('_run_text', '') + f' Best Shot {len(bs_legs)} legs ~${payout_5:,.0f} on $5' + (' — short of $5K, no coin-flip pad.' if payout_5 < 5000 else '.')
p['singles'], p['parlays'], p['lottery'] = singles, parlays, lottery
p['results']['totals'] = totals
for k in ('singles', 'parlays', 'lottery'):
    p['results'][k] = copy.deepcopy(totals[k])
p['results']['sources'] = 'FanDuel PA public odds (event-page API, pulled at build); ESPN scoreboards (NCAAF/NCAAB/NHL/NBA 11/7); injury/availability reports (ESPN Thamel, SEC/Big Ten availability, CBS/DK UFC previews, MLSsoccer.com Decision Day scenarios); lessons.md'
p['results']['topLessons'] = GRADES.get('_top_lessons', p['results'].get('topLessons', []))
json.dump(p, open('/workspace/csb/picks.json', 'w'), indent=1)

print('TOTALS', json.dumps(o))
for s in singles: print('SINGLE', s['pick'], s['odds'], s['start'])
for t in parlays: print('PARLAY', t['name'], t['odds'], [(l['pick'], l['odds']) for l in t['legs']])
for t in lottery: print('LOTTO', t['name'], t['odds'], len(t['legs']), [(l['pick'], l['odds']) for l in t['legs']])
print('BS payout $5 ->', payout_5)
