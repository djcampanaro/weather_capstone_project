import pandas as pd
import sqlalchemy as sa
import sqlite3

tables = ['weather_new', 'sun_new', 'world_weather_new', 'city_locations_new']


def load_db():
    '''Create templates for the SQL database'''
    with sqlite3.connect('../db/weather_site.db',isolation_level='IMMEDIATE') as conn:
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            year TEXT,
            full_date TEXT,
            temp_high INTEGER,
            temp_low INTEGER,
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
            mil_miles TEXT,
            year TEXT
            )                       
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS world_weather (
            city TEXT,
            date_time TEXT,
            weather_description TEXT,
            temperature TEXT,
            temp_in_F TEXT
            )                       
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS city_locations (
            city TEXT,
            latitude TEXT,
            longitude TEXT,
            elevation TEXT,
            longitude_numeric TEXT,
            latitude_numeric TEXT,
            elevation_numeric TEXT
            )
        """)

    engine = sa.create_engine('sqlite:///../db/weather_site.db')

    # Cycle through tables and add to the weather_site database
    for table in tables:
        t_name = table.split('_n')[0].lower()
        csv_file = "../csv/" + table + ".csv"
        data = pd.read_csv(csv_file, sep=',')
        new_data = data.to_sql(t_name, engine, if_exists='append', index=False)
