import os
import re
import json
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
}
message_token = os.environ.get("MESSAGE_TOKEN")

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

def operate_database(sql):
    conn = sqlite3.connect('download-recording.db')
    cursor = conn.cursor()

    # 使用 CREATE TABLE IF NOT EXISTS 避免重复创建表的错误
    create_table_sql = [
        """
        CREATE TABLE IF NOT EXISTS download_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- 设置 id 自动递增
            name TEXT,
            magnet TEXT,
            jishu INTEGER
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS wechat_notification_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- 设置 id 自动递增
            date TEXT,
            time TEXT,
            content TEXT
        );
        """
    ]
    # 创建动漫下载记录表、微信通知发送记录表
    [cursor.execute(sql) for sql in create_table_sql]

    cursor.execute(sql)
    # 提交事务
    conn.commit()
    rows = cursor.fetchall()

    conn.close()
    return rows

def send_wechat_notification(message_title, content):
    if not message_token:
        print('ERROR! 没有获取到message token!')
    payload = {
        "token": message_token,
        "title": message_title,
        "content": content,
        # "topic": "code", 消息将会发送给加入群组编码为code的成员
        "template": "html"
    }
    headers = {
       'Content-Type': 'application/json'
    }
    res = requests.post("https://www.pushplus.plus/send", data=json.dumps(payload), headers=headers)
    print(res.status_code)
    print(res.text)

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
    utc_now = datetime.utcnow()
    beijing_time = utc_now + timedelta(hours=8)

    today = beijing_time.weekday()
    current_date_str = beijing_time.strftime("%Y-%m-%d")
    current_time_str = beijing_time.strftime("%H:%M:%S")
    if current_time_str > '20:01:00':
        if not operate_database(f"select * from wechat_notification_records where date='{current_date_str}'"):
            operate_database(f"INSERT INTO wechat_notification_records (date, time, content) VALUES ('{current_date_str}', '{current_time_str}', '淘宝下单纸巾');")
            send_wechat_notification(message_title='淘宝下单纸巾', content='第一单20-23点，第二单任意时间，第三单11点之前')
            operate_database(f"delete from wechat_notification_records where date='{current_date_str}'")
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
            sql = f"select * from download_records where jishu={jishu}"
            if operate_database(sql):
                print(f"\t{title}, 第{jishu}集已经下载过了, 继续检测最新链接, 本次跳过..")
            else:
                print(f'检测到{title} 最新集: {jishu}\n磁力链接获取成功:\n{magnet}')
                sql = f"INSERT INTO download_records (name, magnet, jishu) VALUES ('{title}', '{magnet}', {jishu});"
                operate_database(sql)
                operate_database(f"INSERT INTO wechat_notification_records (date, time, content) VALUES ('{current_date_str}', '{current_time_str}', '{cartoon_name}（已更新）');")
                send_wechat_notification(message_title=cartoon_name + '（已更新）', content=template)
                print('记录已经写入DB, 成功!')
                break
