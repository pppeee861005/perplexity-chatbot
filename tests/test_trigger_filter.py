"""
關鍵字偵測過濾器之測試
此乃驗證觸發機制之試煉
"""

from hypothesis import given, strategies as st
from chatbot.handlers.trigger_filter import TriggerFilter


class TestTriggerFilterBasic:
    """基礎功能測試"""

    def test_is_triggered_with_keyword(self):
        """驗證包含關鍵字之訊息被正確識別"""
        message = "請幫我查詢 /請查詢 Python 教學"
        assert TriggerFilter.is_triggered(message) is True

    def test_is_triggered_without_keyword(self):
        """驗證不含關鍵字之訊息被正確識別"""
        message = "請幫我解釋 Python 的概念"
        assert TriggerFilter.is_triggered(message) is False

    def test_extract_content_with_keyword(self):
        """驗證關鍵字後之內容被正確提取"""
        message = "/請查詢 Python 教學"
        content = TriggerFilter.extract_content(message)
        assert content == "Python 教學"

    def test_extract_content_with_prefix(self):
        """驗證關鍵字前有文字時，仍能正確提取後續內容"""
        message = "請幫我 /請查詢 最新之 AI 技術"
        content = TriggerFilter.extract_content(message)
        assert content == "最新之 AI 技術"

    def test_extract_content_without_keyword(self):
        """驗證不含關鍵字時返回 None"""
        message = "請幫我解釋 Python"
        content = TriggerFilter.extract_content(message)
        assert content is None

    def test_extract_content_keyword_only(self):
        """驗證僅含關鍵字無後續內容時返回 None"""
        message = "/請查詢"
        content = TriggerFilter.extract_content(message)
        assert content is None

    def test_extract_content_keyword_with_spaces(self):
        """驗證關鍵字後僅有空白時返回 None"""
        message = "/請查詢   "
        content = TriggerFilter.extract_content(message)
        assert content is None


# 屬性測試
@given(st.text())
def test_property_5_keyword_identification(message: str):
    """
    **Feature: perplexity-chatbot, Property 5: 關鍵字正確識別**
    
    對任何包含 `/請查詢` 之訊息，系統應正確識別此關鍵字並觸發 Perplexity 查詢。
    
    **Validates: Requirements 4.1**
    """
    # 若訊息包含關鍵字，is_triggered 應返回 True
    if "/請查詢" in message:
        assert TriggerFilter.is_triggered(message) is True
    # 若訊息不包含關鍵字，is_triggered 應返回 False
    else:
        assert TriggerFilter.is_triggered(message) is False


@given(
    prefix=st.text(),
    query=st.text(min_size=1).filter(lambda x: x.strip())  # 排除純空白之查詢
)
def test_property_6_content_extraction(prefix: str, query: str):
    """
    **Feature: perplexity-chatbot, Property 6: 內容正確提取**
    
    對任何格式為 `/請查詢 <查詢內容>` 之訊息，系統應正確提取 `<查詢內容>` 部分作為查詢。
    
    **Validates: Requirements 4.2, 4.4**
    """
    # 構造訊息：前置文字 + 關鍵字 + 空白 + 查詢內容
    # 根據需求 4.4，系統應忽略前置文字，僅處理關鍵字後之內容
    message = f"{prefix}{TriggerFilter.TRIGGER_KEYWORD} {query}"
    
    # 提取內容
    content = TriggerFilter.extract_content(message)
    
    # 驗證提取之內容應等於查詢部分（已去除前後空白）
    assert content is not None
    assert content == query.strip()
