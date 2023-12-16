import requests


location_index = int(input('Enter 0 for temp_clerkenwell and 1 temp_hadley_wood: '))
prediction_length = int(input('Input prediction length in hours (e.g., 24 or 72): '))

url = 'http://localhost:5000/predict'
data = {'location_index': location_index, 'prediction_length': prediction_length}
response = requests.post(url, json=data)
if response.status_code == 200:
    try:
        # Try to parse JSON response
        result = response.json()
        print(result)
    except requests.exceptions.JSONDecodeError:
        print("Error decoding JSON. Response may be empty or not in JSON format.")
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)  