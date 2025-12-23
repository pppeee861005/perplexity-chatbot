"""
主要聊天機器人類別
此乃對話之樞紐，協調各元件
"""

import logging
from typing import Optional

from chatbot.models import ConversationManager
from chatbot.services import APIHandler
from .trigger_filter import TriggerFilter

logger = logging.getLogger(__name__)


class ChatBot:
    """
    主要業務邏輯，協調 APIHandler 與 ConversationManager
    """

    def __init__(
        self,
        api_handler: APIHandler,
        conversation_manager: ConversationManager
    ):
        """
        初始化聊天機器人
        
        參數：
            api_handler: API 處理器
            conversation_manager: 對話歷史管理器
        """
        self.api_handler = api_handler  # API 處理器
        self.conversation_manager = conversation_manager  # 對話歷史管理器

    def process_message(self, user_id: str, message: str) -> str:
        """
        處理使用者訊息
        
        參數：
            user_id: 使用者識別
            message: 使用者訊息
        
        返回：
            聊天機器人之回應
        
        異常：
            Exception: 處理訊息時發生錯誤
        """
        try:
            # 新增使用者訊息到歷史
            self.conversation_manager.add_message(user_id, message)

            # 取得對話歷史
            history = self.conversation_manager.get_history(user_id)

            # 檢查是否觸發 Perplexity 查詢
            if TriggerFilter.is_triggered(message):
                # 提取查詢內容
                query_content = TriggerFilter.extract_content(message)
                if not query_content:
                    return "請提供查詢內容。"

                # 調用 Perplexity API
                response = self.api_handler.query_perplexity(query_content)
            else:
                # 構建 Gemini 提示詞
                history_str = "\n".join(history[:-1]) if len(history) > 1 else "（無歷史）"
                prompt = f"對話歷史:\n{history_str}\n\n使用者訊息: {message}"

                # 調用 Gemini API
                response = self.api_handler.query_gemini(prompt)

            # 新增 AI 回覆到歷史
            self.conversation_manager.add_message(user_id, response)

            return response

        except Exception as e:
            logger.error(f"處理訊息時出錯: {e}")
            error_message = "抱歉，處理您的訊息時出現錯誤。請稍後再試。"
            return error_message
