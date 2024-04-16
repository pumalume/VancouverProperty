import pandas as pd
from Chrome import ChromeConnection
import datetime
from datetime import date
from datetime import timedelta
import SQL
import os



def get_check_times(i, ii):
    check_in_date = date.today() + timedelta(i)
    check_out_date = check_in_date + timedelta(ii)
    check_in_date = str(check_in_date)
    check_out_date = str(check_out_date)
    return {'check_in':check_in_date, 'check_out':check_out_date}

def get_checkin_out_dates(i, ii):
    check_in_date = date.today() + timedelta(i)
    check_out_date = check_in_date + timedelta(ii)
    check_in_date = str(check_in_date)
    check_out_date = str(check_out_date)
    return [check_in_date, check_out_date]


def get_url_for_serach_listing_with_id(id, i, ii):
    http_head = "https://www.airbnb.ca/rooms/"
    id = str(id)
    c = get_check_times(i, ii)
    check_in = "?adults=2&check_in=" + c['check_in']
    check_out = '&check_out=' + c['check_out']
    url = http_head + id + check_in + check_out
    return url


def is_list_of_unqualified_listings():
    temp_list = {}
    unqualified_id = SQL.select_listings_not_in_listings()
    if unqualified_id is None:return None
    for element in unqualified_id:
        dict = {'search_type': element[1], 'search_neighbourhood':element[2]}
        temp_list[element[0]] = dict
    return temp_list




#map = "&ne_lat=49.30127049027083&ne_lng=-123.02522784189227&sw_lat=49.19875145191093&sw_lng=-123.22272765886953&zoom=12.75315647402387&zoom_level=12.75315647402387&search_by_map=true"

def clean_the_price():
    query = "SELECT id, price FROM Listings"
    rows = SQL.select_query(query)
    cnxn = SQL.get_cnxn()
    cursor = cnxn.cursor()
    for row in rows:
        i = row[0]
        if row[1] is not None:
            if not row[1].isnumeric():print(row[1])
            price = row[1].replace(',','')
    #         query = f"UPDATE Listings SET price = '{price}' WHERE id ='{i}'"
    #         try:
    #             print("the query is, ", query)
    #             cursor.execute(query)
    #             print("Good__________________")
    #         except Exception as ex:
    #             print("failed to update: ", query)
    #             print("ERROR: ", ex)
    # cursor.commit()

