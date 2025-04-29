CREATE TABLE locations (
    name TEXT PRIMARY KEY,
    latitude REAL,
    longitude REAL
);

CREATE TABLE forecasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_name TEXT,
    forecast_date TEXT,
    temperature REAL,
    precipitation REAL,
    wind_speed REAL,
    FOREIGN KEY (location_name) REFERENCES locations (name)
);