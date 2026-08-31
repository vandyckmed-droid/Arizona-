"""Curated cross-asset ETF / ETP universe, built around distinct economic bets.

One canonical fund per exposure. Issuer duplication is removed on principle --
SPY/VOO/IVV/VTI are one bet, not four -- but two funds stay when they express
genuinely different constructions or different bets: cap-weight beside equal
weight, a sector beside a narrow industry inside it, spot metal beside the
miners. Every row carries the reason it is here; if the reason does not survive
being written down, the row does not belong.

The 756-session correlation matrix is a cleanup check on this list, not the way
it was designed. Correlation tells you two funds moved together over one
particular three years; it cannot tell you whether they are the same bet.

Each row is (ticker, name, group, category, bet, structure).

name      -- short, human-readable label for display.
group     -- the design bucket this was chosen to fill.
category  -- broad asset class for display and filtering. Never affects ranking.
bet       -- the distinct economic exposure this ticker exists to express.
structure -- best-effort product structure. Nothing keys off it yet.
             fund     conventional open-end ETF
             physical spot / physically backed trust
             futures  futures-based product
             equity   listed-equity proxy for a commodity or theme
             partnership  MLP / LP structure

Excluded throughout, by judgment rather than by a rules engine: leveraged and
inverse products, buffered and other path-dependent payoffs, covered-call and
options-income funds, volatility products, and anything whose exposure is
already fully expressed by another row. A liquidity floor is applied separately
in build.py from the price history itself.
"""

