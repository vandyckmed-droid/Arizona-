# Cross-asset ETF / ETP momentum screener

A phone-first ranking sheet for a curated cross-asset ETF/ETP universe, plus a
long-horizon correlation map that shows which of those instruments are really
the same bet.

Four files do the work: a hand-written universe, a thin FMP client, one build
script, and one HTML page. There is no backend, no database and no framework.

```
screener/universe.py   the curated universe: ticker, category, exposure, structure
screener/fmp.py        FMP client (dividend-adjusted daily EOD + quote names)
screener/fetch.py      pulls the histories into data/prices.json
screener/build.py      ranking + correlation -> web/data.json
web/index.html         the phone UI (reads web/data.json, no build step)
```

## Running it

```bash
export API_KEY=<financial modeling prep key>
pip install numpy

python3 screener/fetch.py     # ~15s, one request per ticker
python3 screener/build.py     # ~2s, writes web/data.json
python3 -m http.server -d web 8000
```

`web/data.json` is committed, so the UI runs without an API key. Re-running
`fetch.py` then `build.py` refreshes it. `data/prices.json` is the raw cache and
is gitignored — `build.py` reads it and never calls the network, so the ranking
and correlation work can be re-run offline.

## Method

**Prices.** FMP `stable/historical-price-eod/dividend-adjusted` — a total-return
series, so bond and dividend ETFs are not penalised for their distributions.
About 3.2 calendar years are requested per ticker. Nothing is imputed and
nothing is forward-filled: a null or non-positive print is dropped, and any
series whose last price is older than the reference calendar's last session is
excluded outright rather than carried forward. SPY's dates are the reference
trading calendar. Sessions dated today are not completed sessions and are cut.

**Universe.** 286 hand-picked instruments (cap: 300), spanning broad U.S.
equity, size and style, sectors, industries and subindustries, international and
regional equity, themes, the Treasury duration ladder, IG and high-yield credit,
inflation-linked and international/EM bonds, broad commodity baskets, precious
metals, energy, industrial metals, agriculture, and spot bitcoin and ether ETPs.
Leveraged, inverse, buffered, covered-call and volatility products are left out
by judgment when writing the list, not by a rules engine. Product structure is
not a filter — trusts, ETNs and partnerships are in where they carry a useful
exposure — but each row records a coarse `structure` tag (`fund`, `physical`,
`futures`, `etn`, `equity`) that nothing keys off yet.

Two mechanical filters run in `build.py`: drop anything stale in FMP, and drop
anything whose median dollar volume over the last 60 sessions is under $1M.

**Ranking eligibility** is 253 completed sessions — 252 for the 12–1 lookback
plus the one extra observation the indexing needs. Newer ETPs qualify as soon as
they clear that bar.

**Momentum.** With prices oldest-first and `p[-1]` the last completed session:

| | window | return | vol |
|---|---|---|---|
| 12–1 | `p[-253]` → `p[-22]` | 231 sessions | sd of the 231 daily returns |
| 6–1 | `p[-127]` → `p[-22]` | 105 sessions | sd of the 105 daily returns |

Each score is `return / realized daily vol` of the matching window. Returns and
vols are left un-annualized — the cross-sectional z-score is scale-invariant, so
annualizing would change nothing. The two scores are z-scored separately across
the ranked universe, blended 50/50, and sorted. All categories rank together;
category is display metadata only.

**Correlation eligibility** is separate and stricter: an instrument needs a price
on every one of the last 756 reference sessions. The window is never shortened
to admit newer products. Instruments that can be ranked but not correlated stay
in the ranking, marked with a dot.

**Correlation.** Pearson on raw daily returns over 755 returns spanning 756
aligned sessions. Signed, un-residualized, no benchmark, no factor model, no R².
Grouping is average-linkage (UPGMA) agglomerative clustering cut at ρ ≥ 0.90;
pairs at ρ ≥ 0.98 are additionally listed as near-duplicates. Nothing is deleted
or consolidated — the groups exist to be looked at.

## What the current run produced

286 in the universe → **270 ranked** → **259 with the full 756-session history**.
Sixteen were dropped: five stale in FMP, eleven under the liquidity floor.

Ranked mix: 88 U.S. equity, 77 international equity, 39 credit, 30 commodity,
23 rates, 13 crypto.

**45 groups at ρ ≥ 0.90 and 110 near-duplicate pairs.** The groups reproduce the
obvious structure without being told any of it — gold (GLD/IAU/GLDM/SGOL/BAR,
avg ρ 0.999), silver (SLV/SIVR, 1.000), REITs (VNQ/SCHH/XLRE, 0.991), banks
(KBE/KRE, 0.993), utilities (VPU/XLU, 0.997), long Treasuries (TLT/VGLT/SPTL/
EDV/ZROZ/TLH + BLV + LTPZ, 0.970), high yield (HYG/JNK/USHY/SHYG/SJNK/ANGL/FALN,
0.960), oil (USO/BNO/DBO/DBC/GSG/PDBC/DBE/COMT, 0.935), EM (EEM/IEMG/VWO/SCHE/
AAXJ, 0.972).

## Known limitations

- **T-bill funds dominate the ranking.** SGOV, BIL and SHV take the top three
  slots at blended z ≈ +7.7 to +8.9, with FLOT fourth. Their 12–1 returns are
  ordinary (~3.5%) but realized daily vol is ~0.01%, so `return / vol` explodes.
  This is exactly what the specified formula produces; it is not a bug, and it
  is the first thing to review. It is also amplified by FMP's two-decimal
  rounding, which quantizes near-cash price series (BIL has 146 consecutive
  unchanged closes in 809 sessions, FLOT 169). Two consequences: four near-cash
  instruments squat at the top, and the z-score standard deviation is inflated
  (31.1 with them, 13.2 without), compressing everything else toward zero.
  Relative order *below* those four is barely affected — dropping them from the
  z-score leaves the next nine in almost the same sequence.
- **FMP staleness.** SPLG, IRBO and FM return histories that simply stop
  (2025-10-30, 2024-09-04, 2025-01-08) with no gap or error to signal it. The
  ETNs JO and NIB return a single bar. There were no interior gaps anywhere —
  every series aligns exactly to the SPY calendar from its first date — so the
  only integrity problem found was truncation at the end.
- **Crypto correlation coverage is thin.** Only GBTC and ETHE clear 756 sessions
  (they traded as OTC trusts before converting). The eleven 2024-vintage spot
  ETPs rank but sit outside the correlation matrix, so the obvious IBIT/FBTC/
  BITB/ARKB near-duplication is invisible to it. GBTC/ETHE correlate at 0.79 and
  form no group at ρ ≥ 0.90, which is correct — bitcoin and ether are related
  but not the same bet.
- **Commodity-producer equity is filed as equity.** GDX, COPX, URA, TAN and
  similar are categorised as International Equity, not Commodity. The
  correlation matrix agrees (GDX–GLD is 0.83, not 0.99), but the label may read
  oddly on a commodity screen.
- Category assignment, the $1M liquidity floor, and the 0.90 / 0.98 correlation
  thresholds are all judgment calls, not optimized values.

Not investment advice.
