from datetime import date

import Price
import Ratings
import bs4
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import Components

global number_of_pages
global driver
global next_button
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Chrome import ChromeConnection
import bs4 as bs
import Furbishings


def scrape_unqualified_listings(master: {}):
    driver = ChromeConnection.make_chrome_connection()
    airbnb_listings = {}
    for id, value in master.items():
        url = Components.get_url_for_serach_listing_with_id(id, 2, 2)
        print(url)
        driver.get(url)
        time.sleep(1)
        temp = get_details(driver)
        if temp is None: continue
        temp['search_type'] = value['search_type']
        temp['neighbourhood'] = value['search_neighbourhood']
        temp['search_date'] = str(date.today())
        airbnb_listings[id] = temp
    return airbnb_listings



def get_details(driver):
    master = {}
    main_element = get_main_element(driver)
    if main_element is None: return None
    rating = Ratings.get_rating_type(main_element)
    price = Price.get_price(main_element)
    furbishing = Furbishings.get_furbishing_master(main_element)
    if rating:
        for key, value in rating.items(): master[key] = value
    if price:
        for key, value in price.items():master[key] = value
    if furbishing:
        for key, value in furbishing.items(): master[key] = value
    return master
def get_main_element(driver):
    path = '//*[@id="site-content"]'
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, path))
        )
        main_element = driver.find_element(By.XPATH, path)
        if main_element is None: return None
    except: return None
    return main_element







# PATH = '//*[@id="site-content"]//div[@data-plugin-in-point-id="GUEST_FAVORITE_BANNER"]//div[@aria-hidden="true"]'
 #    PATH2 = '//*[@id="site-content"]//div[@data-plugin-in-point-id="OVERgVIEW_DEFAULT_V2"]/div/div/section/div[3]'