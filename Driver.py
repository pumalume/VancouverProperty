import time
import Components
import MainPageScraper
import Maps
import Price
import SQL
import SuitesList
from Chrome import ChromeConnection


# def scan_airbnb_mainpage(master,type):
#     dates = Components.get_check_times(1)
#     cin = str(dates['check_in'])
#     cout = str(dates['check_out'])
#     meta = {'cin':cin,'cout':cout,'type':type}
#     url = Components.get_url_to_search_various_types_of_listings(type, cin,cout)
#     MainPageScraper.scrape_main_pages(url, master, meta)
#     SQL.insert_available_listings_to_ListingsDate(master)


########################################

def run_through_the_types_of_listings_in_neighbourhoods(i, ii):
    master = {}
    cin, cout = Components.get_checkin_out_dates(i, ii)
    for neighbourhood in Maps.create_neighbourhood_master():
        house_type = Maps.create_house_master()
        for type in house_type:
            meta = {'neighbourhood':neighbourhood, 'type':type, 'cin':cin, 'cout':cout}
            url = get_url_to_search_various_types_of_listings(neighbourhood, type, cin, cout)
            MainPageScraper.scrape_main_pages(url, master, meta)
    SQL.make_daily_update_of_Listings(master, meta)


def update_available_listings_today(i, ii):
    master = {}
    cin, cout = Components.get_checkin_out_dates(i, ii)
    for neighbourhood in Maps.create_neighbourhood_master():
        house_type = Maps.create_house_master()
        for type in house_type:
            meta = {'neighbourhood':neighbourhood, 'type':type, 'cin':cin, 'cout':cout}
            url = get_url_to_search_various_types_of_listings(neighbourhood, type, cin, cout)
            MainPageScraper.scrape_main_pages(url, master, meta)
    SQL.make_daily_update_of_AvailableListings(master, meta)



def get_url_to_search_various_types_of_listings(neighbourhood, type, cin, cout):
    geo_coordinates = Maps.create_neighbourhood_master()[neighbourhood]
    http_head= "https://www.airbnb.ca/s/vancouver/homes"
    check_in = "?adults=2&checkin=" + cin
    check_out = '&checkout=' + cout
    if type == 0:
        url = http_head+check_in+check_out+geo_coordinates
    else:
        home_type = Maps.house_type_url(type)
        url = http_head+check_in+check_out+home_type+geo_coordinates
    return url


def print_url_for_each_neighbourhood():
  master = {}
  cin, cout = Components.get_checkin_out_dates(1, 3)
  for neighbourhood in Maps.create_neighbourhood_master():
      house_type = Maps.create_house_master()
      for type in house_type:
          meta = {'neighbourhood': neighbourhood, 'type': type, 'cin': cin, 'cout': cout}
          url = get_url_to_search_various_types_of_listings(neighbourhood, type, cin, cout)
          print(url)
          MainPageScraper.scrape_main_pages(url, master, meta)


def up_the_search_one_day():
    for i in range(2,6):
        run_through_the_types_of_listings_in_neighbourhoods(i, 3)


def insert_new_listings():
    master = Components.is_list_of_unqualified_listings()
    print(master)
    airbnb_listing = SuitesList.scrape_unqualified_listings(master)
    SQL.insert_master_key_values_into_Listings(airbnb_listing)



def run_through_multi_day_cycle(days):
    for i in range(days, 0, -1):
        update_available_listings_today(i,3)


