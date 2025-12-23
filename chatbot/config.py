"""
環境變數配置與驗證
此乃系統啟動之門，驗證祕鑰之有無
"""

import logging
import os
import sys

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def load_environment_variables() -> dict:
    """
    載入並驗證環境變數
    
    返回：
        包含所有必需環境變數的字典
    
    異常：
        SystemExit: 若缺失必需環境變數
    """
    # 載入 .env 檔案（若尚未載入）
    load_dotenv(override=False)

    # 必需的環境變數
    required_vars = {
        'GEMINI_API_KEY': 'Gemini 祕鑰',
        'PERPLEXITY_API_KEY': 'Perplexity 祕鑰',
    }

    # 驗證環境變數
    config = {}
    missing_vars = []

    for var_name, var_description in required_vars.items():
        value = os.environ.get(var_name)
        if not value:
            missing_vars.append(f"{var_name} ({var_description})")
        else:
            config[var_name] = value

    # 若缺失環境變數，記錄錯誤並終止
    if missing_vars:
        error_message = f"缺失必需環境變數:\n" + "\n".join(missing_vars)
        logger.error(error_message)
        sys.exit(1)

    return config
