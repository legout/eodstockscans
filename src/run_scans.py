from stockScreener import io_, Screener
from pathlib import Path
from stockCharts.plotly import Chart
import json
import yaml

with open(Path(__file__).parent.parent / "config.yaml", "r") as f:
    config = yaml.full_load(f)

RESULTS_PATH = Path(config["BASE_PATH"]) / config["RESULTS_PATH"]
IMAGES_PATH = Path(config["BASE_PATH"]) / config["IMAGES_PATH"]

class Scans:
    def __init__(self, exchanges: list, market: str, date: str = None):
        self._exchanges = exchanges
        self._market = market
        (
            self._history,
            self._history_screener,
            self._stock_info,
            self._quote_summary,
        ) = io_.load(exchanges)

        self._screener = Screener(
            None,
            self._history_screener,
            self._stock_info,
            self._quote_summary,
            threads=8,
        )

        if date is None:
            self._date = self._history_screener.index.levels[1].max().date()
        else:
            self._date = date

        self._symbol_ids = dict()
        self._all_symbol_ids = set()

    def run_scan(
        self,
        group_name: str,
        scan_name: str,
        query: str,
        order: str,
        limit: int,
        save: bool = True,
    ):
        """ """

        if not group_name in self._symbol_ids:
            self._symbol_ids[group_name] = dict()

        self._screener.name = scan_name

        res = self._screener.run(
            query=query, order=order, limit=limit, time=str(self._date)
        )
        summary = self._screener.summary

        self._symbol_ids[group_name][scan_name] = self._screener._symbol_ids
        self._all_symbol_ids.update(self._screener._symbol_ids)

        if save:
            if len(self._symbol_ids[group_name][scan_name]) > 0:
                path_summary_csv = (
                    RESULTS_PATH
                    / "zip"
                    / self._market
                    / str(self._date)
                    / group_name
                    / f"{scan_name}.zip"
                )
                path_summary_csv.parent.mkdir(parents=True, exist_ok=True)
                summary.to_csv(
                    path_summary_csv,
                    index=False,
                    compression=dict(method="zip", archive_name=f"{scan_name}.csv"),
                )

                path_summary_parquet = (
                    # Path(__file__).parent.parent
                    # / "results"
                    RESULTS_PATH
                    / "summary"
                    / f"market={self._market}"
                    / f"date={str(self._date)}"
                    / f"group_name={group_name}"
                    / f"scan_name={scan_name}"
                    / "data.parquet"
                )
                path_summary_parquet.parent.mkdir(parents=True, exist_ok=True)
                summary.reset_index().to_parquet(path_summary_parquet, index=False)

    def run_scans(self, eod_scans: dict, save: bool = True):

        for group_name in eod_scans:
            print("Running scans of group", group_name)
            for scan_name in eod_scans[group_name]["scans"]:
                print("\t-->", scan_name)

                scan = eod_scans[group_name]["scans"][scan_name]
                query = scan["query"]
                order = scan["order"]
                limit = scan["limit"]

                self.run_scan(
                    group_name=group_name,
                    scan_name=scan_name,
                    query=query,
                    order=order,
                    limit=limit,
                    save=save,
                )

        path_symbol_ids = (
            # Path(__file__).parent.parent
            # / "results"
            RESULTS_PATH
            / "symbol_ids"
            / self._market
            / f"{str(self._date)}.json"
        )
        path_symbol_ids.parent.mkdir(parents=True, exist_ok=True)
        with open(path_symbol_ids, "w") as f:
            json.dump(self._symbol_ids, f)

        print("Finished running scans.")

    def gen_charts(self, chart_params: dict):
        self._screener("close>0", "close", 1000000)
        summary_idx = self._screener.summary.index
        summary_idx = [sid for sid in self._all_symbol_ids if sid in summary_idx]
        summary = self._screener.summary.loc[summary_idx]
        history = self._history.loc[list(self._all_symbol_ids)]
        sc = Chart(history=history, summary=summary)

        for size_theme in chart_params:
            print("Generating charts for theme", size_theme)

            path_images = (
                # Path(__file__).parent.parent
                # / "images"
                IMAGES_PATH
                / self._market
                / str(self._date)
                / size_theme
            )
            path_images.mkdir(parents=True, exist_ok=True)

            charts = sc.plot_chart(**chart_params[size_theme])

            for symbol_id in charts:
                charts[symbol_id].write_image(
                    str(path_images / str(symbol_id)) + ".svg", scale=1
                )
        print("Finished generating charts.")


# @app.command()
# def main():

#     for market in MARKETS:
#         exchanges = MARKETS[market]["exchanges"]
#         scale = MARKETS[market]["scale"]
#         eod_scans = EOD(scale=scale)

#         scanner = Scans(exchanges=exchanges, market=market.lower().replace(" ", "_"))
#         scanner.run_scans(eod_scans=eod_scans)
#         scanner.gen_charts(chart_params=CHART_PARAMS)


# if __name__ == "__main__":
#     import time

#     s = time.time()
#     main()
#     print("Finished in:", time.time() - s, "seconds")
