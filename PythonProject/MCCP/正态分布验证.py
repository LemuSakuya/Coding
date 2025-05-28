import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

data = pd.read_excel('Sequential_teacher2.xlsx', sheet_name='Sheet1')

plt.figure(figsize=(10, 6))
sns.histplot(data, kde=True, stat="density", linewidth=0)
plt.title("Histogram with Density Curve")
plt.show()