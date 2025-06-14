from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from map_extractor import run_map_extraction
from slime_mold_extractor import run_slime_mold_extraction
import os
import json

app = Flask(__name__)
# Update CORS to allow requests from Vercel domains
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3000",
            "https://*.vercel.app",
            "https://city-planner.vercel.app"
        ]
    }
})

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
    geojson_path = run_map_extraction(stations, city="Jaipur", mode="drive")

    with open(geojson_path, 'r') as f:
        geojson_data = json.load(f)  # Load as dict

    print("✅ Route computed and GeoJSON loaded.")
    return jsonify(geojson_data)

@app.route('/generate-slime-route', methods=['POST'])
def generate_slime_route():
    data = request.get_json()
    print("🔹 /generate-slime-route called with data:", data)

    if not data or 'stations' not in data:
        return jsonify({'error': 'No stations provided'}), 400

    stations = [
        {"name": s["label"], "lat": s["lat"], "lon": s["lng"]}
        for s in data['stations']
    ]

    print(f"🔸 Running slime mold extraction for {len(stations)} stations")
    geojson_path = run_slime_mold_extraction(stations, city="Jaipur", mode="drive")

    with open(geojson_path, 'r') as f:
        geojson_data = json.load(f)  # Load as dict

    print("✅ Slime mold route computed and GeoJSON loaded.")
    return jsonify(geojson_data)

if __name__ == '__main__':
    app.run(debug=True)
