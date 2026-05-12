import requests
from typing import Optional

class CurrencyConverter:
    """
    Currency converter using ExchangeRate-API (exchangerate-api.com).
    
    Free tier: 1500 requests per month.
    Get your API key at: https://www.exchangerate-api.com/
    """
    
    def __init__(self, api_key: str):
        """
        Initialise the currency converter.
        
        Args:
            api_key: API key from ExchangeRate-API
        """
        self.api_key = api_key
        self.base_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest"
    
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Convert an amount from one currency to another.
        
        Args:
            amount: Amount of money to convert
            from_currency: Source currency code (e.g., 'USD', 'EUR')
            to_currency: Target currency code (e.g., 'VND', 'JPY')
        
        Returns:
            Converted amount
        
        Raises:
            Exception: If API call fails
            ValueError: If currency code is invalid
        
        Example:
            >>> converter = CurrencyConverter("your_api_key")
            >>> result = converter.convert(100, "USD", "EUR")
        """
        url = f"{self.base_url}/{from_currency.upper()}"
        
        try:
            # Add timeout to avoid hanging
            response = requests.get(url, timeout=30)
            
            if response.status_code != 200:
                raise Exception(f"API call failed with status {response.status_code}: {response.text}")
            
            data = response.json()
            rates = data.get("conversion_rates")
            
            if not rates:
                raise Exception("No conversion rates found in API response")
            
            to_currency_upper = to_currency.upper()
            
            if to_currency_upper not in rates:
                available = ", ".join(list(rates.keys())[:10])  # Show first 10
                raise ValueError(f"Currency '{to_currency}' not found. Available: {available}...")
            
            return amount * rates[to_currency_upper]
            
        except requests.exceptions.Timeout:
            raise Exception("Currency conversion request timed out. Please try again.")
        except requests.exceptions.ConnectionError:
            raise Exception("Network error. Please check your internet connection.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def get_supported_currencies(self) -> Optional[list]:
        """
        Get list of supported currency codes.
        
        Returns:
            List of currency codes (e.g., ['USD', 'EUR', 'VND', ...]) or None if error
        """
        try:
            # Use USD as base to get all rates
            url = f"{self.base_url}/USD"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                rates = response.json().get("conversion_rates", {})
                return list(rates.keys())
            return None
        except Exception:
            return None