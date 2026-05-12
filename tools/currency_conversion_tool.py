import os
from typing import List
from dotenv import load_dotenv
from langchain.tools import tool
from utils.currency_converter import CurrencyConverter

class CurrencyConverterTool:
    """
    Currency converter tool for LangChain agents.
    Provides exchange rate conversion between different currencies.
    """
    
    def __init__(self):
        """Initialise the currency converter with API key from environment."""
        load_dotenv()
        self.api_key = os.environ.get("EXCHANGE_RATE_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "EXCHANGE_RATE_API_KEY not found. "
                "Please add it to your .env file"
            )
        
        self.currency_service = CurrencyConverter(self.api_key)
        self.currency_converter_tool_list = self._setup_tools()
    
    def _setup_tools(self) -> List:
        """Setup and return the currency conversion tool."""
        
        @tool
        def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
            """
            Convert an amount from one currency to another.
            
            Args:
                amount: The amount to convert (e.g., 100)
                from_currency: Source currency code (e.g., 'USD', 'EUR', 'GBP')
                to_currency: Target currency code (e.g., 'VND', 'JPY', 'CNY')
            
            Returns:
                float: The converted amount
            
            Example:
                convert_currency(100, 'USD', 'EUR')
            """
            return self.currency_service.convert(amount, from_currency, to_currency)
        
        return [convert_currency]