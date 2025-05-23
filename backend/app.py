from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from map_extractor import run_map_extraction
import os
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/generate-route', methods=['POST'])
def generate_route():
    data = request.get_json()
    print("🔹 /generate-route called with data:", data)

    if not data or 'stations' not in data:
        return jsonify({'error': 'No stations provided'}), 400

    stations = [
        {"name": s["label"], "lat": s["lat"], "lon": s["lng"]}
        for s in data['stations']
    ]

    print(f"🔸 Running extraction for {len(stations)} stations")
    geojson_path = run_map_extraction(stations, city="Bengaluru", mode="drive")

    with open(geojson_path, 'r') as f:
        geojson_data = json.load(f)  # Load as dict

    print("✅ Route computed and GeoJSON loaded.")
    return jsonify(geojson_data)

if __name__ == '__main__':
    app.run(debug=True)
