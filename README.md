# NYC Weather Capstone Project

This repository collects and visualizes NYC summer weather and world city temperatures. It includes scraper scripts that gather data from timeanddate.com, CSV cleaning and transformation code, and a Streamlit app for interactive visualization.

**Database schema (created by `load_db.py`)**
- `weather` (year TEXT, full_date TEXT, temp_high INTEGER, temp_low INTEGER, wind INTEGER)
- `sun` (date TEXT, sunrise TEXT, sunset TEXT, length TEXT, diff TEXT, solar_noon TEXT, mil_miles TEXT, year TEXT)
- `world_weather` (city TEXT, date_time TEXT, weather_description TEXT, temperature TEXT, temp_in_F TEXT)
- `city_locations` (city TEXT, latitude TEXT, longitude TEXT, elevation TEXT, longitude_numeric TEXT, latitude_numeric TEXT, elevation_numeric TEXT)

## Datasets

| Dataset | Table |
|---|---|
| NYC Summer Weather| `weather` |
| Sun Distance | `sun` |
| World Temperatures | `world_weather` |
| City Location/Elevation | `city_locations` |

## Years Covered
- 2015-2024

Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Prepare the database
1. Run the scrapers and CSV cleaning via `programs/app.py`:

```bash
cd programs
python app.py
```

This will prompt whether you want to run the scrapers. Say `y` to run them. The script produces cleaned CSVs in `csv/` with `_new` suffix.

2. Load CSVs into SQLite DB:
   app.py will automatically load the SQLite DB. However, if changes need to be made or the DB needs to be reloaded:

```bash
python programs/load_db.py
```

Run the Streamlit dashboard

```bash
streamlit run programs/streamlit_app.py
```

**Tabs:**
- **NYC Summer Temperature Highs** — Two line charts that can overlay year options. First is temperature highs by date. Second average highs by month
- **NYC Sunlight** — Two bar charts that follow the distance of NYC from the sun. The first can add an overlay of a line chart depicting the highs of the given year. The second compares the sun's distance with solar noon over the summer.
- **Current World Temperatures** — Scatter plot showing current temps(depending on last scrape) against each cities longitude or elevation.

<img width="1507" height="822" alt="Screenshot 2026-06-19 at 9 26 14 PM" src="https://github.com/user-attachments/assets/db04b855-c30c-4910-82e2-7886cb1affcc" />


Notes & tips
- Scraping: the scrapers use `selenium` and `webdriver-manager` and will open a Chrome instance. If you don't want to scrape, you can manually place CSVs in `csv/` and run `load_db.py`.
- Dates: the `weather` table stores `full_date` as text in `YYYY-MM-DD` format; many charts in `streamlit_app.py` rely on that.
- If you encounter dependency issues, ensure the virtual environment is activated and use `pip install -r requirements.txt`.

---
Generated README for quick onboarding and usage. If you want a longer README with screenshots and examples, tell me which sections to expand.
