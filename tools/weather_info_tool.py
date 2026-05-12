import os
from typing import List
from dotenv import load_dotenv
from langchain.tools import tool
from utils.weather_info import WeatherForecastTool


class WeatherInfoTool:
    """
    Weather information tool for getting current weather and forecasts.
    Provides tools for travel planning to check weather conditions at destinations.
    """
    
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
        
        if not self.api_key:
            raise ValueError("OPENWEATHERMAP_API_KEY not found in environment variables")
        
        self.weather_service = WeatherForecastTool(self.api_key)
        self.weather_tool_list = self._setup_tools()
    
    def _setup_tools(self) -> List:
        """Setup all tools for the weather forecast tool."""
        
        @tool
        def get_current_weather(city: str) -> str:
            """
            Get current weather for a city.
            
            Args:
                city: Name of the city (e.g., "Hanoi", "London", "New York")
            
            Returns:
                Current weather information including temperature in Celsius and conditions
            """
            weather_data = self.weather_service.get_current_weather(city)
            
            if weather_data:
                temp = weather_data.get('main', {}).get('temp', 'N/A')
                desc = weather_data.get('weather', [{}])[0].get('description', 'N/A')
                return f"Current weather in {city}: {temp}°C, {desc}"
            
            return f"Could not fetch weather for {city}"
        
        @tool
        def get_weather_forecast(city: str) -> str:
            """
            Get weather forecast for a city.
            
            Args:
                city: Name of the city (e.g., "Hanoi", "London", "New York")
            
            Returns:
                Weather forecast with temperatures and conditions for the next few days
            """
            forecast_data = self.weather_service.get_forecast_weather(city)
            
            if not forecast_data or 'list' not in forecast_data:
                return f"Could not fetch forecast for {city}"
            
            forecast_summary = []
            for item in forecast_data['list']:
                date = item['dt_txt'].split(' ')[0]
                temp = item['main']['temp']
                desc = item['weather'][0]['description']
                forecast_summary.append(f"{date}: {temp}°C, {desc}")
            
            return f"Weather forecast for {city}:\n" + "\n".join(forecast_summary)
        
        return [get_current_weather, get_weather_forecast]