import os
import requests
import json
import asyncio

# --- НАСТРОЙКИ ---
telegram_token = os.environ.get("TG_TOKEN")
chat_id = os.environ.get("TG_ID")
tiktok_user = "zveroboypeace"
# -----------------

def check_and_notify():
    # Ссылка API
    url = f"https://www.tiktok.com/api-live/user/room/?aid=1988&uniqueId={tiktok_user}&sourceType=54"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
    }

    try:
        print(f"🔍 Проверяю статус {tiktok_user}...")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            live_room = data.get('data', {}).get('liveRoom', {})
            
            # --- ГЛАВНОЕ ИЗМЕНЕНИЕ ТУТ ---
            status = live_room.get('status')
            print(f"Текущий статус API: {status}") # Пишем в лог для проверки

            # Реагируем ТОЛЬКО на статус 2 (LIVE)
            # И дополнительно проверяем, что статус вообще пришел (не None)
            if status == 2:
                title = live_room.get('title', 'Стрим без названия')
                stats = live_room.get('stats', {})
                viewers = stats.get('userCount', 'неизвестно')
                
                msg = (f"🚨 <b>{tiktok_user} В ЭФИРЕ!</b>\n"
                       f"👀 Зрителей: {viewers}\n"
                       f"📝 Тема: {title}\n"
                       f"👉 <a href='https://www.tiktok.com/@{tiktok_user}/live'>СМОТРЕТЬ СТРИМ</a>")
                
                # Отправляем
                tg_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
                payload = {
                    "chat_id": chat_id, 
                    "text": msg, 
                    "parse_mode": "HTML"
                }
                requests.post(tg_url, data=payload)
                print("✅ Уведомление отправлено!")
            
            elif status == 4:
                print("⚠️ Стрим недавно закончился (Статус 4). Игнорирую.")
            else:
                print("❌ Стрима нет.")
        else:
            print(f"Ошибка доступа к ТикТок: {response.status_code}")

    except Exception as e:
        print(f"Ошибка скрипта: {e}")

if __name__ == "__main__":
    check_and_notify()
