"""
Download all amenity and building types accessible within a certain radius
to build a picture of a 15-minute city.

Process: Let's create an exhaustive list of tags available on OSM, organized as 
we see fit, then reduce the results to unique entries.
"""

import yaml

import osmnx as ox
import pandas as pd
from tqdm import tqdm

from directories import DATA_DIR
from . import circle_markers


def load_osm_tags_to_query_for():
    filepath = DATA_DIR / "osm-tags.yaml"
    with open(filepath) as file:
        config = yaml.load(file, Loader=yaml.loader.SafeLoader)
    return config


def download_by_tag(lat_lng, dist):
    config = load_osm_tags_to_query_for()
    dataframes = []

    for category, tags in tqdm(config.items(), desc="Downloading places..."):
        results = ox.features_from_point(lat_lng, tags=tags, dist=dist)
        results["Category"] = [category]*results.shape[0]
        results = circle_markers.add_to_dataframe(results)
        dataframes.append(results)
        
    df = pd.concat(dataframes)
    return df