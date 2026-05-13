import sys
import requests
from typing import Dict, Any, Optional
from exception.exceptionhandling import CustomException
from logger.logging import logging

logger = logging.getLogger(__name__)

class WeatherForecastTool:
    """
    Weather forecast tool using OpenWeatherMap API.
    Free tier: 60 calls per minute, 1,000,000 calls per month.
    Get API key at: https://openweathermap.org/api
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_current_weather(self, place: str) -> Optional[Dict[str, Any]]:
        """
        Get current weather of a place.
        
        Args:
            place: City name (e.g., "Hanoi", "London")
        
        Returns:
            Weather data dict, or None if error
        """
        try:
            logger.info("Get current weather")
            url = f"{self.base_url}/weather"
            params = {
                "q": place,
                "appid": self.api_key,
                "units": "metric"  
            }
            response = requests.get(url, params=params, timeout=30) # timeout = 30s
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Weather API error: {response.status_code}")
                return None
            
        except Exception as e:
            custom_error = CustomException(e, sys)
            logger.error(custom_error)
            raise custom_error
    
    def get_forecast_weather(self, place: str) -> Optional[Dict[str, Any]]:
        """
        Get 5-day weather forecast of a place (3-hour intervals).
        
        Args:
            place: City name (e.g., "Hanoi", "London")
        
        Returns:
            Forecast data dict, or None if error
        """
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": place,
                "appid": self.api_key,
                # "cnt": 10,  # Retrieve only 10 news items (~30 hours). The default is 40 (5 full days).
                "units": "metric"
            }
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Forecast API error: {response.status_code}")
                return None

        except Exception as e:
            custom_error = CustomException(e, sys)
            logger.error(custom_error)
            raise custom_error