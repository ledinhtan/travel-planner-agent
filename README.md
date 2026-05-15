# ✈️ Travel Planner Agentic Application

An AI Agent for personalised travel itineraries, expense tracking, and real-time recommendations.

![Python](https://img.shields.io/badge/python-3.10+-3670A0?logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-121D33?logo=parrot)
![LangGraph](https://img.shields.io/badge/LangGraph-1C2D42?logo=diagram-next&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F55036?logo=groq&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Gemini-1A1A2E?logo=googlegemini&logoColor=8E75FF)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)
[![Licence](https://img.shields.io/badge/licence-MIT-blue.svg)](LICENcE)


---

## 📋 Overview

**Travel Planner Agentic** is an AI-powered travel planning assistant that helps users create comprehensive travel itineraries with real-time data. The system uses LangGraph to orchestrate multiple AI tools, including weather information, place search, currency conversion, and expense calculation.

---

### 🌟 Key Features

- 🤖 **AI-Powered Planning** - Multiple LLM support (Groq, Gemini, OpenAI)
- 🌤️ **Weather Information** - Current weather and forecast via OpenWeatherMap API
- 🗺️ **Place Search** - Find Attractions, restaurants, and activities with Google Places API (fallback to Tavily)
- 💱 **Currency Conversion** - Real-time exchange rates for 165+ currencies via ExchangeRate-API
- 💰 **Expense Calculator** - Hotel cost estimation, daily budgets, total expense tracking
- 📄 **Auto-save** - All travel plans automatically saved as Markdown files
- 🎨 **Chat Interface** - Clean, responsive web UI with Markdown support
- 🔧 **Configurable** - Easy to switch between LLM providers via config.yml

---

## 🎨 Demo

![Travel Planner Demo](docs/demo_screenshot.png)

*The main chat interface of the Travel Planner Agent*

---

## 🏗️ Architecture

The agent follows this flow:

1. **User** sends a message via the HTML chat interface
2. **FastAPI backend** receives the request
3. **LangGraph Agent** decides which tools to use
4. **Tools** fetch real-time data from external APIs:
   - Weather API (OpenWeatherMap)
   - Places API (Google Places)
   - Currency API (ExchangeRate-API)
   - Calculator (built-in)
5. **AI** synthesises the response and returns it to the user

![LangGraph Workflow](docs/my_graph.png)
---

## 🛠️ Tech Stack

| Category | Technologies |
|:---|:---|
| **Backend & UI** | FastAPI, Python 3.10, Static HTML/CSS/JS |
| **AI/LLM** | LangChain, LangGraph, Groq, Gemini, OpenAI |
| **APIs** | OpenWeatherMap, Google Places, Tavily, ExchangeRate-API |
| **Logging** | Custom logging with file rotation |
| **Exception Handling** | Custom exception with traceback capture |

--- 

## 📁 Project Structure

```bash
travel_planner_agent/
├─ agent/                           # LangGraph agent workflow
│  ├─ __init__.py
│  └─ agentic_workflow.py
├─ config/                          # Configuration files
│  ├─ __init__.py
│  └─ config.yml
├─ docs/                            # Documentation
│  ├─ demo_screenshot.png           # UI demo screenshot
│  └─ my_graph.png                  # LangGraph workflow visualisation
├─ exception/                       # Custom exception handling
│  ├─ __init__.py
│  └─ exceptionhandling.py
├─ logger/                          # Logging configuration
│  ├─ __init__.py
│  └─ logging.py
├─ notebooks/
│  └─ experiments.ipynb
├─ prompt_library/                  # System prompts
│  ├─ __init__.py
│  └─ prompt.py
├─ templates/                       # HTML frontend
│  └─ index.html
├─ tools/                           # LangChain tools
│  ├─ __init__.py
│  ├─ calculator_tool.py
│  ├─ currency_conversion_tool.py
│  ├─ place_search_tool.py
│  └─ weather_info_tool.py
├─ utils/                           # Utility modules
│  ├─ __init__.py
│  ├─ calculator.py
│  ├─ config_loader.py
│  ├─ currency_converter.py
│  ├─ model_loader.py
│  ├─ place_info_search.py
│  ├─ save_to_document.py
│  └─ weather_info.py
├─ .dockerignore
├─ .env.example                     # Template for environment variables   
├─ .gitignore
├─ .python-version
├─ Dockerfile
├─ LICENSE
├─ main.py                          # FastAPI entry point
├─ pyproject.toml
├─ README.md
├─ requirements.txt
└─ setup.py

```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Docker (optional, for containerized deployment)
- API keys for (see `.env.example`):
  - LLM Provider (Groq/Gemini/OpenAI)
  - [OpenWeatherMap](https://openweathermap.org/api)
  - [Google Places API](https://developers.google.com/maps/documentation/places/web-service/get-api-key)
  - [Tavily](https://tavily.com/) (fallback search)
  - [ExchangeRate-API](https://www.exchangerate-api.com/)

### Local Development

#### 1. Clone the repository
   ```bash
   git clone https://github.com/ledinhtan/travel-planner-agent.git
   cd travel_planner_agent
   ```

#### 2. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```
#### 4. Set up environment variables
Create a `.env` file:
```bash
cp .env.example .env
# Edit .env with your API keys
```
Example configuration of `.env`:
```env
OPENAI_API_KEY="your_openai_api_key"
GROQ_API_KEY="your_groq_api_key"
GOOGLE_API_KEY="your_google_api_key"
GOOGLE_PLACES_API_KEY="your_google_place_api_key"
TAVILY_API_KEY="your_tavily_api_key"
OPENWEATHERMAP_API_KEY="your_openweathermap_api_key"
EXCHANGE_RATE_API_KEY="your_exchange_rate_api_key"
```

#### 5. Run the application
```bash
uvicorn main:app --reload --port 8000
```

---

## 📜 Licence

- **Code**: MIT Licence (see [LICENSE](LICENSE) file)