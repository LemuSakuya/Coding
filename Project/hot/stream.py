import pandas as pd
import os

data_folder = r'E:\VSCode\Coding\Project\hot\附件'
all_cities = os.listdir(data_folder)

max_score = 0
bs_attractions = []
city_bs_counts = {}

for city_file in all_cities:
    try:
        city_name = city_file.split('.')[0]
        df = pd.read_csv(os.path.join(data_folder, city_file), encoding='utf-8')
        
        # 确保评分列是数值类型
        df['评分'] = pd.to_numeric(df['评分'], errors='coerce')
        
        # 移除NaN值
        df = df.dropna(subset=['评分'])
        
        current_max = df['评分'].max()
        
        if current_max > max_score:
            max_score = current_max
            bs_attractions = df[df['评分'] == max_score]['名字'].tolist()
        elif current_max == max_score:
            bs_attractions.extend(df[df['评分'] == max_score]['名字'].tolist())
        
        city_bs_count = len(df[df['评分'] == max_score])
        city_bs_counts[city_name] = city_bs_count
        
    except Exception as e:
        print(f"处理文件{city_file}时出错:", str(e))
        continue

# 输出结果
print(f"全国景点最高评分(BS)是: {max_score}")
print(f"全国获得最高评分(BS)的景点数量: {len(bs_attractions)}")
print("拥有最高评分(BS)景点最多的前10个城市:")
top_10 = sorted(city_bs_counts.items(), key=lambda x: x[1], reverse=True)[:10]
for i, (city, count) in enumerate(top_10, 1):
    print(f"{i}. {city}: {count}个")