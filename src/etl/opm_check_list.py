import pandas as pd
import sqlite3

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql_query("""
SELECT
    id,
    company_id,
    year,
    sales,
    operating_profit,
    opm_percentage
FROM profitandloss
""", conn)

df["calculated_opm"] = (
    df["operating_profit"] / df["sales"]
) * 100

df["difference"] = abs(
    df["calculated_opm"] - df["opm_percentage"]
)

failures = df[df["difference"] > 1]

print(failures[[
    "company_id",
    "year",
    "sales",
    "operating_profit",
    "opm_percentage",
    "calculated_opm",
    "difference"
]].head(20))