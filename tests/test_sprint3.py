import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

print("=" * 70)
print("SPRINT 3 VALIDATION")
print("=" * 70)

# ----------------------------------------------------
# financial_ratios
# ----------------------------------------------------

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

print("financial_ratios rows :", len(ratios))

assert len(ratios) > 1000

# ----------------------------------------------------
# peer_percentiles
# ----------------------------------------------------

peer = pd.read_sql(
    "SELECT * FROM peer_percentiles",
    conn
)

print("peer_percentiles rows :", len(peer))

assert len(peer) > 10000

# ----------------------------------------------------
# Composite Score
# ----------------------------------------------------

assert "composite_quality_score" in ratios.columns

print("Composite Score : PASS")

# ----------------------------------------------------
# CAGR
# ----------------------------------------------------

assert "revenue_cagr_5yr" in ratios.columns

assert "pat_cagr_5yr" in ratios.columns

print("CAGR : PASS")

# ----------------------------------------------------
# PE
# ----------------------------------------------------

assert "pe_ratio" in ratios.columns

print("PE Ratio : PASS")

# ----------------------------------------------------
# PB
# ----------------------------------------------------

assert "pb_ratio" in ratios.columns

print("PB Ratio : PASS")

# ----------------------------------------------------
# Dividend Yield
# ----------------------------------------------------

assert "dividend_yield_pct" in ratios.columns

print("Dividend Yield : PASS")

print()
print("=" * 70)
print("SPRINT 3 COMPLETED SUCCESSFULLY")
print("=" * 70)

conn.close()