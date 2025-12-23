"""
聊天機器人 - 以文言文風格實現
此乃一個簡潔之對話系統，藉 Gemini 模型與用戶往來
"""

from dotenv import dotenv_values
from google import genai
from google.genai import types

# 初始化配置
config = dotenv_values()
GOOGLE_API_KEY = config.get("GOOGLE_API_KEY")  # 祕鑰
client = genai.Client(api_key=GOOGLE_API_KEY)  # 客戶端
MODEL_ID = "gemini-2.5-flash"  # 模型名

# 對話狀態
chat_log = []  # 對話錄
backtrace = 2  # 回溯數


def ask(sys_msg, user_msg):
    """
    問答之門，承前啟後
    
    參數：
        sys_msg: 系統角色設定
        user_msg: 用戶提問
    
    返回：
        AI 之回應
    """
    global chat_log
    
    # 建對話
    chat = client.chats.create(
        model=MODEL_ID,
        history=chat_log,
        config=types.GenerateContentConfig(
            system_instruction=f'你是{sys_msg}',
        )
    )
    
    # 問以辭
    response = chat.send_message(user_msg)
    
    # 更新對話錄
    chat_log = chat.get_history()[-2 * backtrace:]
    
    return response


def main():
    """主程序 - 循問答，至無言止"""
    sys_msg = '繁體中文小助理'  # 預設角色
    print(f'AI 角色設定為: {sys_msg}\n')
    
    try:
        while True:
            msg = input('[汝曰]:')
            if not msg.strip():
                break
            
            reply = ask(sys_msg, msg)
            print(f'[{sys_msg}]: {reply.text}\n')
        
        # 顯示使用元數據
        if 'reply' in locals():
            print(f'使用元數據: {reply.usage_metadata}')
    
    except KeyboardInterrupt:
        print('\n對話已終止。')


if __name__ == '__main__':
    main()
