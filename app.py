import streamlit as st

import src.download as download
from src import _isochrone
from src import logic as lg
from src import cost_of_living
from src import maps


st.set_page_config(page_title="Tokyo Travel Guide",
                   page_icon="tokyo-tower",
                   layout="wide",
)

_, narrow, _ = st.columns([2,5,2])
with narrow:
    lg.page_title_and_subtitle()
    lg.image("header_image")
    lg.write_text("introduction", header_level=None)
    lg.write_text("An Organic Metropolis", header_level=2)
    lg.write_text("Slow Down", header_level=2)
    lg.write_text("Temples & Shrines", header_level=4)
    lg.write_text("Architecture", header_level=4)
    cost_of_living()
    lg.write_text("Cost of Living", header_level=None)
    lg.write_text("Eating Well", header_level=2)
    st.write("")
lg.food_and_drink()


_, narrow, _ = st.columns([2,5,2])
with narrow:
    lg.write_text("Change is Constant", header_level=4)
    lg.write_text("A 15-Minute City", header_level=2)
maps.azabu_and_west_town()


_, narrow, _ = st.columns([2,5,2])
with narrow:    
    lg.write_text("Etiquette", header_level=2)
    lg.write_text("Table Manners", header_level=4)
    lg.write_text("Take Your Shoes Off", header_level=4)

    lg.write_text("Onsen", header_level=2)
    lg.write_text("How To", header_level=4)
lg.onsens()
    

_, narrow, _ = st.columns([2,5,2])
with narrow:
    lg.write_text("Navigation", header_level=2)
    lg.image("tokyo_subway_map")
    lg.write_text("navigation_1", header_level=None)
    st.write("")
    _, col1, _, col2, _ = st.columns([1,5,1,5,1])
    with col1:
        lg.image("google_maps_1")
    with col2:
        lg.image("google_maps_2")
    lg.write_text("navigation_2", header_level=None)
    lg.write_text("navigation_3", header_level=None)

    lg.write_text("Tabelog", header_level=4)
    col1, col2 = st.columns(2)
    with col1:
        lg.write_text("Ramen Beast", header_level=4)
    with col2:
        lg.write_text("MyMizu", header_level=4)

    lg.citations()