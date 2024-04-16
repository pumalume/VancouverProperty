import datetime
import time

import pandas as pd
import pyodbc
import csv
from datetime import date


def get_cnxn():
    try:
        cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.1.74,1434;DATABASE=AirBnB;UID=pumal;PWD=Maylee08')
        print("Made connection")
        return cnxn

    except pyodbc.Error as ex:
        print("Connection failed")
        print(ex)
        return None


def make_daily_update_of_Listings(master, meta):
    today = str(datetime.date.today())
    cnxn = get_cnxn()
    cursur = cnxn.cursor()
    for id, value in master.items():
        # values_tuple = (id, meta['cin'], meta['cout'], meta['type'], meta['neighbourhood'], today, id, meta['cin'])
        values_tuple = (id, meta['cin'], meta['type'], meta['neighbourhood'], today)
        listingDateQuery = get_query_string_to_insert_available_listings_to_ListingsDate()
        # loop_through_master_to_load_cursor_with_updates(cursur, master)
        print(listingDateQuery)
        print(values_tuple)
        base_update_execution_with_values(cursur, listingDateQuery, values_tuple)
    cnxn.commit()
    cnxn.close()


def make_daily_update_of_AvailableListings(master, meta):
    today = str(datetime.date.today())
    cnxn = get_cnxn()
    cursur = cnxn.cursor()
    for id, value in master.items():
        values_tuple = (id, meta['cin'], meta['cout'], today)
        listingDateQuery = 'INSERT INTO dbo.AvailableListings (ListingID, cin, cout, InsertDate) SELECT ?,?,?,?'
        # loop_through_master_to_load_cursor_with_updates(cursur, master)
        print(listingDateQuery)
        print(values_tuple)
        base_update_execution_with_values(cursur, listingDateQuery, values_tuple)
    cnxn.commit()
    cnxn.close()


def base_update_execution_with_values(cursor, query, values):
    try:
        cursor.execute(query, values)
        print("commited to: ", query)
        print("commited values: ", values)
    except Exception as ex:
        print("failed to update: ", query)
        print("failed values ", values)
        print(ex)


def base_update_execution_without_values(cursor, query):
    try:
        cursor.execute(query)
        print("commited to: ", query)
    except Exception as ex:
        print("failed to update: ", query)
        print(ex)


def full_select_execution(query):
    master = []
    cnxn = get_cnxn()
    crsr = cnxn.cursor()
    try:
        crsr.execute(query)
        for row in crsr.fetchall():
            master.append(row)
        print("select query finished")
    except pyodbc.Error as ex:
        print("Didn't work")
        cnxn.close()
        return None
    cnxn.close()
    print('connection closed')
    return master


def insert_master_key_values_into_Listings(master):
    cnxn = get_cnxn()
    cursur = cnxn.cursor()
    loop_through_master_to_load_cursor_with_inserts(cursur, master)
    cnxn.commit()
    cnxn.close()


def update_master_key_values_into_Listings(master):
    cnxn = get_cnxn()
    cursur = cnxn.cursor()
    loop_through_master_to_load_cursor_with_updates(cursur, master)
    cnxn.commit()
    cnxn.close()


def loop_through_master_to_load_cursor_with_inserts(cursor, master):
    for key in master:
        column_titles, column_values = get_key_value_from_master(key, master)
        query = get_query_string_to_insert_details_to_Listing(key, column_titles)
        base_update_execution_with_values(cursor, query, tuple(column_values))


def loop_through_master_to_load_cursor_with_updates(cursor, master):
    for key in master:
        query = get_query_to_update_listing(key, master)
        base_update_execution_without_values(cursor, query)


def get_key_value_from_master(key, master):
    list1 = ['id']
    list2 = [key]
    for k, v in master[key].items():
        list1.append(k)
        list2.append(v)
    return list1, list2


######################################
## get query strings for SQL Server ## 
######################################
def get_query_string_to_insert_details_to_Listing(key, columns_list):
    query = "INSERT INTO dbo.Listings ({columns}) SELECT {value_placeholders} WHERE NOT EXISTS(SELECT id FROM dbo.Listings WHERE id = '{id_key}')".format(
        columns=", ".join(columns_list),
        value_placeholders=", ".join(["?"] * len(columns_list)),
        id_key=key
    )
    return query


def get_query_string_to_insert_available_listings_to_ListingsDate():
    sql = 'INSERT INTO dbo.ListingDate (ListingID, ListingDate, ListingType, ListingNeighbourhood, InsertDate) SELECT ?,?,?,?,?'
    return sql


def get_query_string_to_insert_available_listings_to_ListingsDate2():
    sql = 'INSERT INTO dbo.Date (ListingID, ListingDate, cout, ListingType, ListingNeighbourhood, InsertDate) SELECT ?,?,?,?,?'
    return sql


def get_query_to_update_listing(key, master):
    temp = []
    for k, v in master[key].items():
        temp.append(f"{k}='{v}'")
        print(temp)
    query = "UPDATE dbo.Listings SET {value_placeholders} WHERE id = '{ID}'".format(
        value_placeholders=",".join(temp),
        ID=key
    )
    return query


def select_listings_not_in_listings():
    query = 'SELECT ListingID, ListingType, ListingNeighbourhood FROM ListingDate WHERE ListingID NOT IN (SELECT id FROM Listings WHERE Listings.active = \'yes\')'
    print(query)
    return full_select_execution(query)