UNIVERSE = [
    # ============================================================ U.S. broad, style, factors (12)
    ("SPY",  "S&P 500",              "U.S. broad/style/factors", "U.S. Equity",
     "U.S. large-cap beta, the default equity exposure", "fund"),
    ("RSP",  "S&P 500 Equal Weight", "U.S. broad/style/factors", "U.S. Equity",
     "The same 500 names without mega-cap concentration -- a different bet, not a different wrapper", "fund"),
    ("QQQ",  "Nasdaq 100",           "U.S. broad/style/factors", "U.S. Equity",
     "Mega-cap growth and tech concentration", "fund"),
    ("IWM",  "Russell 2000",         "U.S. broad/style/factors", "U.S. Equity",
     "U.S. small cap: domestic revenue, floating-rate debt, higher beta", "fund"),
    ("IJH",  "S&P MidCap 400",       "U.S. broad/style/factors", "U.S. Equity",
     "Mid cap, which behaves like neither large nor small", "fund"),
    ("IWD",  "Russell 1000 Value",   "U.S. broad/style/factors", "U.S. Equity",
     "Value style: cheap multiples, cyclical and financial tilt. The growth leg is QQQ -- "
     "Russell 1000 Growth was cut for correlating 0.973 with it on a near-identical sector profile",
     "fund"),
    ("MTUM", "Momentum Factor",      "U.S. broad/style/factors", "U.S. Equity",
     "Systematic momentum -- the benchmark this screen should be measured against", "fund"),
    ("QUAL", "Quality Factor",       "U.S. broad/style/factors", "U.S. Equity",
     "High return on equity and stable earnings", "fund"),
    ("USMV", "Min Volatility",       "U.S. broad/style/factors", "U.S. Equity",
     "Low-beta defensive equity", "fund"),
    ("COWZ", "Free Cash Flow Yield", "U.S. broad/style/factors", "U.S. Equity",
     "Cash-flow value, which behaves differently from book-value value", "fund"),
    ("SCHD", "Dividend Quality",     "U.S. broad/style/factors", "U.S. Equity",
     "Dividend payers with balance-sheet screens: the income equity bet", "fund"),

    # ============================================================ U.S. sectors (11)
    ("XLK",  "Technology",           "U.S. sectors", "U.S. Equity",
     "Technology sector", "fund"),
    ("XLF",  "Financials",           "U.S. sectors", "U.S. Equity",
     "Financials sector", "fund"),
    ("XLV",  "Health Care",          "U.S. sectors", "U.S. Equity",
     "Health care sector", "fund"),
    ("XLE",  "Energy",               "U.S. sectors", "U.S. Equity",
     "Energy sector: integrated majors and large producers", "fund"),
    ("XLI",  "Industrials",          "U.S. sectors", "U.S. Equity",
     "Industrials sector", "fund"),
    ("XLY",  "Consumer Discretionary", "U.S. sectors", "U.S. Equity",
     "Consumer discretionary sector", "fund"),
    ("XLP",  "Consumer Staples",     "U.S. sectors", "U.S. Equity",
     "Consumer staples: the defensive consumer bet", "fund"),
    ("XLU",  "Utilities",            "U.S. sectors", "U.S. Equity",
     "Utilities: bond-proxy equity and power demand", "fund"),
    ("XLB",  "Materials",            "U.S. sectors", "U.S. Equity",
     "Materials sector", "fund"),
    ("XLRE", "Real Estate",          "U.S. sectors", "U.S. Equity",
     "U.S. REITs and real estate", "fund"),
    ("XLC",  "Communication Services", "U.S. sectors", "U.S. Equity",
     "Communication services sector", "fund"),

    # ============================================================ distinct industries and themes (18)
    ("SMH",  "Semiconductors",       "Industries/themes", "U.S. Equity",
     "Semis: the cyclical core of technology, far more volatile than the sector", "fund"),
    ("IGV",  "Software",             "Industries/themes", "U.S. Equity",
     "Software: recurring revenue, the other half of tech and uncorrelated with semis", "fund"),
    ("CIBR", "Cyber Security",       "Industries/themes", "U.S. Equity",
     "Security spending, which holds up through IT budget cuts", "fund"),
    ("XBI",  "Biotech",              "Industries/themes", "U.S. Equity",
     "Equal-weight biotech: binary clinical risk and rate sensitivity, unlike large-cap pharma", "fund"),
    ("IHI",  "Medical Devices",      "Industries/themes", "U.S. Equity",
     "Devices: procedure volumes rather than drug pipelines", "fund"),
    ("KRE",  "Regional Banks",       "Industries/themes", "U.S. Equity",
     "Deposit funding, net interest margin and credit -- a different bet from XLF's money centres", "fund"),
    ("KIE",  "Insurance",            "Industries/themes", "U.S. Equity",
     "Underwriting and float, which earn more as rates rise", "fund"),
    ("ITA",  "Aerospace & Defense",  "Industries/themes", "U.S. Equity",
     "Defence budgets and aircraft build rates", "fund"),
    ("JETS", "Airlines",             "Industries/themes", "U.S. Equity",
     "Airlines: fuel costs, labour and travel demand", "fund"),
    ("XRT",  "Retail",               "Industries/themes", "U.S. Equity",
     "Equal-weight retail: actual store economics, not XLY's Amazon and Tesla weighting", "fund"),
    ("ITB",  "Homebuilders",         "Industries/themes", "U.S. Equity",
     "Housing starts and mortgage rates", "fund"),
    ("XOP",  "Oil & Gas E&P",        "Industries/themes", "U.S. Equity",
     "Equal-weight producers: direct leverage to the oil price, unlike the integrated majors", "fund"),
    ("OIH",  "Oil Services",         "Industries/themes", "U.S. Equity",
     "Drilling and completion capex, which cycles later than the oil price", "fund"),
    ("XME",  "Metals & Mining",      "Industries/themes", "U.S. Equity",
     "Steel, coal and base metals producers", "equity"),
    ("GDX",  "Gold Miners",          "Industries/themes", "International Equity",
     "Operationally geared to the gold price -- correlates ~0.83 with bullion, not ~1.0", "equity"),
    ("URA",  "Uranium",              "Industries/themes", "International Equity",
     "Nuclear fuel and the power-demand build-out", "equity"),
    ("ICLN", "Clean Energy",         "Industries/themes", "International Equity",
     "Renewable generation and equipment: a rate-sensitive capex bet", "fund"),
    ("AMLP", "Midstream MLPs",       "Industries/themes", "U.S. Equity",
     "Pipeline toll-road cash flows, tied to volumes rather than the commodity price", "partnership"),

    # ============================================================ international, regions, countries (15)
    ("VGK",  "Europe",               "International/regions", "International Equity",
     "Developed Europe", "fund"),
    ("EWU",  "United Kingdom",       "International/regions", "International Equity",
     "Sterling, plus an index dominated by energy, pharma and banks", "fund"),
    ("EWJ",  "Japan",                "International/regions", "International Equity",
     "Japan: governance reform, the yen and a distinct monetary cycle", "fund"),
    ("EWC",  "Canada",               "International/regions", "International Equity",
     "Developed-market resource and banking economy", "fund"),
    ("EWA",  "Australia",            "International/regions", "International Equity",
     "Iron ore, banks and the China-demand channel", "fund"),
    ("SCZ",  "Developed Small Cap",  "International/regions", "International Equity",
     "Ex-U.S. small cap: domestic European and Japanese economies, not global exporters", "fund"),
    ("EEM",  "Emerging Markets",     "International/regions", "International Equity",
     "Broad EM beta", "fund"),
    ("MCHI", "China",                "International/regions", "International Equity",
     "China all-share", "fund"),
    ("KWEB", "China Internet",       "International/regions", "International Equity",
     "China's platform companies, driven by regulation as much as by growth", "fund"),
    ("INDA", "India",                "International/regions", "International Equity",
     "India: domestic demand, structurally uncorrelated with China", "fund"),
    ("EWT",  "Taiwan",               "International/regions", "International Equity",
     "The semiconductor supply chain, plus geopolitical risk", "fund"),
    ("EWY",  "South Korea",          "International/regions", "International Equity",
     "Memory, shipbuilding and autos: the cyclical export bet", "fund"),
    ("EWZ",  "Brazil",               "International/regions", "International Equity",
     "Commodity EM with a high domestic rate cycle", "fund"),
    ("EWW",  "Mexico",               "International/regions", "International Equity",
     "The nearshoring and U.S.-linked EM bet", "fund"),
    ("VNM",  "Vietnam",              "International/regions", "International Equity",
     "Frontier manufacturing and the supply-chain shift out of China", "fund"),

    # ============================================================ rates, bonds, credit (13)
    ("BIL",  "T-Bills",              "Rates/bonds/credit", "Rates",
     "Cash and the front end of the curve", "fund"),
    ("SHY",  "Treasuries 1-3y",      "Rates/bonds/credit", "Rates",
     "Short duration: the policy-rate bet", "fund"),
    ("IEF",  "Treasuries 7-10y",     "Rates/bonds/credit", "Rates",
     "Intermediate duration, the belly of the curve", "fund"),
    ("TLT",  "Treasuries 20y+",      "Rates/bonds/credit", "Rates",
     "Long duration: the purest rates and term-premium bet", "fund"),
    ("TIP",  "TIPS",                 "Rates/bonds/credit", "Rates",
     "Real yields and breakeven inflation", "fund"),
    ("MBB",  "Agency MBS",           "Rates/bonds/credit", "Credit",
     "Mortgage convexity, which is not the same as Treasury duration", "fund"),
    ("LQD",  "IG Corporates",        "Rates/bonds/credit", "Credit",
     "Investment-grade spread plus long duration", "fund"),
    ("HYG",  "High Yield",           "Rates/bonds/credit", "Credit",
     "Credit risk: the equity-like leg of the bond market", "fund"),
    ("BKLN", "Senior Loans",         "Rates/bonds/credit", "Credit",
     "Floating-rate credit -- spread risk with the duration stripped out", "fund"),
    ("PFF",  "Preferred Stock",      "Rates/bonds/credit", "Credit",
     "Hybrid bank capital: subordinated credit and duration together", "fund"),
    ("EMB",  "EM Sovereign USD",     "Rates/bonds/credit", "Credit",
     "Sovereign credit spread without the currency", "fund"),
    ("EMLC", "EM Local Currency",    "Rates/bonds/credit", "Credit",
     "EM local rates and EM FX -- the currency bet EMB deliberately excludes", "fund"),
    ("BNDX", "Intl Bonds (Hedged)",  "Rates/bonds/credit", "Credit",
     "Non-U.S. developed duration, currency-hedged", "fund"),

    # ============================================================ commodities (8)
    ("PDBC", "Broad Commodities",    "Commodities", "Commodity",
     "Diversified commodity basket", "futures"),
    ("GLD",  "Gold",                 "Commodities", "Commodity",
     "Monetary metal: real rates and debasement", "physical"),
    ("SLV",  "Silver",               "Commodities", "Commodity",
     "Half monetary, half industrial -- a higher-beta cousin of gold", "physical"),
    ("PPLT", "Platinum",             "Commodities", "Commodity",
     "Autocatalyst and industrial precious metal with its own supply story", "physical"),
    ("USO",  "Crude Oil",            "Commodities", "Commodity",
     "WTI crude", "futures"),
    ("UNG",  "Natural Gas",          "Commodities", "Commodity",
     "U.S. natural gas: weather, storage and LNG export demand", "futures"),
    ("CPER", "Copper",               "Commodities", "Commodity",
     "The industrial-cycle and electrification metal", "futures"),
    ("DBA",  "Agriculture",          "Commodities", "Commodity",
     "Grains and softs: a weather-driven basket uncorrelated with everything else", "futures"),

    # ============================================================ other distinct macro bets (3)
    ("UUP",  "US Dollar",            "Other macro", "Macro",
     "The dollar itself -- nothing else in the universe expresses it directly", "futures"),
    ("IGF",  "Global Infrastructure", "Other macro", "International Equity",
     "Regulated real assets with inflation-linked cash flows", "fund"),
    ("VNQI", "Intl Real Estate",     "Other macro", "International Equity",
     "Property outside the U.S., where XLRE does not reach", "fund"),

    # ============================================================ crypto (2)
    ("IBIT", "Bitcoin",              "Crypto", "Crypto",
     "Spot bitcoin", "physical"),
    ("ETHA", "Ether",                "Crypto", "Crypto",
     "Spot ether, which trades on its own cycle rather than as bitcoin beta", "physical"),
]

