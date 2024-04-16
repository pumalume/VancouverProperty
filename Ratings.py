from selenium.webdriver.common.by import By

def get_basic_rating_details(element):
    basic_rating_path = '//div[@data-plugin-in-point-id="OVERVIEW_DEFAULT_V2"]/div/div/section/div[3]/*'
    try:
        basic_rating = element.find_elements(By.XPATH, basic_rating_path)
        if basic_rating is None or not basic_rating: return None
    except:
        return None
    return basic_rating


def get_favorite_rating_details(element):
    favorite_rating_path = '//div[@data-plugin-in-point-id="GUEST_FAVORITE_BANNER"]//div[@aria-hidden="true"]'
    try:
        favorite_rating = element.find_elements(By.XPATH, favorite_rating_path)
        if favorite_rating is None or not favorite_rating: return None
    except:
        return None
    return favorite_rating


def get_rating_type(element):
    favorite = get_favorite_rating(element)
    if favorite is not None: return favorite
    return get_basic_rating(element)


def get_basic_rating(element):
    basic_rating = get_basic_rating_details(element)
    if basic_rating is None: return basic_rating
    if len(basic_rating) > 3:
        basic_rating = clean_basic_rating(basic_rating)
    else:
        basic_rating = None
    return basic_rating


def get_favorite_rating(element):
    favorite_rating = get_favorite_rating_details(element)
    if favorite_rating is None: return favorite_rating
    if len(favorite_rating) > 2:
        favorite_rating = clean_favorite_rating(favorite_rating)
    else:
        favorite_rating = None
    return favorite_rating


def clean_basic_rating(rating_list):
    temp_basic = []
    for element in rating_list:
        temp_string = element.get_attribute("innerHTML")
        if any(char in temp_string for char in ('star', '·', '<')): continue
        if '.' in temp_string: temp_basic.append(temp_string)
        if 'review' in temp_string: temp_basic.append(temp_string.split(' ')[0])
    if not temp_basic: return None
    if len(temp_basic) > 1:
        if '.' in temp_basic[0]: return {'rating': temp_basic[0], 'reviews': temp_basic[1]}
    return None


def clean_favorite_rating(rating_list):
    temp = []
    for element in rating_list:
        try:
            temp_string = element.get_attribute("innerHTML")
        except:
            continue
        if temp is None: continue
        if temp_string.isalpha(): continue
        temp.append(temp_string)
    if not temp: return None
    if '.' in temp[0]: return {'rating': temp[0], 'reviews': temp[1]}
    return None
