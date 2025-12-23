"""
關鍵字偵測過濾器
此乃觸發之門，識別 /請查詢 之關鍵字
"""

from typing import Optional


class TriggerFilter:
    """
    檢測訊息中的關鍵字 /請查詢
    """

    TRIGGER_KEYWORD: str = "/請查詢"  # 觸發關鍵字

    @classmethod
    def is_triggered(cls, message: str) -> bool:
        """
        檢查訊息是否包含觸發關鍵字
        
        參數：
            message: 使用者訊息
        
        返回：
            True 若訊息包含關鍵字，否則 False
        """
        return cls.TRIGGER_KEYWORD in message

    @classmethod
    def extract_content(cls, message: str) -> Optional[str]:
        """
        提取關鍵字後的內容
        
        參數：
            message: 使用者訊息
        
        返回：
            關鍵字後的內容，若無則返回 None
        """
        if not cls.is_triggered(message):
            return None

        # 找到關鍵字的位置
        keyword_index = message.find(cls.TRIGGER_KEYWORD)
        # 提取關鍵字後的內容
        content = message[keyword_index + len(cls.TRIGGER_KEYWORD):].strip()

        # 若無內容則返回 None
        return content if content else None
