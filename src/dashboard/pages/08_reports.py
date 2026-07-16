import streamlit as st
import sqlite3
import pandas as pd

st.title("📄 Reports")

conn = sqlite3.connect("db/nifty100.db")

company = pd.read_sql(
    """
    SELECT
    id,
    company_name,
    bse_profile
    FROM companies
    """,
    conn
)

conn.close()

ticker = st.selectbox(
    "Company",
    company["id"]
)

row = company[
    company["id"] == ticker
].iloc[0]

st.subheader(row["company_name"])

st.write("BSE Report Link")

st.write(row["bse_profile"])

st.success("Annual reports available through BSE profile.")