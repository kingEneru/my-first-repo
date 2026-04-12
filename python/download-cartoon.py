import os
import re
import json
import sys

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from supabase import create_client, Client

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
}

MESSAGE_TOKEN = os.environ.get("MESSAGE_TOKEN", '')
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://myapp.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'anno_key') # anno key

def get_WanMei_Link(result):
    print('正在获取完美世界 最新集下载链接..')
    url = 'https://www.i6v.tv/donghuapian/15719.html'
    print(f'完美世界 下载链接: {url}')
    # Step 1: 获取网页内容并确保编码正确
    resp = requests.get(url, headers=headers, timeout=10)
    resp.encoding = resp.apparent_encoding  # 自动识别编码
    html = resp.text

    # Step 2: 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html, "html.parser")

    # Step 3: 查找所有磁力链接（magnet:? 开头）
    links = soup.find_all("a", href=re.compile(r"^magnet:\?"))

    episodes = []

    for a in links:
        # 找到上层文字（磁力所在行的文本）
        text = a.text.strip()
        href = a["href"].strip()

        # 过滤掉空链接，并且只保留第5季的磁力链接
        if not text or not href or "国语中字无水印" not in text:
            continue

        episodes.append((text, href))
    if episodes:
        latest_1080p = episodes[-2]
        latest_2160p = episodes[-1]
        resource = [
            {
                'title': latest_1080p[0],
                'magnet': latest_1080p[1]
            },
            {
                'title': latest_2160p[0],
                'magnet': latest_2160p[1]
            }
        ]
        result['resources'].extend(resource)
        result['cartoon_name'] = '完美世界'
        # print(f'检测到完美世界 最新集: {latest_1080p[0]}\n磁力链接获取成功:\n{latest_1080p[1]}')
    return result

def get_DouPo_Link(result):
    print('正在获取斗破苍穹 最新集下载链接..')
    url = "https://www.i6v.tv/donghuapian/17003.html"
    print(f'斗破苍穹 下载链接: {url}')
    # Step 1: 获取网页内容并确保编码正确
    resp = requests.get(url, headers=headers, timeout=10)
    resp.encoding = resp.apparent_encoding  # 自动识别编码
    html = resp.text

    # Step 2: 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html, "html.parser")

    # Step 3: 查找所有磁力链接（magnet:? 开头）
    links = soup.find_all("a", href=re.compile(r"^magnet:\?"))

    episodes = []

    for a in links:
        # 找到上层文字（磁力所在行的文本）
        text = a.text.strip()
        href = a["href"].strip()

        # 过滤掉空链接，并且只保留第5季的磁力链接
        if not text or not href or "斗破苍穹 第5季" not in text:
            continue

        episodes.append((text, href))

    # Step 4: 从剧集名字中提取“第XXX集”序号，以便排序找到最新一集
    def get_episode_number(name):
        match = re.search(r"第(\d+)[集季]", name)
        if match:
            return int(match.group(1))
        return -1

    episodes.sort(key=lambda x: get_episode_number(x[0]), reverse=True)
    length = len(episodes)
    for index in range(length):
        title = episodes[index][0]
        if '4k' in title:
            latest_1080p = episodes[index-1]
            resource = [
                {
                    'title': latest_1080p[0],
                    'magnet': latest_1080p[1]
                }
            ]
            result['resources'].extend(resource)
            result['cartoon_name'] = '斗破苍穹·年番'
            # print(f'检测到斗破苍穹 最新集: {latest_1080p[0]}\n磁力链接获取成功:\n{latest_1080p[1]}')
            break
    return result

def get_DouLuo_Link(result):
    print('正在获取斗罗大陆·绝世唐门 最新集下载链接..')
    url = 'https://www.i6v.tv/donghuapian/21341.html'
    print(f'斗罗大陆·绝世唐门 下载链接: {url}')
    # Step 1: 获取网页内容并确保编码正确
    resp = requests.get(url, headers=headers, timeout=10)
    resp.encoding = resp.apparent_encoding  # 自动识别编码
    html = resp.text

    # Step 2: 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html, "html.parser")

    # Step 3: 查找所有磁力链接（magnet:? 开头）
    links = soup.find_all("a", href=re.compile(r"^magnet:\?"))

    episodes = []

    for a in links:
        # 找到上层文字（磁力所在行的文本）
        text = a.text.strip()
        href = a["href"].strip()

        # 过滤掉空链接，并且只保留第5季的磁力链接
        if not text or not href or "国语中字无水印" not in text:
            continue
        episodes.append((text, href))
    if episodes:
        latest_1080p = episodes[-2]
        latest_2160p = episodes[-1]
        resource = [
            {
                'title': latest_1080p[0],
                'magnet': latest_1080p[1]
            },
            {
                'title': latest_2160p[0],
                'magnet': latest_2160p[1]
            }
        ]
        result['resources'].extend(resource)
        result['cartoon_name'] = '斗罗大陆·绝世唐门'
        # print(f'检测到斗罗大陆 绝世唐门 最新集: {latest_1080p[0]}\n磁力链接获取成功:\n{latest_1080p[1]}')
    return  result

