"""Curated cross-asset ETF / ETP universe.

Hand-picked rather than screened out of a full ETF catalogue: the brief asks for
broad coverage of *materially different investable exposures*, not an exhaustive
catalogue, and a curated list is the smallest thing that does that job honestly.

Each row is (ticker, category, exposure, structure).

category   -- broad asset class used for display only. It never affects ranking.
              U.S. Equity | International Equity | Rates | Credit | Commodity | Crypto
exposure   -- short human label for what the thing actually bets on.
structure  -- best-effort, easy-to-know product structure. Nothing keys off it yet.
              fund     conventional open-end ETF
              physical spot / physically backed trust
              futures  futures-based product
              etn      exchange-traded note
              equity   equity proxy for a commodity or theme (miners, partnerships)

Deliberately excluded across the board: leveraged and inverse products, buffered
and other path-dependent payoffs, covered-call / options-income funds, volatility
products, and anything without a meaningful independent exposure. That is applied
by judgment when writing this list, not by a rules engine. A liquidity floor is
applied later in build.py from the price history itself.
"""

UNIVERSE = [
    # ---------------------------------------------------------------- broad U.S. equity
    ("SPY",  "U.S. Equity", "S&P 500", "fund"),
    ("VOO",  "U.S. Equity", "S&P 500", "fund"),
    ("IVV",  "U.S. Equity", "S&P 500", "fund"),
    ("SPLG", "U.S. Equity", "S&P 500", "fund"),
    ("VTI",  "U.S. Equity", "Total U.S. market", "fund"),
    ("ITOT", "U.S. Equity", "Total U.S. market", "fund"),
    ("SCHB", "U.S. Equity", "Total U.S. market", "fund"),
    ("QQQ",  "U.S. Equity", "Nasdaq 100", "fund"),
    ("QQQM", "U.S. Equity", "Nasdaq 100", "fund"),
    ("DIA",  "U.S. Equity", "Dow 30", "fund"),
    ("IWB",  "U.S. Equity", "Russell 1000", "fund"),
    ("RSP",  "U.S. Equity", "S&P 500 equal weight", "fund"),

    # ---------------------------------------------------------------- size and style
    ("IWM",  "U.S. Equity", "Small cap", "fund"),
    ("IJR",  "U.S. Equity", "Small cap", "fund"),
    ("VB",   "U.S. Equity", "Small cap", "fund"),
    ("IJH",  "U.S. Equity", "Mid cap", "fund"),
    ("MDY",  "U.S. Equity", "Mid cap", "fund"),
    ("VO",   "U.S. Equity", "Mid cap", "fund"),
    ("VTV",  "U.S. Equity", "Large value", "fund"),
    ("IWD",  "U.S. Equity", "Large value", "fund"),
    ("VUG",  "U.S. Equity", "Large growth", "fund"),
    ("IWF",  "U.S. Equity", "Large growth", "fund"),
    ("IWN",  "U.S. Equity", "Small value", "fund"),
    ("VBR",  "U.S. Equity", "Small value", "fund"),
    ("IWO",  "U.S. Equity", "Small growth", "fund"),
    ("VBK",  "U.S. Equity", "Small growth", "fund"),
    ("MTUM", "U.S. Equity", "Momentum factor", "fund"),
    ("QUAL", "U.S. Equity", "Quality factor", "fund"),
    ("USMV", "U.S. Equity", "Min volatility factor", "fund"),
    ("VLUE", "U.S. Equity", "Value factor", "fund"),
    ("COWZ", "U.S. Equity", "Free cash flow yield", "fund"),
    ("SCHD", "U.S. Equity", "Dividend quality", "fund"),
    ("VYM",  "U.S. Equity", "High dividend yield", "fund"),
    ("VIG",  "U.S. Equity", "Dividend growth", "fund"),
    ("NOBL", "U.S. Equity", "Dividend aristocrats", "fund"),
    ("DVY",  "U.S. Equity", "High dividend yield", "fund"),

    # ---------------------------------------------------------------- U.S. sectors
    ("XLK",  "U.S. Equity", "Technology sector", "fund"),
    ("VGT",  "U.S. Equity", "Technology sector", "fund"),
    ("XLF",  "U.S. Equity", "Financials sector", "fund"),
    ("VFH",  "U.S. Equity", "Financials sector", "fund"),
    ("XLV",  "U.S. Equity", "Health care sector", "fund"),
    ("VHT",  "U.S. Equity", "Health care sector", "fund"),
    ("XLE",  "U.S. Equity", "Energy sector", "fund"),
    ("VDE",  "U.S. Equity", "Energy sector", "fund"),
    ("XLI",  "U.S. Equity", "Industrials sector", "fund"),
    ("XLY",  "U.S. Equity", "Consumer discretionary sector", "fund"),
    ("XLP",  "U.S. Equity", "Consumer staples sector", "fund"),
    ("XLU",  "U.S. Equity", "Utilities sector", "fund"),
    ("VPU",  "U.S. Equity", "Utilities sector", "fund"),
    ("XLB",  "U.S. Equity", "Materials sector", "fund"),
    ("XLRE", "U.S. Equity", "Real estate sector", "fund"),
    ("VNQ",  "U.S. Equity", "U.S. REITs", "fund"),
    ("SCHH", "U.S. Equity", "U.S. REITs", "fund"),
    ("XLC",  "U.S. Equity", "Communication services sector", "fund"),

    # ---------------------------------------------------------------- industries / subindustries
    ("SMH",  "U.S. Equity", "Semiconductors", "fund"),
    ("SOXX", "U.S. Equity", "Semiconductors", "fund"),
    ("XSD",  "U.S. Equity", "Semiconductors equal weight", "fund"),
    ("IGV",  "U.S. Equity", "Software", "fund"),
    ("CIBR", "U.S. Equity", "Cyber security", "fund"),
    ("HACK", "U.S. Equity", "Cyber security", "fund"),
    ("SKYY", "U.S. Equity", "Cloud computing", "fund"),
    ("WCLD", "U.S. Equity", "Cloud software", "fund"),
    ("XBI",  "U.S. Equity", "Biotech equal weight", "fund"),
    ("IBB",  "U.S. Equity", "Biotech cap weight", "fund"),
    ("IHI",  "U.S. Equity", "Medical devices", "fund"),
    ("XPH",  "U.S. Equity", "Pharmaceuticals", "fund"),
    ("IHF",  "U.S. Equity", "Health care providers", "fund"),
    ("KRE",  "U.S. Equity", "Regional banks", "fund"),
    ("KBE",  "U.S. Equity", "Banks", "fund"),
    ("KIE",  "U.S. Equity", "Insurance", "fund"),
    ("IAI",  "U.S. Equity", "Broker dealers / exchanges", "fund"),
    ("XRT",  "U.S. Equity", "Retail", "fund"),
    ("ITB",  "U.S. Equity", "Home construction", "fund"),
    ("XHB",  "U.S. Equity", "Homebuilders and suppliers", "fund"),
    ("ITA",  "U.S. Equity", "Aerospace and defense", "fund"),
    ("JETS", "U.S. Equity", "Airlines", "fund"),
    ("IYT",  "U.S. Equity", "Transportation", "fund"),
    ("PAVE", "U.S. Equity", "U.S. infrastructure", "fund"),
    ("XME",  "U.S. Equity", "Metals and mining equity", "equity"),
    ("XOP",  "U.S. Equity", "Oil and gas E&P equity", "equity"),
    ("OIH",  "U.S. Equity", "Oil services equity", "equity"),
    ("AMLP", "U.S. Equity", "Midstream MLPs", "equity"),
    ("MLPX", "U.S. Equity", "Midstream infrastructure", "equity"),
    ("REM",  "U.S. Equity", "Mortgage REITs", "fund"),
    ("MOO",  "International Equity", "Agribusiness equity", "equity"),
    ("WOOD", "International Equity", "Timber and forestry equity", "equity"),

    # ---------------------------------------------------------------- thematic equity
    ("ARKK", "U.S. Equity", "Disruptive innovation", "fund"),
    ("ARKG", "U.S. Equity", "Genomics", "fund"),
    ("ARKW", "U.S. Equity", "Next gen internet", "fund"),
    ("BOTZ", "International Equity", "Robotics and AI", "fund"),
    ("ROBO", "International Equity", "Robotics and automation", "fund"),
    ("IRBO", "International Equity", "Robotics and AI", "fund"),
    ("AIQ",  "International Equity", "Artificial intelligence", "fund"),
    ("FINX", "International Equity", "Fintech", "fund"),
    ("IPAY", "International Equity", "Payments", "fund"),
    ("SOCL", "International Equity", "Social media", "fund"),
    ("ESPO", "International Equity", "Video games and esports", "fund"),
    ("HERO", "International Equity", "Video games and esports", "fund"),
    ("BETZ", "International Equity", "Sports betting and gaming", "fund"),
    ("ICLN", "International Equity", "Clean energy", "fund"),
    ("QCLN", "U.S. Equity", "Clean energy", "fund"),
    ("PBW",  "U.S. Equity", "Clean energy", "fund"),
    ("TAN",  "International Equity", "Solar equity", "equity"),
    ("FAN",  "International Equity", "Wind energy equity", "equity"),
    ("GRID", "International Equity", "Grid infrastructure", "fund"),
    ("NLR",  "International Equity", "Nuclear energy equity", "equity"),
    ("URNM", "International Equity", "Uranium miners", "equity"),
    ("URA",  "International Equity", "Uranium miners", "equity"),
    ("LIT",  "International Equity", "Lithium and battery equity", "equity"),
    ("COPX", "International Equity", "Copper miners", "equity"),
    ("GDX",  "International Equity", "Gold miners", "equity"),
    ("GDXJ", "International Equity", "Junior gold miners", "equity"),
    ("SIL",  "International Equity", "Silver miners", "equity"),
    ("BLOK", "International Equity", "Blockchain equity", "equity"),
    ("BITQ", "International Equity", "Crypto industry equity", "equity"),
    ("XT",   "International Equity", "Exponential technologies", "fund"),
    ("KOMP", "International Equity", "Space and innovation", "fund"),
    ("ONLN", "U.S. Equity", "Online retail", "fund"),

    # ---------------------------------------------------------------- international / regional equity
    ("VT",   "International Equity", "All-world equity", "fund"),
    ("ACWI", "International Equity", "All-world equity", "fund"),
    ("VXUS", "International Equity", "Total ex-U.S. equity", "fund"),
    ("VEU",  "International Equity", "Total ex-U.S. equity", "fund"),
    ("EFA",  "International Equity", "Developed ex-North America", "fund"),
    ("IEFA", "International Equity", "Developed ex-North America", "fund"),
    ("VEA",  "International Equity", "Developed ex-U.S.", "fund"),
    ("SCHF", "International Equity", "Developed ex-U.S.", "fund"),
    ("EEM",  "International Equity", "Emerging markets", "fund"),
    ("IEMG", "International Equity", "Emerging markets", "fund"),
    ("VWO",  "International Equity", "Emerging markets", "fund"),
    ("SCHE", "International Equity", "Emerging markets", "fund"),
    ("VGK",  "International Equity", "Europe", "fund"),
    ("IEUR", "International Equity", "Europe", "fund"),
    ("EZU",  "International Equity", "Eurozone", "fund"),
    ("FEZ",  "International Equity", "Euro Stoxx 50", "fund"),
    ("VPL",  "International Equity", "Developed Pacific", "fund"),
    ("AAXJ", "International Equity", "Asia ex-Japan", "fund"),
    ("ILF",  "International Equity", "Latin America", "fund"),
    ("EWJ",  "International Equity", "Japan", "fund"),
    ("DXJ",  "International Equity", "Japan currency hedged", "fund"),
    ("EWG",  "International Equity", "Germany", "fund"),
    ("EWU",  "International Equity", "United Kingdom", "fund"),
    ("EWQ",  "International Equity", "France", "fund"),
    ("EWI",  "International Equity", "Italy", "fund"),
    ("EWP",  "International Equity", "Spain", "fund"),
    ("EWL",  "International Equity", "Switzerland", "fund"),
    ("EWD",  "International Equity", "Sweden", "fund"),
    ("EWN",  "International Equity", "Netherlands", "fund"),
    ("EWA",  "International Equity", "Australia", "fund"),
    ("EWC",  "International Equity", "Canada", "fund"),
    ("EWY",  "International Equity", "South Korea", "fund"),
    ("EWT",  "International Equity", "Taiwan", "fund"),
    ("MCHI", "International Equity", "China all-share", "fund"),
    ("FXI",  "International Equity", "China large cap", "fund"),
    ("KWEB", "International Equity", "China internet", "fund"),
    ("ASHR", "International Equity", "China A-shares", "fund"),
    ("INDA", "International Equity", "India", "fund"),
    ("EWZ",  "International Equity", "Brazil", "fund"),
    ("EWW",  "International Equity", "Mexico", "fund"),
    ("EZA",  "International Equity", "South Africa", "fund"),
    ("TUR",  "International Equity", "Turkey", "fund"),
    ("EPOL", "International Equity", "Poland", "fund"),
    ("EIS",  "International Equity", "Israel", "fund"),
    ("GREK", "International Equity", "Greece", "fund"),
    ("ARGT", "International Equity", "Argentina", "fund"),
    ("EWH",  "International Equity", "Hong Kong", "fund"),
    ("EWS",  "International Equity", "Singapore", "fund"),
    ("THD",  "International Equity", "Thailand", "fund"),
    ("EIDO", "International Equity", "Indonesia", "fund"),
    ("EPHE", "International Equity", "Philippines", "fund"),
    ("EWM",  "International Equity", "Malaysia", "fund"),
    ("VNM",  "International Equity", "Vietnam", "fund"),
    ("FM",   "International Equity", "Frontier markets", "fund"),
    ("EDEN", "International Equity", "Denmark", "fund"),
    ("ENOR", "International Equity", "Norway", "fund"),
    ("SCZ",  "International Equity", "Developed ex-U.S. small cap", "fund"),
    ("EEMS", "International Equity", "EM small cap", "fund"),

    # ---------------------------------------------------------------- government bonds / duration ladder
    ("BIL",  "Rates", "T-bills 1-3 month", "fund"),
    ("SGOV", "Rates", "T-bills 0-3 month", "fund"),
    ("SHV",  "Rates", "T-bills 0-1 year", "fund"),
    ("SHY",  "Rates", "Treasury 1-3 year", "fund"),
    ("SCHO", "Rates", "Treasury 1-3 year", "fund"),
    ("VGSH", "Rates", "Treasury 1-3 year", "fund"),
    ("IEI",  "Rates", "Treasury 3-7 year", "fund"),
    ("SCHR", "Rates", "Treasury 3-10 year", "fund"),
    ("IEF",  "Rates", "Treasury 7-10 year", "fund"),
    ("VGIT", "Rates", "Treasury 3-10 year", "fund"),
    ("TLH",  "Rates", "Treasury 10-20 year", "fund"),
    ("TLT",  "Rates", "Treasury 20+ year", "fund"),
    ("VGLT", "Rates", "Treasury long", "fund"),
    ("SPTL", "Rates", "Treasury long", "fund"),
    ("EDV",  "Rates", "Treasury STRIPS 20-30 year", "fund"),
    ("ZROZ", "Rates", "Treasury zero coupon 25+ year", "fund"),
    ("GOVT", "Rates", "Treasury all maturities", "fund"),

    # ---------------------------------------------------------------- inflation linked
    ("TIP",  "Rates", "TIPS broad", "fund"),
    ("SCHP", "Rates", "TIPS broad", "fund"),
    ("SPIP", "Rates", "TIPS broad", "fund"),
    ("VTIP", "Rates", "TIPS 0-5 year", "fund"),
    ("STIP", "Rates", "TIPS 0-5 year", "fund"),
    ("LTPZ", "Rates", "TIPS 15+ year", "fund"),

    # ---------------------------------------------------------------- investment grade credit / aggregate
    ("AGG",  "Credit", "U.S. aggregate bond", "fund"),
    ("BND",  "Credit", "U.S. aggregate bond", "fund"),
    ("SPAB", "Credit", "U.S. aggregate bond", "fund"),
    ("BIV",  "Credit", "Intermediate-term bond", "fund"),
    ("BLV",  "Credit", "Long-term bond", "fund"),
    ("BSV",  "Credit", "Short-term bond", "fund"),
    ("LQD",  "Credit", "IG corporate broad", "fund"),
    ("USIG", "Credit", "IG corporate broad", "fund"),
    ("VCSH", "Credit", "IG corporate short", "fund"),
    ("IGSB", "Credit", "IG corporate short", "fund"),
    ("VCIT", "Credit", "IG corporate intermediate", "fund"),
    ("IGIB", "Credit", "IG corporate intermediate", "fund"),
    ("VCLT", "Credit", "IG corporate long", "fund"),
    ("MBB",  "Credit", "Agency MBS", "fund"),
    ("VMBS", "Credit", "Agency MBS", "fund"),
    ("FLOT", "Credit", "IG floating rate", "fund"),

    # ---------------------------------------------------------------- high yield / loans / preferred
    ("HYG",  "Credit", "High yield corporate", "fund"),
    ("JNK",  "Credit", "High yield corporate", "fund"),
    ("USHY", "Credit", "High yield corporate broad", "fund"),
    ("SHYG", "Credit", "High yield short duration", "fund"),
    ("SJNK", "Credit", "High yield short duration", "fund"),
    ("ANGL", "Credit", "Fallen angel high yield", "fund"),
    ("FALN", "Credit", "Fallen angel high yield", "fund"),
    ("BKLN", "Credit", "Senior bank loans", "fund"),
    ("SRLN", "Credit", "Senior bank loans", "fund"),
    ("PFF",  "Credit", "Preferred stock", "fund"),
    ("PGX",  "Credit", "Preferred stock", "fund"),

    # ---------------------------------------------------------------- municipal
    ("MUB",  "Credit", "Municipal bonds", "fund"),
    ("VTEB", "Credit", "Municipal bonds", "fund"),
    ("HYD",  "Credit", "High yield municipal", "fund"),

    # ---------------------------------------------------------------- international / EM bonds
    ("BNDX", "Credit", "International bonds hedged", "fund"),
    ("BWX",  "Credit", "International treasuries unhedged", "fund"),
    ("IGOV", "Credit", "International treasuries unhedged", "fund"),
    ("EMB",  "Credit", "EM sovereign USD", "fund"),
    ("PCY",  "Credit", "EM sovereign USD", "fund"),
    ("VWOB", "Credit", "EM sovereign USD", "fund"),
    ("EMLC", "Credit", "EM sovereign local currency", "fund"),
    ("LEMB", "Credit", "EM sovereign local currency", "fund"),
    ("EBND", "Credit", "EM sovereign local currency", "fund"),

    # ---------------------------------------------------------------- broad commodity baskets
    ("DBC",  "Commodity", "Broad commodity basket", "futures"),
    ("PDBC", "Commodity", "Broad commodity basket", "futures"),
    ("GSG",  "Commodity", "Energy-heavy commodity index", "futures"),
    ("DJP",  "Commodity", "Broad commodity index", "etn"),
    ("BCI",  "Commodity", "Broad commodity basket", "futures"),
    ("FTGC", "Commodity", "Broad commodity active", "futures"),
    ("USCI", "Commodity", "Broad commodity basket", "futures"),
    ("COMT", "Commodity", "Commodity plus equity", "futures"),

    # ---------------------------------------------------------------- precious metals
    ("GLD",  "Commodity", "Gold spot", "physical"),
    ("IAU",  "Commodity", "Gold spot", "physical"),
    ("GLDM", "Commodity", "Gold spot", "physical"),
    ("SGOL", "Commodity", "Gold spot", "physical"),
    ("BAR",  "Commodity", "Gold spot", "physical"),
    ("SLV",  "Commodity", "Silver spot", "physical"),
    ("SIVR", "Commodity", "Silver spot", "physical"),
    ("PPLT", "Commodity", "Platinum spot", "physical"),
    ("PALL", "Commodity", "Palladium spot", "physical"),

    # ---------------------------------------------------------------- energy commodities
    ("USO",  "Commodity", "WTI crude oil", "futures"),
    ("BNO",  "Commodity", "Brent crude oil", "futures"),
    ("DBO",  "Commodity", "WTI crude oil", "futures"),
    ("UNG",  "Commodity", "Natural gas", "futures"),
    ("UNL",  "Commodity", "Natural gas 12-month", "futures"),
    ("UGA",  "Commodity", "Gasoline", "futures"),
    ("DBE",  "Commodity", "Energy basket", "futures"),

    # ---------------------------------------------------------------- industrial metals
    ("CPER", "Commodity", "Copper", "futures"),
    ("DBB",  "Commodity", "Industrial metals basket", "futures"),

    # ---------------------------------------------------------------- agriculture
    ("DBA",  "Commodity", "Agriculture basket", "futures"),
    ("CORN", "Commodity", "Corn", "futures"),
    ("WEAT", "Commodity", "Wheat", "futures"),
    ("SOYB", "Commodity", "Soybeans", "futures"),
    ("CANE", "Commodity", "Sugar", "futures"),
    ("JO",   "Commodity", "Coffee", "etn"),
    ("NIB",  "Commodity", "Cocoa", "etn"),

    # ---------------------------------------------------------------- crypto
    ("IBIT", "Crypto", "Spot bitcoin", "physical"),
    ("FBTC", "Crypto", "Spot bitcoin", "physical"),
    ("BITB", "Crypto", "Spot bitcoin", "physical"),
    ("ARKB", "Crypto", "Spot bitcoin", "physical"),
    ("GBTC", "Crypto", "Spot bitcoin", "physical"),
    ("BTC",  "Crypto", "Spot bitcoin", "physical"),
    ("HODL", "Crypto", "Spot bitcoin", "physical"),
    ("BTCO", "Crypto", "Spot bitcoin", "physical"),
    ("BRRR", "Crypto", "Spot bitcoin", "physical"),
    ("ETHA", "Crypto", "Spot ether", "physical"),
    ("FETH", "Crypto", "Spot ether", "physical"),
    ("ETHE", "Crypto", "Spot ether", "physical"),
    ("ETHW", "Crypto", "Spot ether", "physical"),
    ("ETHV", "Crypto", "Spot ether", "physical"),
    ("EZET", "Crypto", "Spot ether", "physical"),
]

MAX_UNIVERSE = 300

CATEGORIES = ["U.S. Equity", "International Equity", "Rates", "Credit", "Commodity", "Crypto"]


def tickers():
    return [row[0] for row in UNIVERSE]


def as_dicts():
    return [
        {"ticker": t, "category": c, "exposure": e, "structure": s}
        for t, c, e, s in UNIVERSE
    ]


def _check():
    seen, dupes = set(), []
    for t, c, _, _ in UNIVERSE:
        if t in seen:
            dupes.append(t)
        seen.add(t)
        assert c in CATEGORIES, f"{t}: unknown category {c}"
    assert not dupes, f"duplicate tickers: {dupes}"
    assert len(UNIVERSE) <= MAX_UNIVERSE, f"universe is {len(UNIVERSE)}, cap is {MAX_UNIVERSE}"


_check()

if __name__ == "__main__":
    from collections import Counter
    print(f"{len(UNIVERSE)} instruments (cap {MAX_UNIVERSE})")
    for cat, n in Counter(c for _, c, _, _ in UNIVERSE).most_common():
        print(f"  {cat:22s} {n}")
