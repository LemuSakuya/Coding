import requests
from bs4 import BeautifulSoup

def extract_subtitle_from_html(bvid):
    url = f"https://www.bilibili.com/video/BV1bJ411y7Fm"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 查找字幕JSON链接（可能需要调整选择器）
    script_tags = soup.find_all("script")
    for script in script_tags:
        if "subtitle_url" in script.text:
            subtitle_url = script.text.split('"subtitle_url":"')[1].split('"')[0]
            subtitle_url = "https:" + subtitle_url.replace("\\/", "/")
            subtitle_data = requests.get(subtitle_url).json()
            # 转换为SRT（同方法1）
            return subtitle_data
    return None