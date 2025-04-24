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
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000';
      const response = await fetch(`${apiUrl}/api`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ city }),
      });

      const result = await response.json();
      console.log('Result:', result);

      if (!response.ok || result.error) {
        throw new Error(result.error || 'City not found');
      }

      setData(result);
    } catch (err) {
      console.error('Fetch error:', err.message);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getWeatherIcon = (iconCode) =>
    `https://openweathermap.org/img/wn/${iconCode}@2x.png`;

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

      {data && (
        <div className="weather-card">
          <h2>{data.city}, {data.country}</h2>

          {data.icon && (
            <img src={getWeatherIcon(data.icon)} alt={data.description} />
          )}

          <p className="temp">{Math.round(data.temperature)}°C</p>
          <p className="description">{data.description}</p>

          <div className="details">
            <p>Feels Like: {Math.round(data.feels_like)}°C</p>
            <p>Humidity: {data.humidity}%</p>
            <p>Wind Speed: {data.wind_speed} km/h</p>
            <p>Pressure: {data.pressure} hPa</p>
            <p>Visibility: {data.visibility / 1000} km</p>
            <p>Cloudiness: {data.cloudiness}%</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
