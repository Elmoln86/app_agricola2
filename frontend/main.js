const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

const out = document.getElementById("raw");
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
  card.innerHTML = `<div class="title">/weather</div><div class="muted">${url}</div>`;
  show(data);
});

let rawOpen = true;
document.getElementById("btnToggleRaw").addEventListener("click", () => {
  rawOpen = !rawOpen;
  document.getElementById("raw").classList.toggle("hidden", !rawOpen);
});
