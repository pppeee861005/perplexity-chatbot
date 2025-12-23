"""
對話歷史管理模型
此乃對話之記錄，承前啟後
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class Message:
    """訊息資料類別"""
    user_id: str  # 使用者識別
    content: str  # 訊息內容
    timestamp: datetime  # 時間戳記
    is_from_user: bool  # 是否來自使用者
    source: str  # 來源："user", "gemini", "perplexity"


@dataclass
class ConversationManager:
    """
    管理每個使用者的對話歷史
    限制為 2 個回合（4 條訊息）
    """

    max_exchanges: int = 2  # 最大回合數
    conversations: Dict[str, List[str]] = field(default_factory=dict)  # 對話錄

    @property
    def max_messages(self) -> int:
        """計算最大訊息數"""
        return self.max_exchanges * 2

    def add_message(self, user_id: str, content: str) -> None:
        """新增訊息到使用者的對話歷史"""
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        self.conversations[user_id].append(content)
        # 超過上限時移除最舊訊息
        if len(self.conversations[user_id]) > self.max_messages:
            self.conversations[user_id] = self.conversations[user_id][-self.max_messages:]

    def get_history(self, user_id: str) -> List[str]:
        """取得使用者的對話歷史"""
        return self.conversations.get(user_id, [])

    def clear_history(self, user_id: str) -> None:
        """清除使用者的對話歷史"""
        self.conversations.pop(user_id, None)
