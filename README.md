# NYC Weather Capstone Project

This repository collects and visualizes NYC summer weather and world city temperatures. It includes scraper scripts that gather data from timeanddate.com, CSV cleaning and transformation code, and a Streamlit app for interactive visualization.

**Contents**
- `csv/` — source and cleaned CSV files.
- `db/` — SQLite database (weather_site.db) created by `programs/load_db.py`.
- `programs/` — main scripts:
	- `app.py` — main data-cleaning and optional scraping driver (runs the scrapers and produces cleaned CSVs, then calls `load_db`).
	- `load_db.py` — creates DB schema and loads `_new` CSV files into `db/weather_site.db`.
	- `streamlit_app.py` — Streamlit dashboard to explore the data.
	- `sun.py`, `weather_scrape.py`, `world_weather.py` — scraper modules used by `app.py`.

**Database schema (created by `load_db.py`)**
- `weather` (year TEXT, full_date TEXT, temp_high INTEGER, temp_low INTEGER, wind INTEGER)
- `sun` (date TEXT, sunrise TEXT, sunset TEXT, length TEXT, diff TEXT, solar_noon TEXT, mil_miles TEXT, year TEXT)
- `world_weather` (city TEXT, date_time TEXT, weather_description TEXT, temperature TEXT, temp_in_F TEXT)
- `city_locations` (city TEXT, latitude TEXT, longitude TEXT, elevation TEXT, longitude_numeric TEXT, latitude_numeric TEXT, elevation_numeric TEXT)

Prerequisites
- Python 3.8+
- A modern browser (Chrome) if you will run the scrapers.

Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Optional scraping dependencies
pip install selenium webdriver-manager
```

Prepare the database
1. (Optional) Run the scrapers and CSV cleaning via `programs/app.py`:

```bash
cd programs
python app.py
```

This will prompt whether you want to run the scrapers. Say `y` to run them (requires Chrome + webdriver). The script produces cleaned CSVs in `csv/` with `_new` suffix.

2. Load CSVs into SQLite DB:

```bash
python -c "import programs.load_db as L; L.load_db()"
# or from repository root
python programs/load_db.py
```

Run the Streamlit dashboard

```bash
streamlit run programs/streamlit_app.py
```

Notes & tips
- Scraping: the scrapers use `selenium` and `webdriver-manager` and will open a Chrome instance. If you don't want to scrape, you can manually place CSVs in `csv/` and run `load_db.py`.
- Dates: the `weather` table stores `full_date` as text in `YYYY-MM-DD` format; many charts in `streamlit_app.py` rely on that.
- If you encounter dependency issues, ensure the virtual environment is activated and use `pip install -r requirements.txt`.

Files of interest
- `programs/streamlit_app.py` — interactive charts (Plotly + Streamlit) and examples of overlaying temperature lines on other charts.
- `programs/load_db.py` — database creation and CSV-to-table loading logic.

License & contact
- No license specified. For questions about this project, contact the maintainer (project owner).

---
Generated README for quick onboarding and usage. If you want a longer README with screenshots and examples, tell me which sections to expand.