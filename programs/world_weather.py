from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from time import sleep

import pandas as pd


def world_weather(driver):
    '''Scrape the current world temperatures. Then gather longitude and elevation info.'''
    weather_table = driver.find_element(By.CSS_SELECTOR, '.tb-scroll table tbody')
    weather_sects = weather_table.find_elements(By.TAG_NAME, 'tr')

    sleep(3)

    weather_data = []
    city_loc = []
    # Find all the elements of current conditions and add them to a list
    for sect in weather_sects:
        try:
            city_url = sect.find_elements(By.CSS_SELECTOR, 'td a')
            cities = [link.text for link in city_url]

            date_times = [c.find_element(By.XPATH, '../following-sibling::td').text for c in city_url]
            weather_descriptions_img = sect.find_elements(By.CSS_SELECTOR, '.r img')
            weather_descriptions = [img.get_attribute('alt') for img in weather_descriptions_img]
            temperatures = sect.find_elements(By.CSS_SELECTOR, '.rbi')
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

    cities = [x['city'] for x in weather_data]
    # Move through the cities found in the previous list and move to their pages to find longitude and elevation stats
    for city in cities:
        try:
            city_url = driver.find_element(By.LINK_TEXT, city)
            city_url.click()
            sleep(1)
            bk_nav = driver.find_element(By.CSS_SELECTOR, '#bk-nav a')
            bk_nav.click()
            sleep(1)
            city_info = driver.find_elements(By.CSS_SELECTOR, '.bk-focus__info table tbody tr td')
        except Exception as e:
            print(f"couldn't click on the link for {city}")
            print(f"Exception: {type(e).__name__} {e}")
            continue
        else:
            # Parse through the text to extrude desired info
            lat_long = city_info[1].text
            elevation = city_info[2].text
            if '/' not in lat_long:
                lat_long = city_info[2].text
                elevation = city_info[3].text
            latitude = lat_long.split('/')[0].strip()
            longitude = lat_long.split('/')[1].strip()
            city_loc.append({
                'city': city,
                'latitude': latitude,
                'longitude': longitude,
                'elevation': elevation,
            })

    df = pd.DataFrame.from_dict(weather_data)
    df.to_csv('../csv/world_weather.csv', index=False)

    df_city_loc = pd.DataFrame.from_dict(df)
    df_city_loc.to_csv('../csv/city_locations.csv', index=False)
