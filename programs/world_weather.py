from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from time import sleep

import json
import pandas as pd
import sqlite3


def world_weather(driver):
    weather_table = driver.find_element(By.CSS_SELECTOR, '.tb-scroll table tbody')
    weather_pairs = weather_table.find_elements(By.TAG_NAME, 'tr')
    city_links = weather_table.find_elements(By.TAG_NAME, 'a')

    sleep(5)

    weather_data = []
    for pair in weather_pairs:
        try:
            city_url = pair.find_elements(By.CSS_SELECTOR, 'td a')
            cities = [link.text for link in city_url]
            urls = [link.get_attribute('href') for link in city_url]

            date_times = [c.find_element(By.XPATH, '../following-sibling::td').text for c in city_url]
            weather_descriptions_img = pair.find_elements(By.CSS_SELECTOR, '.r img')
            weather_descriptions = [img.get_attribute('alt') for img in weather_descriptions_img]
            temperatures = pair.find_elements(By.CSS_SELECTOR, '.rbi')
        except Exception as e:
            print("couldn't extract data from the row")
            print(f"Exception: {type(e).__name__} {e}")
            continue
        else:
            for city, date_time, weather_description, temperature in zip(cities, date_times, weather_descriptions, temperatures):
                weather_data.append({
                    'city': city,
                    'date_time': date_time,
                    'weather_description': weather_description,
                    'temperature': temperature.text
                })

    df = pd.DataFrame.from_dict(weather_data)
    df.to_csv('../csv/world_weather.csv', index=False)

    df['date_time_to_datetime'] = pd.to_datetime(df['date_time'], errors='coerce')
    df['weather_description_clean'] = df.weather_description.str.lower().str.split('. ')
    df.weather_description_clean = ", ".join(df.weather_description_clean)
    df['temerature_numeric'] = df.temperature.str.split(' °').str[0].astype(float)
    df = df.dropna()
