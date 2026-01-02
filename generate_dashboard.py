import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

os.makedirs("docs", exist_ok=True)

SECTOR_TOTALS = {
    "Industrial Products": 146,
    "Finance": 118,
    "Chemicals & Petrochemicals": 105,
    "Pharmaceuticals & Biotechnology": 102,
    "Consumer Durables": 97,
    "Auto Components": 90,
    "Industrial Manufacturing": 68,
    "Electrical Equipment": 63,
    "Realty": 55,
    "Textiles & Apparels": 55,
    "Construction": 54,
    "IT - Software": 50,
    "Commercial Services & Supplies": 46,
    "Leisure Services": 45,
    "Capital Markets": 39,
    "Fertilizers & Agrochemicals": 36,
    "Healthcare Services": 36,
    "IT - Services": 36,
    "Agricultural Food & other Products": 35,
    "Retailing": 34,
    "Food Products": 33,
    "Banks": 32,
    "Transport Services": 29,
    "Cement & Cement Products": 28,
    "Power": 28,
    "Aerospace & Defense": 25,
    "Entertainment": 16,
    "Beverages": 16,
    "Paper, Forest & Jute Products": 14,
    "Transport Infrastructure": 14,
    "Telecom - Services": 14,
    "Ferrous Metals": 14,
    "Automobiles": 14,
    "Insurance": 13,
    "Oil": 12,
    "Other Utilities": 12,
    "Petroleum Products": 12,
    "Agricultural, Commercial & Construction Vehicles": 11,
    "Other Consumer Services": 11,
    "Non - Ferrous Metals": 10,
    "Personal Products": 10,
    "Gas": 10,
    "Minerals & Mining": 9,
    "Media": 9,
    "IT - Hardware": 8,
    "Diversified": 7,
    "Healthcare Equipment & Supplies": 7,
    "Household Products": 7,
    "Telecom - Equipment & Accessories": 6,
    "Financial Technology (Fintech)": 5,
}

df = pd.read_csv("data/industry_data.csv")
df["date"] = pd.to_datetime(df["date"]).dt.date

df = df[df["industry"].isin(SECTOR_TOTALS.keys())]
df = df[df["count"].notna() & (df["count"] > 0)]

df["total_in_sector"] = df["industry"].map(SECTOR_TOTALS)
df["percentage"] = (df["count"] / df["total_in_sector"]) * 100

# Get top 10 industries by average percentage for cleaner visualization
top_industries = df.groupby("industry")["percentage"].mean().nlargest(10).index
df_filtered = df[df["industry"].isin(top_industries)]

# Create figure
fig = go.Figure()

# Add traces for each industry
for industry in top_industries:
    industry_data = df_filtered[df_filtered["industry"] == industry]
    fig.add_trace(go.Scatter(
        x=industry_data["date"],
        y=industry_data["percentage"],
        name=industry,
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=8),
        hovertemplate='%{y:.1f}%<extra>' + industry + '</extra>'
    ))

# Update layout with range selector
fig.update_layout(
    title={
        'text': "52-Week High Stocks by Industry (% of Sector)",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 24},
        'y': 0.95
    },
    xaxis_title="Date",
    yaxis_title="% of Stocks in Sector",
    hovermode="x unified",
    legend_title="Industry",
    height=700,
    margin=dict(t=150, b=80, l=80, r=80),
    yaxis=dict(
        ticksuffix="%",
        range=[0, 100]
    ),
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
