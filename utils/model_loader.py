# import os
# from typing import Literal, Optional, Any
# from pydantic import BaseModel, Field
# from utils.config_loader import load_config
# from langchain_groq import ChatGroq
# from langchain_openai import ChatOpenAI
# from langchain_google_genai import ChatGoogleGenerativeAI

# class ConfigLoader:
#     def __init__(self):
#         print(f"Loaded config.....")
#         self.config = load_config()
    
#     def __getitem__(self, key):
#         return self.config[key]

# class ModelLoader(BaseModel):
#     model_provider: Literal["groq", "gemini", "openai"] = "groq"
#     config: Optional[ConfigLoader] = Field(default=None, exclude=True)

#     def model_post_init(self, __context: Any) -> None:
#         self.config = ConfigLoader()
    
#     class Config:
#         arbitrary_types_allowed = True
    
#     def load_llm(self):
#         """
#         Load and return the LLM model.
#         """
#         print("LLM loading...")
#         print(f"Loading model from provider: {self.model_provider}")
#         if self.model_provider == "groq":
#             print("Loading LLM from Groq..............")
#             groq_api_key = os.getenv("GROQ_API_KEY")
#             model_name = self.config["llm"]["groq"]["model_name"]
#             llm=ChatGroq(model=model_name, api_key=groq_api_key)
#         elif self.model_provider == "gemini":
#             print("Loading LLM from Gemini..............")
#             google_api_key = os.getenv("GOOGLE_API_KEY")
#             model_name = self.config["llm"]["gemini"]["model_name"]
#             llm = ChatGoogleGenerativeAI(model_name=model_name, api_key=google_api_key)
#         else:
#             print("Loading LLM from OpenAI..............")
#             openai_api_key = os.getenv("OPENAI_API_KEY")
#             model_name = self.config["llm"]["openai"]["model_name"]
#             llm = ChatOpenAI(model_name=model_name, api_key=openai_api_key)
        
#         return llm
    

import os
from typing import Literal
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from utils.config_loader import load_config

load_dotenv()


class ModelLoader:
    """
    Simple LLM model loader for different providers.
    Supports: groq, gemini, openai
    """
    
    def __init__(self, model_provider: Literal["groq", "gemini", "openai"] = "groq"):
        """
        Initialise model loader.
        
        Args:
            model_provider: LLM provider name ('groq', 'gemini', or 'openai')
        
        Raises:
            ValueError: If API key is missing for the selected provider
        """
        self.model_provider = model_provider
        self.config = load_config()
        self._validate_api_key()
    
    def _validate_api_key(self):
        """Check if the required API key is present."""
        key_map = {
            "groq": "GROQ_API_KEY",
            "gemini": "GOOGLE_API_KEY",
            "openai": "OPENAI_API_KEY"
        }
        
        key_name = key_map.get(self.model_provider)
        api_key = os.getenv(key_name)
        
        if not api_key:
            raise ValueError(f"{key_name} not found in environment variables")
        
        return api_key
    
    def _get_model_config(self):
        """Get model configuration from config file."""
        return self.config["llm"][self.model_provider]
    
    def load_llm(self):
        """
        Load and return the LLM model.
        
        Returns:
            Chat model instance
        """
        print(f"🔄 Loading LLM from: {self.model_provider.upper()}")
        
        providers = {
            "groq": self._load_groq,
            "gemini": self._load_gemini,
            "openai": self._load_openai
        }
        
        loader = providers.get(self.model_provider)
        if not loader:
            raise ValueError(f"Unsupported provider: {self.model_provider}")
        
        return loader()
    
    def _load_groq(self):
        """Load Groq LLM."""
        model_config = self._get_model_config()
        api_key = os.getenv("GROQ_API_KEY")
        
        print(f"✅ Loading Groq model: {model_config['model_name']}")
        return ChatGroq(
            model=model_config["model_name"],
            api_key=api_key,
            temperature=model_config.get("temperature", 0)
        )
    
    def _load_gemini(self):
        """Load Google Gemini LLM."""
        model_config = self._get_model_config()
        api_key = os.getenv("GOOGLE_API_KEY")
        
        print(f"✅ Loading Gemini model: {model_config['model_name']}")
        return ChatGoogleGenerativeAI(
            model=model_config["model_name"],
            api_key=api_key,
            temperature=model_config.get("temperature", 0)
        )
    
    def _load_openai(self):
        """Load OpenAI LLM."""
        model_config = self._get_model_config()
        api_key = os.getenv("OPENAI_API_KEY")
        
        print(f"✅ Loading OpenAI model: {model_config['model_name']}")
        return ChatOpenAI(
            model=model_config["model_name"],
            api_key=api_key,
            temperature=model_config.get("temperature", 0)
        )