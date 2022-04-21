from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import pandas as pd
from .config import MARKETS, SUMMARY

# from .run_scans import main
import pyarrow.dataset as ds
import duckdb
import base64


class Site:
    def __init__(self, market: str, date: str):
        self._file_loader = FileSystemLoader(Path(__file__).parent.parent / "templates")
        self._env = Environment(loader=self._file_loader)
        self._market = market.lower().replace(" ", "_")
        self._market_org = market
        self._date = date

        summary = ds.dataset(SUMMARY, partitioning="hive")
        self._summary = duckdb.from_arrow_table(summary)

    def svg2base64(self, path: str) -> str:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def load_summary(self, group_name: str, scan_name: str) -> pd.DataFrame:
        summary = (
            self._summary.filter(
                f"market='{self._market}' AND date='{self._date}' AND group_name='{group_name}' AND scan_name='{scan_name}'"
            )
            .df()
            .round(2)
        )

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

    def render(self, eod_scans: dict):

        navbar_brand = self.svg2base64(
            path=Path(__file__).parent.parent
            / f"images/3884113_growth_income_invest_market_stock_icon.svg"
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
                table = self.summary2html(summary=summary)

                symbol_ids = summary["symbol_id"]
                charts = dict()
                minicharts = dict()

                for sid in symbol_ids:
                    symbol = summary.query(f"symbol_id=={sid}")["symbol"].iloc[0]

                    minicharts[symbol] = self.svg2base64(
                        path=Path(__file__).parent.parent
                        / f"images/{self._market}/{self._date}/xs_light/{sid}.svg"
                    )

                    charts[symbol] = self.svg2base64(
                        path=Path(__file__).parent.parent
                        / f"images/{self._market}/{self._date}/xl_light/{sid}.svg"
                    )

                for tab in ["result_table", "minicharts", "charts", "criteria"]:
                    if "charts" in tab:
                        rendered = self._render(
                            template="charts.html",
                            market=self._market,
                            navbar_brand=navbar_brand,
                            market_org=self._market_org,
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

                    self.save(
                        html=rendered,
                        path=Path(__file__).parent.parent
                        / f"site/{self._market}/{group_name}/{scan_name}_{tab}.html",
                    )
