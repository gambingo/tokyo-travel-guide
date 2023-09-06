import osmnx as ox
import networkx as nx


def compute_subgraph(graph, starting_location, travel_time):
      starting_node = get_nearest_node(graph, starting_location)
      subgraph = nx.ego_graph(graph, starting_node, 
                              radius=travel_time, distance="time")
      return subgraph


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



