import sqlite3

conn = sqlite3.connect("db/nifty100.db")

checks = [
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios",
    "market_cap",
    "peer_groups",
    "sectors",
    "stock_prices"
]

print("FK CHECKS")

for table in checks:

    query = f"""
    SELECT COUNT(*)
    FROM {table}
    WHERE company_id NOT IN
    (
        SELECT id
        FROM companies
    )
    """

    invalid = conn.execute(query).fetchone()[0]

    print(f"{table}: invalid FK = {invalid}")

conn.close()