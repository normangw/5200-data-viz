# The Way Flight Pricing Works is Unfair

**DSAN 5200 Data-Driven Narrative Project**
Akshay Arun, Alexa Nakanishi, Norman Wang — Georgetown University, Spring 2026

## About

This project analyzes US domestic airline pricing using BTS DB1B Market data (Q3 2024 – Q2 2025, 25M+ records). We show that distance alone does not explain what you pay — market structure and carrier concentration play a significant role in driving fares higher.

## Site

Hosted on GU Domains: *(add URL here)*

## Project Structure

```
report/          # Main narrative report (report.qmd)
technical-details/
  data-cleaning/ # Data pipeline notebooks
  eda/           # Exploratory data analysis
  story/         # Visualization notebooks
  appendix.qmd   # Technical appendix
logs/            # Progress log and LLM usage log
assets/data/     # Pre-aggregated JSON data files
```

## Build

```bash
# Render report only
quarto render report/report.qmd

# Render full site
quarto render
```

## Data Sources

- BTS DB1B Market Survey (Q3 2024 – Q2 2025)
- BTS Form 41 P6 carrier financials
- BTS T100 segment data
- OurAirports (lat/lon)

Raw data files are git-ignored due to size.
