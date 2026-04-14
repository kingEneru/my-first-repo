import os
import json
import requests
from datetime import datetime, timedelta
from supabase import create_client, Client

MESSAGE_TOKEN = os.environ.get("MESSAGE_TOKEN", '')
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://myapp.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'anno_key') # anno key
FRIENDS_TOKEN = os.environ.get('FRIENDS_TOKEN', '') # 如果需要发给多个人,用逗号分隔.

def send_wechat_notification(message_title, content, to: str = ''):
    if not MESSAGE_TOKEN:
        print('ERROR! 没有获取到message token!')
    payload = {
        "to": to, # 需要填写好友令牌，不填 则发给自己
        "token": MESSAGE_TOKEN,
        "title": message_title,
        "content": content,
        "template": "html",
        "channel": "wechat",
    }
    headers = {
       'Content-Type': 'application/json'
    }
    res = requests.post("https://www.pushplus.plus/api/send", data=json.dumps(payload), headers=headers)
    if res.status_code == 200 and res.json().get('code', 0) == 200:
        print("✅ 已发送微信通知")
    else:
        print(f'❌ 微信通知发送失败: {res.text}')

class NotificationDB:
    def __init__(self):
        self.supabase: Client = create_client(
            SUPABASE_URL,
            SUPABASE_KEY
        )
        # table = 'wechat_notification_records' or 'download_records'
    def has_notification_today(self, date_str: str) -> bool:
        """检查今天是否已发送通知"""
        result = self.supabase.table('wechat_notification_records') \
            .select("*") \
            .eq('date', date_str) \
            .execute()
        return len(result.data) > 0

    def add_notification(self, date_str: str, time_str: str, content: str):
        """添加通知记录"""
        data = {
            'date': date_str,
            'time': time_str,
            'content': content
        }
        result = self.supabase.table('wechat_notification_records').insert(data).execute()
        return result.data

    def delete_notification(self, date_str: str):
        """删除通知记录"""
        result = self.supabase.table('wechat_notification_records') \
            .delete() \
            .eq('date', date_str) \
            .execute()
        return result.data

    def process_notification(self, current_date_str: str, current_time_str: str, content: str = '淘宝下单纸巾'):
        """处理通知逻辑"""
        if not self.has_notification_today(current_date_str):
            self.add_notification(current_date_str, current_time_str, content)
            send_wechat_notification(message_title='淘宝下单纸巾',content='第一单20-23点，第二单任意时间，第三单11点之前')
            print(f"✅ 已发送通知: {content}")
            # 如果确实需要立即删除，取消下面的注释
            # self.delete_notification(current_date_str)
            # print("📝 已删除通知记录")
            return True
        else:
            print(f"⏭️ 今天已发送过下单通知，跳过")
            return False

if __name__ == '__main__':
    db = NotificationDB()

    utc_now = datetime.utcnow()
    beijing_time = utc_now + timedelta(hours=8)

    today = beijing_time.weekday()
    current_date_str = beijing_time.strftime("%Y-%m-%d")
    current_time_str = beijing_time.strftime("%H:%M:%S")

    if current_time_str > '20:01:00':
        db.process_notification(current_date_str, current_time_str, '淘宝下单纸巾')
