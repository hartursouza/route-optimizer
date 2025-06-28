const map = L.map("map").setView([-3.7319, -38.5267], 13); // Fortaleza

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 18,
}).addTo(map);

const coordenadas = [
  [-38.5267, -3.7319], // [lon, lat]
  [-38.52, -3.74],
  [-38.51, -3.735],
];

fetch("/route/create", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ coordenadas }),
})
  .then((res) => res.json())
  .then((data) => {
    const coords = data.features[0].geometry.coordinates.map((coord) => [
      coord[1], // lat
      coord[0], // lon
    ]);
    L.polyline(coords, { color: "blue" }).addTo(map);
    map.fitBounds(L.polyline(coords).getBounds());
  })
  .catch((err) => console.error(err));
