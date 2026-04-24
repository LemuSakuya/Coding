import requests
from datetime import datetime

def get_repo_creation_date(username):
    url = f"https://api.github.com/users/{username}/repos?sort=created&direction=asc&per_page=1"
    response = requests.get(url)
    if response.ok:
        repo = response.json()[0]
        created_at = repo["created_at"]
        print(f"最早仓库创建时间: {created_at}")
        # 注册时间通常早于或等于此时间
    else:
        print("无法获取数据，请检查用户名是否正确")

# 示例使用（替换为你的GitHub用户名）
get_repo_creation_date("LemuSakuya")