MAX_UNIVERSE = 100

CATEGORIES = ["U.S. Equity", "International Equity", "Rates", "Credit",
              "Commodity", "Macro", "Crypto"]

GROUPS = ["U.S. broad/style/factors", "U.S. sectors", "Industries/themes",
          "International/regions", "Rates/bonds/credit", "Commodities",
          "Other macro", "Crypto"]


def tickers():
    return [row[0] for row in UNIVERSE]


def as_dicts():
    return [
        {"ticker": t, "name": n, "group": g, "category": c, "bet": b, "structure": s}
        for t, n, g, c, b, s in UNIVERSE
    ]


def _check():
    seen, dupes = set(), []
    for t, n, g, c, b, _ in UNIVERSE:
        if t in seen:
            dupes.append(t)
        seen.add(t)
        assert c in CATEGORIES, f"{t}: unknown category {c}"
        assert g in GROUPS, f"{t}: unknown group {g}"
        assert n and len(n) <= 24, f"{t}: display name missing or too long: {n!r}"
        assert b, f"{t}: no stated bet"
    assert not dupes, f"duplicate tickers: {dupes}"
    assert len(UNIVERSE) < MAX_UNIVERSE, f"universe is {len(UNIVERSE)}, hard cap is {MAX_UNIVERSE}"


_check()

if __name__ == "__main__":
    from collections import Counter
    print(f"{len(UNIVERSE)} instruments (hard cap {MAX_UNIVERSE})\n")
    by_group = Counter(g for _, _, g, _, _, _ in UNIVERSE)
    for g in GROUPS:
        print(f"  {g:28s} {by_group[g]:3d}")
    print()
    by_cat = Counter(c for _, _, _, c, _, _ in UNIVERSE)
    for c in CATEGORIES:
        print(f"  {c:28s} {by_cat[c]:3d}")
