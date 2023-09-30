WITH dim_weather_city_of_london_training_filtered AS (
    SELECT * FROM {{ ref('dim_weather_city_of_london_training_filtered') }}
),
dim_weather_cockfosters_historical_filtered AS (
    SELECT * FROM {{ ref('dim_weather_cockfosters_historical_filtered') }}
)

SELECT
    col.dt AS col_dt,
    coc.dt AS coc_dt,
    city_name, 
    lat, 
    lon, 
    temp, 
    pressure, 
    wind_speed, 
    wind_deg
    
FROM
  dim_weather_city_of_london_training_filtered as col  
JOIN 
  dim_weather_cockfosters_historical_filtered as coc
on 
  col.dt = coc.dt