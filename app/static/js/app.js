// FORMULÁRIO - Página de criação de rota
const form = document.getElementById("route-form");
if (form) {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    document.getElementById("loading-message").style.display = "block";

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

    sessionStorage.setItem("rota", JSON.stringify(data));
    window.location.href = "/";
  });

  // Botão de adicionar campo
  document.querySelector("button[onclick='addField()']").onclick = () => {
    const div = document.createElement("div");
    div.innerHTML = `<input type="text" name="address" placeholder="Outro endereço" required />`;
    document.getElementById("addresses").appendChild(div);
  };
}

// MAPA - Página inicial
const mapContainer = document.getElementById("map");
if (mapContainer) {
  const rotaSalva = sessionStorage.getItem("rota");
  const map = L.map("map", { zoomControl: false }).setView(
    [-5.79448, -35.211],
    13
  );

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
  }).addTo(map);

  L.control
    .zoom({
      position: "topright",
    })
    .addTo(map);

  if (rotaSalva) {
    const data = JSON.parse(rotaSalva);

    const coords = data.features[0].geometry.coordinates.map((c) => [
      c[1],
      c[0],
    ]);
    const polyline = L.polyline(coords, { color: "blue" }).addTo(map);
    map.fitBounds(polyline.getBounds());

    data.waypoints.forEach((coord) => {
      const latlng = [coord[1], coord[0]];
      L.marker(latlng).addTo(map);
    });

    sessionStorage.removeItem("rota");
  }
}
