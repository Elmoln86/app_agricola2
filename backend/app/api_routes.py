from fastapi import APIRouter, HTTPException, Query
from app.utils import fetch_coords, fetch_weather

router = APIRouter()

@router.get("/weather")
async def get_weather(city: str = Query(..., description="Nome da cidade, ex: Recife")):
    try:
        lat, lon = await fetch_coords(city)
        raw = await fetch_weather(lat, lon)

        # Normaliza saída
        weather = raw.get("weather", [{}])[0]
        main = raw.get("main", {})
        wind = raw.get("wind", {})
        out = {
            "city": raw.get("name") or city,
            "coords": {"lat": lat, "lon": lon},
            "description": weather.get("description"),
            "icon": weather.get("icon"),
            "temp": main.get("temp"),
            "feels_like": main.get("feels_like"),
            "humidity": main.get("humidity"),
            "pressure": main.get("pressure"),
            "wind": {"speed": wind.get("speed"), "deg": wind.get("deg")},
            "raw": raw  # opcional: útil para depurar
        }
        return out

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
