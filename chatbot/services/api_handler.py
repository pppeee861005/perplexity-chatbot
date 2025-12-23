"""
API 處理層 - 統一管理 Gemini 與 Perplexity API 呼叫
此乃通往兩大 AI 之門
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class APIHandler:
    """
    統一管理 Gemini 與 Perplexity API 呼叫
    """

    def __init__(self, gemini_key: str, perplexity_key: str):
        """
        初始化 API 處理器
        
        參數：
            gemini_key: Gemini 祕鑰
            perplexity_key: Perplexity 祕鑰
        """
        self.gemini_key = gemini_key  # Gemini 祕鑰
        self.perplexity_key = perplexity_key  # Perplexity 祕鑰
        self.timeout = 30  # 超時時間（秒）

    def query_gemini(self, prompt: str) -> str:
        """
        查詢 Gemini API
        
        參數：
            prompt: 提示詞
        
        返回：
            Gemini 之回應
        
        異常：
            Exception: API 呼叫失敗時
        """
        try:
            from google import genai

            client = genai.Client(api_key=self.gemini_key)
            response = client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=[prompt]
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini API 呼叫失敗: {e}")
            raise

    def query_perplexity(self, query: str) -> str:
        """
        查詢 Perplexity API
        
        參數：
            query: 查詢內容
        
        返回：
            Perplexity 之回應
        
        異常：
            Exception: API 呼叫失敗時
        """
        try:
            import requests

            headers = {
                "Authorization": f"Bearer {self.perplexity_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": "sonar",
                "messages": [
                    {"role": "user", "content": query}
                ],
            }
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Perplexity API 呼叫失敗: {e}")
            raise
