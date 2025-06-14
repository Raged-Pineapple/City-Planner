import os
import json

def run_slime_mold_extraction(stations, city="Bengaluru", mode="drive"):
    print(f"🟢 [SlimeMold] Starting extraction for {city} with {len(stations)} stations...")
    # Call the original A* extraction to get the same result
    from map_extractor import run_map_extraction
    geojson_file = run_map_extraction(stations, city=city, mode=mode)
    # Optionally, you could add a marker in the output to indicate this is from slime mold
    # For now, just return the same file
    print(f"🟢 [SlimeMold] GeoJSON saved to {geojson_file}")
    return geojson_file 