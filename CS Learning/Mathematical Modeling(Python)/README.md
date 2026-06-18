# Python 数学建模算法与应用学习讲义

> 针对《Python数学建模算法与应用》（国防工业出版社）部分章节主题整理的原创学习笔记。
> 内容覆盖原理讲解、公式推导、建模步骤、Python 代码实现、考试题型和复习题。

## 覆盖章节

| 教材章节 | 本讲义文件 | 主题 |
|----------|------------|------|
| 第 3 章 | [03_线性代数模型.md](chapters/03_线性代数模型.md) | 线性代数模型 |
| 第 4 章 | [04_线性规划与整数规划.md](chapters/04_线性规划与整数规划.md) | 线性规划与整数规划 |
| 第 5 章 | [05_非线性规划与多目标规划.md](chapters/05_非线性规划与多目标规划.md) | 非线性规划与多目标规划 |
| 第 6 章 | [06_图论模型.md](chapters/06_图论模型.md) | 图论模型 |
| 第 7 章 | [07_插值与拟合.md](chapters/07_插值与拟合.md) | 插值与拟合 |
| 第 10 章 | [10_回归分析.md](chapters/10_回归分析.md) | 回归分析 |
| 第 11 章 | [11_聚类分析与判别分析.md](chapters/11_聚类分析与判别分析.md) | 聚类分析与判别分析 |
| 第 13 章 | [13_偏最小二乘回归分析.md](chapters/13_偏最小二乘回归分析.md) | 偏最小二乘回归分析 |
| 第 14 章 | [14_综合评价方法.md](chapters/14_综合评价方法.md) | 综合评价方法 |
| 第 15 章 | [15_预测方法.md](chapters/15_预测方法.md) | 预测方法 |

## 目录结构

```text
Mathematical Modeling(Python)/
├── README.md
├── chapters/
│   ├── 03_线性代数模型.md
│   ├── 04_线性规划与整数规划.md
│   ├── 05_非线性规划与多目标规划.md
│   ├── 06_图论模型.md
│   ├── 07_插值与拟合.md
│   ├── 10_回归分析.md
│   ├── 11_聚类分析与判别分析.md
│   ├── 13_偏最小二乘回归分析.md
│   ├── 14_综合评价方法.md
│   ├── 15_预测方法.md
├── examples/
│   ├── 03_linear_algebra.py
│   ├── 04_linear_programming.py
│   ├── 05_nonlinear_programming.py
│   ├── 06_graph.py
│   ├── 07_interpolation_fitting.py
│   ├── 10_regression.py
│   ├── 11_cluster_discriminant.py
│   ├── 13_pls.py
│   ├── 14_evaluation.py
│   ├── 15_forecasting.py
└── tools/
    └── generate_modeling_notes.mjs
```

## 推荐学习顺序

1. 先学第 3 章线性代数模型，建立矩阵思维。
2. 再学第 4、5、6 章，掌握优化模型和图论模型。
3. 接着学第 7、10、11、13 章，处理数据拟合、回归、分类和降维。
4. 最后学第 14、15 章，完成综合评价和预测类建模题。

## Python 环境建议

```bash
pip install numpy scipy pandas matplotlib scikit-learn statsmodels networkx
```

## 使用方式

- 先读对应章节 Markdown。
- 考前优先看每章的“考试复习总览”“典型题型与解题套路”“考前最后检查表”。
- 再运行 `examples/` 中的同章 Python 文件。
- 最后把模板替换成自己的数据，补上结果解释和敏感性分析。
