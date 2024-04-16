import time

from selenium.webdriver.common.by import By
import re

import MainPageScraper
from Chrome import ChromeConnection


def get_price(main_element):
    price_element = get_price_element_from_main_element(main_element)
    if price_element is None: return None
    prices = get_prices(price_element)
    return prices


def get_price_element_from_main_element(element):
    path_to_price_menu = '//section//div[@class="_tr4owt"]/span'
    try:
        price = element.find_elements(By.XPATH, path_to_price_menu)

        if price is None or not price: return None
    except:
        return None
    return price


def get_prices(price_elements):
    master = {'price': 'N/A', 'cleaning': 'N/A', 'service': 'N/A', 'taxes': 'N/A'}
    for i in range(len(price_elements)):
        html_string = price_elements[i].get_attribute('innerHTML')
        if 'night' in html_string:
            master['price'] = get_price_at_head_of_string(html_string)
        if 'Tax' in html_string:
            master['taxes'] = get_price_at_head_of_string(get_html_string(price_elements[i + 1]))
        if 'service' in html_string:
            master['service'] = get_price_at_head_of_string(get_html_string(price_elements[i + 1]))
        if 'Clean' in html_string:
            master['cleaning'] = get_price_at_head_of_string(get_html_string(price_elements[i + 1]))
    return master


def get_html_string(element):
    return re.sub('<.*?>', '', element.get_attribute('innerHTML'))


def get_price_at_head_of_string(html_string):
    html_string = re.sub('<.*?>', '', html_string)
    return html_string.split('&')[0][1:]


def update_price_from_thumbnails():
    path = ""


def clean_thumbnail_price(price_elements):
    prices = []
    if not price_elements: return None
    word_chuncks = price_elements.split(' ')
    for chunky in word_chuncks:
        chunk = chunky.replace('$', '')
        if chunk.isnumeric(): prices.append(chunk)
    if not prices:return None
    return min(prices)


def scrape_thumbnails_for_prices(url, master):
    driver = ChromeConnection.make_chrome_connection()
    driver.get(url)
    print(url)
    time.sleep(1)
    number_of_pages = MainPageScraper.get_number_of_pages(driver)
    print("number of pages: ")
    print(number_of_pages)
    start_thumbnail_price_scrape(driver, number_of_pages, master)


def start_thumbnail_price_scrape(driver, number_of_links, master):
    if number_of_links == 1:
        print("scrape page one time")
        scrape_airbnb_thumbnail_page(driver,master)
    for i in range(number_of_links):
        print("scrape page: ", i)
        scrape_airbnb_thumbnail_page(driver, master)
        if ChromeConnection.click_next_button(driver) is None:
            print("no more pages")
            return



def scrape_airbnb_thumbnail_page(driver, master):
    sample_elements = MainPageScraper.get_the_sample_elements_on_page(driver)
    if sample_elements is None:
        return None
    for element in sample_elements:
        id = MainPageScraper.get_unit_id_from_sample_element(element)
        price = MainPageScraper.get_unit_price_from_sample_element(element)
        price = clean_thumbnail_price(price)
        if id is not None and price is not None:
            master[id] = {'price': price}
