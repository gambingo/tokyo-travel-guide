import streamlit as st
from PIL import Image

from directories import DATA_DIR, IMG_DIR
from . import utils


@st.cache_data
def load_config_file(filename="article.yaml"):
    filepath = DATA_DIR / filename
    config = utils.load_yaml_file(filepath)
    return config


def page_title_and_subtitle():
    _, cntr, _  = st.columns([1,2.5,1])
    cntr.title("Tokyo Travel Guide")
    
    config = load_config_file()
    content = config["subtitle"][0]
    st.caption(content)
    st.write("")


def image(key):
    config = load_config_file("images.yaml")
    filename = config[key]["filename"]
    filepath = IMG_DIR / filename
    image = Image.open(filepath)
    caption = config[key]["caption"]
    st.image(image, caption=caption)


def write_text(section_title, header_level=3):
    if header_level is not None:
        size = "#"*header_level
        st.markdown(f"{size} {section_title}")

    config = load_config_file()
    for paragraph in config[section_title]:
        st.write(paragraph)


def food_and_drink():
    st.markdown("#### Eat")
    restaurant_sub_sections("restaurants")
    st.markdown("#### Drink")
    restaurant_sub_sections("bars")


def onsens():
    st.markdown("#### Relax")
    restaurant_sub_sections("onsens")


def restaurant_sub_sections(key="restaurants"):
    col1, col2, col3, col4 = st.columns(4)
    columns = {0:  col1, 1:  col2, 2:  col3, 3:  col4,}

    config = load_config_file("recomendations.yaml")
    for ii, (name, dtls) in enumerate(config[key].items()):
        col = columns[ii%4]
        with col:
            restaurant_image(dtls)
            st.markdown(f"**[{name}]({dtls['link']})**")
            for paragraph in dtls['text']:
                st.write(paragraph)
            if "second image" in dtls:
                restaurant_image(dtls, key="second image")


@st.cache_data
def restaurant_image(rstrnt, key="image"):
    if rstrnt[key] is not None:
        filepath = IMG_DIR / rstrnt[key]
    else:
        filepath = IMG_DIR / "arisugawa.jpg"

    if "user" in rstrnt:
        caption = f"Photo by Google Maps user {rstrnt['user']}"
    else:
        caption = None
    st.image(Image.open(filepath), caption=caption)
    

def citations(header_level=5):
    st.markdown("---")
    section_title = "Citations & References"
    size = "#"*header_level
    st.markdown(f"{size} {section_title}")

    config = load_config_file()
    for ii, citation in config[section_title].items():
        st.markdown(f"{ii}. {citation}")