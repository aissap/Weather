from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get the API key from environment variables
apiKey = os.getenv('API_KEY')

@app.route('/api', methods=['POST'])
def current_weather():
    city = request.get_json()
    if city and "city" in city:
        res = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={city["city"]}&appid={apiKey}&units=metric'
        ).json()
        if res.get("cod") != "404":
            return jsonify(res)
        return jsonify({'error': 'City not found'}), 404
    return jsonify({'error': 'Missing city name'}), 400

@app.route('/forecast', methods=['POST'])
def forecast():
    city = request.get_json()
    if city and "city" in city:
        res = requests.get(
            f'http://api.openweathermap.org/data/2.5/forecast?q={city["city"]}&appid={apiKey}&units=metric'
        ).json()
        if res.get("cod") != "404":
            return jsonify(res)
        return jsonify({'error': 'City not found'}), 404
    return jsonify({'error': 'Missing city name'}), 400

@app.route('/air-quality', methods=['POST'])
def air_quality():
    data = request.get_json()
    if data and "lat" in data and "lon" in data:
        res = requests.get(
            f"http://api.openweathermap.org/data/2.5/air_pollution?lat={data['lat']}&lon={data['lon']}&appid={apiKey}"
        ).json()
        return jsonify(res)
    return jsonify({'error': 'Missing lat/lon'}), 400

if __name__ == '__main__':
    app.run(debug=True)
