import os
import osmnx as ox
import networkx as nx
import geopandas as gpd
from shapely.geometry import LineString, Point
import json

def run_map_extraction(stations, city="Bengaluru", mode="walk"):
    print(f"🚀 Starting map extraction for {city} with {len(stations)} stations...")

    output_dir = os.path.join("backend", "output")
    os.makedirs(output_dir, exist_ok=True)
    geojson_file = os.path.join(output_dir, f"{city.lower().replace(' ', '_')}_metro_routes.geojson")

    print(f"📥 Downloading road network for {city} using mode: {mode}")
    G = ox.graph_from_place(city + ", India", network_type=mode)

    station_nodes = []
    for station in stations:
        nearest_node = ox.distance.nearest_nodes(G, station['lon'], station['lat'])
        station_nodes.append((station['name'], nearest_node))

    print("🧠 Computing optimal routes between stations...")
    routes = []
    for i in range(len(station_nodes) - 1):
        name1, node1 = station_nodes[i]
        name2, node2 = station_nodes[i + 1]
        try:
            route = nx.shortest_path(G, node1, node2, weight='length')
            routes.append((name1, name2, route))
            print(f"   ✅ {name1} → {name2} | {len(route)} nodes")
        except nx.NetworkXNoPath:
            print(f"   ❌ No path between {name1} and {name2}")

    print("🧾 Generating GeoJSON output...")
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

    print(f"📦 GeoJSON saved to {geojson_file}")
    return geojson_file
