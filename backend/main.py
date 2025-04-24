from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

apiKey = '1a404bebef2c226c6daa2907d7bd6917'

# Function to convert Unix timestamp to human-readable time
def convert_unix_to_time(unix_timestamp):
    return datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/api', methods=['POST'])
def current_weather():
    city = request.get_json()
    if city and "city" in city:
        res = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={city["city"]}&appid={apiKey}&units=metric'
        ).json()
        
        if res.get("cod") != "404":
            weather_data = {
                "city": res["name"],
                "country": res["sys"]["country"],
                "temperature": res["main"]["temp"],
                "feels_like": res["main"]["feels_like"],
                "humidity": res["main"]["humidity"],
                "pressure": res["main"]["pressure"],
                "visibility": res["visibility"],
                "wind_speed": res["wind"]["speed"],
                "wind_deg": res["wind"]["deg"],
                "cloudiness": res["clouds"]["all"],
                "description": res["weather"][0]["description"],
                "icon": res["weather"][0]["icon"],
                "sunrise": convert_unix_to_time(res["sys"]["sunrise"]),
                "sunset": convert_unix_to_time(res["sys"]["sunset"]),
            }

            # Get UV index
            lat = res["coord"]["lat"]
            lon = res["coord"]["lon"]
            uv_res = requests.get(
                f'http://api.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&appid={apiKey}'
            ).json()
            weather_data["uv_index"] = uv_res.get("value", "N/A")

            return jsonify(weather_data)
        
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
            forecast_data = []
            for item in res["list"]:
                forecast_data.append({
                    "time": convert_unix_to_time(item["dt"]),
                    "temperature": item["main"]["temp"],
                    "description": item["weather"][0]["description"],
                    "icon": item["weather"][0]["icon"],
                    "wind_speed": item["wind"]["speed"],
                    "humidity": item["main"]["humidity"],
                    "pressure": item["main"]["pressure"],
                })
            return jsonify({"city": res["city"]["name"], "forecast": forecast_data})
        
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
