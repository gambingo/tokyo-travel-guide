import folium
import pandas as pd

from src import DATA_DIR


def prep_data_for_display():
    filepath = DATA_DIR / "azabu_restaurants.pkl"
    df = load_data(filepath)
    df.to_pickle(DATA_DIR / "azabu_restaurants_prepped.pkl")

    filepath = DATA_DIR / "west_town_restaurants.pkl"
    df = load_data(filepath)
    df.to_pickle(DATA_DIR / "west_town_restaurants_prepped.pkl")


def load_data(filepath):
    df = pd.read_pickle(filepath)
    # df = clean_data(df)
    # df = reduce_data(df)    
    df = prepare_circle_markers(df)
    return just_what_is_needed(df)


# def clean_data(df):
#     if "lat" not in df.columns:
#         # Extract Lat / Lng
#         latitude = lambda geom: geom.centroid.coords[0][1]
#         longitude = lambda geom: geom.centroid.coords[0][0]
#         df["lat"] = df["geometry"].apply(latitude)
#         df["lon"] = df["geometry"].apply(longitude)
#     return df


# def reduce_data(df, travel_limit=20):
#     # Limit to most that can be displayed
#     subset = ["walking time", "biking time"]
#     df = df.dropna(subset=subset) 
#     df = df[df["biking time"] <= travel_limit]
#     return df


def prepare_circle_markers(df):
    """
    make them ahead of time!
    """
    if "lat" not in df.columns:
        # Extract Lat / Lng
        latitude = lambda geom: geom.centroid.coords[0][1]
        longitude = lambda geom: geom.centroid.coords[0][0]
        df["lat"] = df["geometry"].apply(latitude)
        df["lon"] = df["geometry"].apply(longitude)

    df["Marker"] = df.apply(
        lambda row: create_circle_marker(row.lat, row.lon, row["name"], row["amenity"]),
        axis = 1
    )
    return df


def create_circle_marker(lat, lng, name, amenity_type):
    marker_radius = 1
    color = "#9EA856"
    return folium.CircleMarker(
        location=[lat, lng], 
        radius=marker_radius, 
        tooltip=f"{name} ({amenity_type.replace('_', ' ')})",
        color=color,
        )


def just_what_is_needed(df):
    columns_to_keep = [
        "walking time",
        # "biking time",
        "Marker",
    ]
    return df[columns_to_keep]



if __name__ == "__main__":
    filepath = DATA_DIR / "azabu_restaurants.pkl"
    df = load_data(filepath)
    df.to_pickle(DATA_DIR / "azabu_restaurants_prepped.pkl")

    filepath = DATA_DIR / "west_town_restaurants.pkl"
    df = load_data(filepath)
    df.to_pickle(DATA_DIR / "west_town_restaurants_prepped.pkl")