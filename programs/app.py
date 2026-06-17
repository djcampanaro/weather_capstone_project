from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from time import sleep

import load_db
import pandas as pd
import sqlalchemy as sa
import sqlite3
import sun
# import weather_scrape
import world_weather


# Month and year codes for search. Set up the dict to store the scraped data
nyc_months = ['06', '07', '08', '09']
nyc_years = ['2021', '2022', '2023', '2024', '2025']

run_scrape = 'y'
# run_scrape = input('Do you want to run the scrape programs? (y/n): ')
if run_scrape == 'y':
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    try:
        driver.get("https://www.timeanddate.com/weather/")
    except Exception as e:
        print("couldn't get the web page")
        print(f"Exception: {type(e).__name__} {e}")
    world_weather.world_weather(driver)

    # Search for city names on the main world weather page. Find 'New York' and click to get to that page
    weather_table = driver.find_element(By.CSS_SELECTOR, '.tb-scroll table tbody')
    weather_pairs = weather_table.find_elements(By.TAG_NAME, 'tr')
    city_links = weather_table.find_elements(By.TAG_NAME, 'a')
    for link in city_links:
        if link.text == 'New York':
            link.click()
            break
        else:
            pass
    # weather_scrape.scrape_nyc(driver, nyc_months, nyc_years)
    # sun.sun_times(driver, nyc_months, nyc_years)

# load_db.load_db()
