import os
import json
import requests
from datetime import datetime, timezone, timedelta

def send_line_message():
    # 1. ดึงค่าจาก Secrets
    LINE_ACCESS_TOKEN = os.environ.get('LINE_ACCESS_TOKEN')
    LINE_USER_ID = os.environ.get('LINE_USER_ID')

    if not LINE_ACCESS_TOKEN or not LINE_USER_ID:
        print("Error: Missing LINE_ACCESS_TOKEN or LINE_USER_ID")
        return

    # 2. คำนวณวันปัจจุบันตามเวลาประเทศไทย (UTC+7)
    tz_thai = timezone(timedelta(hours=7))
    now_thai = datetime.now(tz_thai)
    day_name = now_thai.strftime('%A') # ได้ชื่อวัน เช่น Monday, Tuesday...

    # แปลงชื่อวันเป็นภาษาไทยสำหรับแสดงผล
    days_th = {
        'Monday': 'วันจันทร์',
        'Tuesday': 'วันอังคาร',
        'Wednesday': 'วันพุธ',
        'Thursday': 'วันพฤหัสบดี',
        'Friday': 'วันศุกร์',
        'Saturday': 'วันเสาร์',
        'Sunday': 'วันอาทิตย์'
    }
    today_th = days_th.get(day_name, day_name)

    # 3. อ่านข้อความแต่งกายจากไฟล์ outfit.json
    outfit_today = "ชุดนักเรียน" # ค่าเริ่มต้นกรณีอ่านไฟล์ไม่ได้
    try:
        with open('outfit.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            schedule = data.get('schedule', {})
            outfit_today = schedule.get(day_name, "ชุดนักเรียน")
    except Exception as e:
        print(f"Error reading outfit.json: {e}")

    # 4. สร้างข้อความแจ้งเตือน
    msg_text = f"👕 แจ้งเตือนการแต่งกายประจำวัน\n({today_th} / {day_name.upper()}):\n\n• วันนี้แต่งกาย: {outfit_today}"

    # 5. ส่งข้อความผ่าน Messaging API
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
    }
    payload = {
        'to': LINE_USER_ID,
        'messages': [
            {
                'type': 'text',
                'text': msg_text
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.status_code}, {response.text}")

if __name__ == '__main__':
    send_line_message()
