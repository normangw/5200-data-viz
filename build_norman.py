import json, uuid

def cell(cell_type, source, outputs=None):
    return {
        "cell_type": cell_type,
        "id": uuid.uuid4().hex[:8],
        "metadata": {},
        "source": [source],
        **({"outputs": outputs or [], "execution_count": None} if cell_type == "code" else {})
    }

raw_header = (
    "---\n"
    'title: "Carrier Competition & Fare — Linked View"\n'
    "format:\n"
    "  html:\n"
    "    toc: true\n"
    "    embed-resources: true\n"
    "    theme: yeti\n"
    "    code-fold: true\n"
    "execute:\n"
    "  echo: true\n"
    "  warning: false\n"
    "---"
)

md_intro = (
    "# Linked View: Airport Competition vs. Fare\n\n"
    "**Norman's contribution to Example 2 — Monopolistic Pricing.**\n\n"
    "Argument: airports served by fewer carriers have systematically higher average fares.\n\n"
    "- **Map**: each airport dot colored by number of carriers (blue = competitive, red = monopoly)\n"
    "- **Scatterplot**: avg fare vs carrier count — click a dot on the map to highlight it here"
)

md_s1 = "## 1. Setup & Data Prep"

code_setup = (
    "import pandas as pd\n"
    "import numpy as np\n"
    "import json\n"
    "import plotly.graph_objects as go\n"
    "import plotly.io as pio\n"
    "from IPython.display import HTML\n"
    "\n"
    'pio.renderers.default = "plotly_mimetype+notebook_connected"\n'
    "\n"
    'DATA      = "../../assets/data"\n'
    'CLEAN_CSV = "../../data/cleandata/T_DB1B_MARKET_CLEAN.csv"\n'
    "\n"
    "# Load airport carrier data (lat/lon + carrier shares)\n"
    'with open(f"{DATA}/airport_carriers.json", encoding="utf-8") as f:\n'
    "    ap_raw = json.load(f)\n"
    "\n"
    "ap_df = pd.DataFrame([\n"
    "    {\n"
    '        "AIRPORT":       d["AIRPORT"],\n'
    '        "LAT":           d["LAT"],\n'
    '        "LON":           d["LON"],\n'
    '        "TOTAL_PAX":     d["TOTAL_PAX"],\n'
    '        "CARRIER_COUNT": len(d["carriers"]),\n'
    "    }\n"
    "    for d in ap_raw\n"
    "])\n"
    "\n"
    "# Compute avg fare per origin airport from clean CSV\n"
    'fare_df = (\n'
    '    pd.read_csv(CLEAN_CSV, usecols=["ORIGIN", "MARKET_FARE", "REPORTING_CARRIER"])\n'
    '    .groupby("ORIGIN")\n'
    '    .agg(AVG_FARE=("MARKET_FARE", "mean"))\n'
    "    .reset_index()\n"
    '    .rename(columns={"ORIGIN": "AIRPORT"})\n'
    ")\n"
    "\n"
    "airport = (\n"
    "    ap_df\n"
    '    .merge(fare_df, on="AIRPORT", how="inner")\n'
    '    .query("LON > -130 and LON < -60 and LAT > 24 and LAT < 50")\n'
    "    .reset_index(drop=True)\n"
    ")\n"
    "\n"
    'airport.to_json(f"{DATA}/airport_summary.json", orient="records", indent=2)\n'
    'print(f"Airport summary: {len(airport)} airports")\n'
    'print(airport[["AIRPORT","CARRIER_COUNT","AVG_FARE","TOTAL_PAX"]].describe())\n'
    "airport.head()"
)

md_s2 = "## 2. Map — Carrier Count per Airport"

