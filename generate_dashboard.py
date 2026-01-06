import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

os.makedirs("docs", exist_ok=True)

SECTOR_URLS = {
    "Aerospace & Defense": "https://www.screener.in/market/IN07/IN0702/IN070201/",
    "Agricultural Food & other Products": "https://www.screener.in/market/IN04/IN0401/IN040101/",
    "Agricultural, Commercial & Construction Vehicles": "https://www.screener.in/market/IN07/IN0702/IN070202/",
    "Auto Components": "https://www.screener.in/market/IN02/IN0201/IN020102/",
    "Automobiles": "https://www.screener.in/market/IN02/IN0201/IN020101/",
    "Banks": "https://www.screener.in/market/IN05/IN0501/IN050102/",
    "Beverages": "https://www.screener.in/market/IN04/IN0401/IN040102/",
    "Capital Markets": "https://www.screener.in/market/IN05/IN0501/IN050103/",
    "Cement & Cement Products": "https://www.screener.in/market/IN01/IN0102/IN010203/",
    "Chemicals & Petrochemicals": "https://www.screener.in/market/IN01/IN0101/IN010101/",
    "Commercial Services & Supplies": "https://www.screener.in/market/IN09/IN0901/IN090104/",
    "Construction": "https://www.screener.in/market/IN07/IN0701/IN070101/",
    "Consumer Durables": "https://www.screener.in/market/IN02/IN0202/IN020201/",
    "Electrical Equipment": "https://www.screener.in/market/IN07/IN0702/IN070203/",
    "Entertainment": "https://www.screener.in/market/IN02/IN0204/IN020402/",
    "Ferrous Metals": "https://www.screener.in/market/IN01/IN0103/IN010301/",
    "Fertilizers & Agrochemicals": "https://www.screener.in/market/IN01/IN0101/IN010102/",
    "Finance": "https://www.screener.in/market/IN05/IN0501/IN050101/",
    "Food Products": "https://www.screener.in/market/IN04/IN0401/IN040104/",
    "Gas": "https://www.screener.in/market/IN03/IN0301/IN030101/",
    "Healthcare Services": "https://www.screener.in/market/IN06/IN0601/IN060103/",
    "Industrial Manufacturing": "https://www.screener.in/market/IN07/IN0702/IN070204/",
    "Industrial Products": "https://www.screener.in/market/IN07/IN0702/IN070205/",
    "Insurance": "https://www.screener.in/market/IN05/IN0501/IN050104/",
    "IT - Services": "https://www.screener.in/market/IN08/IN0801/IN080102/",
    "IT - Software": "https://www.screener.in/market/IN08/IN0801/IN080101/",
    "Leisure Services": "https://www.screener.in/market/IN02/IN0206/IN020601/",
    "Media": "https://www.screener.in/market/IN02/IN0204/IN020401/",
    "Non - Ferrous Metals": "https://www.screener.in/market/IN01/IN0103/IN010302/",
    "Oil": "https://www.screener.in/market/IN03/IN0301/IN030102/",
    "Other Consumer Services": "https://www.screener.in/market/IN02/IN0206/IN020602/",
    "Other Utilities": "https://www.screener.in/market/IN11/IN1102/IN110201/",
    "Paper, Forest & Jute Products": "https://www.screener.in/market/IN01/IN0104/IN010401/",
    "Personal Products": "https://www.screener.in/market/IN04/IN0401/IN040105/",
    "Petroleum Products": "https://www.screener.in/market/IN03/IN0301/IN030103/",
    "Pharmaceuticals & Biotechnology": "https://www.screener.in/market/IN06/IN0601/IN060101/",
    "Power": "https://www.screener.in/market/IN11/IN1101/IN110101/",
    "Realty": "https://www.screener.in/market/IN02/IN0205/IN020501/",
    "Retailing": "https://www.screener.in/market/IN02/IN0206/IN020603/",
    "Telecom - Services": "https://www.screener.in/market/IN10/IN1001/IN100101/",
    "Textiles & Apparels": "https://www.screener.in/market/IN02/IN0203/IN020301/",
    "Transport Infrastructure": "https://www.screener.in/market/IN09/IN0901/IN090103/",
    "Transport Services": "https://www.screener.in/market/IN09/IN0901/IN090102/",
}

