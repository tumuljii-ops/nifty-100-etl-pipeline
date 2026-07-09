import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=" * 70)
print("DAY 19 - RADAR CHART GENERATION")
print("=" * 70)

# -----------------------------------------------------
# Create Output Folder
# -----------------------------------------------------

os.makedirs("reports/radar_charts", exist_ok=True)

# -----------------------------------------------------
# Load Data
# -----------------------------------------------------

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

metrics = [
    "return_on_equity_pct",
    "roce_percentage",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "pat_cagr_5yr",
    "revenue_cagr_5yr",
    "composite_quality_score"
]

# Convert numeric columns
for col in metrics:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

# -----------------------------------------------------
# One latest record per company
# -----------------------------------------------------

df = df.sort_values("year")
df = df.groupby("company_id").tail(1)

# -----------------------------------------------------
# Fill missing values
# -----------------------------------------------------

df[metrics] = df[metrics].fillna(0)

labels = metrics
angles = np.linspace(
    0,
    2*np.pi,
    len(labels),
    endpoint=False
).tolist()

angles += angles[:1]

count = 0

# -----------------------------------------------------
# Generate Charts
# -----------------------------------------------------

for _, row in df.iterrows():

    values = [row[m] for m in metrics]
    values += values[:1]

    fig = plt.figure(figsize=(6,6))

    ax = plt.subplot(111, polar=True)

    ax.plot(
        angles,
        values,
        linewidth=2
    )

    ax.fill(
        angles,
        values,
        alpha=0.25
    )

    ax.set_xticks(angles[:-1])

    ax.set_xticklabels(
        [
            "ROE",
            "ROCE",
            "NPM",
            "D/E",
            "FCF",
            "PAT CAGR",
            "REV CAGR",
            "Score"
        ],
        fontsize=8
    )

    plt.title(row["company_id"])

    plt.savefig(
        f"reports/radar_charts/{row['company_id']}_radar.png",
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()

    count += 1

print()

print("Radar Charts Generated :", count)

conn.close()