code_map = (
    "fig_map = go.Figure(go.Scattergeo(\n"
    '    lon=airport["LON"],\n'
    '    lat=airport["LAT"],\n'
    '    text=airport["AIRPORT"],\n'
    '    customdata=airport[["AIRPORT", "CARRIER_COUNT", "AVG_FARE"]].values,\n'
    '    mode="markers",\n'
    "    marker=dict(\n"
    '        size=(airport["TOTAL_PAX"] / airport["TOTAL_PAX"].max() * 22 + 5).clip(5, 27),\n'
    '        color=airport["CARRIER_COUNT"],\n'
    '        colorscale="RdBu_r",\n'
    "        colorbar=dict(title=\"# Carriers\", x=1.01),\n"
    '        line=dict(width=0.5, color="white"),\n'
    "        opacity=0.85,\n"
    "    ),\n"
    "    hovertemplate=(\n"
    '        "<b>%{customdata[0]}</b><br>"\n'
    '        "Carriers: %{customdata[1]}<br>"\n'
    '        "Avg Fare: $%{customdata[2]:.0f}<br>"\n'
    '        "<extra></extra>"\n'
    "    ),\n"
    "))\n"
    "\n"
    "fig_map.update_layout(\n"
    "    geo=dict(\n"
    '        scope="usa",\n'
    '        projection_type="albers usa",\n'
    "        showland=True, landcolor=\"#f5f5f5\",\n"
    "        showlakes=True, lakecolor=\"#d0e8f5\",\n"
    "        showsubunits=True, subunitcolor=\"#ddd\",\n"
    "    ),\n"
    "    height=420,\n"
    "    margin=dict(l=0, r=60, t=30, b=0),\n"
    '    paper_bgcolor="white",\n'
    "    title=dict(text=\"Number of Carriers per Airport\", x=0.5, font=dict(size=14)),\n"
    ")\n"
    "\n"
    "fig_map.show()"
)

md_s3 = "## 3. Scatterplot — Carrier Count vs. Avg Fare"

code_scatter = (
    "fig_scatter = go.Figure(go.Scatter(\n"
    '    x=airport["CARRIER_COUNT"],\n'
    '    y=airport["AVG_FARE"],\n'
    '    mode="markers",\n'
    '    text=airport["AIRPORT"],\n'
    '    customdata=airport[["AIRPORT", "CARRIER_COUNT", "AVG_FARE", "TOTAL_PAX"]].values,\n'
    "    marker=dict(\n"
    "        size=8,\n"
    '        color=airport["CARRIER_COUNT"],\n'
    '        colorscale="RdBu_r",\n'
    "        colorbar=dict(title=\"# Carriers\", x=1.01),\n"
    '        line=dict(width=0.5, color="white"),\n'
    "        opacity=0.75,\n"
    "    ),\n"
    "    hovertemplate=(\n"
    '        "<b>%{customdata[0]}</b><br>"\n'
    '        "Carriers: %{customdata[1]}<br>"\n'
    '        "Avg Fare: $%{customdata[2]:.0f}<br>"\n'
    '        "Passengers: %{customdata[3]:,.0f}<br>"\n'
    '        "<extra></extra>"\n'
    "    ),\n"
    "))\n"
    "\n"
    "# Trendline\n"
    'm = np.polyfit(airport["CARRIER_COUNT"], airport["AVG_FARE"], 1)\n'
    'x_line = np.linspace(airport["CARRIER_COUNT"].min(), airport["CARRIER_COUNT"].max(), 100)\n'
    "fig_scatter.add_trace(go.Scatter(\n"
    "    x=x_line, y=np.polyval(m, x_line),\n"
    '    mode="lines", name="Trend",\n'
    '    line=dict(color="#555", dash="dash", width=1.5),\n'
    '    hoverinfo="skip",\n'
    "))\n"
    "\n"
    "fig_scatter.update_layout(\n"
    '    xaxis_title="Number of Carriers",\n'
    '    yaxis_title="Average Fare (USD)",\n'
    "    height=420,\n"
    "    margin=dict(l=60, r=60, t=30, b=50),\n"
    '    plot_bgcolor="white",\n'
    '    paper_bgcolor="white",\n'
    "    showlegend=False,\n"
    "    title=dict(text=\"Fewer Carriers \u2192 Higher Fares\", x=0.5, font=dict(size=14)),\n"
    ")\n"
    'fig_scatter.update_xaxes(showgrid=True, gridcolor="#eee")\n'
    'fig_scatter.update_yaxes(showgrid=True, gridcolor="#eee")\n'
    "\n"
    "fig_scatter.show()"
)

