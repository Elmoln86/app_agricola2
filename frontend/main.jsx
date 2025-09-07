const API_BASE =   import.meta.env.MODE === "production"
    ? "https://api.seudominio.com"  // produção via Caddy (HTTPS)
    : (import.meta.env.VITE_API_BASE || "http://localhost:8000"); // dev



const out = document.getElementById("raw"); // usa o <div id="raw"> que já existe
const card = document.getElementById("card");
const apiBaseEl = document.getElementById("apiBase");
if (apiBaseEl) apiBaseEl.textContent = API_BASE;

function show(obj) {
  out.textContent = typeof obj === "string" ? obj : JSON.stringify(obj, null, 2);
}

async function getJson(url) {
  try {
    const res = await fetch(url);
    const txt = await res.text();
    try { return JSON.parse(txt); } catch { return txt; }
  } catch (e) {
    return { error: String(e), url };
  }
}

document.getElementById("btnHealth").addEventListener("click", async () => {
  const data = await getJson(`${API_BASE}/health`);
  card.innerHTML = `<div class="title">/health</div>`;
  show(data);
});

document.getElementById("btnWeather").addEventListener("click", async () => {
  const city = document.getElementById("city").value || "Recife";
  const url = `${API_BASE}/weather?city=${encodeURIComponent(city)}`;
  const data = await getJson(url);

  if (data && !data.error && !data.detail) {
    const iconUrl = data.icon ? `https://openweathermap.org/img/wn/${data.icon}@2x.png` : "";
    card.innerHTML = `
      <div class="title">${data.city}</div>
      <div class="muted">Lat: ${data.coords?.lat?.toFixed?.(4)} • Lon: ${data.coords?.lon?.toFixed?.(4)}</div>
      <div style="display:flex; align-items:center; gap:12px; margin-top:10px">
        ${iconUrl ? `<img src="${iconUrl}" alt="icon" width="64" height="64" />` : ""}
        <div>
          <div style="font-size:28px; font-weight:700">${Math.round(data.temp)}°C</div>
          <div class="muted">${data.description || "—"}</div>
          <div class="muted">Sensação: ${Math.round(data.feels_like)}°C • Umidade: ${data.humidity}%</div>
          <div class="muted">Vento: ${data.wind?.speed ?? "?"} m/s</div>
        </div>
      </div>
    `;
  } else {
    card.innerHTML = `<div class="title">Erro</div><div class="muted">${data?.detail || data?.error || "Falha ao obter dados"}</div>`;
  }
  show(data);
});


