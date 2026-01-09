from fastapi import FastAPI, HTTPException
import httpx
import os
from typing import Optional

app = FastAPI(title="FastAPI GCP Pro", description="A simple FastAPI backend deployed on GCP")

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI GCP Pro"}

@app.get("/greet")
async def greet(name: Optional[str] = "World"):
    """A simple greeting endpoint"""
    return {"message": f"Hello, {name}!"}

@app.get("/weather/today")
async def fetch_weather_today(city: str = "London"):
    """Fetch today's weather for a given city"""
    try:
        # Using OpenWeatherMap API (you'll need to sign up for a free API key)
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="Weather API key not configured")
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
        
        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
        
        return weather_info
        
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Weather API error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weather: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)