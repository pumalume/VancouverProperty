import time
from datetime import date

import Components
import Driver
import MainPageScraper
import Price
import SQL
import SuitesList
from Chrome import ChromeConnection
from SuitesList import get_details


# def get_list_of_id_from_SQL():
#     count = 0
#     id_raw_list = SQL.select_all_id()
#     new_list = [x[0]for x in id_raw_list]
#     print(len(new_list))
#     updated_listings = get_updated_listing(new_list)
#     SQL.insert_listing_details_into_Listings(updated_listings)


def get_updated_listing(master, i, ii):
    count = 0
    print(len(master))
    driver = ChromeConnection.make_chrome_connection()
    airbnb_listings = {}
    for id in master:
        print(count)
        count=count+1
        url = Components.get_url_for_serach_listing_with_id(id, i,ii)
        print(url)
        driver.get(url)
        time.sleep(1)
        temp = just_get_price(driver)
        if temp is None: continue
        temp['search_date'] = str(date.today())
        print(temp)
        airbnb_listings[id] = temp
    return airbnb_listings



def update_listing_without_price():
    days_ahead = 2
    while True:
        print("round ----------------------------")
        without_prices = get_list_without_price()
        if len(without_prices)<20: return
        print("len: ", len(without_prices))
        results = get_updated_listing(without_prices, days_ahead, 3)
        SQL.update_listing_without_price(results)
        days_ahead = days_ahead + 3

def get_list_without_price():
    id_raw_list = SQL.select_listings_without_price()
    new_list = [x[0] for x in id_raw_list]
    return new_list




def just_get_price_listing(master):
    driver = ChromeConnection.make_chrome_connection()
    airbnb_listings = {}
    for id, value in master.items():
       url = Components.get_url_for_serach_listing_with_id(id, 1, 2)
       print(url)
       driver.get(url)
       time.sleep(1)
       temp = just_get_price(driver)
       if temp is None: continue
       temp['search_date'] = str(date.today())
       airbnb_listings[id] = temp
    return airbnb_listings


def just_get_price(driver):
    master = {}
    main_element = SuitesList.get_main_element(driver)
    if main_element is None: return None
    price = Price.get_price(main_element)
    if price:
        for key, value in price.items():master[key] = value
    return master

def get_list_of_homes_in_neighbourhood(i,ii):
    master = {}
    house_type = Driver.create_house_master()
    cin, cout = Components.get_checkin_out_dates(i, ii)
    for neighbourhood in Driver.create_neighbourhood_master():
        for type in house_type:
            meta = {'neighbourhood':neighbourhood, 'type':type, 'cin':cin, 'cout':cout}
            url = Driver.get_url_to_search_various_types_of_listings(neighbourhood, type, cin, cout)
            MainPageScraper.scrape_main_pages(url, master, meta)
    return master

def control_the_homes_in_neighbourhood():
    i = 27
    while 1:
        # listingIDs_with_no_neighbours = SQL.get_list_of_null_neighbourhood()
        listingIDs_with_no_neighbours = SQL.get_list_of_all_listings()
        l = len(listingIDs_with_no_neighbours)
        if l < 50: return
        homes_in_neighbourhoods = get_list_of_homes_in_neighbourhood(i, 3)
        for listingID_with_no_neighbour in listingIDs_with_no_neighbours:
            if listingID_with_no_neighbour in homes_in_neighbourhoods:
                id = listingID_with_no_neighbour
                neighbourhood = homes_in_neighbourhoods[id]['neighbourhood']
                SQL.insert_neighbourhood(listingID_with_no_neighbour, neighbourhood)
        i = i + 4

        def clean_the_price():
            query = "SELECT id, price FROM Listings"
            rows = SQL.select_query(query)
            cnxn = SQL.get_cnxn()
            cursor = cnxn.cursor()
            for row in rows:
                i = row[0]
                if row[1] is not None:
                    if not row[1].isnumeric(): print(row[1])
                    price = row[1].replace(',', '')
            #         query = f"UPDATE Listings SET price = '{price}' WHERE id ='{i}'"
            #         try:
            #             print("the query is, ", query)
            #             cursor.execute(query)
            #             print("Good__________________")
            #         except Exception as ex:
            #             print("failed to update: ", query)
            #             print("ERROR: ", ex)
            # cursor.commit()

