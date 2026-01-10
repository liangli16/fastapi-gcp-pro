from fastapi import FastAPI, HTTPException
import os
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FastAPI GCP Pro", description="A simple FastAPI backend deployed on GCP")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001", 
        "https://launch-an-app-sigma.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI GCP Pro"}

@app.get("/greet/{name}")
async def greet(name: str):
    """A simple greeting endpoint"""
    return {"message": f"Hello, {name}!"}

@app.get("/weather")
async def fetch_weather_today(city: str = "London"):
    """Fetch today's weather for a given city (using mock data)"""
    # Mock weather data
    weather_info = {
        "city": city,
        "temperature": 22.5,
        "description": "Partly cloudy",
        "humidity": 65,
        "wind_speed": 5.2
    }
    
    return weather_info