import os
import time
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json

# 1. 代理管理（简化版）
class SimpleProxyManager:
    def __init__(self):
        self.proxies = []
        
    def get_proxy(self):
        """如果没有代理则直连"""
        return random.choice(self.proxies) if self.proxies else None

# 2. 城市列表（确保有ID列）
city_data = [
    {'城市': '北京', 'ID': '101010100', '区域': '华北'},
    {'城市': '上海', 'ID': '101020100', '区域': '华东'},
    {'城市': '广州', 'ID': '101280101', '区域': '华南'},
    {'城市': '深圳', 'ID': '101280601', '区域': '华南'}
]
city_df = pd.DataFrame(city_data)

# 3. 核心爬取函数
def get_weather(city_id):
    """获取单个城市天气"""
    url = f"http://www.weather.com.cn/weather40dn/{city_id}.shtml"
    try:
        res = requests.get(
            url,
            headers={'User-Agent': UserAgent().random},
            timeout=10
        )
        soup = BeautifulSoup(res.text, 'html.parser')
        table = soup.find('table', class_='history-table')
        
        data = []
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) >= 4:
                data.append({
                    '日期': cols[0].text.strip(),
                    '最高温': cols[1].text.replace('℃', '').strip(),
                    '最低温': cols[2].text.replace('℃', '').strip(),
                    '天气': cols[3].text.strip(),
                    '城市ID': city_id
                })
        return pd.DataFrame(data)
    except Exception as e:
        print(f"获取{city_id}失败:", str(e))
        return None

# 4. 主流程
def main():
    # 确保有ID列
    if 'ID' not in city_df.columns:
        raise ValueError("城市列表缺少ID列！")
    
    valid_cities = city_df[city_df['ID'].notna()]['ID'].tolist()
    print(f"准备爬取{len(valid_cities)}个城市")
    
    all_data = []
    for city_id in valid_cities[:3]:  # 测试前3个
        df = get_weather(city_id)
        if df is not None:
            all_data.append(df)
        time.sleep(random.uniform(2, 5))  # 控制频率
    
    if all_data:
        result = pd.concat(all_data)
        result.to_excel('weather_result.xlsx', index=False)
        print(f"成功获取{len(result)}条数据")
    else:
        print("未获取到有效数据")

if __name__ == '__main__':
    main()