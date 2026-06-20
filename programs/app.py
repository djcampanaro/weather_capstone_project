from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from time import sleep

import matplotlib.pyplot as plt
import load_db
import pandas as pd
import re
import sun
import weather_scrape
import world_weather


def split_month(x, slice):
    '''Takes date data from weather csv and splits the year and month'''
    return x.split('-')[slice]


def remove_arrow(t):
    '''Removes the arrows from the sunrise/sunset times'''
    t = t.split(' ')
    t.pop(2)
    t = ' '.join(t)
    return t


def correct_date(d):
    '''Corrects the format from world_weather scrape'''
    d = d.split('-')
    day = d[1]
    d.pop(1)
    d.append(day)
    d = '-'.join(d)
    return d


def longitude_latitude_float(loc):
    loc_list = re.split(r"[°']+", loc)
    loc_num = float(loc_list[0]) + (float(loc_list[1]) / 60)
    if loc_list[2] == 'S' or loc_list[2] == 'W':
        loc_num *= -1
    return round(loc_num, 3)


# Month and year codes for search. Set up the dict to store the scraped data
nyc_months = ['06', '07', '08', '09']
nyc_years = ['2015', '2025']

run_scrape = input('Do you want to run the scrape programs? (y/n): ')
if run_scrape == 'y':
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    try:
        driver.get("https://www.timeanddate.com/weather/")
    except Exception as e:
        print("couldn't get the web page")
        print(f"Exception: {type(e).__name__} {e}")

    world_weather.world_weather(driver)
    weather_scrape.scrape_nyc(driver, nyc_months, nyc_years)
    sun.sun_times(driver, nyc_months, nyc_years)

# Clean weather data. Save as new csv.
df = pd.read_csv('../csv/weather.csv')
df['year'] = df.month.apply(lambda x: split_month(x, 0))
df['full_date'] = df.month.apply(lambda x: split_month(x, 0)) + '-' + df.month.apply(lambda x: split_month(x, 1)) + '-' + df.date.apply(lambda x: x.split(' ')[2])
df.full_date = pd.to_datetime(df.full_date, errors='coerce')
df.info()
print(df.head())

df_new = df.groupby(['year', 'full_date']).agg({'temp_high': 'max', 'temp_low': 'min', 'wind': 'max'})
df_new.temp_high = df_new.temp_high.apply(lambda x: x.split(':')[1])
df_new.temp_low = df_new.temp_low.apply(lambda x: x.split(':')[1])
df_new.info()
df_new.to_csv('../csv/weather_new.csv')

# # Clean sun data. Save as csv.
df_sun = pd.read_csv('../csv/sun.csv')
df_sun['year'] = df_sun.date.apply(lambda x: x.split('-')[0])
df_sun.date = df_sun.date.apply(lambda x: correct_date(x))
df_sun.date = pd.to_datetime(df_sun.date, errors='coerce')
df_sun.sunrise = df_sun.sunrise.apply(lambda x: remove_arrow(x))
df_sun.sunset = df_sun.sunset.apply(lambda x: remove_arrow(x))
df_sun.info()
print(df_sun.head())

df_sun.to_csv('../csv/sun_new.csv', index=False)

# Clean world_weather data.
df_world = pd.read_csv('../csv/world_weather.csv')
df_world['temp_in_F'] = df_world.temperature.apply(lambda x: x.split(' ')[0])
df_world.info()
print(df_world.head())

df_world.to_csv('../csv/world_weather_new.csv', index=False)

# Clean city location data.
df_city_loc = pd.read_csv('../csv/city_locations.csv')
df_city_loc['longitude_numeric'] = df_city_loc.longitude.apply(lambda x: longitude_latitude_float(x))
df_city_loc['latitude_numeric'] = df_city_loc.latitude.apply(lambda x: longitude_latitude_float(x))
df_city_loc['elevation_numeric'] = df_city_loc.elevation.apply(lambda x: float(x.split(' ')[0]))
df_city_loc.info()
print(df_city_loc.head())

df_city_loc.to_csv('../csv/city_locations_new.csv', index=False)

load_db.load_db()

