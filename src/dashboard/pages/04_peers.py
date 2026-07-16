import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.title("👥 Peer Comparison")

conn = sqlite3.connect("db/nifty100.db")

peer = pd.read_sql(
    "SELECT * FROM peer_percentiles",
    conn
)

conn.close()

groups = sorted(
    peer["peer_group_name"]
    .dropna()
    .unique()
)

group = st.selectbox(
    "Peer Group",
    groups
)

data = peer[
    peer["peer_group_name"] == group
]

metric = st.selectbox(
    "Metric",
    sorted(
        data["metric"].unique()
    )
)

plot = data[
    data["metric"] == metric
]

fig = px.bar(
    plot,
    x="company_id",
    y="percentile_rank",
    color="percentile_rank",
    title=f"{metric} Percentile Rank"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(
    plot,
    use_container_width=True
)