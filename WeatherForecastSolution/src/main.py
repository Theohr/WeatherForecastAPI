import sqlite3
from datetime import datetime, timedelta
from meteomatics_client import MeteomaticsClient


def fetch_and_store_forecasts():
    # Initialize Meteomatics client (replace with your credentials)
    client = MeteomaticsClient(username='theoltd_herodotou_theodoros', password='iL2lhB65Xj')
    
    # Create database and tables
    conn = create_database()
    
    # Define 3 locations (latitude, longitude, name)
    locations = [
        (51.5074, -0.1278, 'London'),
        (40.7128, -74.0060, 'New York'),
        (-33.8688, 151.2093, 'Sydney')
    ]
    
    # Insert locations into database
    for lat, lon, name in locations:
        insert_location(conn, name, lat, lon)
    
    # Fetch 7-day forecast for each location
    start_date = datetime.now()
    end_date = start_date + timedelta(days=7)
    
    for lat, lon, name in locations:
        forecasts = client.get_forecast(
            lat=lat,
            lon=lon,
            start_date=start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            end_date=end_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            interval='PT24H',
            parameters=['t_2m:C', 'precip_24h:mm', 'wind_speed_10m:kmh']
        )
        
        for forecast in forecasts:
            insert_forecast(
                conn,
                name,
                forecast['valid_date'],
                forecast['t_2m:C'],
                forecast['precip_24h:mm'],
                forecast['wind_speed_10m:kmh']
            )
    
    conn.commit()
    conn.close()

def create_database():
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    
    # Create locations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            name TEXT PRIMARY KEY,
            latitude REAL,
            longitude REAL
        )
    ''')
    
    # Create forecasts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_name TEXT,
            forecast_date TEXT,
            temperature REAL,
            precipitation REAL,
            wind_speed REAL,
            FOREIGN KEY (location_name) REFERENCES locations (name)
        )
    ''')
    
    conn.commit()
    return conn

def insert_location(conn, name, latitude, longitude):
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO locations (name, latitude, longitude) VALUES (?, ?, ?)',
                   (name, latitude, longitude))

def insert_forecast(conn, location_name, forecast_date, temperature, precipitation, wind_speed):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO forecasts (location_name, forecast_date, temperature, precipitation, wind_speed)
        VALUES (?, ?, ?, ?, ?)
    ''', (location_name, forecast_date, temperature, precipitation, wind_speed))
if __name__ == '__main__':
    fetch_and_store_forecasts()