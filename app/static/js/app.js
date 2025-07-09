function addField() {
  const div = document.createElement("div");
  div.innerHTML = `<input type="text" name="address" placeholder="Outro endereço" required />`;
  document.getElementById("addresses").appendChild(div);
}

const map = L.map("map").setView([-3.7319, -38.5267], 13);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 18,
}).addTo(map);

let polyline = null;
let markers = [];

document.getElementById("route-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const inputs = document.querySelectorAll("input[name='address']");
  const enderecos = Array.from(inputs).map((i) => i.value);

  const res = await fetch("/route/optimized", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ enderecos }),
  });

  const data = await res.json();
  if (data.erro) {
    alert("Erro: " + data.erro);
    return;
  }

  const coords = data.features[0].geometry.coordinates.map((c) => [c[1], c[0]]);

  if (polyline) map.removeLayer(polyline);
  polyline = L.polyline(coords, { color: "blue" }).addTo(map);
  map.fitBounds(polyline.getBounds());

  markers.forEach((m) => map.removeLayer(m));
  markers = [];

  data.waypoints.forEach((coord, i) => {
    const latlng = [coord[1], coord[0]];
    const marker = L.marker(latlng).addTo(map);
    markers.push(marker);
  });
});
