# Claude's Sports Bot — publishing steps
Each leg in picks.json: `marketId` (FanDuel PA, `742.` prefix), `selectionId`, and `marketIdMD` (FanDuel MD, `724.` prefix; selectionId is the same in both states).
The site has a PA/MD toggle (localStorage `csbState`, default PA); MD links use `marketIdMD`, and a leg without it shows the "IDs not verified" fallback.
Every run: write picks.json with PA IDs, then `python3 md_map.py` (fills marketIdMD), then `./publish.sh`.
Links: `https://sportsbook.fanduel.com/addToBetslip?marketId[0]=..&selectionId[0]=..&marketId[1]=..`

## Results schema (`results` in picks.json) — PERMANENT, never delete history
- `history[]`: one entry per graded ticket, appended every run (keep old entries when replacing today's picks):
  `{date:"YYYY-MM-DD", run:"10:30 AM"|"3:00 PM", type:"single"|"parlay"|"lottery", name, odds, stake, result:"won"|"lost"|"pending"|"push", profit, legs:[{pick, odds, event, result:"hit"|"miss"|"pending"|"void", actual}], whyExplanation, lesson}`
  Singles are tracked at a $10 notional stake. profit = payout - stake if won, -stake if lost, 0 if pending.
- `totals`: `{singles, parlays, lottery, overall}` each `{won, lost, pending, winPct, staked, profit, roiPct}`, plus `legs:{hit,miss,pending,void}` (void = postponed/cancelled leg, removed by FanDuel). Recompute from history every run. (`singles/parlays/lottery` top-level copies kept for back-compat.)
- `topLessons[]`, `updated`, `sources`.
- Grade only with verified finals (ESPN box scores/play-by-play, official league/club sites). Unverifiable legs stay `pending`; a ticket is `lost` once any leg misses, `won` only when all legs hit.
- Before posting new picks, re-grade pending items, append to `lessons.md`, and apply the lessons there.
