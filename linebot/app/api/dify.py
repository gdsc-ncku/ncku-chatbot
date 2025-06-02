"""Dify API client implementation for chat interactions."""

import logging
import json
import os
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from functools import wraps
import time

import requests
from dotenv import load_dotenv
from requests.exceptions import RequestException
from ..repositories.user_repository import UserRepository

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


@dataclass
class DifyConfig:
    """Configuration for Dify API client."""

    api_key: str
    base_url: str = "https://dify-ncku-chatbot.yenslife.top/v1"
    max_retries: int = 1
    retry_delay: float = 1.0


def retry_on_error(max_retries: int = 1, delay: float = 1.0):
    """Decorator for implementing retry logic."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except RequestException as e:
                    if attempt == max_retries - 1:
                        raise
                    logger.warning(
                        f"Attempt {attempt + 1} failed: {str(e)}. Retrying..."
                    )
                    time.sleep(delay * (attempt + 1))
            return None

        return wrapper

    return decorator


class DifyClient:
    """Client for interacting with Dify API."""

    def __init__(self, config: DifyConfig, user_repository: UserRepository):
        self.config = config
        self.user_repository = user_repository
        self._validate_config()

    def _validate_config(self) -> None:
        """Validate the API configuration."""
        if not self.config.api_key:
            raise ValueError("DIFY_API_KEY is not set in environment variables")

    def _prepare_headers(self) -> Dict[str, str]:
        """Prepare HTTP headers for API requests."""
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

    def _prepare_files(self, file_url: str) -> List[Dict[str, str]]:
        """Prepare files payload for API request."""
        return [{"type": "image", "transfer_method": "remote_url", "url": file_url}]

    @retry_on_error()
    def inference(
        self, query: str, line_id: str = "abc-123", file_url: Optional[str] = None
    ) -> str:
        """
        Make an inference request to Dify API.

        Args:
            query: The user's query text
            line_id: The LINE user ID
            file_url: Optional URL to an image file

        Returns:
            str: The API response text

        Raises:
            RequestException: If the API request fails
        """
        user = self.user_repository.get_user(line_id)

        payload = {
            "inputs": {},
            "query": "請分析這張圖片" if file_url else query,
            "response_mode": "blocking",
            "conversation_id": user.conversation_id or "",
            "user": line_id,
            "files": self._prepare_files(file_url) if file_url else None,
        }

        logger.info(f"Sending request to Dify API with payload: {payload}")

        try:
            response = requests.post(
                f"{self.config.base_url}/chat-messages",
                headers=self._prepare_headers(),
                json=payload,
            )

            response.raise_for_status()
            logger.info(f"Received response with status code: {response.status_code}")

            try:
                response_data = json.loads(response.content.decode("utf-8"))
                answer = response_data["answer"]

                # Update conversation ID if present
                if new_conversation_id := response_data.get("conversation_id"):
                    self.user_repository.update_conversation_id(
                        line_id, new_conversation_id
                    )
                    logger.info(f"Updated conversation ID: {new_conversation_id}")

                return answer

            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error: {str(e)}")
            except KeyError as e:
                logger.error(f"Missing required field in response: {str(e)}")

        except RequestException as e:
            logger.error(f"API request error: {str(e)}")
            raise

        return "無法取得回應，請稍後再試"


# Create global instances
config = DifyConfig(api_key=os.getenv("DIFY_API_KEY", ""))
user_repository = UserRepository()
dify_client = DifyClient(config, user_repository)


# Provide a simple interface for backward compatibility
def inference(query: str, line_id: str = "abc-123", files: Optional[str] = None) -> str:
    """Backward compatible interface for Dify API inference."""
    try:
        return dify_client.inference(query, line_id, files)
    except Exception as e:
        logger.error(f"Inference error: {str(e)}")
        return "系統發生錯誤，請稍後再試"


if __name__ == "__main__":
    pass
