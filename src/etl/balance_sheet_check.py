# src/etl/balance_sheet_check.py

import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    id,
    company_id,
    year,
    total_assets,
    total_liabilities
FROM balancesheet
WHERE ABS(total_assets - total_liabilities) > 1
"""

df = pd.read_sql_query(query, conn)

print("Failures:", len(df))

df.to_csv(
    "outputs/balance_sheet_failures.csv",
    index=False
)

conn.close()