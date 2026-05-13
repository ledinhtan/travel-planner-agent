import sys
import requests
from typing import Optional
from exception.exceptionhandling import CustomException
from logger.logging import logging

logger = logging.getLogger(__name__)

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
            logger.info("Currency converter starts")
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

        except Exception as e:
            custom_error = CustomException(e, sys)
            logger.error(custom_error)
            raise custom_error    

def get_supported_currencies(self) -> Optional[list]:
    """
    Get list of supported currency codes from ExchangeRate-API.
    
    Returns:
        List of currency codes (e.g., ['USD', 'EUR', 'VND', ...]) or None if error
    
    Example response:
        {
            "result": "success",
            "supported_codes": [
                ["AED", "UAE Dirham"],
                ["AFN", "Afghan Afghani"],
                ...
            ]
        }
    """
    try:
        url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/codes"

        logger.info(f"Fetching supported currencies from: {url}")
        
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("result") == "success":
                # supported_codes is list of [code, name]
                supported_codes = data.get("supported_codes", [])
                # Extract only the code (the first element of each pair)
                currency_codes = [item[0] for item in supported_codes]
                logger.info(f"Successfully fetched {len(currency_codes)} supported currencies")
                return currency_codes
        
        logger.error(f"Failed to fetch supported currencies: {response.status_code}")

        return None
        
    except Exception as e:
        custom_error = CustomException(e, sys)
        logger.error(custom_error)
        raise custom_error