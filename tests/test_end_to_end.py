"""
端對端測試 - 驗證完整之訊息處理流程
此乃整體系統之試煉，驗證各元件之協調
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from chatbot.handlers.chatbot import ChatBot
from chatbot.models import ConversationManager
from chatbot.services import APIHandler


class TestEndToEndMessageProcessing:
    """端對端訊息處理測試"""

    @pytest.fixture
    def setup(self):
        """設置測試環境"""
        # 建立模擬之 API 處理器
        api_handler = Mock(spec=APIHandler)
        api_handler.query_gemini = Mock(return_value="Gemini 之回應")
        api_handler.query_perplexity = Mock(return_value="Perplexity 之回應")

        # 建立真實之對話管理器
        conversation_manager = ConversationManager()

        # 建立聊天機器人
        chatbot = ChatBot(api_handler, conversation_manager)

        return {
            'chatbot': chatbot,
            'api_handler': api_handler,
            'conversation_manager': conversation_manager
        }

    def test_message_without_keyword_uses_gemini(self, setup):
        """
        驗證無關鍵字訊息使用 Gemini

        **Feature: perplexity-chatbot, Property 1: 無關鍵字訊息使用 Gemini**
        **Validates: Requirements 1.1**
        """
        chatbot = setup['chatbot']
        api_handler = setup['api_handler']
        user_id = "test_user"
        message = "請解釋 Python 的概念"

        # 處理訊息
        response = chatbot.process_message(user_id, message)

        # 驗證 Gemini 被調用
        assert api_handler.query_gemini.called
        assert not api_handler.query_perplexity.called
        assert response == "Gemini 之回應"

    def test_message_with_keyword_uses_perplexity(self, setup):
        """
        驗證含關鍵字訊息使用 Perplexity

        **Feature: perplexity-chatbot, Property 2: 含關鍵字訊息使用 Perplexity**
        **Validates: Requirements 1.2**
        """
        chatbot = setup['chatbot']
        api_handler = setup['api_handler']
        user_id = "test_user"
        message = "/請查詢 最新之 AI 技術"

        # 處理訊息
        response = chatbot.process_message(user_id, message)

        # 驗證 Perplexity 被調用
        assert api_handler.query_perplexity.called
        assert not api_handler.query_gemini.called
        assert response == "Perplexity 之回應"

    def test_message_added_to_history(self, setup):
        """
        驗證訊息被新增至對話歷史

        **Feature: perplexity-chatbot, Property 3: 訊息新增至歷史**
        **Validates: Requirements 1.3**
        """
        chatbot = setup['chatbot']
        conversation_manager = setup['conversation_manager']
        user_id = "test_user"
        message = "你好"

        # 處理訊息前，歷史應為空
        initial_history = conversation_manager.get_history(user_id)
        assert len(initial_history) == 0

        # 處理訊息
        chatbot.process_message(user_id, message)

        # 驗證訊息被新增至歷史
        history = conversation_manager.get_history(user_id)
        assert len(history) == 2  # 使用者訊息 + AI 回應
        assert message in history

    def test_multi_turn_conversation_preserves_history(self, setup):
        """
        驗證多輪對話保留歷史

        **Feature: perplexity-chatbot, Property 4: 對話歷史上限管理**
        **Validates: Requirements 1.4, 3.3**
        """
        chatbot = setup['chatbot']
        conversation_manager = setup['conversation_manager']
        user_id = "test_user"

        # 進行多輪對話
        messages = [
            "第一輪訊息",
            "第二輪訊息",
            "第三輪訊息"
        ]

        for message in messages:
            chatbot.process_message(user_id, message)

        # 驗證歷史被保留（最多 4 條訊息）
        history = conversation_manager.get_history(user_id)
        assert len(history) <= 4  # max_exchanges=2 表示最多 4 條訊息

        # 驗證最新之訊息在歷史中
        assert messages[-1] in history

    def test_user_isolation_in_conversation(self, setup):
        """
        驗證不同使用者之對話歷史隔離

        **Feature: perplexity-chatbot, Property 7: 使用者隔離**
        **Validates: Requirements 3.1, 3.2**
        """
        chatbot = setup['chatbot']
        conversation_manager = setup['conversation_manager']

        # 為不同使用者新增訊息
        user1_message = "使用者 1 之訊息"
        user2_message = "使用者 2 之訊息"

        chatbot.process_message("user1", user1_message)
        chatbot.process_message("user2", user2_message)

        # 驗證歷史隔離
        user1_history = conversation_manager.get_history("user1")
        user2_history = conversation_manager.get_history("user2")

        assert user1_message in user1_history
        assert user1_message not in user2_history
        assert user2_message in user2_history
        assert user2_message not in user1_history

    def test_error_handling_on_api_failure(self, setup):
        """
        驗證 API 呼叫失敗時之錯誤處理

        **Feature: perplexity-chatbot, Property 8: 錯誤處理穩定性**
        **Validates: Requirements 2.1, 2.2**
        """
        chatbot = setup['chatbot']
        api_handler = setup['api_handler']

        # 模擬 API 呼叫失敗
        api_handler.query_gemini.side_effect = Exception("API 呼叫失敗")

        # 處理訊息
        response = chatbot.process_message("test_user", "測試訊息")

        # 驗證返回友善之錯誤訊息
        assert "錯誤" in response or "抱歉" in response
        assert response != ""

    def test_keyword_extraction_in_message_processing(self, setup):
        """
        驗證訊息處理中之關鍵字提取

        **Feature: perplexity-chatbot, Property 6: 內容正確提取**
        **Validates: Requirements 4.2, 4.4**
        """
        chatbot = setup['chatbot']
        api_handler = setup['api_handler']
        user_id = "test_user"

        # 構造含關鍵字之訊息
        message = "/請查詢 Python 教學"

        # 處理訊息
        chatbot.process_message(user_id, message)

        # 驗證 Perplexity 被調用，且提取之查詢內容被傳遞
        assert api_handler.query_perplexity.called
        # 取得呼叫時之參數
        call_args = api_handler.query_perplexity.call_args
        # 驗證查詢內容被正確提取
        assert "Python 教學" in str(call_args)

    def test_message_without_query_content_after_keyword(self, setup):
        """
        驗證關鍵字後無查詢內容時之處理

        **Feature: perplexity-chatbot, Property 6: 內容正確提取**
        **Validates: Requirements 4.3**
        """
        chatbot = setup['chatbot']
        user_id = "test_user"

        # 訊息僅包含關鍵字，無後續內容
        message = "/請查詢"

        # 處理訊息
        response = chatbot.process_message(user_id, message)

        # 驗證返回提示訊息
        assert "提供查詢內容" in response or "查詢" in response

    def test_complete_conversation_flow(self, setup):
        """
        驗證完整之對話流程

        此測試驗證：
        1. 使用者發送訊息
        2. 系統識別關鍵字
        3. 系統調用適當之 API
        4. 系統新增訊息至歷史
        5. 系統返回回應

        **Validates: Requirements 1.1, 1.2, 1.3, 1.4**
        """
        chatbot = setup['chatbot']
        conversation_manager = setup['conversation_manager']
        api_handler = setup['api_handler']
        user_id = "test_user"

        # 第一輪：無關鍵字訊息
        response1 = chatbot.process_message(user_id, "你好")
        assert api_handler.query_gemini.called
        history1 = conversation_manager.get_history(user_id)
        assert len(history1) == 2

        # 重置模擬
        api_handler.reset_mock()

        # 第二輪：含關鍵字訊息
        response2 = chatbot.process_message(user_id, "/請查詢 天氣")
        assert api_handler.query_perplexity.called
        history2 = conversation_manager.get_history(user_id)
        assert len(history2) == 4  # 達到上限

        # 驗證歷史包含兩輪對話
        assert "你好" in history2
        # 訊息被完整儲存，包含關鍵字
        assert "/請查詢 天氣" in history2
