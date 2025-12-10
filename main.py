import os
import requests
import json
import asyncio

# --- НАСТРОЙКИ ---
# Берем секреты из GitHub
telegram_token = os.environ.get("TG_TOKEN")
chat_id = os.environ.get("TG_ID")
tiktok_user = "zveroboypeace"
# -----------------

def check_and_notify():
    # Специальная ссылка, через которую приложение проверяет статус
    url = f"https://www.tiktok.com/api-live/user/room/?aid=1988&uniqueId={tiktok_user}&sourceType=54"
    
    # Притворяемся браузером Chrome, чтобы ТикТок нас пустил
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
    }

    try:
        print(f"🔍 Проверяю статус {tiktok_user}...")
        response = requests.get(url, headers=headers, timeout=10)
        
        # Если ТикТок ответил
        if response.status_code == 200:
            data = response.json()
            
            # Ищем информацию о стриме внутри ответа
            # Обычно status 2 или 4 означает LIVE
            live_room = data.get('data', {}).get('liveRoom', {})
            status = live_room.get('status')
            
            print(f"Статус стрима (код): {status}")

            if status == 2 or status == 4:
                title = live_room.get('title', 'Без названия')
                cover = live_room.get('coverUrl', '')
                
                msg = (f"🚨 <b>{tiktok_user} В ЭФИРЕ!</b>\n"
                       f"📝 Описание: {title}\n"
                       f"👉 <a href='https://www.tiktok.com/@{tiktok_user}/live'>СМОТРЕТЬ СТРИМ</a>")
                
                # Отправляем сообщение в Телеграм
                tg_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
                payload = {
                    "chat_id": chat_id, 
                    "text": msg, 
                    "parse_mode": "HTML"
                }
                requests.post(tg_url, data=payload)
                print("✅ Уведомление отправлено в Telegram!")
            else:
                print("❌ Стрима сейчас нет.")
        else:
            print(f"Ошибка доступа к ТикТок: {response.status_code}")

    except Exception as e:
        print(f"Произошла ошибка в скрипте: {e}")

if __name__ == "__main__":
    check_and_notify()