SECTOR_TOTALS = {
    "Industrial Products": 159,
    "Finance": 127,
    "Chemicals & Petrochemicals": 108,
    "Consumer Durables": 106,
    "Pharmaceuticals & Biotechnology": 104,
    "Auto Components": 90,
    "Industrial Manufacturing": 70,
    "Textiles & Apparels": 67,
    "Electrical Equipment": 66,
    "Realty": 63,
    "Construction": 61,
    "IT - Software": 53,
    "Leisure Services": 50,
    "Commercial Services & Supplies": 49,
    "Agricultural Food & other Products": 41,
    "Banks": 41,
    "IT - Services": 40,
    "Capital Markets": 39,
    "Healthcare Services": 37,
    "Fertilizers & Agrochemicals": 36,
    "Transport Services": 36,
    "Food Products": 36,
    "Retailing": 35,
    "Power": 33,
    "Cement & Cement Products": 29,
    "Aerospace & Defense": 25,
    "Entertainment": 23,
    "Telecom - Services": 19,
    "Automobiles": 17,
    "Beverages": 17,
    "Ferrous Metals": 15,
    "Transport Infrastructure": 15,
    "Paper, Forest & Jute Products": 14,
    "Insurance": 13,
    "Other Utilities": 12,
    "Petroleum Products": 12,
    "Oil": 12,
    "Agricultural, Commercial & Construction Vehicles": 11,
    "Other Consumer Services": 11,
    "Gas": 11,
    "Personal Products": 10,
    "Media": 10,
    "Non - Ferrous Metals": 10,
}

df = pd.read_csv("data/industry_data.csv")
df["date"] = pd.to_datetime(df["date"]).dt.date

df = df[df["industry"].isin(SECTOR_TOTALS.keys())]
df = df[df["count"].notna() & (df["count"] > 0)]

df["total_in_sector"] = df["industry"].map(SECTOR_TOTALS)
df["percentage"] = (df["count"] / df["total_in_sector"]) * 100

# Filter to only show industries with percentage > 25%
df_filtered = df[df["percentage"] > 25]
top_industries = df_filtered["industry"].unique()

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

chart_html = fig.to_html(include_plotlyjs="cdn", full_html=False)

# Calculate rising sectors for different timeframes
def calculate_changes(df, days):
    latest_date = df["date"].max()
    
    if days is None:
        # YTD calculation
        target_date = datetime(latest_date.year, 1, 1).date()
    else:
        target_date = latest_date - timedelta(days=days)
    
    closest_date = df[df["date"] <= target_date]["date"].max()
    
    if pd.isna(closest_date):
        return pd.Series(dtype=float)
    
    latest_data = df[df["date"] == latest_date][["industry", "percentage"]].set_index("industry")
    previous_data = df[df["date"] == closest_date][["industry", "percentage"]].set_index("industry")
    
    changes = latest_data.join(previous_data, lsuffix="_latest", rsuffix="_previous")
    changes["change"] = changes["percentage_latest"] - changes["percentage_previous"]
    return changes["change"]

timeframes = [
    ("1W", 7),
    ("2W", 14),
    ("1M", 30),
    ("3M", 90),
    ("6M", 180),
    ("YTD", None),
    ("1Y", 365),
]

change_data = {}
for label, days in timeframes:
    result = calculate_changes(df, days)
    if not result.empty:
        change_data[label] = result

if change_data:
    change_df = pd.DataFrame(change_data)
    change_df = change_df.dropna(how="all")
    sort_col = "1W" if "1W" in change_df.columns else change_df.columns[0]
    change_df = change_df.sort_values(sort_col, ascending=False, na_position="last")
else:
    change_df = pd.DataFrame()

def get_cell_color(val):
    if pd.isna(val):
        return "#f5f5f5"
    if val > 0:
        intensity = min(val / 30, 1)
        r = int(255 - (intensity * 55))
        g = 255
        b = int(255 - (intensity * 55))
        return f"rgb({r}, {g}, {b})"
    elif val < 0:
        intensity = min(abs(val) / 30, 1)
        r = 255
        g = int(255 - (intensity * 55))
        b = int(255 - (intensity * 55))
        return f"rgb({r}, {g}, {b})"
    return "#f5f5f5"

