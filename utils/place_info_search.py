from langchain_tavily import TavilySearch
from langchain_google_community import GooglePlacesTool, GooglePlacesAPIWrapper

class GooglePlaceSearchTool:
    """
    A tool wrapper for Google Places API to search for locations, attractions, 
    restaurants, and other points of interest.
    
    This tool provides a clean interface to query Google Places data for
    travel planning purposes.
    """
    
    def __init__(self, api_key: str):
        """
        Initialise the Google Places search tool.
        
        Args:
            api_key (str): Google Places API key (get from Google Cloud Console)
        """
        self.places_wrapper = GooglePlacesAPIWrapper(gplaces_api_key=api_key)
        self.places_tool = GooglePlacesTool(api_wrapper=self.places_wrapper)
    
    def _search(self, query: str) -> str:
        """
        Internal method to execute search queries.
        
        Args:
            query (str): The search query string
            
        Returns:
            str: Search results or error message
        """
        try:
            result = self.places_tool.run(query)
            return result if result else "No results found."
        except Exception as e:
            return f"Search error: {str(e)}"
    
    def search_attractions(self, place: str) -> str:
        """
        Find popular attractions in a specific location.
        
        Args:
            place (str): City or location name (e.g., "Bali", "Paris")
            
        Returns:
            str: List of attractions with descriptions
        """
        return self._search(f"top attractive places in and around {place}")
    
    def search_restaurants(self, place: str) -> str:
        """
        Find top-rated restaurants and eateries in a location.
        
        Args:
            place (str): City or location name
            
        Returns:
            str: List of restaurants with ratings and reviews
        """
        return self._search(f"what are the top 10 restaurants and eateries in and around {place}?")
    
    def search_activities(self, place: str) -> str:
        """
        Find popular activities and things to do in a location.
        
        Args:
            place (str): City or location name
            
        Returns:
            str: List of activities and experiences
        """
        return self._search(f"Activities in and around {place}")
    
    def search_transportation(self, place: str) -> str:
        """
        Find available transportation options in a location.
        
        Args:
            place (str): City or location name
            
        Returns:
            str: Available transportation modes (taxi, bus, train, etc.)
        """
        return self._search(f"What are the different modes of transportations available in {place}")


class TavilyPlaceSearchTool:
    """
    A search tool wrapper for Tavily API that provides web search capabilities
    for travel-related queries. Useful as a fallback or supplement to Google Places.
    """
    
    def __init__(self):
        """Initialise the Tavily search tool with default configuration."""
        self.tavily_tool = TavilySearch(
            topic="general", 
            include_answer="advanced"
        )
    
    def _search(self, query: str) -> str:
        """
        Internal method to execute Tavily search queries.
        
        Args:
            query (str): The search query string
            
        Returns:
            str: Search results extracted from API response
        """
        try:
            result = self.tavily_tool.invoke({"query": query})
            
            # Extract the answer field if available
            if isinstance(result, dict) and result.get("answer"):
                return result["answer"]
            
            return str(result) if result else "No results found."
            
        except Exception as e:
            return f"Search error: {str(e)}"
    
    def search_attractions(self, place: str) -> str:
        """
        Search for tourist attractions using web search.
        
        Args:
            place (str): City or location name
            
        Returns:
            str: Web search results for attractions
        """
        return self._search(f"top attractive places in and around {place}")
    
    def search_restaurants(self, place: str) -> str:
        """
        Search for restaurants and dining options using web search.
        
        Args:
            place (str): City or location name
            
        Returns:
            str: Web search results for restaurants
        """
        return self._search(f"what are the top 10 restaurants and eateries in and around {place}.")
    
    def search_activities(self, place: str) -> str:
        """
        Search for activities and entertainment using web search.
        
        Args:
            place (str): City or location name
            
        Returns:
            str: Web search results for activities
        """
        return self._search(f"activities in and around {place}")
    
    def search_transportation(self, place: str) -> str:
        """
        Search for transportation options using web search.
        
        Args:
            place (str): City or location name
            
        Returns:
            str: Web search results for transportation
        """
        return self._search(f"What are the different modes of transportations available in {place}")