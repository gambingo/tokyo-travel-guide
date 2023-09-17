import numpy as np
import osmnx as ox
import networkx as nx
from tqdm import tqdm


tqdm.pandas()


def street_network_and_restaurants(lat_lng, max_travel_time, 
                                   walk_speed=None, bike_speed=None):
    """
    TKTK
    """
    walk_graph, bike_graph = None, None

    # Calculate Radius
    max_speed = walk_speed if bike_speed is None else bike_speed
    radius_miles = (max_travel_time/60) * max_speed
    radius_meters = radius_miles * 1610

    if walk_speed is not None:
        print("Downloading Walking Graph...")
        walk_graph = ox.graph_from_point(lat_lng, network_type="walk", dist=radius_meters)
        walk_graph = add_travel_time_to_graph(walk_graph, walk_speed, "walking time")

    if bike_speed is not None:
        print("Downloading Biking Graph...")
        bike_graph = ox.graph_from_point(lat_lng, network_type="bike", dist=radius_meters)
        bike_graph = add_travel_time_to_graph(bike_graph, bike_speed, "biking time")

    # Restaurants
    # sustenance = ["bar","biergarten","cafe","fast_food","food_court","ice_cream","pub","restaurant"]
    # tags = {"amenity": sustenance}
    tags = {"amenity": True}
    print("Downloading Amenities...")
    amenities = ox.features_from_point(lat_lng, tags=tags, dist=radius_meters)
    
    if walk_speed is not None:
        amenities = calculate_travel_times(walk_graph, amenities, lat_lng, "walking time")
    if bike_speed is not None:
        amenities = calculate_travel_times(bike_graph, amenities, lat_lng, "biking time")

    # Extract Lat / Lng
    latitude = lambda geom: geom.centroid.coords[0][1]
    longitude = lambda geom: geom.centroid.coords[0][0]
    amenities["lat"] = amenities["geometry"].apply(latitude)
    amenities["lon"] = amenities["geometry"].apply(longitude)

    return walk_graph, bike_graph, amenities


def add_travel_time_to_graph(graph, travel_speed, weight_name):
    """
    Specify `travel_speed` in miles per hour
    """
    # Conver miles per hour to meters per minut
    meters_in_a_mile = 1609.34
    meters_per_minute = travel_speed * meters_in_a_mile / 60
    for u, v, k, data in graph.edges(data=True, keys=True):
        data[weight_name] = data['length'] / meters_per_minute
    return graph


def calculate_travel_times(graph, amenities, lat_lng, column):
    """
    The graph nodes are intersections. First, calculate the closest 
    intersection to each amenity, then calcualte the travel times between
    each intersection and graph center. This means that many amentities will
    have the same travel time, but that's an ok estimate for our purposes.
    """
    # Closest Intersection
    centroid_to_latlng = lambda geom: (geom.centroid.coords[0][1], geom.centroid.coords[0][0])
    amenities["graph node"] = amenities["geometry"].apply(
        lambda geom: get_nearest_node(graph, centroid_to_latlng(geom))
        )
    
    # Travel time to graph center (my apartment)
    aprtmnt = get_nearest_node(graph, lat_lng)
    print(f"Calculating {column.title()}...")
    amenities[column] = amenities["graph node"].progress_apply(
         lambda node: shortest_path_length(graph, aprtmnt, node, column)
    )
    return amenities


def shortest_path_length(graph, source, dest, weight):
    try: 
        return nx.shortest_path_length(graph, source, dest, weight=weight)
    except nx.NetworkXNoPath:
        return np.nan


def get_nearest_node(graph, lat_lng):
    """
    Used to find the center node of the graph. If there is no one closest node, 
    osmnx returns a list. Here we simply take the first node from that list. 
    All the nodes will be right on top of each other and there's no point for 
    our purposes in distinguishing between them.
    """
    lat = lat_lng[0]
    lng = lat_lng[1]
    nearest_node = ox.distance.nearest_nodes(graph, lng, lat)
    # nearest_node = ox.distance.nearest_nodes(graph, lat, lng)

    if not isinstance(nearest_node, int):
        nearest_node = nearest_node[0]

    return nearest_node