def format_cell_content(val):
    if pd.isna(val):
        return '<span style="color: #999;">N/A</span>'
    if val > 0:
        return f'<span style="color: #166534;">+{val:.1f}pp</span>'
    elif val < 0:
        return f'<span style="color: #991b1b;">{val:.1f}pp</span>'
    return '<span>0.0pp</span>'

def format_cell(val):
    if pd.isna(val):
        return '<td style="background-color: #f5f5f5; color: #999; text-align: center;">N/A</td>'
    
    if val > 0:
        intensity = min(val / 30, 1)
        r = int(255 - (intensity * 55))
        g = 255
        b = int(255 - (intensity * 55))
        color = f"rgb({r}, {g}, {b})"
        text = f"+{val:.1f}pp"
    elif val < 0:
        intensity = min(abs(val) / 30, 1)
        r = 255
        g = int(255 - (intensity * 55))
        b = int(255 - (intensity * 55))
        color = f"rgb({r}, {g}, {b})"
        text = f"{val:.1f}pp"
    else:
        color = "#f5f5f5"
        text = "0.0pp"
    
    return f'<td style="background-color: {color}; text-align: center; font-weight: 500;">{text}</td>'

def get_sector_link(industry):
    url = SECTOR_URLS.get(industry, "#")
    return f'<a href="{url}" target="_blank" class="sector-link">{industry}</a>'

if not change_df.empty:
    available_timeframes = [(label, days) for label, days in timeframes if label in change_df.columns]
    
    table_rows = []
    for industry in change_df.index:
        cells = "".join([f'<td data-value="{change_df.loc[industry, label] if not pd.isna(change_df.loc[industry, label]) else ""}">{format_cell_content(change_df.loc[industry, label])}</td>' for label, _ in available_timeframes])
        table_rows.append(f'<tr><td class="industry-cell">{get_sector_link(industry)}</td>{cells}</tr>')
    
    header_cells = "".join([f'<th class="sortable" data-col="{i+1}">{label} <span class="sort-arrow">⇅</span></th>' for i, (label, _) in enumerate(available_timeframes)])
    
    table_html = f"""
<div style="margin-top: 40px; font-family: Arial, sans-serif;">
    <h2 style="text-align: center; color: #333; margin-bottom: 20px;">Rising & Falling Sectors by Timeframe</h2>
    <p style="text-align: center; color: #666; margin-bottom: 20px;">Change in % of stocks at 52-week high (click column headers to sort)</p>
    <table id="sector-table" style="width: 100%; max-width: 900px; margin: 0 auto; border-collapse: collapse; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <thead>
            <tr style="background-color: #4a5568; color: white;">
                <th class="sortable" data-col="0">Sector <span class="sort-arrow">⇅</span></th>
                {header_cells}
            </tr>
        </thead>
        <tbody>
            {"".join(table_rows)}
        </tbody>
    </table>
</div>
"""
else:
    table_html = """
<div style="margin-top: 40px; font-family: Arial, sans-serif;">
    <h2 style="text-align: center; color: #333; margin-bottom: 20px;">Rising & Falling Sectors by Timeframe</h2>
    <p style="text-align: center; color: #999;">Not enough historical data to calculate changes.</p>
</div>
"""

