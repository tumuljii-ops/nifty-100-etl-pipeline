import sqlite3

conn = sqlite3.connect("db/nifty100.db")

checks = [

    ("companies","id"),
    ("profitandloss","id"),
    ("balancesheet","id"),
    ("cashflow","id"),
    ("financial_ratios","id"),
    ("market_cap","id"),
    ("peer_groups","id"),
    ("sectors","id"),
    ("stock_prices","id")
]

for table,col in checks:

    query = f"""
    SELECT COUNT(*) - COUNT(DISTINCT {col})
    FROM {table}
    """

    duplicates = conn.execute(query).fetchone()[0]

    print(
        f"{table}: duplicate {col} = {duplicates}"
    )

conn.close()