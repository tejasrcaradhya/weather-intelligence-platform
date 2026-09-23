from fastapi import FastAPI

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