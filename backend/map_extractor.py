import os
import osmnx as ox
import networkx as nx
import geopandas as gpd
from shapely.geometry import LineString, Point
import json
import pickle

def get_cached_network(city, mode):
    cache_dir = os.path.join("cache")
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, f"{city.lower().replace(' ', '_')}_{mode}_network.pkl")
    
    if os.path.exists(cache_file):
        print(f"Loading cached network for {city} ({mode})...")
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    
    print(f"Downloading road network for {city} using mode: {mode}")
    G = ox.graph_from_place(city + ", India", network_type=mode)
    
    print(f"Caching network for future use...")
    with open(cache_file, 'wb') as f:
        pickle.dump(G, f)
    
    return G

def run_map_extraction(stations, city="Bengaluru", mode="walk"):
    print(f"Starting map extraction for {city}...")

    output_dir = os.path.join("output")
    os.makedirs(output_dir, exist_ok=True)
    geojson_file = os.path.join(output_dir, f"{city.lower().replace(' ', '_')}_metro_routes.geojson")

    # Use cached network instead of downloading each time
    G = get_cached_network(city, mode)

    print("Finding nearest nodes for each station...")
    station_nodes = []
    for station in stations:
        nearest_node = ox.distance.nearest_nodes(G, station['lon'], station['lat'])
        station_nodes.append((station['name'], nearest_node))

    print("Computing optimal routes between stations...")
    routes = []
    for i in range(len(station_nodes) - 1):
        name1, node1 = station_nodes[i]
        name2, node2 = station_nodes[i + 1]
        print(f"  {name1} → {name2}")
        try:
            route = nx.shortest_path(G, node1, node2, weight='length')
            routes.append((name1, name2, route))
        except nx.NetworkXNoPath:
            print(f"  No path between {name1} and {name2}")

    print("Generating GeoJSON output...")
    features = []

    for name, coords in zip([s['name'] for s in stations], [(s['lon'], s['lat']) for s in stations]):
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": coords},
            "properties": {"type": "station", "name": name}
        })

    for name1, name2, route in routes:
        linestring = LineString([ (G.nodes[node]['x'], G.nodes[node]['y']) for node in route ])
        features.append({
            "type": "Feature",
            "geometry": json.loads(gpd.GeoSeries([linestring]).to_json())['features'][0]['geometry'],
            "properties": {"type": "route", "from": name1, "to": name2}
        })

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(geojson_file, 'w') as f:
        json.dump(geojson_data, f)

    print(f"GeoJSON saved to {geojson_file}")
    return geojson_file
