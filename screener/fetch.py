"""Download the universe's price history from FMP into data/prices.json.

Kept separate from build.py so the ranking and correlation work can be re-run
offline without hitting the API again.
"""

import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from screener import fmp, universe

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "data", "prices.json")

# ~3.2 calendar years of calendar days. 756 completed sessions is a little under
# three years, so this leaves margin for holidays without pulling a fourth year.
LOOKBACK_DAYS = 1180


def main():
    today = dt.date.today()
    start = (today - dt.timedelta(days=LOOKBACK_DAYS)).isoformat()
    end = today.isoformat()
    tickers = universe.tickers()

    print(f"fetching {len(tickers)} tickers from FMP ({start} .. {end})")
    results = fmp.fetch_all(tickers, start, end)
    names = fmp.names(tickers)
    print("fetching composition (sector / country weights)")
    comps = fmp.fetch_all_composition(tickers)

    prices, problems = {}, []
    for ticker, rows, err in results:
        if err:
            problems.append(f"{ticker}: request failed -- {err}")
            continue
        if not rows:
            problems.append(f"{ticker}: FMP returned no price history")
            continue
        # A session dated today is not a completed session yet.
        rows = [r for r in rows if r[0] < end]
        prices[ticker] = {
            "dates": [r[0] for r in rows],
            "close": [r[1] for r in rows],
            "volume": [r[2] for r in rows],
        }

    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    with open(CACHE, "w") as fh:
        json.dump(
            {
                "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                "source": "FMP stable/historical-price-eod/dividend-adjusted",
                "start": start,
                "end": end,
                "names": names,
                "composition": comps,
                "prices": prices,
                "problems": problems,
            },
            fh,
        )

    print(f"cached {len(prices)} tickers -> {os.path.relpath(CACHE, ROOT)}")
    for p in problems:
        print("  !", p)


if __name__ == "__main__":
    main()
