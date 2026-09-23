import httpx
from typing import Any

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


async def geocode_city(city: str) -> dict[str, Any]:
    """Convert a city name into latitude/longitude using Open-Meteo's geocoding API."""
    params = {
        "name": city,
        "count": 5,
        "language": "en",
        "format": "json",
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(GEOCODING_URL, params=params)
        response.raise_for_status()
        data = response.json()

    results = data.get("results", [])
    if not results:
        return {"results": []}

    cleaned = [
        {
            "name": r.get("name"),
            "country": r.get("country"),
            "admin1": r.get("admin1"),
            "latitude": r.get("latitude"),
            "longitude": r.get("longitude"),
            "timezone": r.get("timezone"),
        }
        for r in results
    ]

    return {"results": cleaned}


async def get_current_weather(lat: float, lon: float) -> dict[str, Any]:
    """Fetch current weather for given coordinates from Open-Meteo."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
        "hourly": "temperature_2m,relative_humidity_2m",
        "timezone": "auto",
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(FORECAST_URL, params=params)
        response.raise_for_status()
        data = response.json()

    return data