"""
聊天機器人主程式
此乃系統之啟動門戶，驗證祕鑰之有無
"""

import logging
import sys

from chatbot import (
    load_environment_variables,
    ChatBot,
    ConversationManager,
    APIHandler,
)

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    主程式入口點
    驗證環境變數，初始化系統
    """
    try:
        # 驗證環境變數
        logger.info("驗證環境變數中...")
        config = load_environment_variables()
        logger.info("環境變數驗證成功")

        # 初始化各元件
        logger.info("初始化系統元件中...")
        api_handler = APIHandler(
            gemini_key=config['GEMINI_API_KEY'],
            perplexity_key=config['PERPLEXITY_API_KEY']
        )
        conversation_manager = ConversationManager()
        chatbot = ChatBot(api_handler, conversation_manager)
        logger.info("系統初始化完成")

        # 簡單之互動迴圈
        logger.info("聊天機器人已啟動，請輸入訊息（輸入 'quit' 以退出）")
        user_id = "default_user"

        while True:
            try:
                user_input = input("\n[汝曰]: ").strip()
                if not user_input:
                    continue
                if user_input.lower() == 'quit':
                    logger.info("使用者要求退出")
                    break

                # 處理訊息
                response = chatbot.process_message(user_id, user_input)
                print(f"[機器人]: {response}")

            except KeyboardInterrupt:
                logger.info("使用者中斷程式")
                break
            except Exception as e:
                logger.error(f"處理訊息時出錯: {e}")
                print("抱歉，處理您的訊息時出現錯誤。請稍後再試。")

    except SystemExit as e:
        # 環境變數驗證失敗，已由 load_environment_variables() 記錄錯誤並終止
        logger.error("應用程式因環境變數驗證失敗而終止")
        sys.exit(e.code)
    except Exception as e:
        logger.error(f"應用程式啟動失敗: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
