"""
對話歷史管理器之測試
此乃驗證對話記錄之試煉
"""

from hypothesis import given, strategies as st
from chatbot.models import ConversationManager


class TestConversationManagerBasic:
    """基礎功能測試"""

    def test_add_message_creates_new_user(self):
        """驗證新使用者首次發送訊息時建立新的對話歷史"""
        manager = ConversationManager()
        manager.add_message("user1", "你好")
        assert "user1" in manager.conversations
        assert manager.conversations["user1"] == ["你好"]

    def test_add_message_appends_to_existing(self):
        """驗證訊息被正確新增至現有對話歷史"""
        manager = ConversationManager()
        manager.add_message("user1", "訊息1")
        manager.add_message("user1", "訊息2")
        assert manager.conversations["user1"] == ["訊息1", "訊息2"]

    def test_get_history_returns_empty_for_unknown_user(self):
        """驗證未知使用者返回空列表"""
        manager = ConversationManager()
        history = manager.get_history("unknown_user")
        assert history == []

    def test_get_history_returns_correct_history(self):
        """驗證取得正確之對話歷史"""
        manager = ConversationManager()
        manager.add_message("user1", "訊息1")
        manager.add_message("user1", "訊息2")
        history = manager.get_history("user1")
        assert history == ["訊息1", "訊息2"]

    def test_clear_history_removes_user(self):
        """驗證清除歷史後使用者記錄被移除"""
        manager = ConversationManager()
        manager.add_message("user1", "訊息1")
        manager.clear_history("user1")
        assert "user1" not in manager.conversations

    def test_clear_history_nonexistent_user(self):
        """驗證清除不存在之使用者不拋出異常"""
        manager = ConversationManager()
        manager.clear_history("nonexistent")
        # 應無異常拋出
        assert True

    def test_max_messages_limit(self):
        """驗證訊息超過上限時移除最舊訊息"""
        manager = ConversationManager(max_exchanges=2)  # 最多 4 條訊息
        manager.add_message("user1", "訊息1")
        manager.add_message("user1", "訊息2")
        manager.add_message("user1", "訊息3")
        manager.add_message("user1", "訊息4")
        manager.add_message("user1", "訊息5")  # 超過上限
        
        # 應保留最新之 4 條訊息
        assert manager.conversations["user1"] == ["訊息2", "訊息3", "訊息4", "訊息5"]


# 屬性測試
@given(
    user_id=st.text(min_size=1, max_size=10),
    content=st.text(max_size=50)
)
def test_property_3_message_addition(user_id: str, content: str):
    """
    **Feature: perplexity-chatbot, Property 3: 訊息新增至歷史**
    
    對任何使用者發送之訊息，系統應將其新增至該使用者之對話歷史。
    
    **Validates: Requirements 1.3**
    """
    manager = ConversationManager()
    
    # 新增訊息前，歷史應為空
    initial_history = manager.get_history(user_id)
    initial_length = len(initial_history)
    
    # 新增訊息
    manager.add_message(user_id, content)
    
    # 新增後，歷史長度應增加 1
    new_history = manager.get_history(user_id)
    assert len(new_history) == initial_length + 1
    
    # 新增之訊息應在歷史中
    assert content in new_history


@given(
    user_id=st.text(min_size=1, max_size=10),
    messages=st.lists(st.text(max_size=30), min_size=1, max_size=8)
)
def test_property_4_history_limit_management(user_id: str, messages: list):
    """
    **Feature: perplexity-chatbot, Property 4: 對話歷史上限管理**
    
    對任何使用者，其對話歷史長度應不超過設定上限（預設 4 條訊息）；超過時應移除最舊訊息。
    
    **Validates: Requirements 1.4, 3.3**
    """
    manager = ConversationManager(max_exchanges=2)  # 最多 4 條訊息
    max_messages = manager.max_messages
    
    # 新增所有訊息
    for message in messages:
        manager.add_message(user_id, message)
    
    # 取得最終歷史
    history = manager.get_history(user_id)
    
    # 驗證歷史長度不超過上限
    assert len(history) <= max_messages
    
    # 若訊息數超過上限，應保留最新之訊息
    if len(messages) > max_messages:
        # 應保留最後 max_messages 條訊息
        expected_history = messages[-max_messages:]
        assert history == expected_history


@given(
    user_id=st.text(min_size=1, max_size=10),
    messages=st.lists(st.text(min_size=1, max_size=30), min_size=1, max_size=3)
)
def test_property_7_user_isolation(user_id: str, messages: list):
    """
    **Feature: perplexity-chatbot, Property 7: 使用者隔離**
    
    對任何使用者，其對話歷史應完全隔離；新增訊息後，歷史應精確反映該使用者之訊息。
    
    **Validates: Requirements 3.1, 3.2**
    """
    manager = ConversationManager()
    
    # 為使用者新增訊息
    for message in messages:
        manager.add_message(user_id, message)
    
    # 取得使用者之歷史
    history = manager.get_history(user_id)
    
    # 驗證歷史精確反映所有訊息
    assert history == messages
    
    # 驗證歷史長度與訊息數相符
    assert len(history) == len(messages)
