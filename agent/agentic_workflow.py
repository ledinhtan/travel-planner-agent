from typing import List
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition

from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT

from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool


class GraphBuilder:
    """
    Builds and manages the LangGraph workflow for the travel planner agent.
    Combines all tools (weather, places, calculator, currency) into a single agent.
    """
    
    def __init__(self, model_provider: str = "groq"):
        """
        Initialise the graph builder with all tools and LLM.
        
        Args:
            model_provider: LLM provider ('groq', 'gemini', 'openai')
        """
        # Initialise model
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()
        
        # Initialise all tools
        self._init_tools()
        
        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        
        # System prompt
        self.system_prompt = SYSTEM_PROMPT
        
        # Graph will be built when __call__ is invoked
        self._graph = None
    
    def _init_tools(self):
        """Initialise all tool instances and combine them into a single list."""
        weather_tools = WeatherInfoTool()
        place_tools = PlaceSearchTool()
        calculator_tools = CalculatorTool()
        currency_tools = CurrencyConverterTool()
        
        # Combine all tool lists
        self.tools: List = [
            *weather_tools.weather_tool_list,
            *place_tools.place_search_tool_list,
            *calculator_tools.calculator_tool_list,
            *currency_tools.currency_converter_tool_list,
        ]
        
        # Store individual tool instances for potential future use
        self.weather_tools = weather_tools
        self.place_tools = place_tools
        self.calculator_tools = calculator_tools
        self.currency_tools = currency_tools
        
        print(f"✅ Loaded {len(self.tools)} tools:")
        for tool in self.tools:
            print(f"   - {tool.name}")
    
    def _agent_function(self, state: MessagesState):
        """
        Main agent function that processes user messages with tools.
        
        Args:
            state: Current conversation state containing messages
        
        Returns:
            Dict with updated messages including agent response
        """
        user_messages = state["messages"]
        messages_with_prompt = [self.system_prompt] + user_messages
        response = self.llm_with_tools.invoke(messages_with_prompt)

        return {"messages": [response]}
    
    def _build_graph(self):
        """
        Build the LangGraph workflow.
        
        Returns:
            Compiled StateGraph ready for execution
        """
        graph_builder = StateGraph(MessagesState)
        
        # Add nodes
        graph_builder.add_node("agent", self._agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        
        # Add edges
        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge("tools", "agent")
        graph_builder.add_edge("agent", END) 
        
        # Compile and return
        return graph_builder.compile()
    
    def get_graph(self):
        """Get the compiled graph (builds if not already built)."""
        if self._graph is None:
            self._graph = self._build_graph()
            
        return self._graph
    
    def __call__(self):
        """Make the instance callable, returning the compiled graph."""
        return self.get_graph()