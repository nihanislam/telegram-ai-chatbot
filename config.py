import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_API_BASE = "https://models.inference.ai.azure.com"

AVAILABLE_MODELS = {
    '1': {'name': 'gpt-4o', 'display': 'GPT-4o (Most Capable)', 'emoji': '🧠'},
    '2': {'name': 'gpt-4o-mini', 'display': 'GPT-4o Mini (Fast)', 'emoji': '⚡'},
    '3': {'name': 'meta-llama-3.1-70b-instruct', 'display': 'Llama 3.1 70B', 'emoji': '🦙'},
    '4': {'name': 'meta-llama-3.1-405b-instruct', 'display': 'Llama 3.1 405B', 'emoji': '🦙'},
    '5': {'name': 'mistral-large', 'display': 'Mistral Large', 'emoji': '🌪️'},
    '6': {'name': 'phi-3-medium-128k-instruct', 'display': 'Phi-3 Medium', 'emoji': '🔬'},
}

DEFAULT_MODEL = 'gpt-4o-mini'
DEFAULT_SYSTEM_PROMPT = "You are a helpful AI assistant."
MAX_CONVERSATION_HISTORY = 20
MAX_TOKENS = 2000