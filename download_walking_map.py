import pandas as pd

from directories import DATA_DIR
from src import download


# How fast do we travel?
walking_speed = 3   #mph

# How far could we go in a straight line?
max_travel_time = 20    #minutes

# My Apartment in Tokyo
print("Tokyo!")
tanuki_zaka = (35.655584, 139.730749)
_, _, azabu_places = download.street_network_and_places(
    tanuki_zaka, 
    max_travel_time, 
    walk_speed=walking_speed, 
    )
azabu_places.to_pickle(DATA_DIR / "azabu_places.pkl")

# My Apartment in Chicago
print("Chicago!")
winchester_ave = (41.897995, -87.675876)
_, _, west_town_places = download.street_network_and_places(
    winchester_ave, 
    max_travel_time, 
    walk_speed=walking_speed, 
    )
west_town_places.to_pickle(DATA_DIR / "west_town_places.pkl")


# Reduce to what's necessary
just_what_is_needed = ["Category", "walking time", "name", "Marker"]

azabu_places = pd.read_pickle(DATA_DIR / "azabu_places.pkl")
azabu_places = azabu_places[just_what_is_needed]
azabu_places = azabu_places[azabu_places["walking time"] <= max_travel_time]
azabu_places.to_pickle(DATA_DIR / "azabu_places.pkl")

west_town_places = pd.read_pickle(DATA_DIR / "west_town_places.pkl")
west_town_places = west_town_places[just_what_is_needed]
west_town_places = west_town_places[west_town_places["walking time"] <= max_travel_time]
west_town_places.to_pickle(DATA_DIR / "west_town_places.pkl")