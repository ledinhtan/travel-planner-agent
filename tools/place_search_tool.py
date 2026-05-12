import os
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv
from utils.place_info_search import GooglePlaceSearchTool, TavilyPlaceSearchTool

class PlaceSearchTool:
    def __init__(self):
        load_dotenv()
        self.google_place_api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
        self.google_places_search = GooglePlaceSearchTool(self.google_place_api_key)
        self.tavily_search = TavilyPlaceSearchTool()
        self.place_search_tool_list = self._setup_tools()

    def _search_with_fallback(self, place: str, search_type: str) -> str:
        """
        Generic search with fallback from Google to Tavily.
        
        Args:
            place: Location to search
            search_type: Type of search ("attractions", "restaurants", "activities", "transportation")
        
        Returns:
            Search result string
        """
        # Map search type to method names
        google_methods = {
            "attractions": self.google_places_search.google_search_attractions,
            "restaurants": self.google_places_search.google_search_restaurants,
            "activities": self.google_places_search.google_search_activity,
            "transportation": self.google_places_search.google_search_transportation,
        }
        
        tavily_methods = {
            "attractions": self.tavily_search.tavily_search_attractions,
            "restaurants": self.tavily_search.tavily_search_restaurants,
            "activities": self.tavily_search.tavily_search_activity,
            "transportation": self.tavily_search.tavily_search_transportation,
        }
        
        # Display names for user feedback
        display_names = {
            "attractions": "attractions",
            "restaurants": "restaurants",
            "activities": "activities",
            "transportation": "transportation modes",
        }
        
        try:
            # Try Google first
            result = google_methods[search_type](place)
            if result:
                return f"Following are the {display_names[search_type]} of {place} as suggested by Google: {result}"
        except Exception as e:
            # Fallback to Tavily
            tavily_result = tavily_methods[search_type](place)
            return f"Google cannot find the details due to {e}. \nFollowing are the {display_names[search_type]} of {place}: {tavily_result}"
        
        # If Google returned empty result
        tavily_result = tavily_methods[search_type](place)
        return f"Google returned no results. \nFollowing are the {display_names[search_type]} of {place}: {tavily_result}"

    def _setup_tools(self) -> List:
        """Setup all tools for the place search tool"""
        
        @tool
        def search_attractions(place: str) -> str:
            """Search attractions of a place"""
            return self._search_with_fallback(place, "attractions")
        
        @tool
        def search_restaurants(place: str) -> str:
            """Search restaurants of a place"""
            return self._search_with_fallback(place, "restaurants")
        
        @tool
        def search_activities(place: str) -> str:
            """Search activities of a place"""
            return self._search_with_fallback(place, "activities")
        
        @tool
        def search_transportation(place: str) -> str:
            """Search transportation options of a place"""
            return self._search_with_fallback(place, "transportation")
        
        return [search_attractions, search_restaurants, search_activities, search_transportation]