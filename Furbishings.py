import re
import datetime
from selenium.webdriver.common.by import By
from dateutil.relativedelta import relativedelta



def get_furbishings(elements):
    master = {}
    for i in range(len(elements)):
        html = elements[i].get_attribute('innerHTML')
        html = clean_the_finer_details_of_listing(html)
        if 'guest' in html: master['guest']= html.split(' ')[0]
        if 'bedroom' in html: master['bedroom']= html.split(' ')[0]
        if 'bed' in html and 'room' not in html: master['bed']= html.split(' ')[0]
        if 'bath' in html:
            s = html.split(' ')
            if s[0].isnumeric(): str(s[0])
            else: master['bath'] = '1'
        if 'Superhost' in html: master['superhost']= '1'
        if 'month' in html:
            month = html.split(' ')[0]
            if month.isnumeric():
                master['year'] = calculate_start_year_from_month(int(month))
        if 'year' in html:
            year = html.split(' ')[0]
            if year.isnumeric():
                master['year'] = calculate_start_year_from_year(int(year))
    return master

def clean_the_finer_details_of_listing(html):
    html = html.replace(' · ', '')
    html = re.sub('<.*?>', '', html)
    html = html.replace("·", "")
    return html

def calculate_start_year_from_month(i):
    today_year = (datetime.date.today()-relativedelta(months=i)).year
    return str(today_year)
def calculate_start_year_from_year(i):
    today_year = (datetime.date.today() - relativedelta(years=i)).year
    return str(today_year)


def get_element_for_furbishings(element):
    PATH = '//li[@class="l7n4lsf atm_9s_1o8liyq_keqd55 dir dir-ltr"]'
    try:
        list_of_elements = element.find_elements(By.XPATH, PATH)
        if list_of_elements is None: return None
    except: return None
    return list_of_elements



def get_furbishing_master(main_element):
    elements = get_element_for_furbishings(main_element)
    master = get_furbishings(elements)
    return master

