from utils.calculator import Calculator
from typing import List
from langchain.tools import tool

class CalculatorTool:
    """
    Calculator tool for travel expense management.
    
    Provides tools for calculating hotel costs, total expenses, 
    and daily budgets for travel planning.
    """
    
    def __init__(self):
        self.calculator = Calculator()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all calculator tools for the agent."""
        
        @tool
        def estimate_total_hotel_cost(price_per_night: float, total_days: float) -> float:
            """
            Calculate total hotel cost for the entire stay.
            
            Args:
                price_per_night: Hotel price per night in USD
                total_days: Total number of nights/days
                
            Returns:
                float: Total hotel cost
                
            Example:
                estimate_total_hotel_cost(75.50, 5)  # 5 nights at $75.50 = $377.50
            """
            return self.calculator.multiply(price_per_night, total_days)
        
        @tool
        def calculate_total_expense(*costs: float) -> float:
            """
            Calculate total expense summing up all provided costs.
            
            Args:
                *costs: Variable number of expense amounts
                
            Returns:
                float: Sum of all expenses
                
            Example:
                calculate_total_expense(100, 250, 75.50)  # = 425.5
            """
            if not costs:
                return 0.0
            return self.calculator.calculate_total(*costs)
        
        @tool
        def calculate_daily_expense_budget(total_cost: float, days: int) -> float:
            """
            Calculate average daily expense budget.
            
            Args:
                total_cost: Total cost of the trip
                days: Number of travel days
                
            Returns:
                float: Average cost per day
                
            Example:
                calculate_daily_expense_budget(1000, 5)  # = 200 per day
            """
            if days <= 0:
                return 0.0
            return self.calculator.calculate_daily_budget(total_cost, days)
        
        return [
            estimate_total_hotel_cost, 
            calculate_total_expense, 
            calculate_daily_expense_budget
        ]