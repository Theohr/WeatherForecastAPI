from fastapi import FastAPI, HTTPException
import sqlite3
from pydantic import BaseModel
from typing import List

app_API = FastAPI()

class Location(BaseModel):
    name: str
    latitude: float
    longitude: float

class Forecast(BaseModel):
    location_name: str
    forecast_date: str
    temperature: float
    precipitation: float
    wind_speed: float

class AvgForecast(BaseModel):
    location_name: str
    forecast_date: str
    avg_temperature: float

@app_API.get("/locations", response_model=List[Location])
async def list_locations():
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, latitude, longitude FROM locations")
    locations = [Location(name=row[0], latitude=row[1], longitude=row[2]) for row in cursor.fetchall()]
    conn.close()
    return locations

@app_API.get("/forecasts/latest", response_model=List[Forecast])
async def list_latest_forecasts():
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT f.location_name, f.forecast_date, f.temperature, f.precipitation, f.wind_speed
        FROM forecasts f
        INNER JOIN (
            SELECT location_name, MAX(forecast_date) as max_date
            FROM forecasts
            GROUP BY location_name, date(forecast_date)
        ) latest
        ON f.location_name = latest.location_name AND f.forecast_date = latest.max_date
    """)
    forecasts = [Forecast(location_name=row[0], forecast_date=row[1], temperature=row[2], 
                         precipitation=row[3], wind_speed=row[4]) for row in cursor.fetchall()]
    conn.close()
    return forecasts

@app_API.get("/forecasts/avg_temperature", response_model=List[AvgForecast])
async def list_avg_temperature():
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT location_name, date(forecast_date) as forecast_date, 
               AVG(temperature) as avg_temperature
        FROM (
            SELECT location_name, forecast_date, temperature,
                   ROW_NUMBER() OVER (PARTITION BY location_name, date(forecast_date) 
                                    ORDER BY forecast_date DESC) as rn
            FROM forecasts
        ) t
        WHERE rn <= 3
        GROUP BY location_name, date(forecast_date)
    """)
    avg_forecasts = [AvgForecast(location_name=row[0], forecast_date=row[1], avg_temperature=row[2]) 
                     for row in cursor.fetchall()]
    conn.close()
    return avg_forecasts

@app_API.get("/top_locations/{metric}/{n}", response_model=List[Forecast])
async def top_locations(metric: str, n: int):
    valid_metrics = ['temperature', 'precipitation', 'wind_speed']
    if metric not in valid_metrics:
        raise HTTPException(status_code=400, detail="Invalid metric")
    
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    query = f"""
        SELECT location_name, forecast_date, temperature, precipitation, wind_speed
        FROM forecasts
        ORDER BY {metric} DESC
        LIMIT ?
    """
    cursor.execute(query, (n,))
    top_forecasts = [Forecast(location_name=row[0], forecast_date=row[1], temperature=row[2], 
                             precipitation=row[3], wind_speed=row[4]) for row in cursor.fetchall()]
    conn.close()
    return top_forecasts