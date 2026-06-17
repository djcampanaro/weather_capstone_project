from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from time import sleep

import json
import pandas as pd
import sqlite3


# def scroll_to_select(driver):
#     iframe = driver.find_element(By.CLASS_NAME, 'tb-options')
#     ActionChains(driver)\
#         .scroll_to_element(iframe)\
#         .perform()
#     sleep(1)


def sun_scrape(driver, year, month):
    sun_table = driver.find_element(By.ID, 'as-monthsun')
    sun_table_body = sun_table.find_element(By.TAG_NAME, 'tbody')
    sun_table_days = sun_table_body.find_elements(By.TAG_NAME, 'tr')

    for day in sun_table_days:
        date = day.find_element(By.TAG_NAME, 'th').text
        date = f'{year}-{date}-{month}'
        sun_data['date'].append(date)
        day_values = day.find_elements(By.TAG_NAME, 'td')
        for i in range(len(day_values)):
            if 4 <= i <= 9:
                continue
            elif i < 4:
                cat = sun_data_keys[i+1]
            else:
                cat = sun_data_keys[i-5]
            sun_data[cat].append(day_values[i].text)


def sun_times(sun_driver, nyc_months, nyc_years):
    sleep(2)
    driver = sun_driver
    bk_nav = driver.find_element(By.ID, 'bk-nav')
    bk_links = bk_nav.find_elements(By.TAG_NAME, 'a')

    for item in bk_links:
        if item.text == 'Sun & Moon':
            item.click()
            break
        else:
            pass
    
    sleep(2)
    nav_section = driver.find_element(By.CSS_SELECTOR, 'nav.nav-3')
    nav_links = nav_section.find_elements(By.TAG_NAME, 'a')

    for link in nav_links:
        if link.text == 'Sunrise & Sunset':
            link.click()
            break
        else:
            pass
    sleep(1)

    # scroll_to_select(driver)

    for year in nyc_years:
        year_parent = driver.find_element(By.CLASS_NAME, 'freetextselect')
        year_select = Select(year_parent.find_element(By.TAG_NAME, 'select'))
        year_select.select_by_value(year)
        for month in nyc_months:
            sleep(1)
            month_parent = driver.find_element(By.CLASS_NAME, 'tb-select')
            month_select = Select(month_parent.find_element(By.TAG_NAME, 'select'))
            month_select.select_by_value(month.strip('0'))
            driver.find_element(By.CSS_SELECTOR, 'input.mgl10').click()
            sleep(1)

            sun_scrape(driver, year, month)

    driver.quit()

    df = pd.DataFrame.from_dict(sun_data)
    df.to_csv('../csv/sun.csv', index=False)



sun_data = {
        'date': [],
        'sunrise': [],
        'sunset': [],
        'length': [],
        'diff': [],
        'solar_noon': [],
        'mil_miles': []
    }
sun_data_keys = list(sun_data.keys())
