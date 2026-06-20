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

DB_PATH = '/db/weather_site.db'


def get_entries(month, driver):
    '''Takes the current month being searched.
    Scrapes variables for the dates that are visible and adds them to the weather_data dict.'''
    weather_section = driver.find_element(By.ID, 'weather')
    entries = weather_section.find_elements(By.CLASS_NAME, 'section')
    # Using try blocks in case an element doesn't load in time. If the data is missed, the program will keep running
    for entry in entries:
        try:
            date = entry.find_element(By.CLASS_NAME, 'date').text
        except NoSuchElementException:
            continue
        try:
            temp_low = entry.find_element(By.CLASS_NAME, 'tempLow').text
        except NoSuchElementException:
            continue
        try:
            time_of_day = entry.find_element(By.CLASS_NAME, 'time').text
        except NoSuchElementException:
            continue
        try:
            temp_high = entry.find_element(By.CLASS_NAME, 'temp').text
        except NoSuchElementException:
            continue
        try:
            wind = entry.find_element(By.CSS_SELECTOR, '.wind div').text
        except NoSuchElementException:
            continue
        if time_of_day:
            try:
                weather_data['month'].append(month)
                weather_data['date'].append(date)
                weather_data['time'].append(time_of_day)
                weather_data['temp_low'].append(temp_low)
                weather_data['temp_high'].append(temp_high)
                weather_data['wind'].append(wind)
            except Exception as e:
                print(e)
                pass


def scrape_nyc(driver, nyc_months, nyc_years):
    try:
        driver.get("https://www.timeanddate.com/weather/")
    except Exception as e:
        print("couldn't get the web page")
        print(f"Exception: {type(e).__name__} {e}")

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

    sleep(3)

    # Find link to past weather and click
    layout_hero = driver.find_element(By.CLASS_NAME, 'layout-grid__hero')
    fixed_links = layout_hero.find_elements(By.CSS_SELECTOR, 'nav div a')
    for i in fixed_links:
        if 'Past' in i.text:
            i.click()
            break
        else:
            pass

    sleep(2)

    # Iterate through each month for each year. Find the links to move the visible dates on the page
    for year in range(int(nyc_years[0]), int(nyc_years[1])):
    # for year in [nyc_years[1]]:
        for month in nyc_months:
        # for month in [nyc_months[0]]:
            month_option = str(year) + '-' + month
            month_nav = Select(driver.find_element(By.ID, 'month'))
            month_nav.select_by_value(month_option)
            weather_links = driver.find_element(By.CLASS_NAME, 'weatherLinks')
            next_date_page = weather_links.find_elements(By.TAG_NAME, 'a')
            sleep(1)
            page = 0
            # Paginate through the dates, call the get_entries function to scrap five visible dates. Increase the scroll by 5 dates
            while page < 32:
                try:
                    next_date_page[page].click()
                    sleep(1)
                    get_entries(month_option, driver)
                except IndexError:
                    pass
                page += 5

    try:
        df = pd.DataFrame.from_dict(weather_data)
        df.to_csv('../csv/weather.csv', index=False)
    except Exception as e:
        print(f'Exception: {e}')

weather_data = {
    'month': [],
    'date': [],
    'time': [],
    'temp_low': [],
    'temp_high': [],
    'wind': []

}
