from flask import Flask, request, jsonify
import tensorflow as tf
import joblib
from keras.models import load_model
from tensorflow import keras
from helper_functions import get_data, generate_pred_dict


features = ['temp_clerkenwell', 'pressure_clerkenwell', 'humidity_clerkenwell']
scaler = joblib.load('WeatherProphetPro\scaler_model.pkl')
context_hours = 24*3
# prediction_length = 24
model = load_model("WeatherProphetPro\your_model.h5")  

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)

    location_index = data['location_index']
    prediction_length = data['prediction_length']
    X, y = get_data(scaler, features, context_hours)
    pred_dict = generate_pred_dict(X, y, location_index, model, prediction_length, scaler)

    return jsonify({'prediction': pred_dict})


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
