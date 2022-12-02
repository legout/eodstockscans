from datetime import datetime
from pathlib import Path

# Pathes
BASE_PATH = Path("/Volumes/FinData/eod_stockmarket_scans")
RESULTS_PATH = BASE_PATH / "results"
IMAGES_PATH = BASE_PATH / "images"
SUMMARY_PATH = RESULTS_PATH / "summary"

# Date
TODAY = datetime.now().date()

# Markets
MARKETS = {
    "Australia": {"exchanges": ["Sydney"], "scale": {"volume": 0.5, "price": 1}},
    "Hong Kong": {"exchanges": ["Hong Kong"], "scale": {"volume": 1, "price": 5}},
    "Japan": {"exchanges": ["Tokyo"], "scale": {"volume": 0.5, "price": 100}},
    "Singapore": {"exchanges": ["Singapore"], "scale": {"volume": 0.2, "price": 1}},
    "Indonesia": {"exchanges": ["Jakarta"], "scale": {"volume": 0.2, "price": 100}},
    "Nordic Markets": {
        "exchanges": ["Stockholm", "Oslo", "Copenhagen", "Helsinki"],
        "scale": {"volume": 0.2, "price": 4},
    },
    "Poland": {"exchanges": ["Warsaw"], "scale": {"volume": 0.1, "price": 4}},
    "Germany": {"exchanges": ["XETRA"], "scale": {"volume": 0.1, "price": 1}},
    "France": {"exchanges": ["Paris"], "scale": {"volume": 0.1, "price": 1}},
    "Belgium": {"exchanges": ["Brussels"], "scale": {"volume": 0.1, "price": 1}},
    "Netherlands": {"exchanges": ["Amsterdam"], "scale": {"volume": 0.1, "price": 1}},
    "Italy": {"exchanges": ["Milan"], "scale": {"volume": 0.1, "price": 1}},
    "United Kingdom": {"exchanges": ["London"], "scale": {"volume": 0.5, "price": 1}},
    "Canada": {
        "exchanges": ["Toronto", "TSXV", "CSE"],
        "scale": {"volume": 0.5, "price": 1},
    },
    "United States": {
        "exchanges": ["NASDAQ", "NYSE"],
        "scale": {"volume": 1, "price": 1},
    },
}

# chart params
CHART_PARAMS = {
    "xs_light": {
        "size": "XS",
        "up_color": "gray",
        "down_color": "black",
        "template": "plotly_white",
        "show_info": False,
        "add_indicators": ["ema(9)", "ema(21)", "sma(50)", "sma(100)"],
    },
    "xl_light": {
        "size": "XL",
        "up_color": "gray",
        "down_color": "black",
        "template": "plotly_white",
        "show_info": True,
        "add_indicators": ["ema(9)", "ema(21)", "sma(50)", "sma(100)", "rs"],
    },
}
