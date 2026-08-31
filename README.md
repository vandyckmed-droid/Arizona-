# Cross-asset ETF / ETP momentum screener

A phone-first ranking sheet for a deliberately compact cross-asset ETF/ETP
universe — 81 instruments, one per distinct economic bet — plus a
long-horizon correlation map that shows which of those instruments are really
the same bet.

Five small files do the work: a hand-written universe, a thin FMP client, one
build script, one HTML page, and a bundler. There is no backend, no database
and no framework.

```
screener/universe.py   the curated universe: ticker, category, exposure, structure
screener/fmp.py        FMP client (dividend-adjusted daily EOD + quote names)
screener/fetch.py      pulls the histories into data/prices.json
screener/build.py      ranking + correlation + chart series -> web/data.json
screener/app.html      the phone UI (one file, no framework)
screener/artifact.py   inlines data.json into app.html -> web/index.html
```

`web/index.html` is generated, not hand-edited: change `screener/app.html` and
re-run `artifact.py`.

## Running it

```bash
export API_KEY=<financial modeling prep key>
pip install numpy

python3 screener/fetch.py     # ~15s, one request per ticker
python3 screener/build.py     # ~2s, writes web/data.json
python3 screener/artifact.py  # writes web/index.html, self-contained
```

`web/index.html` is one ~915 KB file with the data inlined. Open it straight off
disk or drop it on any static host -- it needs no server and makes no network
call except the Google Fonts stylesheet. It is a generated bundle and is
gitignored; `web/data.json` is committed, so one `artifact.py` run rebuilds the
page without an API key. `data/prices.json` is the raw cache and
is gitignored — `build.py` reads it and never calls the network, so the ranking
and correlation work can be re-run offline.

`build.py` is a pure function of the cached prices, down to the bytes: it writes
no build timestamp, so re-running it on unchanged prices leaves `web/data.json`
untouched and `git status` clean. That keeps a dirty working tree meaningful —
it means the numbers moved. Freshness is reported by `prices_fetched_at` and
`last_session`, which describe the data rather than the moment the script ran.

## Method

**Composition.** FMP's top-holdings endpoints (`etf/holdings`,
`etf/asset-exposure`) are **restricted on this API key** and return
"Restricted Endpoint". Sector and country weightings are available, and answer
most of the same question: EEM's page shows 26.8% Taiwan, 20.6% Korea and 42.3%
technology, which tells you it is largely a semiconductor bet. 56 rows carry
sector weights and 70 carry country weights; the 10 that carry neither are the
metals, futures and crypto products, where there is genuinely nothing to look
through to.

Sector weights are attached **only for equity funds**, because FMP returns
confident nonsense elsewhere — DBA, an agriculture futures fund, comes back
16.8% Healthcare; HYG, a broad high-yield bond fund, comes back 99.6%
Utilities. Country weights survive on bond funds, where they are informative
(EMB, EMLC and BNDX all break down sensibly). Placeholder buckets
("Cash & Others", "Other") and impossible weights are dropped — FMP reports
AMLP as 109.31% United States.

**Prices.** FMP `stable/historical-price-eod/dividend-adjusted` — a total-return
series, so bond and dividend ETFs are not penalised for their distributions.
About 3.2 calendar years are requested per ticker. Nothing is imputed and
nothing is forward-filled: a null or non-positive print is dropped, and any
series whose last price is older than the reference calendar's last session is
excluded outright rather than carried forward. SPY's dates are the reference
trading calendar. Sessions dated today are not completed sessions and are cut.

**Universe.** 81 instruments, hard-capped at 100, built around **distinct
economic bets rather than coverage**. One canonical fund per exposure: SPY/VOO/
IVV/VTI are one bet, not four. Two funds stay only when the constructions are
genuinely different — cap-weight beside equal weight (SPY/RSP), a sector beside
a narrower industry inside it (XLE/XOP), spot metal beside the miners
(GLD/GDX).

Every row states the bet it exists to express, in `universe.py` and on the
instrument's page. The test is simple: if the reason does not survive being
written down, the row does not belong. Rows also carry a `group` (the design
bucket), a short display `name`, and a coarse `structure` tag.

| group | n |
|---|---|
| U.S. broad / style / factors | 11 |
| U.S. sectors | 11 |
| Distinct industries and themes | 18 |
| International, regions, countries | 15 |
| Rates, bonds, credit | 13 |
| Commodities | 8 |
| Other macro bets | 3 |
| Crypto | 2 |

