from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import pandas as pd

import pyarrow.dataset as ds
import duckdb
import base64
import unicodedata
import yaml

with open(Path(__file__).parent.parent / "config.yaml", "r") as f:
    config = yaml.full_load(f)

SUMMARY_PATH = (
    Path(config["BASE_PATH"]) / config["RESULTS_PATH"] / config["SUMMARY_PATH"]
)
IMAGES_PATH = Path(config["BASE_PATH"]) / config["IMAGES_PATH"]


class Site:
    def __init__(self, market: str, date: str, all_markets: list):
        self._file_loader = FileSystemLoader(Path(__file__).parent.parent / "templates")
        self._env = Environment(loader=self._file_loader)
        self._market = market.lower().replace(" ", "_")
        self._market_org = market
        self._all_markets_org = all_markets
        self._all_markets = [market.lower().replace(" ", "_") for market in all_markets]
        self._date = date

        summary = ds.dataset(
            SUMMARY_PATH,
            partitioning="hive",
        )
        self._summary = duckdb.from_arrow(summary)

    def svg2base64(self, path: str) -> str:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def load_summary(self, group_name: str, scan_name: str) -> pd.DataFrame:

        columns = [
            "symbol",
            "yahoo_symbol",
            "name",
            "sector",
            "industry",
            "roc",
            "close",
            "volume",
            "rel Volume",
            "adr(20)",
            "atr(14)",
            "roc(5)",
            "roc(21)",
            "roc(63)",
            "roc(126)",
            "roc(252)",
            "52w High",
            "% below 52w High",
            "52w Low",
            "% above 52w Low",
            "UD Ratio",
            "50d avg Volume",
            "Pocket Pivot",
            "1w Pocket Pivots",
            "1m Pocket Pivots",
            "Rocket Ratio",
            "1m RS",
            "3m RS",
            "RS",
            "Industry 1m RS",
            "Industry 3m RS",
            "Industry RS",
            "ema(9)",
            "% from 9d ema",
            "ema(21)",
            "% from 21d ema",
            "sma(50)",
            "% from 50d sma",
            "EPS Growth Q",
            "EPS Growth Y",
            "EPS Growth FQ",
            "EPS Growth FY",
            "EPS Growth FQ1",
            "EPS Growth FY1",
            "Rev Growth Q",
            "Rev Growth FQ",
            "Rev Growth FY",
            "Rev Growth FQ1",
            "Rev Growth FY1",
            "Insiders %",
            "Institutions %",
            "Institutions No.",
            "Market Cap",
            "Shares Outstanding",
            "Shares Float",
            "Shares Short",
            "Short Ratio",
            "Net Insider Trading %",
            "exchange",
            "country",
            # "forexpros_symbol",
            "IPO Date",
            "market",
            "date",
            "group_name",
            "scan_name",
        ]
        summary = (
            self._summary.filter(
                f"""market='{unicodedata.normalize("NFKD", self._market)}' 
                AND date='{self._date}' 
                AND group_name='{unicodedata.normalize("NFKD", group_name)}' 
                AND scan_name='{unicodedata.normalize("NFKD", scan_name)}'"""
            )
            .df()
            .round(2)
            .set_index("symbol_id")
        )[columns]

        return summary

    def summary2html(self, summary: pd.DataFrame) -> str:
        table = summary.to_html(
            table_id="data", classes=["table", "is-striped", "no-wrap"]
        ).replace('id="data"', 'id="data" style="width:100%; font-size:85%"')

        return table

    def save(self, html: str, path: str):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            f.write(html)

    def _render(self, template: str, **kwargs) -> str:
        _template = self._env.get_template(template)
        rendered = _template.render(**kwargs)

        return rendered

    def render(self, eod_scans: dict, save: bool = True):

        navbar_brand = self.svg2base64(
            path=IMAGES_PATH / f"3884113_growth_income_invest_market_stock_icon.svg"
        )

        # MARKET MONITOR
        rendered = self._render(
            template="market_monitor.html",
            market=self._market,
            eod_scans=eod_scans,
            navbar_brand=navbar_brand,
        )
        self.save(
            html=rendered,
            path=Path(__file__).parent.parent
            / f"site/{self._market}/market_monitor.html",
        )

        # EOD SCANS
        for group_name in eod_scans:
            scan_names = sorted(list(eod_scans[group_name]["scans"].keys()))
            twitter_link = eod_scans[group_name]["link"]
            twitter_name = twitter_link.split("/")[-1]

            for scan_name in scan_names:

                scan = eod_scans[group_name]["scans"][scan_name]
                summary = self.load_summary(group_name=group_name, scan_name=scan_name)
                table = self.summary2html(summary=summary.reset_index(drop=True))

                symbol_ids = summary.index.values.tolist()  # ["symbol_id"]
                charts = dict()
                minicharts = dict()

                for sid in symbol_ids:
                    symbol = summary.loc[sid]["symbol"]

                    minicharts[symbol] = self.svg2base64(
                        path=IMAGES_PATH
                        / f"{self._market}/{self._date}/xs_light/{sid}.svg"
                    )

                    charts[symbol] = self.svg2base64(
                        path=IMAGES_PATH
                        / f"{self._market}/{self._date}/xl_light/{sid}.svg"
                    )

                for tab in ["result_table", "minicharts", "charts", "criteria"]:
                    if "charts" in tab:
                        rendered = self._render(
                            template="charts.html",
                            market=self._market,
                            navbar_brand=navbar_brand,
                            market_org=self._market_org,
                            all_markets=zip(self._all_markets_org, self._all_markets),
                            twitter_link=twitter_link,
                            twitter_name=twitter_name,
                            # title=f"{group_name} - {scan_name}",
                            date=self._date,
                            eod_scans=eod_scans,
                            group_name=group_name,
                            scan_name=scan_name,
                            charts=charts if tab == "charts" else minicharts,
                            tab=tab,
                            path="..",
                        )

                    elif tab == "result_table":
                        rendered = self._render(
                            template="result_table.html",
                            market=self._market,
                            navbar_brand=navbar_brand,
                            market_org=self._market_org,
                            all_markets=zip(self._all_markets_org, self._all_markets),
                            twitter_link=twitter_link,
                            twitter_name=twitter_name,
                            # title=f"{group_name} - {scan_name}",
                            date=self._date,
                            eod_scans=eod_scans,
                            group_name=group_name,
                            scan_name=scan_name,
                            table=table,
                            tab=tab,
                            path="..",
                        )
                    else:
                        rendered = self._render(
                            template="criteria.html",
                            market=self._market,
                            navbar_brand=navbar_brand,
                            market_org=self._market_org,
                            all_markets=zip(self._all_markets_org, self._all_markets),
                            twitter_link=twitter_link,
                            twitter_name=twitter_name,
                            # title=f"{group_name} - {scan_name}",
                            date=self._date,
                            eod_scans=eod_scans,
                            group_name=group_name,
                            scan_name=scan_name,
                            scan=scan,
                            tab=tab,
                            path="..",
                        )
                    if save:
                        self.save(
                            html=rendered,
                            path=Path(__file__).parent.parent
                            / f"site/{self._market}/{group_name}/{scan_name}_{tab}.html",
                        )
