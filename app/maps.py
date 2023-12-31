import folium
import streamlit as st
import altair as alt
from streamlit_folium import st_folium
import pandas as pd
import numpy as np

from directories import DATA_DIR

pd.options.mode.chained_assignment = None


COLORS = {
    "Community & Worship":              "#357036",
    "Eating":                           "#96B7FA",
    "Education":                        "#9C6CE0",
    "Entertainment, Arts & Culture":    "#7D60A6",
    "Drinking":                         "#7DFA7F",
    "Government Services":              "#E09C82",
    "Healthcare":                       "#A62190",
    "Office":                           "#E0DD55",
    "Shopping":                         "#FA64AB",
}


def azabu_and_west_town():
    travel_time = input_widgets()
    azabu, west_town = load_data()
    dual_maps(azabu, west_town, travel_time)


def input_widgets():
    _, narrow, _ = st.columns([2,5,2])
    with narrow:
        st.write("")
        label = "How long are you willing to walk?"
        travel_time = st.slider(label, value=15, 
                                min_value=1, max_value=20,
                                format="%d minutes")
    return travel_time


# @st.cache_data
def load_data():
    azabu = pd.read_pickle(DATA_DIR / "azabu_places.pkl")
    west_town = pd.read_pickle(DATA_DIR / "west_town_places.pkl")
    return azabu, west_town


@st.cache_data
def filter_data(_azabu, _west_town, travel_time):
    column = "walking time"
    azabu = _azabu[_azabu[column] <= travel_time]
    west_town = _west_town[_west_town[column] <= travel_time]
    return azabu, west_town


def dual_maps(azabu, west_town, travel_time=15):
    """
    Two maps, return null so page doesn't rerun
    """
    azabu, west_town = filter_data(azabu, west_town, travel_time)

    # Initialize Tokyo Map
    tanuki_zaka = (35.655584, 139.730749)
    azabu_fg = folium.FeatureGroup(name="One")
    azabu["Marker"].apply(lambda marker: azabu_fg.add_child(marker))
    tokyo = initialize_map(tanuki_zaka, travel_time)
    
    # Initialize Chicago Map
    iowa_winchester = (41.897747, -87.675867)
    west_town_fg = folium.FeatureGroup(name="Two")
    west_town["Marker"].apply(lambda marker: west_town_fg.add_child(marker))
    chicago = initialize_map(iowa_winchester, travel_time)
    
    col1, col2 = st.columns(2)
    with col1:
        display_map(tokyo, "Azabu-Juban", azabu_fg, travel_time)
        x_lim = hortizontal_bar_chart(azabu, travel_time, "Azabu-Juban")
    with col2:
        display_map(chicago, "West Town", west_town_fg, travel_time)
        hortizontal_bar_chart(west_town, travel_time, "West Town", x_lim)


def initialize_map(location, travel_time):
    # zoom_start = 16 if travel_time > 15 else 14
    zoom_start = 16 if travel_time < 10 else 15
    tiles = "cartodbpositron"
    return folium.Map(location=location, 
                      zoom_start=zoom_start, 
                      tiles=tiles,
                      control_scale=True)


def display_map(_map, key, fg, travel_time):
    """Map & Caption"""
    st.write("")
    town = "Chicago" if key == "West Town" else "Tokyo"
    st.markdown(f"##### {key}, {town}")
    width = 725
    st_folium(_map, key=key, width=width, 
              feature_group_to_add=fg, 
              returned_objects=[])
    

def hortizontal_bar_chart(df, travel_time, town, x_lim=None):
    _domain = list(COLORS.keys())
    _range = list(COLORS.values())

    if x_lim is None:
        x_lim = df["Category"].value_counts().max()
        print(x_lim)
        if x_lim > 100:
            base=50
        else:
            base=10
        x_lim = round_up_to(x_lim, base=base)
        print(x_lim)

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("count(Category)", title="Count of Places", 
                scale=alt.Scale(domain=[0,x_lim])),
        y=alt.Y("Category:O", title=None),
        color=alt.Color("Category", legend=None, 
                        scale=alt.Scale(domain=_domain, range=_range))
    ).configure_axis(labelLimit=1000).properties(title={
        "text":     "What Can You Walk To?",
        "subtitle": f"The kinds of places accessible within {travel_time} minutes of my apartment in {town}.",
    })
    st.altair_chart(chart, use_container_width=True)
    return x_lim
    
def round_up_to(x, base=50):
    # return base * round(x/base)
    return base * np.ceil(x/base)