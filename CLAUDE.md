# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a DSAN 5200 data-driven narrative project analyzing US airline routes using BTS DB1B Market data (Q3 2024 – Q2 2025). The final product is a Quarto website hosted on GU Domains.

## Build & Deploy

```bash
# Build the Quarto website
quarto render

# Full build + deploy (interactive: prompts for GU Domains and GitHub push)
bash build.sh
```

The built site goes to `_site/` (git-ignored). Deployment pushes to `normanwg@gtown03.reclaimhosting.com:/home/normanwg/public_html/airlines/` via rsync.

## Project Structure

- `index.qmd` — landing page
- `report/report.qmd` — main narrative report for general public
- `technical-details/` — appendix notebooks for data scientist audience:
  - `data-cleaning/dataclean.ipynb` — combines 4 quarterly BTS DB1B Market CSVs, cleans records, joins airport lat/lon from OurAirports
  - `eda/eda.ipynb` — exploratory data analysis; `story/main.ipynb` — story/vis notebook
  - `progress-log.qmd` and `llm-usage-log.qmd` — required project logs
- `data/cleandata/T_DB1B_MARKET_CLEAN.csv` — cleaned dataset (git-ignored via `/data/`)
- `assets/references.bib` + `assets/nature.csl` — bibliography

## Quarto Configuration

`_quarto.yml` defines a website with theme `yeti`, navbar with Report and Technical Details dropdown. Renders all `*.qmd` and `*.ipynb` files except those in `xtra/`. Audio files in `audio/` are included as resources.

## Visualization Requirements

The project must include (all publication quality, unified theme/color palette):
- ≥2 static visualizations
- ≥2 interactive visualizations
- ≥1 linked view (interaction in one chart updates another)
- ≥1 infographic

Preferred stack: client-side tools (D3.js, Leaflet, Plotly, Observable, etc.) so the site can be statically hosted.

## Key Constraints

- **AI usage**: AI must not write the narrative text. AI usage must be logged in `technical-details/llm-usage-log.qmd`.
- Raw data files are large and git-ignored (`/data/` in `.gitignore`). The cleaned CSV lives in `data/cleandata/`.
- The technical appendix (`technical-details/`) targets a data scientist audience; the main report targets the general public.
