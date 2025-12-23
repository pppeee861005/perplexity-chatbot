# Perplexity Chatbot

## 簡介

此乃一個簡潔而雅致之 Python 聊天機器人系統。系統藉關鍵字 `/請查詢` 之偵測，決定調用 Perplexity 進行網搜，其餘則由 Gemini 模型應答。

## 功能特性

- **智慧路由**: 根據訊息內容自動選擇 Gemini 或 Perplexity
- **對話歷史管理**: 維持使用者對話上下文，支援多輪對話
- **使用者隔離**: 各使用者之對話歷史完全獨立
- **錯誤處理**: 妥善處理 API 呼叫失敗與環境變數缺失
- **簡潔設計**: 參考 `pt_cb.py` 風格，代碼簡潔易讀

## 系統架構

```
訊息輸入 → 關鍵字偵測 → 路由決策 → API 呼叫 → 歷史管理 → 回應輸出
```

### 核心元件

1. **TriggerFilter**: 偵測訊息中之 `/請查詢` 關鍵字
2. **ConversationManager**: 管理各使用者之對話歷史
3. **APIHandler**: 統一管理 Gemini 與 Perplexity API 呼叫
4. **ChatBot**: 主要業務邏輯，協調各元件

## 安裝與配置

### 環境需求

- Python 3.8 或更高版本
- pip 套件管理工具

### 安裝步驟

1. 複製本專案
```bash
git clone <repository-url>
cd perplexity-chatbot
```

2. 建立虛擬環境
```bash
python -m venv venv
```

3. 啟動虛擬環境
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. 安裝依賴套件
```bash
pip install -r requirements.txt
```

5. 配置環境變數
```bash
# 複製 .env.example 為 .env
cp .env.example .env

# 編輯 .env 檔案，填入 API 金鑰
# GOOGLE_API_KEY=your_gemini_api_key
# PERPLEXITY_API_KEY=your_perplexity_api_key
```

## 啟動系統

### 快速啟動

1. **啟動虛擬環境**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

2. **執行主程式**
```bash
python main.py
```

3. **互動使用**

```
[汝曰]: 你好
[機器人]: Gemini 之回應...

[汝曰]: /請查詢 今天天氣如何
[機器人]: Perplexity 之網搜結果...

[汝曰]: quit
```

### 退出系統

系統提供兩種退出方式：

#### 方式一：輸入退出指令

在互動模式中，輸入 `quit` 即可優雅地退出系統：

```
[汝曰]: quit
```

系統將記錄退出日誌，並安全地關閉所有連接。

#### 方式二：中斷信號

按下 `Ctrl+C` 鍵盤快捷鍵，系統將捕捉中斷信號並安全退出：

```bash
Ctrl+C
```

#### 方式三：關閉虛擬環境

若要完全退出虛擬環境，執行：

```bash
deactivate
```

### 使用方式

#### 方式一：互動式命令行

直接執行 `python main.py`，系統將進入互動模式，允許閣下直接輸入訊息與系統對話。

```bash
python main.py
```

#### 方式二：程式化使用

在自己之程式中引入本系統：

```python
from chatbot.handlers.chatbot import ChatBot
from chatbot.services.api_handler import APIHandler
from chatbot.models.conversation import ConversationManager
from dotenv import dotenv_values

# 載入環境變數
config = dotenv_values()

# 初始化元件
api_handler = APIHandler(
    gemini_key=config.get("GOOGLE_API_KEY"),
    perplexity_key=config.get("PERPLEXITY_API_KEY")
)
conversation_manager = ConversationManager()
chatbot = ChatBot(api_handler, conversation_manager)

# 處理訊息
response = chatbot.process_message(user_id="user_123", message="你好")
print(response)

# 使用 Perplexity 進行網搜
response = chatbot.process_message(user_id="user_123", message="/請查詢 Python 最新版本")
print(response)
```

### 關鍵字用法

- **無關鍵字**: 訊息由 Gemini 處理
  ```
  使用者: 你好，今天天氣如何？
  回應: Gemini 之回應
  ```

- **含關鍵字**: 訊息由 Perplexity 進行網搜
  ```
  使用者: /請查詢 今天天氣如何？
  回應: Perplexity 之網搜結果
  ```

## 測試

### 執行所有測試

```bash
python -m pytest tests/ -v
```

### 執行特定測試

```bash
# 測試對話管理
python -m pytest tests/test_conversation_manager.py -v

# 測試關鍵字偵測
python -m pytest tests/test_trigger_filter.py -v

# 測試端對端流程
python -m pytest tests/test_end_to_end.py -v
```

### 屬性測試

系統包含屬性測試以驗證核心功能：

- **屬性 1**: 無關鍵字訊息使用 Gemini
- **屬性 2**: 含關鍵字訊息使用 Perplexity
- **屬性 3**: 訊息新增至歷史
- **屬性 4**: 對話歷史上限管理
- **屬性 5**: 關鍵字正確識別
- **屬性 6**: 內容正確提取
- **屬性 7**: 使用者隔離
- **屬性 8**: 錯誤處理穩定性

## 專案結構

```
perplexity-chatbot/
├── chatbot/
│   ├── __init__.py
│   ├── config.py              # 配置管理
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── chatbot.py         # 主要 ChatBot 類別
│   │   └── trigger_filter.py  # 關鍵字偵測
│   ├── models/
│   ├── __init__.py
│   └── conversation.py    # 對話歷史管理
│   └── services/
│       ├── __init__.py
│       └── api_handler.py     # API 呼叫處理
├── tests/
│   ├── __init__.py
│   ├── test_conversation_manager.py
│   ├── test_trigger_filter.py
│   └── test_end_to_end.py
├── .env                       # 環境變數配置
├── requirements.txt           # 依賴套件
├── pytest.ini                 # pytest 配置
└── README.md                  # 本檔案
```

## 設計原則

1. **簡潔而雅致**: 代碼簡潔易讀，避免過度複雜
2. **文言文註解**: 所有註解使用文言文，保持古雅風格
3. **函數式設計**: 核心邏輯以函數形式實現，易於測試
4. **環境變數配置**: 使用 `.env` 檔案管理敏感資訊
5. **錯誤處理**: 妥善處理各類異常情況

## 錯誤處理

系統妥善處理以下情況：

### API 呼叫失敗
- Perplexity 失敗時返回友善錯誤訊息
- Gemini 失敗時返回友善錯誤訊息
- 設置 30 秒超時機制

### 環境變數缺失
- 啟動時檢查所有必需環境變數
- 若缺失則記錄錯誤並終止程式

### 訊息解析錯誤
- 若關鍵字提取失敗，返回提示訊息

## 正確性保證

系統通過屬性測試驗證以下特性：

- 對話歷史之一致性
- 關鍵字偵測之準確性
- API 回應之有效性
- 使用者隔離之完整性
- 錯誤處理之穩定性

所有 28 項測試均已通過，確保系統之正確性。

## 貢獻指南

歡迎提交 Issue 與 Pull Request。請確保：

1. 所有測試通過
2. 代碼遵循既有風格
3. 新功能包含相應測試
4. 註解使用文言文

## 授權

本專案採用 MIT 授權。詳見 LICENSE 檔案。

## 聯絡方式

如有任何問題或建議，歡迎提出 Issue。

---

*此乃一個簡潔而雅致之聊天機器人系統，願為諸君提供便利之服務。*
