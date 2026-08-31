"""Turn the cached FMP prices into the ranked screen and the redundancy map.

Everything is deterministic: same prices in, same web/data.json out. No random
seeds, no iteration to convergence, no fitted models.
"""

import datetime as dt
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from screener import universe

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "data", "prices.json")
OUT = os.path.join(ROOT, "web", "data.json")

# --- momentum windows, in completed trading sessions ------------------------
LAG = 21             # skip the most recent month (the "-1" in 12-1)
LOOK_12 = 252        # ~12 months
LOOK_6 = 126         # ~6 months
MIN_RANK_SESSIONS = LOOK_12 + 1   # 253: the 12-1 window needs a price 252 sessions back

# --- correlation ------------------------------------------------------------
CORR_SESSIONS = 756  # ~3 years of aligned closes -> 755 daily returns
CLUSTER_CORR = 0.90  # average-linkage cut: "these are broadly the same bet"
DUPLICATE_CORR = 0.98  # pairwise: "these are near-interchangeable"
PEERS = 5

# --- liquidity floor --------------------------------------------------------
LIQ_SESSIONS = 60
MIN_DOLLAR_VOLUME = 1_000_000.0


def load():
    with open(CACHE) as fh:
        return json.load(fh)


def window_stats(prices, lookback):
    """(return, daily vol, vol-adjusted score) over the lookback -> LAG window."""
    n = len(prices)
    i0, i1 = n - 1 - lookback, n - 1 - LAG
    p = np.asarray(prices[i0:i1 + 1], dtype=float)
    ret = float(p[-1] / p[0] - 1.0)
    daily = p[1:] / p[:-1] - 1.0
    vol = float(daily.std(ddof=1))
    if not np.isfinite(vol) or vol <= 0:
        return None
    return ret, vol, ret / vol


def zscore(values):
    a = np.asarray(values, dtype=float)
    sd = a.std(ddof=1)
    if sd <= 0:
        return np.zeros_like(a)
    return (a - a.mean()) / sd


def average_linkage(corr, threshold):
    """Agglomerative average-linkage grouping on correlation.

    Merge the two closest clusters while their average pairwise correlation is
    at or above the threshold. Plain UPGMA -- chosen because it is easy to state
    and easy to audit, not because it was tuned.
    """
    n = corr.shape[0]
    members = {i: [i] for i in range(n)}
    d = corr.astype(float).copy()
    np.fill_diagonal(d, -np.inf)

    while len(members) > 1:
        keys = sorted(members)
        sub = d[np.ix_(keys, keys)]
        flat = int(np.argmax(sub))
        i, j = divmod(flat, len(keys))
        if sub[i, j] < threshold:
            break
        a, b = keys[i], keys[j]
        na, nb = len(members[a]), len(members[b])
        # weighted mean keeps d[a, x] equal to the true average pairwise corr
        for x in keys:
            if x in (a, b):
                continue
            d[a, x] = d[x, a] = (na * d[a, x] + nb * d[b, x]) / (na + nb)
        members[a] = members[a] + members[b]
        del members[b]
        d[b, :] = -np.inf
        d[:, b] = -np.inf

    return [sorted(v) for v in members.values()]


