import os
import sqlite3
import pandas as pd

print("=" * 70)
print("DAY 26 - VALUATION ENGINE")
print("=" * 70)

os.makedirs("output", exist_ok=True)

conn = sqlite3.connect("db/nifty100.db")

# ----------------------------------------------------
# Load Tables
# ----------------------------------------------------

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

companies = pd.read_sql(
    """
    SELECT
        id AS company_id,
        company_name
    FROM companies
    """,
    conn
)

sectors = pd.read_sql(
    """
    SELECT
        company_id,
        broad_sector
    FROM sectors
    """,
    conn
)

# ----------------------------------------------------
# Keep Latest Record Per Company
# ----------------------------------------------------

ratios = (
    ratios
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
)

# ----------------------------------------------------
# Merge
# ----------------------------------------------------

df = ratios.merge(
    companies,
    on="company_id",
    how="left"
)

df = df.merge(
    sectors,
    on="company_id",
    how="left"
)

# ----------------------------------------------------
# Numeric Columns
# ----------------------------------------------------

cols = [
    "market_cap_crore",
    "free_cash_flow_cr",
    "pe_ratio",
    "pb_ratio",
    "ev_ebitda"
]

for col in cols:

    if col in df.columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

# ----------------------------------------------------
# FCF Yield
# ----------------------------------------------------

df["fcf_yield_pct"] = (
    df["free_cash_flow_cr"] /
    df["market_cap_crore"]
) * 100

# ----------------------------------------------------
# Sector Median PE
# ----------------------------------------------------

sector_median = (
    df.groupby("broad_sector_x")["pe_ratio"]
      .median()
      .reset_index()
)

sector_median.rename(
    columns={
        "pe_ratio": "sector_median_pe"
    },
    inplace=True
)

df = df.merge(
    sector_median,
    on="broad_sector_x",
    how="left"
)

# ----------------------------------------------------
# PE Comparison
# ----------------------------------------------------

df["pe_vs_sector_pct"] = (
    df["pe_ratio"] /
    df["sector_median_pe"]
) * 100

# ----------------------------------------------------
# Valuation Flag
# ----------------------------------------------------

def valuation_flag(row):

    if pd.isna(row["pe_ratio"]):
        return "Unknown"

    if pd.isna(row["sector_median_pe"]):
        return "Unknown"

    if row["pe_ratio"] > row["sector_median_pe"] * 1.5:
        return "Caution"

    if row["pe_ratio"] < row["sector_median_pe"] * 0.7:
        return "Discount"

    return "Fair"


df["flag"] = df.apply(
    valuation_flag,
    axis=1
)

# ----------------------------------------------------
# Final Output
# ----------------------------------------------------

final = df[
    [
        "company_id",
        "company_name",
        "broad_sector_x",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "fcf_yield_pct",
        "sector_median_pe",
        "pe_vs_sector_pct",
        "flag"
    ]
].rename(
    columns={
        "broad_sector_x": "broad_sector"
    }
)

# ----------------------------------------------------
# Save Files
# ----------------------------------------------------

final.to_excel(
    "output/valuation_summary.xlsx",
    index=False
)

flags = final[
    final["flag"].isin(
        ["Caution", "Discount"]
    )
]

flags.to_csv(
    "output/valuation_flags.csv",
    index=False
)

final.to_sql(
    "valuation",
    conn,
    if_exists="replace",
    index=False
)

print()
print(final.head())
print()

print("Companies :", len(final))
print("Flags :", len(flags))
print()

print("Excel Generated")
print("CSV Generated")

conn.commit()
conn.close()