full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>52-Week High Stocks by Industry</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #fafafa;
        }}
        #sector-table tbody tr:nth-child(even) {{
            background-color: rgba(0,0,0,0.02);
        }}
        #sector-table tbody tr:hover {{
            background-color: rgba(0,0,0,0.05);
        }}
        #sector-table td, #sector-table th {{
            border-bottom: 1px solid #e2e8f0;
        }}
        #sector-table th.sortable {{
            cursor: pointer;
            user-select: none;
            padding: 12px;
            text-align: center;
            transition: background-color 0.2s;
        }}
        #sector-table th.sortable:first-child {{
            text-align: left;
        }}
        #sector-table th.sortable:hover {{
            background-color: #5a6878;
        }}
        #sector-table th .sort-arrow {{
            margin-left: 5px;
            opacity: 0.5;
        }}
        #sector-table th.sorted-asc .sort-arrow::after {{
            content: "↑";
        }}
        #sector-table th.sorted-desc .sort-arrow::after {{
            content: "↓";
        }}
        #sector-table th.sorted-asc .sort-arrow,
        #sector-table th.sorted-desc .sort-arrow {{
            opacity: 1;
        }}
        #sector-table td {{
            padding: 8px 12px;
            text-align: center;
            font-weight: 500;
        }}
        #sector-table td.industry-cell {{
            text-align: left;
        }}
        .sector-link {{
            color: #2563eb;
            text-decoration: none;
            transition: color 0.2s;
        }}
        .sector-link:hover {{
            color: #1d4ed8;
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    {chart_html}
    {table_html}
    
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        const table = document.getElementById('sector-table');
        if (!table) return;
        
        const headers = table.querySelectorAll('th.sortable');
        let currentSort = {{ col: null, dir: null }};
        
        headers.forEach(header => {{
            header.addEventListener('click', function() {{
                const colIndex = parseInt(this.dataset.col);
                const isNumeric = colIndex > 0;
                
                // Determine sort direction
                let dir = 'desc';
                if (currentSort.col === colIndex) {{
                    dir = currentSort.dir === 'desc' ? 'asc' : 'desc';
                }}
                
                // Update header classes
                headers.forEach(h => {{
                    h.classList.remove('sorted-asc', 'sorted-desc');
                    h.querySelector('.sort-arrow').textContent = '⇅';
                }});
                this.classList.add(dir === 'asc' ? 'sorted-asc' : 'sorted-desc');
                this.querySelector('.sort-arrow').textContent = dir === 'asc' ? '↑' : '↓';
                
                // Sort rows
                const tbody = table.querySelector('tbody');
                const rows = Array.from(tbody.querySelectorAll('tr'));
                
                rows.sort((a, b) => {{
                    let aVal, bVal;
                    
                    if (isNumeric) {{
                        aVal = a.cells[colIndex].dataset.value;
                        bVal = b.cells[colIndex].dataset.value;
                        aVal = aVal === '' ? -Infinity : parseFloat(aVal);
                        bVal = bVal === '' ? -Infinity : parseFloat(bVal);
                    }} else {{
                        aVal = a.cells[colIndex].textContent.trim();
                        bVal = b.cells[colIndex].textContent.trim();
                    }}
                    
                    if (aVal < bVal) return dir === 'asc' ? -1 : 1;
                    if (aVal > bVal) return dir === 'asc' ? 1 : -1;
                    return 0;
                }});
                
                rows.forEach(row => tbody.appendChild(row));
                currentSort = {{ col: colIndex, dir: dir }};
                
                // Re-apply row colors after sorting
                applyRowColors();
            }});
        }});
        
        function applyRowColors() {{
            const rows = table.querySelectorAll('tbody tr');
            rows.forEach((row, index) => {{
                // Apply cell background colors based on data-value
                Array.from(row.cells).forEach((cell, cellIndex) => {{
                    if (cellIndex > 0) {{
                        const val = parseFloat(cell.dataset.value);
                        if (isNaN(val) || cell.dataset.value === '') {{
                            cell.style.backgroundColor = '#f5f5f5';
                        }} else if (val > 0) {{
                            const intensity = Math.min(val / 30, 1);
                            const r = Math.round(255 - (intensity * 55));
                            const g = 255;
                            const b = Math.round(255 - (intensity * 55));
                            cell.style.backgroundColor = `rgb(${{r}}, ${{g}}, ${{b}})`;
                        }} else if (val < 0) {{
                            const intensity = Math.min(Math.abs(val) / 30, 1);
                            const r = 255;
                            const g = Math.round(255 - (intensity * 55));
                            const b = Math.round(255 - (intensity * 55));
                            cell.style.backgroundColor = `rgb(${{r}}, ${{g}}, ${{b}})`;
                        }} else {{
                            cell.style.backgroundColor = '#f5f5f5';
                        }}
                    }}
                }});
            }});
        }}
        
        // Initial color application
        applyRowColors();
    }});
    </script>
</body>
</html>
"""

with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(full_html)
