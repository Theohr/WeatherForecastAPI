import sqlite3

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