Leveraged, inverse, buffered, covered-call and volatility products are left out
by judgment when writing the list, not by a rules engine. Structure is not a
filter — trusts and partnerships are in where they carry a distinct exposure.

Two mechanical filters run in `build.py`: drop anything stale in FMP, and drop
anything whose median dollar volume over the last 60 sessions is under $1M. On
the current universe neither fires — all 81 are current and liquid.

**Correlation is a cleanup pass on this list, not the way it was designed.** It
tells you two funds moved together over one particular three years; it cannot
tell you they are the same bet. It removed exactly one name: Russell 1000 Growth
(IWF), which correlated 0.973 with QQQ on a near-identical sector profile —
55% vs 59% technology — making it the same bet with a different listing venue.
Growth is now expressed by QQQ, value by IWD, breadth by RSP.

**Ranking eligibility** is 253 completed sessions — 252 for the 12–1 lookback
plus the one extra observation the indexing needs. Newer ETPs qualify as soon as
they clear that bar. That single bar is set by the longest window and applies to
all three, so an instrument that can be ranked can be ranked on any of them.
Switching windows in the UI therefore never changes the population, and a
z-score always means the same thing relative to the same 270 names.

**Momentum.** Three windows, all ending 21 sessions back. With prices
oldest-first and `p[-1]` the last completed session:

| | window | daily returns |
|---|---|---|
| 12–1 | `p[-253]` → `p[-22]` | 231 |
| 9–1 | `p[-190]` → `p[-22]` | 168 |
| 6–1 | `p[-127]` → `p[-22]` | 105 |

Each window yields two measures: the **raw return**, and the **vol-adjusted**
`return / realized daily vol` of that same window. Returns and vols are left
un-annualized — the cross-sectional z-score is scale-invariant, so annualizing
would change nothing.

**Both measures are z-scored per window across the ranked universe, and only
z-scores are ever averaged.** That is what makes an equal-weighted blend
actually equal. A raw 12–1 return is mechanically larger than a raw 6–1 return
simply because it covers twice the ground, so averaging the raw numbers would
hand the longest window the loudest vote without anyone choosing that.
Standardising each window first puts them on the same footing. With one window
selected the z-score is a monotone transform of the underlying value, so the
ordering is exactly the raw ordering of that measure.

All categories rank together; category is display metadata only.

**The chart series** is the last 378 sessions per instrument (~18 months: the
253-session 12-1 window plus lead-in), rebased to 1.0 at the 12-1 entry price so
the 12-1 return reads straight off the y-axis. Every series aligns to the same
reference calendar, so the dates are stored once and a short history is placed
by its offset -- never padded or filled. The returns the chart draws reproduce
the ranking's own numbers exactly.

**Correlation eligibility** is separate and stricter: an instrument needs a price
on every one of the last 756 reference sessions. The window is never shortened
to admit newer products. Instruments that can be ranked but not correlated stay
in the ranking, marked with a dot.

**Correlation.** Pearson on raw daily returns over 755 returns spanning 756
aligned sessions. Signed, un-residualized, no benchmark, no factor model, no R².
Grouping is average-linkage (UPGMA) agglomerative clustering cut at ρ ≥ 0.90;
pairs at ρ ≥ 0.98 are additionally listed as near-duplicates. Nothing is deleted
or consolidated — the groups exist to be looked at.

## The UI

Two controls sit above the ranking: **measure** (vol-adjusted or raw return) and
**windows** (any non-empty combination of 12–1, 9–1 and 6–1, equally weighted).
The default is vol-adjusted 12–1 + 6–1, which is the original brief's ranking.
The choice persists per browser, and the twelve reachable combinations were
checked against an independent Python computation of the same orderings.

Raw-return mode is the honest answer to the T-bill problem below: the same four
near-cash names that lead the vol-adjusted table sit at ranks 153–160 on raw
return, which is where their returns alone put them.

The ranking is a list; tapping a row opens that instrument, tapping the star
adds it to a watchlist.

