import folium
import pandas as pd

from directories import DATA_DIR


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


# def prep_data_for_display():
#     filepath = DATA_DIR / "azabu_amenities.pkl"
#     df = process_data(filepath)
#     df.to_pickle(DATA_DIR / "azabu_amenities_prepped.pkl")

#     filepath = DATA_DIR / "west_town_amenities.pkl"
#     df = process_data(filepath)
#     df.to_pickle(DATA_DIR / "west_town_amenities_prepped.pkl")


# def process_data(filepath):
#     df = pd.read_pickle(filepath)
#     # df = clean_data(df)
#     # df = reduce_data(df)    
#     df = add_to_dataframe(df)
#     return just_what_is_needed(df)


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


def add_to_dataframe(df):
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
        lambda row: create_marker(row.lat, row.lon, row["name"], row["Category"]),
        axis = 1
    )
    return df


def create_marker(lat, lng, name, category):
    marker_radius = 1
    # color = "#9EA856"
    color = COLORS[category]
    return folium.CircleMarker(
        location=[lat, lng], 
        radius=marker_radius, 
        tooltip=f"{name} ({category})",
        color=color,
        )


def just_what_is_needed(df):
    columns_to_keep = [
        "walking time",
        # "biking time",
        "Marker",
        "Category",
        "Name",
    ]
    return df[columns_to_keep]



if __name__ == "__main__":
    filepath = DATA_DIR / "azabu_amenities.pkl"
    df = process_data(filepath)
    df.to_pickle(DATA_DIR / "azabu_amenities_prepped.pkl")

    filepath = DATA_DIR / "west_town_amenities.pkl"
    df = process_data(filepath)
    df.to_pickle(DATA_DIR / "west_town_amenities_prepped.pkl")