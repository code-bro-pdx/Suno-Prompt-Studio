import asyncio
import requests
import logging

logger = logging.getLogger("emergentintegrations-mock")

class UserMessage:
    def __init__(self, text: str):
        self.text = text

class LlmChat:
    def __init__(self, api_key: str, session_id: str, system_message: str):
        self.api_key = api_key
        self.session_id = session_id
        self.system_message = system_message
        self.provider = "anthropic"
        self.model_name = "claude-sonnet-4-5-20250929"
        self.max_tokens = 4000

    def with_model(self, provider: str, model_name: str):
        self.provider = provider
        self.model_name = model_name
        return self

    def with_params(self, max_tokens: int):
        self.max_tokens = max_tokens
        return self

    async def send_message(self, message: UserMessage) -> str:
        return await asyncio.to_thread(self._send_message_sync, message)

    def _send_message_sync(self, message: UserMessage) -> str:
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        model = self.model_name
            
        payload = {
            "model": model,
            "max_tokens": self.max_tokens,
            "system": self.system_message,
            "messages": [
                {"role": "user", "content": message.text}
            ]
        }
        
        logger.info(f"[LlmChat] Sending request to Anthropic Messages API (session: {self.session_id}, model: {model})...")
        
        try:
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code != 200:
                logger.error(f"[LlmChat] Anthropic API failed with status {response.status_code}: {response.text}")
                raise RuntimeError(f"Anthropic API error: {response.text}")
                
            data = response.json()
            return data["content"][0]["text"]
        except Exception as e:
            logger.error(f"[LlmChat] Request failed: {e}")
            raise e
