"""Minimal Financial Modeling Prep client.

Only two things are needed from FMP: a name for each ticker and a daily
dividend-adjusted EOD price series. Nothing here abstracts over providers --
FMP is the source, and swapping it out is not a goal of this version.
"""

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = "https://financialmodelingprep.com/stable/"
TIMEOUT = 60
RETRIES = 4


def _key():
    key = os.environ.get("API_KEY")
    if not key:
        raise SystemExit(
            "API_KEY is not set. It must hold a Financial Modeling Prep API key."
        )
    return key


def _get(path, **params):
    params["apikey"] = _key()
    url = BASE + path + "?" + urllib.parse.urlencode(params)
    last = None
    for attempt in range(RETRIES):
        try:
            with urllib.request.urlopen(url, timeout=TIMEOUT) as resp:
                payload = json.load(resp)
            if isinstance(payload, dict) and ("Error Message" in payload or "error" in payload):
                raise RuntimeError(payload.get("Error Message") or payload.get("error"))
            return payload
        except Exception as exc:  # network hiccups and FMP rate limits alike
            last = exc
            if attempt < RETRIES - 1:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"FMP request failed for {path} {params}: {last}") from last


def daily_adjusted(ticker, start, end):
    """[(date, adjusted_close, volume), ...] oldest first. Empty if FMP has nothing."""
    rows = _get(
        "historical-price-eod/dividend-adjusted",
        symbol=ticker,
        **{"from": start, "to": end},
    )
    if not isinstance(rows, list):
        return []
    out = []
    for r in rows:
        px = r.get("adjClose")
        if px is None or px <= 0:
            continue  # a null or non-positive print is dropped, never imputed
        out.append((r["date"], float(px), float(r.get("volume") or 0.0)))
    out.sort(key=lambda x: x[0])
    return out


def names(tickers):
    """{ticker: name} from batched quotes. Missing tickers are simply absent."""
    out = {}
    for i in range(0, len(tickers), 50):
        chunk = tickers[i:i + 50]
        for row in _get("batch-quote", symbols=",".join(chunk)) or []:
            if row.get("symbol"):
                out[row["symbol"]] = row.get("name") or row["symbol"]
    return out


def composition(ticker):
    """Lightweight composition: sector and country weights, largest first.

    FMP's top-holdings endpoints (etf/holdings, etf/asset-exposure) are not
    available on this key -- they return "Restricted Endpoint". Sector and
    country weightings are, and they answer most of the same question for an
    equity fund. Commodity, bond and currency products report a single
    "Cash & Others 100%" bucket, which carries no information; those come back
    empty rather than pretending otherwise.
    """
    def clean(rows, key):
        out = []
        for r in rows or []:
            label = r.get(key)
            w = r.get("weightPercentage")
            if isinstance(w, str):
                w = w.rstrip("%")
            try:
                w = float(w)
            except (TypeError, ValueError):
                continue
            # "Cash & Others" / "Other" are placeholders, not information, and a
            # weight above 100 is impossible (FMP reports 109.31% US for AMLP).
            if not label or label in ("Cash & Others", "Other", "N/A"):
                continue
            if w <= 0.05 or w > 100:
                continue
            out.append({"label": label, "weight": round(w, 2)})
        out.sort(key=lambda x: -x["weight"])
        return out

    try:
        sectors = clean(_get("etf/sector-weightings", symbol=ticker), "sector")
    except Exception:
        sectors = []
    try:
        countries = clean(_get("etf/country-weightings", symbol=ticker), "country")
    except Exception:
        countries = []
    return {"sectors": sectors[:8], "countries": countries[:6]}


def fetch_all_composition(tickers, workers=8):
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return dict(zip(tickers, pool.map(composition, tickers)))


def fetch_all(tickers, start, end, workers=8):
    """Pull every ticker's history concurrently. Failures come back as []."""
    def one(t):
        try:
            return t, daily_adjusted(t, start, end), None
        except Exception as exc:
            return t, [], str(exc)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(one, tickers))
