import sqlite3
import pandas as pd
import yaml


class ScreenerEngine:

    def __init__(self):

        self.conn = sqlite3.connect("db/nifty100.db")

        self.df = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn
        )

        # -----------------------------
        # Convert numeric columns
        # -----------------------------
        numeric_columns = [
            "return_on_equity_pct",
            "debt_to_equity",
            "free_cash_flow_cr",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "eps_cagr_5yr",
            "operating_profit_margin_pct",
            "pe_ratio",
            "pb_ratio",
            "dividend_yield_pct",
            "interest_coverage",
            "market_cap_crore",
            "net_profit",
            "asset_turnover",
            "sales",
            "composite_quality_score"
        ]

        for col in numeric_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(
                    self.df[col],
                    errors="coerce"
                )

        with open(
            "config/screener_config.yaml",
            "r"
        ) as f:
            self.config = yaml.safe_load(f)

    # --------------------------------------------------
    # Apply Filters
    # --------------------------------------------------

    def apply_filters(self, preset_name):

        if preset_name not in self.config:
            raise ValueError("Preset not found.")

        filters = self.config[preset_name]

        df = self.df.copy()

        for key, value in filters.items():

            if key == "roe_min":
                df = df[
                    df["return_on_equity_pct"] >= value
                ]

            elif key == "debt_to_equity_max":

                financials = (
                    df["broad_sector"] == "Financials"
                )

                df = df[
                    financials |
                    (df["debt_to_equity"] <= value)
                ]

            elif key == "free_cash_flow_min":

                df = df[
                    df["free_cash_flow_cr"] >= value
                ]

            elif key == "revenue_cagr_5yr_min":

                df = df[
                    df["revenue_cagr_5yr"] >= value
                ]

            elif key == "pat_cagr_5yr_min":

                df = df[
                    df["pat_cagr_5yr"] >= value
                ]

            elif key == "opm_min":

                df = df[
                    df["operating_profit_margin_pct"] >= value
                ]

            elif key == "pe_max":

                df = df[
                    df["pe_ratio"] <= value
                ]

            elif key == "pb_max":

                df = df[
                    df["pb_ratio"] <= value
                ]

            elif key == "dividend_yield_min":

                df = df[
                    df["dividend_yield_pct"] >= value
                ]

            elif key == "icr_min":

                df = df[
                    (df["interest_coverage"] >= value)
                    |
                    (df["interest_coverage"].isna())
                ]

            elif key == "market_cap_min":

                df = df[
                    df["market_cap_crore"] >= value
                ]

            elif key == "net_profit_min":

                df = df[
                    df["net_profit"] >= value
                ]

            elif key == "eps_cagr_min":

                df = df[
                    df["eps_cagr_5yr"] >= value
                ]

            elif key == "asset_turnover_min":

                df = df[
                    df["asset_turnover"] >= value
                ]

            elif key == "sales_min":

                df = df[
                    df["sales"] >= value
                ]

        df = df.sort_values(
            "composite_quality_score",
            ascending=False
        )

        return df

    def presets(self):

        return list(self.config.keys())


if __name__ == "__main__":

    engine = ScreenerEngine()

    print("Available Presets:")
    print(engine.presets())

    print()

    result = engine.apply_filters(
        "quality_compounder"
    )

    print(result.head(20))

    print()

    print("Companies Found:", len(result))