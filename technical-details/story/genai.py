import json
import os
import pandas as pd
import streamlit as st
import plotly.express as px
from groq import Groq


# -----------------------------
# Groq Setup
# -----------------------------

def load_api_key() -> str:
    with open(os.path.expanduser("~/.api-keys.json")) as f:
        return json.load(f)["groq-final"]


client = Groq(api_key=load_api_key())


# -----------------------------
# Streamlit Setup
# -----------------------------

st.set_page_config(
    page_title="Flight Price & Route Explorer",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ Flight Price & Route Explorer")
st.write(
    "Explore how flight prices relate to distance and route characteristics."
)


# -----------------------------
# Load Pre-Aggregated Data
# -----------------------------

@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)

    required_cols = [
        "ROUTE",
        "avg_fare",
        "median_fare",
        "min_fare",
        "max_fare",
        "std_fare",
        "avg_distance",
        "num_observations",
        "ORIGIN",
        "DEST"
    ]

    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        st.error(f"Missing required columns: {missing}")
        st.stop()

    return df


DATA_PATH = '/Volumes/Extreme Pro/DSAN-5200/final-project/route_summary.csv'
route_summary = load_data(DATA_PATH)


airport_df = pd.read_csv("../../assets/data/airports.csv")

# Merge for ORIGIN
route_summary = route_summary.merge(
    airport_df,
    left_on="ORIGIN",
    right_on="iata_code",
    how="left"
).rename(columns={
    "airport_name": "origin_name",
    "city": "origin_city"
}).drop(columns=["iata_code"])

# Merge for DEST
route_summary = route_summary.merge(
    airport_df,
    left_on="DEST",
    right_on="iata_code",
    how="left"
).rename(columns={
    "airport_name": "dest_name",
    "city": "dest_city"
}).drop(columns=["iata_code"])

route_summary["ROUTE_LABEL"] = (
    route_summary["origin_city"] + " (" + route_summary["ORIGIN"] + ")"
    + " → " +
    route_summary["dest_city"] + " (" + route_summary["DEST"] + ")"
)

# -----------------------------
# Sidebar Filter
# -----------------------------

st.sidebar.header("Filters")

min_obs = st.sidebar.slider(
    "Minimum observations per route",
    min_value=1,
    max_value=int(route_summary["num_observations"].max()),
    value=10
)

filtered_routes = route_summary[
    route_summary["num_observations"] >= min_obs
].copy()

#route_options = sorted(filtered_routes["ROUTE_LABEL"].unique())
route_options = sorted(filtered_routes["ROUTE_LABEL"].dropna().unique())

if len(route_options) < 2:
    st.warning("Not enough routes meet the minimum threshold.")
    st.stop()


# -----------------------------
# Tabs
# -----------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Route Comparison",
    "AI Insight Generator",
    "Data Table"
])


# -----------------------------
# Tab 1: Overview
# -----------------------------

with tab1:
    st.header("Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Observations", f"{route_summary['num_observations'].sum():,}")
    col2.metric("Unique Routes", f"{route_summary['ROUTE_LABEL'].nunique():,}")
    col3.metric("Average Fare", f"${route_summary['avg_fare'].mean():.2f}")
    col4.metric("Average Distance", f"{route_summary['avg_distance'].mean():.0f} mi")

    st.subheader("Fare vs Distance")

    fig_scatter = px.scatter(
        filtered_routes,
        x="avg_distance",
        y="avg_fare",
        size="num_observations",
        color="avg_fare",
        hover_name="ROUTE_LABEL",
        hover_data={
            "avg_distance": ":.0f",
            "avg_fare": ":.2f",
            "median_fare": ":.2f",
            "min_fare": ":.2f",
            "max_fare": ":.2f",
            "num_observations": True
        },
        labels={
            "avg_distance": "Distance (miles)",
            "avg_fare": "Average Fare ($)"
        },
        title="Average Fare vs Distance"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    st.subheader("Top 15 Most Expensive Routes")

    top_expensive = filtered_routes.sort_values("avg_fare", ascending=False).head(15)

    fig_bar = px.bar(
        top_expensive,
        x="avg_fare",
        y="ROUTE_LABEL",
        orientation="h",
        color="avg_distance",
        labels={
            "avg_fare": "Average Fare ($)",
            "ROUTE_LABEL": "Route"
        },
        title="Most Expensive Routes"
    )

    fig_bar.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_bar, use_container_width=True)


