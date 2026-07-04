import sqlite3
import pandas as pd
import os

conn = sqlite3.connect("db/nifty100.db")

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

companies = pd.read_sql(
    "SELECT id, company_name, roce_percentage, roe_percentage FROM companies",
    conn
)

sectors = pd.read_sql(
    "SELECT company_id,broad_sector FROM sectors",
    conn
)

df = ratios.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

df = df.merge(
    sectors,
    on="company_id",
    how="left"
)

os.makedirs("output", exist_ok=True)

log_file = open(
    "output/ratio_edge_cases.log",
    "w",
    encoding="utf-8"
)

log_file.write("RATIO EDGE CASE REPORT\n")
log_file.write("=" * 70 + "\n\n")

#######################################################
# ROE CHECK
#######################################################

log_file.write("ROE DIFFERENCES\n")
log_file.write("-" * 70 + "\n")

for _, row in df.iterrows():

    if pd.isna(row["roe_percentage"]):
        continue

    if pd.isna(row["return_on_equity_pct"]):
        continue

    diff = abs(
        row["roe_percentage"] -
        row["return_on_equity_pct"]
    )

    if diff > 5:

        log_file.write(
            f"{row['company_id']} "
            f"{row['year']} "
            f"Source={row['roe_percentage']} "
            f"Computed={row['return_on_equity_pct']} "
            f"Difference={round(diff,2)} "
            f"Category=Formula Difference\n"
        )

#######################################################
# ROCE CHECK
#######################################################

log_file.write("\n\nROCE DIFFERENCES\n")
log_file.write("-" * 70 + "\n")

for _, row in df.iterrows():

    if pd.isna(row["roce_percentage"]):
        continue

    if pd.isna(row["return_on_equity_pct"]):
        continue

    diff = abs(
        row["roce_percentage"] -
        row["return_on_equity_pct"]
    )

    if diff > 5:

        log_file.write(
            f"{row['company_id']} "
            f"{row['year']} "
            f"Source={row['roce_percentage']} "
            f"Computed={row['return_on_equity_pct']} "
            f"Difference={round(diff,2)} "
            f"Category=Source Difference\n"
        )

#######################################################
# BANK CARVE OUT
#######################################################

log_file.write("\n\nFINANCIAL SECTOR\n")
log_file.write("-" * 70 + "\n")

financial = df[
    df["broad_sector"] == "Financials"
]

for company in financial["company_id"].unique():

    log_file.write(
        f"{company} -> "
        f"High Leverage Warning Ignored\n"
    )

#######################################################
# DUPLICATE RECORDS
#######################################################

log_file.write("\n\nDUPLICATE COMPANY YEAR RECORDS\n")
log_file.write("-" * 70 + "\n")

duplicates = df[
    df.duplicated(
        subset=["company_id", "year"],
        keep=False
    )
]

for _, row in duplicates.iterrows():

    log_file.write(
        f"{row['company_id']} "
        f"{row['year']} "
        f"Duplicate Record Found\n"
    )

log_file.close()

conn.close()

print("=" * 60)
print("DAY 13 COMPLETED")
print("=" * 60)
print("Generated : output/ratio_edge_cases.log")