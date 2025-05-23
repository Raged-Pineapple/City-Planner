// const map = L.map('map').setView([12.9716, 77.5946], 12); // Default: Bengaluru

// L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//     attribution: '&copy; OpenStreetMap contributors'
// }).addTo(map);

// let metroStations = [];

// map.on('click', function(e) {
//     const label = prompt("Enter station name:");
//     if (label) {
//         L.marker(e.latlng).addTo(map).bindPopup(label).openPopup();
//         metroStations.push({ name: label, lat: e.latlng.lat, lon: e.latlng.lng });
//     }
// });

// async function submitStations() {
//     const response = await fetch('http://localhost:5000/compute-routes', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ stations: metroStations })
//     });

//     const data = await response.json();
    
//     // Draw route
//     const routeLayer = L.geoJSON(data, {
//         style: feature => feature.properties.type === "route" ? { color: 'red' } : {}
//     }).addTo(map);

//     // Download link
//     const blob = new Blob([JSON.stringify(data)], { type: "application/json" });
//     const url = URL.createObjectURL(blob);
//     const downloadLink = document.getElementById("download");
//     downloadLink.href = url;
//     downloadLink.style.display = 'inline-block';
// }
let map = L.map('map').setView([12.9716, 77.5946], 12); // Bengaluru
let stations = [];
let markers = [];

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 18,
}).addTo(map);

map.on('click', function(e) {
  let label = prompt("Enter station label:");
  if (label) {
    let marker = L.marker(e.latlng).addTo(map).bindPopup(label).openPopup();
    markers.push(marker);
    stations.push({ label: label, lat: e.latlng.lat, lng: e.latlng.lng });
  }
});

function clearMarkers() {
  // Clear markers from map
  markers.forEach(marker => map.removeLayer(marker));
  markers = [];
  stations = [];
  
  // Clear any existing routes
  map.eachLayer((layer) => {
    if (layer instanceof L.GeoJSON) {
      map.removeLayer(layer);
    }
  });
  
  // Hide download link
  const downloadLink = document.getElementById("download");
  if (downloadLink) {
    downloadLink.style.display = 'none';
  }
}

async function submitStations() {
  if (stations.length < 2) {
    alert('Please add at least 2 stations to generate a route.');
    return;
  }

  try {
    const response = await fetch('http://localhost:5000/generate-route', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ stations: stations })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const geojson = await response.json();
    
    // Clear any existing routes
    map.eachLayer((layer) => {
      if (layer instanceof L.GeoJSON) {
        map.removeLayer(layer);
      }
    });

    // Add the new route
    L.geoJSON(geojson, {
      style: function (feature) {
        return { 
          color: feature.properties.type === "route" ? "red" : "blue",
          weight: 3,
          opacity: 0.7
        };
      }
    }).addTo(map);

    // Create download link for the GeoJSON
    const blob = new Blob([JSON.stringify(geojson)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const downloadLink = document.getElementById("download");
    if (downloadLink) {
      downloadLink.href = url;
      downloadLink.style.display = 'inline-block';
    }
  } catch (error) {
    console.error('Error:', error);
    alert('Failed to generate route. Please try again.');
  }
}