# -----------------------------
# Tab 2: Route Comparison
# -----------------------------

with tab2:
    st.header("Route Comparison")

    col1, col2 = st.columns(2)

    with col1:
        route_a = st.selectbox("Route A", route_options)

    with col2:
        route_b = st.selectbox("Route B", route_options, index=1)

    row_a = filtered_routes[filtered_routes["ROUTE_LABEL"] == route_a].iloc[0]
    row_b = filtered_routes[filtered_routes["ROUTE_LABEL"] == route_b].iloc[0]

    comparison_df = pd.DataFrame({
        "Metric": [
            "Average Fare",
            "Median Fare",
            "Min Fare",
            "Max Fare",
            "Distance",
            "Observations"
        ],
        route_a: [
            f"${row_a['avg_fare']:.2f}",
            f"${row_a['median_fare']:.2f}",
            f"${row_a['min_fare']:.2f}",
            f"${row_a['max_fare']:.2f}",
            f"{row_a['avg_distance']:.0f} mi",
            f"{row_a['num_observations']:,}"
        ],
        route_b: [
            f"${row_b['avg_fare']:.2f}",
            f"${row_b['median_fare']:.2f}",
            f"${row_b['min_fare']:.2f}",
            f"${row_b['max_fare']:.2f}",
            f"{row_b['avg_distance']:.0f} mi",
            f"{row_b['num_observations']:,}"
        ]
    })

    st.dataframe(comparison_df, use_container_width=True, hide_index=True)

    chart_df = pd.DataFrame({
        "Route": [route_a, route_b],
        "Average Fare": [row_a["avg_fare"], row_b["avg_fare"]],
        "Distance": [row_a["avg_distance"], row_b["avg_distance"]]
    })

    metric = st.selectbox("Metric", ["Average Fare", "Distance"])

    fig_compare = px.bar(
        chart_df,
        x="Route",
        y=metric,
        title=f"{metric}: {route_a} vs {route_b}",
        text_auto=True
    )

    st.plotly_chart(fig_compare, use_container_width=True)


# -----------------------------
# Tab 3: AI Insight Generator
# -----------------------------

def generate_ai_explanation(route_a, route_b, row_a, row_b):
    prompt = f"""
Compare these two flight routes:

Route A: {route_a}
Average fare: ${row_a['avg_fare']:.2f}
Median fare: ${row_a['median_fare']:.2f}
Distance: {row_a['avg_distance']:.0f} miles

Route B: {route_b}
Average fare: ${row_b['avg_fare']:.2f}
Median fare: ${row_b['median_fare']:.2f}
Distance: {row_b['avg_distance']:.0f} miles

Explain whether higher price is related to longer distance.
Keep it concise and analytical.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a data analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except:
        return "AI explanation unavailable."


with tab3:
    st.header("AI Insight Generator")

    route_a = st.selectbox("AI Route A", route_options, key="ai_a")
    route_b = st.selectbox("AI Route B", route_options, key="ai_b", index=1)

    row_a = filtered_routes[filtered_routes["ROUTE_LABEL"] == route_a].iloc[0]
    row_b = filtered_routes[filtered_routes["ROUTE_LABEL"] == route_b].iloc[0]

    if st.button("Generate Insight"):
        st.markdown(generate_ai_explanation(route_a, route_b, row_a, row_b))


# -----------------------------
# Tab 4: Data Table
# -----------------------------

with tab4:
    st.header("Route Summary Table")

    st.dataframe(filtered_routes, use_container_width=True)

    st.download_button(
        "Download CSV",
        filtered_routes.to_csv(index=False),
        "routes.csv",
        "text/csv"
    )