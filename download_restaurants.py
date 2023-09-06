from src import download, DATA_DIR, prep_data_for_display

# How fast do we travel?
walking_speed = 3   #mph

# How far could we go in a straight line?
max_travel_time = 20    #minutes

# My Apartment in Tokyo
# print("Tokyo!")
# tanuki_zaka = (35.655584, 139.730749)
# _, _, azabu_amenities = download.street_network_and_restaurants(
#     tanuki_zaka, 
#     max_travel_time, 
#     walk_speed=walking_speed, 
#     )
# azabu_amenities.to_pickle(DATA_DIR / "azabu_restaurants.pkl")

# My Apartment in Chicago
print("Chicago!")
winchester_ave = (41.897995, -87.675876)
_, _, west_town_amenities = download.street_network_and_restaurants(
    winchester_ave, 
    max_travel_time, 
    walk_speed=walking_speed, 
    )
# west_town_amenities.to_pickle(DATA_DIR / "west_town_restaurants.pkl")
west_town_amenities.to_pickle(DATA_DIR / "west_town_amenities.pkl")


# prep_data_for_display()
