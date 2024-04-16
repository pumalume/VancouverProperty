def get_neighbourhood_master(neighbourhood:str):
    return create_neighbourhood_master()[neighbourhood]
def create_neighbourhood_master():
    master={}
    #master['burnaby'] = "&ne_lat=49.296493681860674&ne_lng=-122.83409005743528&sw_lat=49.200454767891785&sw_lng=-123.01910034134568"
    master['burnaby_south'] = "&ne_lat=49.25476697870698&ne_lng=-122.92006886245332&sw_lat=49.20005473342054&sw_lng=-123.02542208570156&zoom=13.659773336747241&zoom_level=13.659773336747241&search_by_map=true"
    master['burnaby_north'] = "&ne_lat=49.293290677351855&ne_lng=-122.94117201975143&sw_lat=49.2464545096769&sw_lng=-123.03143676025837&zoom=13.882773337527778&zoom_level=13.882773337527778&search_by_map=true"
    master['simon_fraser'] = "&ne_lat=49.28973407102367&ne_lng=-122.84948839866212&sw_lat=49.225935152687065&sw_lng=-122.97241452359657&zoom=13.43721623261091&zoom_level=13.43721623261091&search_by_map=true"
    master['downtown'] = "&ne_lat=49.292254028259194&ne_lng=-123.10206194600221&sw_lat=49.27062775934807&sw_lng=-123.14274576719663&zoom=15.032480695752437&zoom_level=15.032480695752437&search_by_map=true"
    master['north_vancouver'] = "&ne_lat=49.377038862732235&ne_lng=-122.97327721975847&sw_lat=49.29062575427793&sw_lng=-123.1360125045365&zoom=13.032480695752437&zoom_level=13.032480695752437&search_by_map=true&search_type=user_map_move"
    master['west_vancouver'] = "&ne_lat=49.27401223879424&ne_lng=-123.11248871440182&sw_lat=49.203541863601046&sw_lng=-123.24821683661685&zoom=13.2942881191607&zoom_level=13.2942881191607&search_by_map=true"
    master['east_vancouver_north'] = "&ne_lat=49.29113050473616&ne_lng=-123.02618292820716&sw_lat=49.253147060884004&sw_lng=-123.09938966679658"
    master['east_vancouver_south'] = "&ne_lat=49.25912055721202&ne_lng=-123.03492489401265&sw_lat=49.20736830881278&sw_lng=-123.13459015017986&zoom=13.73984522407714&zoom_level=13.73984522407714&search_by_map=true"
    master['vancouver_west'] = "&ne_lat=49.40305086342869&ne_lng=-123.12903518200153&sw_lat=49.320981037292384&sw_lng=-123.28749999962884&zoom=13.070845221735528&zoom_level=13.070845221735528&search_by_map=true"
    master['new_westminster']="&ne_lat=49.224859703303345&ne_lng=-122.87977045126854&sw_lat=49.18469072858706&sw_lng=-122.95708391374365&zoom=14.106216234952521&zoom_level=14.106216234952521&search_by_map=true"
    master['deep_cove'] = "&ne_lat=49.34168194163326&ne_lng=-122.91055537467037&sw_lat=49.29846329946732&sw_lng=-122.99192301705943&zoom=14.032480695752437&zoom_level=14.032480695752437&search_by_map=true&search_type=user_map_move"
    return master

def create_house_master():
    return ['room_apt', 'room_house', 'entire_house', 'entire_apt', 'entire_guest']


def house_type_url(type):
    if type is None: return None
    entire_apartment = "&adults=2&room_types%5B%5D=Entire%20home%2Fapt&l2_property_type_ids%5B%5D=3"
    room_in_apartment = "&adults=2&l2_property_type_ids%5B%5D=3&room_types%5B%5D=Private%20room"
    entire_house = "&adults=2&room_types%5B%5D=Entire%20home%2Fapt&l2_property_type_ids%5B%5D=1"
    room_in_house = "&l2_property_type_ids%5B%5D=1&room_types%5B%5D=Private%20room"
    entire_guest = "&adults=2&room_types%5B%5D=Entire%20home%2Fapt&l2_property_type_ids%5B%5D=2"
    types = {"entire_house":entire_house,"entire_apt":entire_apartment,"room_house":room_in_house,"room_apt":room_in_apartment, "entire_guest":entire_guest}
    return types[type]