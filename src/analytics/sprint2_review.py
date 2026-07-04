import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

print("=" * 70)
print("SPRINT 2 REVIEW")
print("=" * 70)

# -------------------------------------------------
# Total Rows
# -------------------------------------------------

count = pd.read_sql(
    "SELECT COUNT(*) AS total_rows FROM financial_ratios",
    conn
)

print("\nFinancial Ratios Table")
print(count)

# -------------------------------------------------
# Null Check
# -------------------------------------------------

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

print("\nNull Values")

print(df.isnull().sum())

# -------------------------------------------------
# ROE Filter
# -------------------------------------------------

print("\nCompanies with ROE > 15")

roe = df[df["return_on_equity_pct"] > 15]

print(roe[[
    "company_id",
    "year",
    "return_on_equity_pct"
]].head(20))

# -------------------------------------------------
# Debt Filter
# -------------------------------------------------

print("\nCompanies with Debt/Equity < 1")

de = df[df["debt_to_equity"] < 1]

print(de[[
    "company_id",
    "year",
    "debt_to_equity"
]].head(20))

# -------------------------------------------------
# Combined Screener
# -------------------------------------------------

print("\nQuality Companies")

quality = df[
    (df["return_on_equity_pct"] > 15) &
    (df["debt_to_equity"] < 1)
]

print(quality[[
    "company_id",
    "year",
    "return_on_equity_pct",
    "debt_to_equity"
]].head(30))

print("\nQuality Company Count :", len(quality))

# -------------------------------------------------
# KPI Columns
# -------------------------------------------------

print("\nColumns")

for col in df.columns:
    print(col)

conn.close()

print("\n" + "=" * 70)
print("SPRINT 2 COMPLETED SUCCESSFULLY")
print("=" * 70)