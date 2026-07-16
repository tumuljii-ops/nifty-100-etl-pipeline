import sqlite3
import pandas as pd

print("=" * 70)
print("DAY 27 - QA REPORT")
print("=" * 70)

conn = sqlite3.connect("db/nifty100.db")

tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios",
    "peer_percentiles",
    "valuation"
]

print("\nTABLE ROW COUNTS")
print("-" * 70)

for table in tables:

    try:
        count = pd.read_sql(
            f"SELECT COUNT(*) AS rows FROM {table}",
            conn
        )

        print(f"{table:<20} {count.iloc[0,0]}")

    except Exception as e:

        print(f"{table:<20} ERROR")

print("\n" + "-" * 70)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

print("Missing Values")

important = [
    "company_id",
    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "market_cap_crore",
    "pe_ratio"
]

for col in important:

    if col in ratios.columns:

        print(
            f"{col:<25}",
            ratios[col].isna().sum()
        )

print("\nDuplicate Company-Year")

dup = ratios.duplicated(
    subset=["company_id","year"]
).sum()

print(dup)

print("\nTop 10 Companies")

print(
    ratios[
        [
            "company_id",
            "composite_quality_score"
        ]
    ]
    .sort_values(
        "composite_quality_score",
        ascending=False
    )
    .head(10)
)

print("\nQA COMPLETE")

conn.close()