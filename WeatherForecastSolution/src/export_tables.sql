-- Export locations table to CSV
.mode csv
.output locations.csv
SELECT * FROM locations;
.output stdout

-- Export forecasts table to CSV
.mode csv
.output forecasts.csv
SELECT * FROM forecasts;
.output stdout