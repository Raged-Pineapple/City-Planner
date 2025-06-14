import osmnx as ox
import networkx as nx
import os

CITY = "Bengaluru, India"
MODE = "drive"
OUTPUT_PATH = os.path.join("backend", "output", "bengaluru_drive.graphml")

print(f"Downloading road network for {CITY} (mode={MODE})...")
G = ox.graph_from_place(CITY, network_type=MODE)
print(f"Saving graph to {OUTPUT_PATH}...")
ox.save_graphml(G, OUTPUT_PATH)
print("Done.") 