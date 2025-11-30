import httpx
import logging
from config import GITHUB_TOKEN, GITHUB_API_BASE

logger = logging.getLogger(__name__)

class GitHubModelsAPI:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Content-Type": "application/json"
        }
    
    async def chat_completion(self, model: str, messages: list, max_tokens: int = 2000, temperature: float = 0.7):
        """Send chat completion request to GitHub Models API"""
        url = f"{GITHUB_API_BASE}/chat/completions"
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                logger.info(f"Calling API with model: {model}")
                response = await client.post(url, json=payload, headers=self.headers)
                response.raise_for_status()
                result = response.json()
                logger.info(f"API call successful")
                return result
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
                return {"error": f"API Error: {e.response.status_code}"}
            except httpx.TimeoutException:
                logger.error("Request timeout")
                return {"error": "Request timeout. Please try again."}
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                return {"error": f"Unexpected error: {str(e)}"}
    
    async def stream_chat_completion(self, model: str, messages: list, max_tokens: int = 2000):
        """Stream chat completion (for future implementation)"""
        # Placeholder for streaming support
        pass