# Claude's Sports Bot — publishing steps
Each leg in picks.json: `marketId` (FanDuel PA, `742.` prefix), `selectionId`, and `marketIdMD` (FanDuel MD, `724.` prefix; selectionId is the same in both states).
The site has a PA/MD toggle (localStorage `csbState`, default PA); MD links use `marketIdMD`, and a leg without it shows the "IDs not verified" fallback.
Every run: write picks.json with PA IDs, then `python3 md_map.py` (fills marketIdMD), then `./publish.sh`.
Links: `https://sportsbook.fanduel.com/addToBetslip?marketId[0]=..&selectionId[0]=..&marketId[1]=..`
