import sqlite3
import pandas as pd
from datetime import datetime

conn = sqlite3.connect("db/nifty100.db")

tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios",
    "market_cap",
    "peer_groups",
    "sectors",
    "stock_prices"
]

audit = []

for table in tables:

    count = conn.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    audit.append({
        "table_name": table,
        "row_count": count,
        "load_timestamp": datetime.now()
    })

df = pd.DataFrame(audit)

df.to_csv(
    "outputs/load_audit.csv",
    index=False
)

print(df)

conn.close()