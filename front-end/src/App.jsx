import React, { useState } from 'react';
import './App.css';

const App = () => {
  const [city, setCity] = useState('');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    setData(null);

    try {
      const apiUrl = process.env.REACT_APP_API_URL; // Use the environment variable

      const response = await fetch(`${apiUrl}/api`, {  // Dynamically use the backend URL
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ city }),
      });

      if (!response.ok) {
        throw new Error('City not found');
      }

      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getWeatherIcon = (iconCode) => `https://openweathermap.org/img/wn/${iconCode}@2x.png`;

  return (
    <div className="app-container">
      <h1 className="title">🌤️ WeatherPro</h1>
      <div className="search-container">
        <input
          type="text"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          placeholder="Enter a city..."
          className="input"
        />
        <button onClick={fetchData} disabled={loading} className="button">
          {loading ? 'Fetching...' : 'Search'}
        </button>
      </div>

      {error && <p className="error">{error}</p>}

      {data && data.main && (
        <div className="weather-card">
          <h2>{data.name}, {data.sys.country}</h2>
          <img src={getWeatherIcon(data.weather[0].icon)} alt="icon" />
          <p className="temp">{Math.round(data.main.temp)}°C</p>
          <p className="description">{data.weather[0].description}</p>
          <div className="details">
            <p>Feels Like: {Math.round(data.main.feels_like)}°C</p>
            <p>Humidity: {data.main.humidity}%</p>
            <p>Wind: {data.wind.speed} km/h</p>
            <p>Pressure: {data.main.pressure} hPa</p>
            <p>Visibility: {data.visibility / 1000} km</p>
            <p>Cloudiness: {data.clouds.all}%</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
