import json
import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from groq import Groq


# api key load
def load_api_key() -> str:
    with open(os.path.expanduser("~/.api-keys.json")) as f:
        return json.load(f)["groq-final"]


client = Groq(api_key=load_api_key())


# streamlit app
st.set_page_config(
    page_title="Flight Price & Route Explorer",
    page_icon="✈️",
    layout="wide"
)

st.title("Flight Price & Route Explorer")
st.write(
    "Explore how flight prices relate to distance and compare routes to each other."
)


## CSS STYLING
st.markdown(
    """
    <style>
    /* Filled track */
    div[data-baseweb="slider"] > div > div > div {
        background-color: #4A90E2 !important;
    }

    /* Slider handle (the circle) */
    div[data-baseweb="slider"] [role="slider"] {
        background-color: #4A90E2 !important;
        border-color: #4A90E2 !important;
    }

    /* Slider value (the red number) */
    div[data-baseweb="slider"] div {
        color: #31333F !important;  /* 👈 match your text color */
    }
    </style>
    """,
    unsafe_allow_html=True
)



## LOAD AGGERGATED DATA
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


DATA_PATH = '../../assets/data/route_summary.csv'
route_summary = load_data(DATA_PATH)


airport_df = pd.read_csv("../../assets/data/airport-codes.csv")

# Merge for ORIGIN
route_summary = route_summary.merge(
    airport_df,
    left_on="ORIGIN",
    right_on="iata_code",
    how="left"
).rename(columns={
    "name": "origin_name",
    "municipality": "origin_city"
}).drop(columns=["iata_code"])

# Merge for DEST
route_summary = route_summary.merge(
    airport_df,
    left_on="DEST",
    right_on="iata_code",
    how="left"
).rename(columns={
    "name": "dest_name",
    "municipality": "dest_city"
}).drop(columns=["iata_code"])

route_summary["ROUTE_LABEL"] = (
    route_summary["origin_city"] + " (" + route_summary["ORIGIN"] + ")"
    + " → " +
    route_summary["dest_city"] + " (" + route_summary["DEST"] + ")"
)

route_options = sorted(route_summary["ROUTE_LABEL"].dropna().unique())

tab1, tab2, tab3 = st.tabs([
    "Overview",
    "Route Comparison",
    "AI Route Summary + Recommendation",
])



# TAB 1: OVERVIEW
with tab1:
    st.header("Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Observations", f"{route_summary['num_observations'].sum():,}")
    col2.metric("Unique Routes", f"{route_summary['ROUTE_LABEL'].nunique():,}")
    col3.metric("Average Fare ($)", f"${route_summary['avg_fare'].mean():.2f}")
    col4.metric("Average Distance (miles)", f"{route_summary['avg_distance'].mean():.0f} mi")


    ## FARE VS DISTANCE PLOT
    st.subheader("Fare vs Distance")

    plot_col, filter_col = st.columns([4, 1])


    with filter_col:
        obs_filter = st.slider(
            "Minimum observations",
            min_value=10,
            max_value=int(route_summary["num_observations"].max()),
            value=10
        )

    plot_df = route_summary[
        route_summary["num_observations"] >= obs_filter
    ].copy()

    with plot_col:
        fig_scatter = px.scatter(
            plot_df,
            x="avg_distance",
            y="avg_fare",
            size="num_observations",
            size_max=25,
            color="avg_fare",
            opacity=0.9,
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
                "avg_fare": "Average Fare ($)",
                "median_fare": "Median Fare ($)",
                "min_fare": "Minimum Fare ($)",
                "max_fare": "Maximum Fare ($)",
            },
            title=f"Average Fare vs Distance | Min Observations: {obs_filter}"
        )

        fig_scatter.update_traces(
            marker=dict(
                opacity=0.9,
                line=dict(width=0.4, color="gray")
            )
        )

        

        st.plotly_chart(fig_scatter, use_container_width=True)


    ## TOP 15 MOST EXPENSIVE ROUTES BAR PLOT
    st.subheader("Top 15 Most Expensive Routes")

    top_expensive = route_summary.sort_values("avg_fare", ascending=False).head(15)

    fig_bar = px.bar(
        top_expensive,
        x="avg_fare",
        y="ROUTE_LABEL",
        orientation="h",
        color="avg_distance",
        hover_name=None,  # 👈 removes default bold title
        hover_data={
            "ROUTE_LABEL": False,
            "avg_fare": ":.2f",
            "avg_distance": ":.0f"
       },
        labels={
            "avg_fare": "Average Fare ($)",
            "avg_distance": "Distance (miles)"
        },
        title="Most Expensive Routes"
    )

    fig_bar.update_layout(
        yaxis={"categoryorder": "total ascending"},
        coloraxis_colorbar=dict(
            title="Distance (miles)"
        )
    )

    st.plotly_chart(fig_bar, use_container_width=True)



## TAB 2: ROUTE COMPARISON
with tab2:
    st.header("Route Comparison")

    col1, col2 = st.columns(2)

    with col1:
        route_a = st.selectbox("Route A", route_options)

    with col2:
        route_b = st.selectbox("Route B", route_options, index=1)

    row_a = route_summary[route_summary["ROUTE_LABEL"] == route_a].iloc[0]
    row_b = route_summary[route_summary["ROUTE_LABEL"] == route_b].iloc[0]

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


## TAB 3: AI ROUTE SUMMARY GENERATOR

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

Provide a recommendation to the user for which route they should take and why.

Do not use "Route A" or "Route B" in your response. Use the actual name of the inputted route. 
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
    st.header("AI Route Summary and Recommendation")

    st.write(
    "Choose the two routes you want to compare and click the button to receive an AI-generated flight route recommendation.")

    route_a = st.selectbox("Route 1", route_options, key="ai_a")
    route_b = st.selectbox("Route 2", route_options, key="ai_b", index=1)

    row_a = route_summary[route_summary["ROUTE_LABEL"] == route_a].iloc[0]
    row_b = route_summary[route_summary["ROUTE_LABEL"] == route_b].iloc[0]

    if st.button("Generate Route Summary"):
        st.markdown(generate_ai_explanation(route_a, route_b, row_a, row_b))

    st.write(
    "NOTE: the following recommendation is based on real data, but it is AI-generated and should not be considered as professional advice. Always contact an airline or airport directly for the most accurate, up-to-date information."
    )