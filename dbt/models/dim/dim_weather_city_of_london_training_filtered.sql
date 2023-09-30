WITH src_weather_city_of_london_training AS (
    SELECT
        *
    FROM
       {{ ref('src_weather_city_of_london_training') }}
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
    src_weather_city_of_london_training
WHERE
    dt IS NOT NULL AND
    city_name IS NOT NULL AND
    lat IS NOT NULL AND
    lon IS NOT NULL AND
    temp IS NOT NULL AND
    pressure IS NOT NULL AND
    wind_speed IS NOT NULL AND
    wind_deg IS NOT NULL 