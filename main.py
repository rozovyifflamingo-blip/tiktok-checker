import asyncio
import os
import requests
from TikTokLive import TikTokLiveClient

# Получаем секретные данные, которые мы спрятали
telegram_token = os.environ.get("TG_TOKEN")
chat_id = os.environ.get("TG_ID")
tiktok_user = "zveroboypeace"  # Ник тиктокера

async def check_stream():
    client = TikTokLiveClient(unique_id=tiktok_user)
    try:
        # Просим ТикТок дать информацию о комнате
        room_info = await client.get_room_info()
        
        # Если статус 2 - значит идет прямой эфир
        if room_info and 'status' in room_info and room_info['status'] == 2:
            print("Стрим идет! Отправляем сообщение.")
            
            message_text = f"🚨 {tiktok_user} НАЧАЛ СТРИМ!\n\nСмотреть тут: https://www.tiktok.com/@{tiktok_user}/live"
            
            # Отправка в Telegram
            url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
            data = {"chat_id": chat_id, "text": message_text}
            requests.post(url, data=data)
            
        else:
            print("Стрима сейчас нет.")
            
    except Exception as e:
        print(f"Ошибка проверки: {e}")

if __name__ == "__main__":
    asyncio.run(check_stream())
