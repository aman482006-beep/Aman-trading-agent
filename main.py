from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create config
config = DEFAULT_CONFIG.copy()

# 🔥 FORCE OLLAMA (ALL POSSIBLE KEYS — no ambiguity)
config.update({
    "llm_provider": "ollama",
    
    # Model names
    "deep_think_llm": "mistral",
    "quick_think_llm": "mistral",
    "deep_thinking_llm": "mistral",
    "quick_thinking_llm": "mistral",
    
    # Backend
    "backend_url": "http://localhost:11434/v1",

    # Disable any OpenAI reasoning settings (just in case)
    "openai_reasoning_effort": None,
})

# 🔥 Force data source (no API needed)
config["data_vendors"] = {
    "core_stock_apis": "yfinance",
    "technical_indicators": "yfinance",
    "fundamental_data": "yfinance",
    "news_data": "yfinance",
}

# Initialize system
ta = TradingAgentsGraph(debug=True, config=config)

# Run analysis
_, decision = ta.propagate("NVDA", "2024-05-10")

print("\nFINAL DECISION:\n")
print(decision)