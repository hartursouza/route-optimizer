// FORMULÁRIO - Página de criação de rota
const form = document.getElementById("route-form");
if (form) {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const errorDiv = document.getElementById("error-message");
    errorDiv.style.display = "none";
    errorDiv.textContent = "";

    document.getElementById("loading-message").style.display = "block";

    const inputs = document.querySelectorAll("input[name='address']");
    const enderecos = Array.from(inputs).map((i) => i.value);
    const profile = document.getElementById("profile").value;

    const res = await fetch("/route/optimized", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ enderecos, profile }),
    });

    const data = await res.json();

    if (data.erro) {
      errorDiv.textContent = data.erro;
      errorDiv.style.display = "block";
      document.getElementById("loading-message").style.display = "none";
      return;
    }

    // Adiciona os campos que vão ser usados para salvar depois
    data.modo = profile;
    data.distancia_km = data.features[0].properties.summary.distance / 1000;
    data.duracao_min = data.features[0].properties.summary.duration / 60;
    data.enderecos = enderecos;

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
      position: "bottomright",
    })
    .addTo(map);

  if (rotaSalva) {
    const data = JSON.parse(rotaSalva);

    document.getElementById("info-box").style.display = "block";
    document.getElementById(
      "info-distancia"
    ).textContent = `Distância: ${data.distancia_km.toFixed(2)} km`;
    document.getElementById(
      "info-duracao"
    ).textContent = `Duração: ${data.duracao_min.toFixed(1)} min`;

    const btnSalvar = document.getElementById("btn-salvar");
    btnSalvar.style.display = "inline-block";

    btnSalvar.onclick = async () => {
      const modo = data.profile || data.modo || "driving-car"; // ou pegue do local correto
      const distancia_total =
        data.features[0].properties.summary.distance / 1000; // km
      const duracao_total = data.features[0].properties.summary.duration / 60; // minutos
      const enderecos = data.enderecos || []; // se você salvou esses endereços junto no objeto

      const res = await fetch("/route/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          modo,
          distancia_total,
          duracao_total,
          enderecos,
        }),
      });

      const resultado = await res.json();

      const mensagem = document.getElementById("success-message");

      if (resultado.sucesso) {
        mensagem.textContent = "Rota salva com sucesso!";
        mensagem.style.display = "block";
        mensagem.className = "text-success mt-2";
      } else {
        mensagem.textContent = "Erro ao salvar rota: " + resultado.erro;
        mensagem.style.display = "block";
        mensagem.className = "text-danger mt-2";
      }
    };

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
