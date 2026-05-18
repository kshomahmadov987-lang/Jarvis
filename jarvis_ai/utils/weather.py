"""
Weather API for Jarvis AI
Provides weather information via OpenWeatherMap
"""

import os
from typing import Optional, Dict


class WeatherAPI:
    """
    Fetches weather data from OpenWeatherMap API.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize weather API.
        
        Args:
            api_key: OpenWeatherMap API key (can also set via OPENWEATHER_API_KEY env var)
        """
        self.api_key = api_key or os.environ.get('OPENWEATHER_API_KEY')
        self._requests_available = False
        self._initialize()
        
    def _initialize(self):
        """Initialize requests library."""
        try:
            import requests
            self._requests_available = True
            print("[WEATHER] requests library initialized")
        except ImportError:
            print("[WARNING] requests not installed. Weather service disabled.")
            
    def get_weather(self, city: str = "London", units: str = "metric") -> Optional[Dict]:
        """
        Get current weather for a city.
        
        Args:
            city: City name
            units: 'metric' for Celsius, 'imperial' for Fahrenheit
            
        Returns:
            Weather data dictionary or None if failed
        """
        if not self._requests_available:
            print("[ERROR] Weather service not available")
            return None
            
        if not self.api_key:
            print("[ERROR] No API key provided. Set OPENWEATHER_API_KEY environment variable.")
            return None
            
        try:
            import requests
            
            base_url = "http://api.openweathermap.org/data/2.5/weather"
            
            params = {
                'q': city,
                'appid': self.api_key,
                'units': units,
                'lang': 'en'
            }
            
            response = requests.get(base_url, params=params, timeout=10)
            data = response.json()
            
            if data.get('cod') != 200:
                error_msg = data.get('message', 'Unknown error')
                print(f"[WEATHER] API error: {error_msg}")
                return None
                
            # Extract relevant data
            weather_data = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'icon': data['weather'][0]['icon']
            }
            
            return weather_data
            
        except Exception as e:
            print(f"[ERROR] Failed to fetch weather: {e}")
            return None
            
    def get_weather_report(self, city: str = "London") -> str:
        """
        Get a human-readable weather report.
        
        Args:
            city: City name
            
        Returns:
            Formatted weather report string
        """
        data = self.get_weather(city)
        
        if not data:
            return f"Unable to retrieve weather for {city}"
            
        unit = "°C" if data.get('temperature') < 100 else "°F"
        
        report = (
            f"In {data['city']}, {data['country']}: "
            f"{data['description'].capitalize()}, "
            f"Temperature: {data['temperature']:.0f}{unit}, "
            f"Feels like: {data['feels_like']:.0f}{unit}, "
            f"Humidity: {data['humidity']}%"
        )
        
        if data.get('wind_speed'):
            report += f", Wind: {data['wind_speed']} m/s"
            
        return report
        
    def get_forecast(self, city: str = "London") -> Optional[list]:
        """
        Get weather forecast (requires premium API key for full access).
        
        Args:
            city: City name
            
        Returns:
            List of forecast data or None if failed
        """
        if not self._requests_available or not self.api_key:
            return None
            
        try:
            import requests
            
            base_url = "http://api.openweathermap.org/data/2.5/forecast"
            
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'en'
            }
            
            response = requests.get(base_url, params=params, timeout=10)
            data = response.json()
            
            if data.get('cod') != '200':
                return None
                
            return data.get('list', [])
            
        except Exception as e:
            print(f"[ERROR] Failed to fetch forecast: {e}")
            return None
