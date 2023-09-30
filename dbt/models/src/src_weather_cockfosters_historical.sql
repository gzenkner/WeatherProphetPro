WITH weather_cockfosters_historical AS (
    SELECT
        *
    FROM
       {{ source('weather_training', 'weather_cockfosters_historical') }}
)
SELECT
    dt, 
    city_name, 
    lat, 
    lon, 
    temp, 
    pressure, 
    wind_speed, 
    wind_deg
FROM
    weather_cockfosters_historical