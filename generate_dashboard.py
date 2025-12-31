import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

os.makedirs("docs", exist_ok=True)

df = pd.read_csv("data/industry_data.csv")
df["date"] = pd.to_datetime(df["date"]).dt.date

# Get top 10 industries by average count for cleaner visualization
top_industries = df.groupby("industry")["count"].mean().nlargest(10).index
df_filtered = df[df["industry"].isin(top_industries)]

# Create figure
fig = go.Figure()

# Add traces for each industry
for industry in top_industries:
    industry_data = df_filtered[df_filtered["industry"] == industry]
    fig.add_trace(go.Scatter(
        x=industry_data["date"],
        y=industry_data["count"],
        name=industry,
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=8)
    ))

# Update layout with range selector
fig.update_layout(
    title={
        'text': "52-Week High Stocks by Industry",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 24},
        'y': 0.95
    },
    xaxis_title="Date",
    yaxis_title="Number of Stocks",
    hovermode="x unified",
    legend_title="Industry",
    height=700,
    margin=dict(t=150, b=80, l=80, r=80),
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="1W", step="day", stepmode="backward"),
                dict(count=14, label="2W", step="day", stepmode="backward"),
                dict(count=21, label="3W", step="day", stepmode="backward"),
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=3, label="3M", step="month", stepmode="backward"),
                dict(count=6, label="6M", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(step="all", label="All")
            ]),
            bgcolor="lightgray",
            activecolor="steelblue",
            x=0.01,
            y=1.02,
            xanchor="left",
            yanchor="bottom",
            font=dict(size=11)
        ),
        rangeslider=dict(visible=False),
        type="date",
        tickformat="%Y-%m-%d",
        dtick=86400000
    )
)

fig.write_html(
    "docs/index.html",
    include_plotlyjs="cdn",
    full_html=True
)
