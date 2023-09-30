WITH weather_city_of_london_training AS (
    SELECT
        *
    FROM
       {{ source('weather_training', 'weather_city_of_london_training') }}
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
    weather_city_of_london_training