def get_TunShi_Link(result):
    print('正在获取吞噬星空 最新集下载链接..')
    url = 'https://www.i6v.tv/donghuapian/14764.html'
    print(f'吞噬星空 下载链接: {url}')
    # Step 1: 获取网页内容并确保编码正确
    resp = requests.get(url, headers=headers, timeout=10)
    resp.encoding = resp.apparent_encoding  # 自动识别编码
    html = resp.text

    # Step 2: 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html, "html.parser")

    # Step 3: 查找所有磁力链接（magnet:? 开头）
    links = soup.find_all("a", href=re.compile(r"^magnet:\?"))

    episodes = []

    for a in links:
        # 找到上层文字（磁力所在行的文本）
        text = a.text.strip()
        href = a["href"].strip()

        # 过滤掉空链接，并且只保留第5季的磁力链接
        if not text or not href or "国语中字无水印" not in text:
            continue

        episodes.append((text, href))
    if episodes:
        latest_1080p = episodes[-2]
        latest_2160p = episodes[-1]
        resource = [
            {
                'title': latest_1080p[0],
                'magnet': latest_1080p[1]
            },
            {
                'title': latest_2160p[0],
                'magnet': latest_2160p[1]
            }
        ]
        result['resources'].extend(resource)
        result['cartoon_name'] = "吞噬星空"
        # result['message'] = latest_1080p[0]
        # result['magnet'] = latest_1080p[1]
        # print(f'检测到吞噬星空 最新集: {latest_1080p[0]}\n磁力链接获取成功:\n{latest_1080p[1]}')
    return result


def send_wechat_notification(message_title, content):
    if not MESSAGE_TOKEN:
        print('ERROR! 没有获取到message token!')
    payload = {
        "token": MESSAGE_TOKEN,
        "title": message_title,
        "content": content,
        # "topic": "code", 消息将会发送给加入群组编码为code的成员
        "template": "html"
    }
    headers = {
       'Content-Type': 'application/json'
    }
    res = requests.post("https://www.pushplus.plus/send", data=json.dumps(payload), headers=headers)
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
    # ----------------------------------
    # 下载动漫处理逻辑
    def process_cartoon(self, title:str , magnet:str, jishu: int, message_title:str, content: str):
        if not self.has_already_downloaded(jishu):
            print(f'检测到{title} 最新集: {jishu}\n磁力链接获取成功:\n{magnet}')
            self.download_recording(title, magnet, jishu)
            send_wechat_notification(message_title, content)
            sys.exit() # 处理完毕，直接退出
        else:
            print(f"⏭️ {title}, 第{jishu}集已经下载过了, 继续检测最新链接, 本次跳过。")
            return False

    def has_already_downloaded(self, jishu: int) -> bool:
        """检查这一集是否已下载过"""
        result = self.supabase.table('download_records') \
            .select("*") \
            .eq('jishu', jishu) \
            .execute()
        return len(result.data) > 0

    def download_recording(self, title: str, magnet: str, jishu: int):
        data = {
            'name': title,
            'magnet': magnet,
            'jishu': jishu
        }
        result = self.supabase.table('download_records').insert(data).execute()
        print('下载记录已经写入DB, 成功!')
        return result.data

    # end
    # -----------------------------------
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
    res = {
        'cartoon_name': '',
        'resources': [
            {
                'title': '',
                'magnet': ''
            }
        ]
    }
    db = NotificationDB()

    utc_now = datetime.utcnow()
    beijing_time = utc_now + timedelta(hours=8)

    today = beijing_time.weekday()
    current_date_str = beijing_time.strftime("%Y-%m-%d")
    current_time_str = beijing_time.strftime("%H:%M:%S")
    if current_time_str > '20:01:00':
        db.process_notification(current_date_str, current_time_str, '淘宝下单纸巾')

    if today + 1 == 2 and current_time_str >= '10:30:00':
        # 吞噬星空每周二更新, 10点
        get_TunShi_Link(res)
    elif today + 1 == 5 and current_time_str >= '10:30:00':
        # 完美世界每周五更新, 10点
        get_WanMei_Link(res)
    elif today + 1 == 6 and current_time_str >= '10:30:00':
        # 斗罗大陆每周六更新, 10点
        get_DouLuo_Link(res)
    elif today + 1 == 7 and current_time_str >= '12:30:00':
        # 斗破苍穹每周日更新, 12点
        get_DouPo_Link(res)
    else:
        print(f'当前时间: {datetime.now().strftime("%Y-%m-%d")} [星期{today+1}] {current_time_str}. `吞噬星空, 完美世界, 斗罗大陆, 斗破苍穹` 暂时都没有更新.')

    cartoon_name = res['cartoon_name']
    for resource in res['resources']:
        if resource['title']:
            title = resource['title']
            magnet = resource['magnet']
            if re.search(r"\d+(?=\.1080p)", title):
                match = re.search(r"\d+(?=\.1080p)", title)
            else:
                match = re.search(r"\d+(?=\.2160p)", title)
            jishu = int(match.group(0))
            template = f"""
                <div style="max-width:320px;background:#fff;border-radius:16px;padding:16px;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto;box-shadow:0 2px 8px rgba(0,0,0,0.06);">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <span style="font-weight:700;font-size:16px;">🎬 {cartoon_name}</span>
                <span style="background:#f5b042;padding:2px 10px;border-radius:20px;font-size:12px;font-weight:600;">第148集</span>
              </div>
              <div style="background:#f5f7fa;border-radius:12px;padding:10px;margin-bottom:12px;font-size:12px;color:#666;">
                📺 {title}
              </div>
              <div style="background:#eef2f6;border-radius:12px;padding:10px;">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                  <span style="font-size:11px;color:#2b7a4b;word-break:break-all;flex:1;">{magnet}</span>
                  <button onclick="navigator.clipboard.writeText(this.previousElementSibling.innerText);alert('✅ 磁力链接已复制')" style="background:#fff;border:1px solid #ddd;border-radius:20px;padding:4px 12px;font-size:11px;cursor:pointer;">📋 复制</button>
                </div>
              </div>
            </div>
                """
            db.process_cartoon(title, magnet, jishu, cartoon_name + '（已更新）', template)
