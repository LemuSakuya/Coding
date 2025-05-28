import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel('教师平均分结果.xlsx')

plt.figure(figsize=(15, 8))

x = np.arange(len(df['教师编号']))
width = 0.35

plt.bar(x - width/2, df['平均分'], width, label='Expert Average Score', color='#1f77b4')
plt.bar(x + width/2, df['综合评分'], width, label='Overall Score', color='#ff7f0e')

plt.xlabel('Teacher ID', fontsize=12)
plt.ylabel('Score', fontsize=12)
plt.title('Comparison of Expert Average Score and Overall Score', fontsize=14, pad=20)
plt.xticks(x, df['教师编号'], rotation=90, fontsize=8)
plt.legend()

plt.tight_layout()

plt.savefig('教师评分对比图.png', dpi=300, bbox_inches='tight')
print("双柱状图已保存为 '教师评分对比图.png'")

plt.show()