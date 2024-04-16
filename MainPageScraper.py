import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import Price
from Chrome import ChromeConnection


def scrape_main_pages(url, master, meta):
    driver = ChromeConnection.make_chrome_connection()
    driver.get(url)
    time.sleep(1)
    number_of_pages=get_number_of_pages(driver)
    start_airbnb(driver, int(number_of_pages), master, meta)


def start_airbnb(driver, number_of_links, master, meta):
    if number_of_links == 1:
        scrape_airbnb_page(driver,master, meta)
        return
    for i in range(number_of_links):
        scrape_airbnb_page(driver, master, meta)
        if ChromeConnection.click_next_button(driver) is None:
            return


def get_number_of_pages(driver):
    path = '//*[@id="site-content"]/div/div[3]/div/div/div/nav/div/a'
    elements = driver.find_elements(By.XPATH, path)
    if not elements:return 1
    last_index = elements[-2].get_attribute('innerHTML')
    return int(last_index)

def scrape_airbnb_page(driver, master, meta):

    sample_elements = get_the_sample_elements_on_page(driver)
    if sample_elements is None:
        print("there are no tumbnails listings one this page")
        return None
    for listing_div in sample_elements:
        temp = get_reading_of_listing_div(listing_div)
        if temp is None:continue
        id = temp.pop('id')
        listing = {}
        for k,v in temp.items():
            listing[k]=v
        listing['neighbourhood'] = meta['neighbourhood']
        listing['type'] = meta['type']
        listing['cin'] = meta['cin']
        listing['cout'] = meta['cout']
        master[id] = listing
        print(id, master[id])

def get_reading_of_listing_div(listing_div):
    temp= {}
    id = get_unit_id_from_sample_element(listing_div)
    if id is None: return None
    else: temp['id'] = id
    price = get_unit_price_from_sample_element(listing_div)
    if price is not None: temp['price'] = price
    rating = get_rating_from_sample_element(listing_div)
    if rating is not None:
        temp['rating'] = rating[0]
        temp['reviews'] = rating[1]
    return temp



def get_the_sample_elements_on_page(driver):
    #path = '//*[@id="site-content"]/div/div[2]/div/div/div/div/div[1]/div'
    #path2 = '//*[@id="site-content"]/div//div[@style="display:contents"])'
    path = '//*[@id="site-content"]//div[@class="df8mizf atm_5sauks_glywfm dir dir-ltr"]/div/div'
    try:
        samples_webelements_from_page = driver.find_elements(By.XPATH,path)
        return samples_webelements_from_page
    except:
        print("no sample ids")
        return None



def get_unit_id_from_sample_element(element):
    try:
        unit_id = element.find_element(By.XPATH, "div/div[2]/div/div/div/div/a").get_attribute("target")
        id = unit_id.replace('listing_', '')
        return id
    except:
      return None



def get_unit_title_from_sample_element(element):
    try:
       unit_title = element.find_element(By.XPATH, 'div//div[@data-testid="listing-card-title"]').text
       return unit_title
    except:
      return None

def get_unit_price_from_sample_element(element):
    try:
        unit_price = element.find_element(By.XPATH, 'div//span[@class="_14y1gc"]').text
        price = re.findall(r'\d+', unit_price)
        return min(price)
    except:
        return None

def get_url_from_sample_element(element):
    try:
        temp_url = element.find_element(By.XPATH, "div/div[2]/div/meta[3]").get_attribute("content")
        return temp_url
    except:
        return None


def get_description_from_sample_element(element):
    try:
        unit_titles = element.find_elements(By.XPATH, 'div/div[2]/div/div/div/div/div/div[2]')
    except:
        return None
    for title in unit_titles:
        list_of_cleaned_strings = get_clean_string_of_first_details(title.get_attribute("innerHTML"))
        description = ";".join(list_of_cleaned_strings[0:3])
    return description


def get_rating_from_sample_element(element):
    try:
        unit_titles = element.find_element(By.XPATH, 'div/div[2]/div/div/div/div/div/div[2]')
        description_string = unit_titles.text
        rating = description_string.split("\n")[-1]
        rating = re.findall(r'\b\d+(?:\.\d+)?\b', rating)
        if len(rating)==2:return rating
        else: return None
    except:
        return None



def get_the_url_for_each_unit_on_webpage(sample_elements, url_map):
    url_map = {}
    count = 0
    for e in sample_elements:
        if count >= 5: break
        id = get_unit_id_from_sample_element(e)
        url_map[id] = get_url_from_sample_element(e)
        count += 1
    return url_map

def get_clean_string_of_first_details(html):
    cleaned_string = html.replace('&nbsp;', '').replace('&amp;', ',').replace('Show price breakdown', '').replace('CAD', '')
    cleaned_string = re.sub('<.*?>', ',', cleaned_string)
    cleaned_string = cleaned_string.split(',')
    cleaned_string = [i for i in cleaned_string if i]
    return cleaned_string

