import os
import json
import requests

def send_line_message():
    line_access_token = os.environ.get('LINE_ACCESS_TOKEN')
    line_user_id = os.environ.get('LINE_USER_ID') # ส่งตรงเข้า User ID หรือ Group ID ก็ได้

    if not line_access_token or not line_user_id:
        print("Error: Missing LINE_ACCESS_TOKEN or LINE_USER_ID")
        return

    # อ่านข้อความจากไฟล์ outfit.json
    try:
        with open('outfit.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            msg_text = data.get('message', 'อย่าลืมแต่งกายไปโรงเรียนวันนี้!')
    except Exception as e:
        print(f"Error reading outfit.json: {e}")
        msg_text = "อย่าลืมตรวจสอบการแต่งกายไปโรงเรียนวันนี้ครับ!"

    # ส่งข้อความผ่าน Messaging API Push Message
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {line_access_token}'
    }
    payload = {
        'to': line_user_id,
        'messages': [
            {
                'type': 'text',
                'text': f"⏰ เตือนแต่งกายไปโรงเรียน (05:30 น.)\n\n{msg_text}"
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
