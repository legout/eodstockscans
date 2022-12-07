from eodstockscans.src.gen_site import Site
from eodstockscans.src.run_scans import Scans
from eodstockscans.src.scans import EOD

# from fintwit_stockmarket_scans.src.config import MARKETS,CHART_PARAMS,EOD
from pathlib import Path
import typer
import yaml
import datetime as dt

app = typer.Typer()

# MARKETS = {
#     "United States": {
#         "exchanges": ["NASDAQ", "NYSE"],
#         "scale": {"volume": 1, "price": 1},
#     },
# }

with open(Path(__file__).parent / "config.yaml", "r") as f:
    config = yaml.full_load(f)

MARKETS = config["MARKETS"]
CHART_PARAMS = config["CHART_PARAMS"]


@app.command()
def run(
    market: str = None, run_scans: bool = True, gen_site: bool = True, date: str = None
):

    if market is None:
        market = MARKETS

    else:
        if isinstance(market, str):
            market = [market.replace("-", " ") for market in market.split(",")]
    #if date is None:
    #    date = str(dt.date.today())

    success = []
    failed = []
    for market_ in market:
        try:
            exchanges = MARKETS[market_]["exchanges"]
            scale = MARKETS[market_]["scale"]
            eod_scans = EOD(scale=scale)
            scanner = Scans(
                exchanges=exchanges, market=market_.lower().replace(" ", "_"), date=date
            )

            if run_scans:
                print(f"Running EOD Scans for market {market_}")

                scanner.run_scans(eod_scans=eod_scans)
                scanner.gen_charts(chart_params=CHART_PARAMS)
                print(f"Done.")

            if gen_site:
                print(f"Generating sites for market {market_}")
                site = Site(
                    market=market_, date=scanner._date, all_markets=list(MARKETS.keys())
                )
                site.render(eod_scans=eod_scans)
                print("Done.\n")
            success.append(market_)
        except:
            print(f"{market_} failed.")
            failed.append(market_)

    print("Success:", success)
    print("Failed:", failed)

    return success, failed

if __name__ == "__main__":
    import time

    s = time.time()
    success, failed = app()
    print("Finished in:", time.time() - s, "seconds")
    print("Success:", success)
    print("Failed:", failed)