md_s4 = "## 4. Linked View — Click Map to Highlight Scatterplot"

# JS block as a plain string — no triple-quote conflict
js_block = (
    "<script>\n"
    "(function() {\n"
    "  function wireLink() {\n"
    "    var mapDiv     = document.getElementById('map-div');\n"
    "    var scatterDiv = document.getElementById('scatter-div');\n"
    "    if (!mapDiv || !scatterDiv) { setTimeout(wireLink, 300); return; }\n"
    "\n"
    "    mapDiv.on('plotly_click', function(data) {\n"
    "      var pt      = data.points[0];\n"
    "      var airport = pt.customdata[0];\n"
    "      var scatterData = scatterDiv.data[0];\n"
    "      var n = scatterData.text.length;\n"
    "      var colors = [], sizes = [];\n"
    "      for (var i = 0; i < n; i++) {\n"
    "        var match = (scatterData.text[i] === airport);\n"
    "        colors.push(match ? '#b2182b' : scatterData.marker.color[i]);\n"
    "        sizes.push(match ? 18 : 8);\n"
    "      }\n"
    "      Plotly.restyle(scatterDiv, {'marker.color': [colors], 'marker.size': [sizes]}, [0]);\n"
    "    });\n"
    "\n"
    "    mapDiv.on('plotly_doubleclick', function() {\n"
    "      var scatterData = scatterDiv.data[0];\n"
    "      var n = scatterData.text.length;\n"
    "      Plotly.restyle(scatterDiv, {\n"
    "        'marker.color': [scatterData.marker.color],\n"
    "        'marker.size':  [Array(n).fill(8)]\n"
    "      }, [0]);\n"
    "    });\n"
    "  }\n"
    "  wireLink();\n"
    "})();\n"
    "</script>"
)

code_linked = (
    "map_html     = fig_map.to_html(full_html=False, include_plotlyjs=False, div_id='map-div')\n"
    "scatter_html = fig_scatter.to_html(full_html=False, include_plotlyjs=False, div_id='scatter-div')\n"
    "\n"
    "js = " + repr(js_block) + "\n"
    "\n"
    "HTML(\n"
    "    '<script src=\"https://cdn.plot.ly/plotly-latest.min.js\"></script>'\n"
    "    + '<p style=\"font-size:13px;color:#555;margin-bottom:8px;\">'\n"
    "    + 'Click an airport on the map to highlight it in the scatterplot. Double-click map to reset.</p>'\n"
    "    + '<div style=\"display:flex;gap:12px;flex-wrap:wrap;\">'\n"
    "    + f'<div style=\"flex:1;min-width:340px\">{map_html}</div>'\n"
    "    + f'<div style=\"flex:1;min-width:340px\">{scatter_html}</div>'\n"
    "    + '</div>'\n"
    "    + js\n"
    ")"
)

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12.12"}
    },
    "cells": [
        cell("raw",      raw_header),
        cell("markdown", md_intro),
        cell("markdown", md_s1),
        cell("code",     code_setup),
        cell("markdown", md_s2),
        cell("code",     code_map),
        cell("markdown", md_s3),
        cell("code",     code_scatter),
        cell("markdown", md_s4),
        cell("code",     code_linked),
    ]
}

path = "C:/Users/Administrator/Desktop/DSAN/5200-data-viz/technical-details/story/norman.ipynb"
with open(path, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Done — norman.ipynb written")
