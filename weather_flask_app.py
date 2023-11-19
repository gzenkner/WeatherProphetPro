from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import joblib



app = Flask(__name__)
# model = tf.keras.models.load_model(r'C:\Users\gabri\VSCode Projects\Weather Prediction\WeatherProphetPro\test_model.keras')
model = tf.keras.models.load_model(r'C:\Users\gabri\VSCode Projects\Weather Prediction\WeatherProphetPro\test_model.h5')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        input_data = np.array(data['data'])
        prediction = model.predict(input_data)
        return jsonify({'prediction': prediction.tolist()})
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
