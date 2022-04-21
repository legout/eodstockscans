from src.gen_site import Site
from src.run_scans import Scans
from src.config import MARKETS,CHART_PARAMS,EOD
import typer

app = typer.Typer()

# MARKETS = {
#     "United States": {
#         "exchanges": ["NASDAQ", "NYSE"],
#         "scale": {"volume": 1, "price": 1},
#     },
# }

@app.command()
def main(run_scans:bool=True, gen_site:bool=True):

    for market in MARKETS:
        exchanges = MARKETS[market]["exchanges"]
        scale = MARKETS[market]["scale"]
        eod_scans = EOD(scale=scale)
        
        if run_scans:
            print(f"Running EOD Scans for market {market}")
            scanner = Scans(exchanges=exchanges, market=market.lower().replace(" ", "_"))
            scanner.run_scans(eod_scans=eod_scans)
            scanner.gen_charts(chart_params=CHART_PARAMS)
            print(f"Done.")

        if gen_site:
            print("Generating sites.")
            site = Site(market=market, date="2022-04-20")
            site.render(eod_scans=eod_scans)
            print("Done.")


if __name__ == "__main__":
    import time

    s = time.time()
    app()
    print("Finished in:", time.time() - s, "seconds")