def main():
    raw = load()
    prices, names = raw["prices"], raw["names"]
    meta_by_ticker = {r["ticker"]: r for r in universe.as_dicts()}

    reference = prices["SPY"]["dates"]      # SPY is the trading calendar
    last_session = reference[-1]
    corr_dates = reference[-CORR_SESSIONS:]

    excluded, kept = [], {}
    for ticker in universe.tickers():
        rec = prices.get(ticker)
        if not rec or not rec["dates"]:
            excluded.append({"ticker": ticker, "reason": "no price history from FMP"})
            continue
        if rec["dates"][-1] != last_session:
            excluded.append({
                "ticker": ticker,
                "reason": f"stale in FMP -- last price {rec['dates'][-1]}",
            })
            continue
        if len(rec["dates"]) < MIN_RANK_SESSIONS:
            excluded.append({
                "ticker": ticker,
                "reason": f"only {len(rec['dates'])} sessions, need {MIN_RANK_SESSIONS}",
            })
            continue
        dv = float(np.median(
            np.array(rec["close"][-LIQ_SESSIONS:]) * np.array(rec["volume"][-LIQ_SESSIONS:])
        ))
        if dv < MIN_DOLLAR_VOLUME:
            excluded.append({
                "ticker": ticker,
                "reason": f"median dollar volume ${dv/1e6:.2f}M below ${MIN_DOLLAR_VOLUME/1e6:.0f}M floor",
            })
            continue
        kept[ticker] = {"rec": rec, "dollar_volume": dv}

    # ---------------------------------------------------------------- ranking
    rows = []
    for ticker, k in kept.items():
        closes = k["rec"]["close"]
        s12, s6 = window_stats(closes, LOOK_12), window_stats(closes, LOOK_6)
        if s12 is None or s6 is None:
            excluded.append({"ticker": ticker, "reason": "zero realized volatility in window"})
            continue
        m = meta_by_ticker[ticker]
        rows.append({
            "ticker": ticker,
            "name": names.get(ticker, ticker),
            "category": m["category"],
            "exposure": m["exposure"],
            "structure": m["structure"],
            "sessions": len(closes),
            "dollar_volume": round(k["dollar_volume"]),
            "ret12": s12[0], "vol12": s12[1], "score12": s12[2],
            "ret6": s6[0], "vol6": s6[1], "score6": s6[2],
        })

    z12 = zscore([r["score12"] for r in rows])
    z6 = zscore([r["score6"] for r in rows])
    for r, a, b in zip(rows, z12, z6):
        r["z12"], r["z6"] = float(a), float(b)
        r["blend"] = float(0.5 * a + 0.5 * b)

    rows.sort(key=lambda r: (-r["blend"], r["ticker"]))
    for i, r in enumerate(rows, 1):
        r["rank"] = i

    # ------------------------------------------------------------ correlation
    corr_set = set(corr_dates)
    corr_rows = []
    for r in rows:
        rec = kept[r["ticker"]]["rec"]
        have = {d: p for d, p in zip(rec["dates"], rec["close"])}
        if corr_set.issubset(have):
            corr_rows.append((r, np.array([have[d] for d in corr_dates], dtype=float)))
        r["corr_ok"] = False

    tickers_c = [r["ticker"] for r, _ in corr_rows]
    px = np.vstack([p for _, p in corr_rows])
    rets = px[:, 1:] / px[:, :-1] - 1.0
    corr = np.corrcoef(rets)
    corr = np.clip(np.nan_to_num(corr), -1.0, 1.0)

    clusters = average_linkage(corr, CLUSTER_CORR)
    cluster_of = {}
    cluster_out = []
    for cid, members in enumerate(
        sorted(clusters, key=lambda m: -len(m)), start=1
    ):
        if len(members) < 2:
            continue
        pairs = [corr[a, b] for i, a in enumerate(members) for b in members[i + 1:]]
        cluster_out.append({
            "id": cid,
            "label": " / ".join(sorted(tickers_c[i] for i in members)),
            "members": sorted(tickers_c[i] for i in members),
            "size": len(members),
            "min_corr": round(float(min(pairs)), 4),
            "avg_corr": round(float(np.mean(pairs)), 4),
        })
        for i in members:
            cluster_of[tickers_c[i]] = cid

    by_ticker = {r["ticker"]: r for r in rows}
    for i, t in enumerate(tickers_c):
        r = by_ticker[t]
        r["corr_ok"] = True
        r["cluster"] = cluster_of.get(t)
        order = np.argsort(-corr[i])
        r["peers"] = [
            {"ticker": tickers_c[j], "corr": round(float(corr[i, j]), 4)}
            for j in order if j != i
        ][:PEERS]
        j = int(np.argmin(corr[i]))
        r["opposite"] = {"ticker": tickers_c[j], "corr": round(float(corr[i, j]), 4)}

    for r in rows:
        r.setdefault("cluster", None)
        r.setdefault("peers", [])
        r.setdefault("opposite", None)

    duplicates = sorted(
        (
            {"a": tickers_c[i], "b": tickers_c[j], "corr": round(float(corr[i, j]), 4)}
            for i in range(len(tickers_c))
            for j in range(i + 1, len(tickers_c))
            if corr[i, j] >= DUPLICATE_CORR
        ),
        key=lambda d: -d["corr"],
    )

    mix = {}
    for r in rows:
        mix[r["category"]] = mix.get(r["category"], 0) + 1

    payload = {
        "meta": {
            "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "price_source": raw["source"],
            "prices_fetched_at": raw["fetched_at"],
            "last_session": last_session,
            "universe_size": len(universe.UNIVERSE),
            "ranked": len(rows),
            "correlation_eligible": len(tickers_c),
            "correlation_sessions": len(corr_dates),
            "correlation_returns": int(rets.shape[1]),
            "correlation_window": [corr_dates[0], corr_dates[-1]],
            "min_rank_sessions": MIN_RANK_SESSIONS,
            "cluster_threshold": CLUSTER_CORR,
            "duplicate_threshold": DUPLICATE_CORR,
            "min_dollar_volume": MIN_DOLLAR_VOLUME,
            "category_mix": mix,
            "excluded": sorted(excluded, key=lambda e: e["ticker"]),
        },
        "rows": rows,
        "clusters": sorted(cluster_out, key=lambda c: (-c["size"], c["label"])),
        "duplicates": duplicates,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(payload, fh, separators=(",", ":"))

    print(f"ranked {len(rows)} of {len(universe.UNIVERSE)} | "
          f"correlation-eligible {len(tickers_c)} over {len(corr_dates)} sessions "
          f"({rets.shape[1]} returns)")
    print(f"clusters (rho>={CLUSTER_CORR}): {len(cluster_out)} | "
          f"near-duplicate pairs (rho>={DUPLICATE_CORR}): {len(duplicates)}")
    print(f"excluded {len(excluded)}: " + ", ".join(e["ticker"] for e in payload["meta"]["excluded"]))
    print(f"wrote {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
