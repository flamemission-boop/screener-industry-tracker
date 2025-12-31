import pandas as pd
import plotly.express as px
import os

os.makedirs("docs", exist_ok=True)

df = pd.read_csv("data/industry_data.csv")
df["date"] = pd.to_datetime(df["date"])

fig = px.line(
    df,
    x="date",
    y="count",
    color="industry",
    title="52-Week High Stocks by Industry",
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Number of Stocks",
    hovermode="x unified",
    legend_title="Industry",
)

fig.write_html(
    "docs/index.html",
    include_plotlyjs="cdn",
    full_html=True
)
