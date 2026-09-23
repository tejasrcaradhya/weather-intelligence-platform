from fastapi import FastAPI, HTTPException, Query

from services.weather import geocode_city, get_current_weather

app = FastAPI(
    title="Weather Intelligence Platform API",
    description="Backend API for the Weather Intelligence Platform",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {
        "message": "Weather Intelligence Platform API is running",
        "status": "ok",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/api/geocode")
async def geocode(q: str = Query(..., min_length=1, description="City name to search")):
    try:
        result = await geocode_city(q)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Geocoding service error: {e}")

    if not result["results"]:
        raise HTTPException(status_code=404, detail=f"No results found for '{q}'")

    return result


@app.get("/api/weather")
async def weather(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
):
    try:
        data = await get_current_weather(lat, lon)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Weather service error: {e}")

    return data