The per-ticker view draws the price line with the selected windows shaded in
place. They all end at the same point, so they nest: 12–1, then 9–1, then 6–1,
each a step darker, with the last 21 sessions hatched to mark what every window
deliberately skips. Bracket rails under the plot label each with its return, and
a table below lists all three windows — including the ones currently switched
off, which is often the interesting part. Gold ranked on 9–1 + 6–1 shows the
point: +20.9% over 12 months, −21.9% over 6. It is the quickest way to see
why something ranks where it does -- IBIT shows a -42% 12-1 window with a sharp
rebound sitting entirely inside the skipped zone.

The watchlist lives in `localStorage`: per-viewer, private to that browser,
never transmitted. It survives reloads and republishes, and it is deliberately
not shared state -- a watchlist is one person's, and the page has no business
publishing it. Reads and writes are wrapped, so blocked storage (private
windows, browsers that refuse site data) degrades to a working session that
simply does not remember.

Category is shown as text on every row and drives the filter chips. An earlier
draft also colour-coded it with a six-hue stripe; that palette failed
colour-vision and normal-vision separation on the all-pairs test, and since the
category is already named in words the stripe was carrying no information, so it
was dropped rather than re-stepped.

## What the current run produced

**81 in the universe → 81 ranked → 79 with the full 756-session history.**
Nothing was dropped for staleness or liquidity. The two without full history are
IBIT and ETHA, the January-2024 spot crypto ETFs.

Display mix: 37 U.S. equity, 20 international equity, 8 credit, 8 commodity,
5 rates, 1 macro, 2 crypto.

**Zero near-duplicate pairs at ρ ≥ 0.98**, down from 110 in the 286-name
version — the issuer duplication is gone. Seven groups remain at ρ ≥ 0.90, and
each is a real economic overlap rather than a wrapper artifact:

| group | avg ρ | why both stay |
|---|---|---|
| IEF / LQD / MBB / TLT | 0.914 | one duration factor dominated 2023–26; credit and convexity separate in other regimes |
| IJH / IWD / IWM / RSP | 0.922 | the whole "not mega-cap tech" complex |
| QQQ / SMH / XLK | 0.932 | concentration, industry and sector views of the same names |
| QUAL / SPY | 0.968 | quality screened out to near-market beta |
| KWEB / MCHI | 0.949 | KWEB is regulatory risk, MCHI is broad China |
| SCZ / VGK | 0.915 | SCZ is ~40% Europe by weight |
| XLE / XOP | 0.930 | integrated majors vs equal-weight producers |

## Known limitations

- **T-bill funds dominate the vol-adjusted ranking.** SGOV, BIL and SHV take the
  top three slots at blended z ≈ +7.7 to +8.9, with FLOT fourth. Switching the
  measure to raw return drops them to 153–160, so the screen now has an answer
  to this even though the underlying point stands. Their 12–1 returns are
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
- **Crypto is invisible to the correlation matrix.** IBIT and ETHA are the
  canonical spot products but launched in 2024, so neither clears 756 sessions.
  The legacy trusts GBTC and ETHE do have the history, at much higher fees.
  Canonical-instrument won over correlation coverage here; swapping them is a
  one-line change if you would rather see crypto in the redundancy map.
- **Commodity-producer equity is filed as equity.** GDX, COPX, URA, TAN and
  similar are categorised as International Equity, not Commodity. The
  correlation matrix agrees (GDX–GLD is 0.83, not 0.99), but the label may read
  oddly on a commodity screen.
- **UNG is path-dependent by construction.** Front-month natural gas futures
  roll at a persistent loss, so part of what the screen measures for UNG is roll
  decay rather than the gas price. The brief excludes highly path-dependent
  products; I kept it because there is no liquid alternative and natural gas is
  too distinct a macro bet to omit. Worth an explicit decision.
- **QUAL correlates 0.968 with SPY.** It survived the cleanup because a quality
  screen is a genuinely different construction, but on this evidence it is the
  weakest row in the universe and the first thing to cut if the count needs to
  come down.
- **The value/growth axis is asymmetric.** Cutting IWF leaves a named value fund
  (IWD) with no named growth counterpart; QQQ carries the growth leg.
- **PFF loses its sector breakdown** to the equity-only gate on sector weights.
  It holds preferred stock, so sectors would be meaningful, but a per-fund
  exception was not worth the complexity.
- Category assignment, the $1M liquidity floor, and the 0.90 / 0.98 correlation
  thresholds are all judgment calls, not optimized values.

Not investment advice.
