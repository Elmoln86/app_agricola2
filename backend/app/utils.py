import os
import httpx

OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")

async def fetch_coords(city: str):
    if not OPENWEATHER_KEY:
        raise RuntimeError("OPENWEATHER_KEY não está definido nas variáveis de ambiente.")
    url = "https://api.openweathermap.org/geo/1.0/direct"
    params = {"q": city, "limit": 1, "appid": OPENWEATHER_KEY}
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        data = r.json()
    if not data:
        raise ValueError(f"Cidade não encontrada: {city}")
    lat = data[0].get("lat")
    lon = data[0].get("lon")
    if lat is None or lon is None:
        raise ValueError(f"Sem coordenadas para: {city}")
    return float(lat), float(lon)

async def fetch_weather(lat: float, lon: float):
    if not OPENWEATHER_KEY:
        raise RuntimeError("OPENWEATHER_KEY não está definido nas variáveis de ambiente.")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"lat": lat, "lon": lon, "appid": OPENWEATHER_KEY, "units": "metric", "lang": "pt_br"}
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        return r.json()