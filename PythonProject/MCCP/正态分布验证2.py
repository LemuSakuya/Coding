#正态分布验证.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from tabulate import tabulate

data = {
    "专家": ["专家1号", "专家2号", "专家3号", "专家4号", "专家5号", "专家6号", "专家7号", "专家8号", "专家9号", "专家10号",
            "专家12号", "专家13号", "专家14号", "专家15号", "专家16号", "专家17号", "专家18号", "专家19号", "专家20号"],
    "ICC值": [0.474, 0.530, 0.594, 0.513, 0.449, 0.528, 0.541, 0.521, 0.557, 0.494,
             0.525, 0.488, 0.528, 0.427, 0.453, 0.436, 0.451, 0.461, 0.408],
    "Z评分": [2.479, 2.230, 1.591, 2.052, 2.011, 2.339, 2.228, 2.293, 2.628, 1.998,
            2.343, 2.027, 2.422, 2.588, 2.387, 2.095, 2.496, 1.651, 2.033]
}
df = pd.DataFrame(data)

def normality_test(data, name):
    shapiro_stat, shapiro_p = stats.shapiro(data)
    ks_stat, ks_p = stats.kstest(data, 'norm', args=(np.mean(data), np.std(data)))
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    stats.probplot(data, dist="norm", plot=plt)
    plt.title(f'{name} Liner Distribution')
    
    plt.subplot(1, 2, 2)
    plt.hist(data, bins=8, density=True, alpha=0.6, color='g')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = stats.norm.pdf(x, np.mean(data), np.std(data))
    plt.plot(x, p, 'k', linewidth=2)
    plt.title(f'{name} normal Distribution')
    
    plt.tight_layout()
    plt.show()
    
    return {
        '检验方法': ['Shapiro-Wilk', 'Kolmogorov-Smirnov'],
        '统计量': [shapiro_stat, ks_stat],
        'p值': [shapiro_p, ks_p],
        '正态性结论': [
            '服从正态分布' if shapiro_p > 0.05 else '不服从正态分布',
            '服从正态分布' if ks_p > 0.05 else '不服从正态分布'
        ]
    }

icc_test = normality_test(df['ICC值'], 'ICC值')
z_test = normality_test(df['Z评分'], 'Z评分')

print("ICC值正态性检验结果:")
print(tabulate(icc_test, headers="keys", tablefmt="grid", showindex=False))

print("\nZ评分正态性检验结果:")
print(tabulate(z_test, headers="keys", tablefmt="grid", showindex=False))

print("\n描述性统计:")
print(df[['ICC值', 'Z评分']].describe().round(3))