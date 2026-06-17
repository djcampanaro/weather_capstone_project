import pandas as pd
import sqlalchemy as sa
import sqlite3

tables = ['weather', 'sun']


def load_db():
    with sqlite3.connect('../db/weather_site.db',isolation_level='IMMEDIATE') as conn:
        # conn = sqlite3.connect("../db/lesson.db",isolation_level='IMMEDIATE')
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            month TEXT,
            date TEXT,
            time TEXT,
            temp_low INTEGER,
            temp_high INTEGER,
            wind INTEGER)
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sun (
            date TEXT,
            sunrise TEXT,
            sunset TEXT,
            length TEXT,
            diff TEXT,
            solar_noon TEXT,
            mil_miles TEXT
            )                       
        """)

    engine = sa.create_engine('sqlite:///../db/weather_site.db')

    for table in tables:
        t_name = table.lower()
        csv_file = "../csv/" + table + ".csv"
        data = pd.read_csv(csv_file, sep=',')
        new_data = data.to_sql(t_name, engine, if_exists='append', index=False)
