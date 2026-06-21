import pandas as pd
import sqlite3

conn = sqlite3.connect("db/nifty100.db")

# CSV files
csv_tables = {
    "companies": "data/processed/companies.csv",
    "profitandloss": "data/processed/profitandloss.csv",
    "balancesheet": "data/processed/balancesheet.csv",
    "cashflow": "data/processed/cashflow.csv"
}

for table, path in csv_tables.items():

    df = pd.read_csv(path)

    df.to_sql(
        table,
        conn,
        if_exists="append",
        index=False
    )

    print(f"{table} loaded : {len(df)} rows")


# Excel files
excel_tables = {
    "financial_ratios": "data/raw/financial_ratios.xlsx",
    "market_cap": "data/raw/market_cap.xlsx",
    "peer_groups": "data/raw/peer_groups.xlsx",
    "sectors": "data/raw/sectors.xlsx",
    "stock_prices": "data/raw/stock_prices.xlsx"
}

for table, path in excel_tables.items():

    df = pd.read_excel(path)

    df.to_sql(
        table,
        conn,
        if_exists="append",
        index=False
    )

    print(f"{table} loaded : {len(df)} rows")

conn.commit()
conn.close()

print("\nAll Data Loaded Successfully")