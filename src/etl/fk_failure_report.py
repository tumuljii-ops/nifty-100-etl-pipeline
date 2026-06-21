import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

tables = [
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios"
]

records = []

for table in tables:

    query = f"""
    SELECT DISTINCT company_id
    FROM {table}
    WHERE company_id NOT IN
    (
        SELECT id
        FROM companies
    )
    """

    rows = conn.execute(query).fetchall()

    for row in rows:

        records.append({
            "rule_id": "DQ03",
            "table_name": table,
            "invalid_company_id": row[0]
        })

df = pd.DataFrame(records)

df.to_csv(
    "outputs/validation_failures.csv",
    index=False
)

print(df)

conn.close()