from google.cloud import bigquery
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

client = bigquery.Client()
project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
dataset_id = 'weather_api'
table_id = 'union_weather_api_training'


def get_data(scaler, features, context_hours):
    query = f"""
    SELECT 
        rounded_event_date as dt, city_name, temp_c,  pressure, humidity
    FROM `{project_id}.{dataset_id}.{table_id}`
    WHERE 
        (city_name = 'clerkenwell' or city_name = 'hadley_wood') AND 
        rounded_event_date >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 97 HOUR)
    order by rounded_event_date desc
    """
    query_job = client.query(query)
    df = query_job.to_dataframe()
    pivot_table = df.pivot(index='dt', columns='city_name', values=['temp_c', 'pressure', 'humidity']).reset_index()
    pivot_table.columns.name = None  # Remove the name from the columns
    pivot_table.columns = ['dt', 'temp_clerkenwell', 'temp_hadley_wood', 'pressure_clerkenwell', 'pressure_hadley_wood', 'humidity_clerkenwell', 'humidity_hadley_wood']
    pivot_table.fillna(method='ffill', inplace=True)
    df_scaled = pd.DataFrame(scaler.transform(pivot_table[features]))
    df_scaled.columns = pivot_table[features].columns

    total_length = pivot_table.shape[0]
    data = df_scaled[features].to_numpy()
    X = []
    y = []

    for i in range(total_length - context_hours):
        X.append(data[i:i + context_hours])
        y.append(data[i + context_hours:i + context_hours + 1]) 

    X = np.array(X)
    y = np.array(y)

    timestamps_array = pivot_table['dt'].to_numpy()
    print(X.shape, y.shape)
    return X, y

def generate_pred_dict(X, y, location_index, model, prediction_length, scaler):
  start = 0
  current_batch = X[start:start+1,:,:] #takes first sample, all windows and all features
  y_pred_scaled = [] 

  future_timestamps = [datetime.utcnow() + timedelta(hours=i) for i in range(prediction_length)]

  for i in range(prediction_length):
    current_pred = model.predict(current_batch).flatten()
    y_pred_scaled.append(current_pred)
    current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)

  y_pred_inv = scaler.inverse_transform(np.array(y_pred_scaled))
  # y_pred_inv_plot = y_pred_inv[:, features.index('temp_clerkenwell')]
  # y_true_inv_plot = scaler.inverse_transform(y[:, features.index('temp_clerkenwell')])
  y_pred_inv_plot = y_pred_inv[:, location_index]
  y_true_inv_plot = scaler.inverse_transform(y[:, location_index])

  y_true_inv_plot = y_true_inv_plot[:, 0]
  df_final = pd.DataFrame(data={
    'future_timestamps': future_timestamps,
    'pred_temp': y_pred_inv_plot.round(0)
  })
  return df_final.to_dict()

