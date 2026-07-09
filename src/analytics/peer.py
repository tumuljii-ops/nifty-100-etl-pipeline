import sqlite3
import pandas as pd

print("=" * 70)
print("DAY 18 - PEER PERCENTILE ENGINE")
print("=" * 70)

conn = sqlite3.connect("db/nifty100.db")

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

peers = pd.read_sql(
    "SELECT * FROM peer_groups",
    conn
)

# ----------------------------------------------------
# Merge Peer Groups
# ----------------------------------------------------

df = ratios.merge(
    peers,
    on="company_id",
    how="left"
)

metrics = [
    "return_on_equity_pct",
    "roce_percentage",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "pat_cagr_5yr",
    "revenue_cagr_5yr",
    "eps_cagr_5yr",
    "interest_coverage",
    "asset_turnover"
]

records = []

for group in df["peer_group_name"].dropna().unique():

    group_df = df[df["peer_group_name"] == group].copy()

    for metric in metrics:

        if metric not in group_df.columns:
            continue

        group_df[metric] = pd.to_numeric(
            group_df[metric],
            errors="coerce"
        )

        # Lower D/E is better
        ascending = (metric == "debt_to_equity")

        ranks = group_df[metric].rank(
            pct=True,
            ascending=ascending
        )

        if metric == "debt_to_equity":
            ranks = 1 - ranks

        for idx, row in group_df.iterrows():

            records.append({
                "company_id": row["company_id"],
                "peer_group_name": group,
                "metric": metric,
                "value": row[metric],
                "percentile_rank": ranks.loc[idx],
                "year": row["year"]
            })

peer_df = pd.DataFrame(records)

peer_df.to_sql(
    "peer_percentiles",
    conn,
    if_exists="replace",
    index=False
)

print()

print(peer_df.head())

print()

print("Rows Written :", len(peer_df))

conn.commit()
conn.close()