import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const root = dirname(here);

const chapters = [
  {
    id: "03",
    file: "03_线性代数模型.md",
    title: "线性代数模型",
    bookTopic: "第 3 章",
    goal: "把矩阵、线性方程组、特征值、最小二乘与 Markov 链转化为可计算的建模工具。",
    keywords: ["矩阵", "线性方程组", "最小二乘", "特征值", "Markov 链", "稳定分布"],
    topics: ["矩阵建模思想", "线性方程组模型", "超定方程与最小二乘", "矩阵分解与数值稳定", "特征值与特征向量", "Markov 链状态转移", "投入产出模型", "PageRank 思想", "敏感性分析", "Python 线性代数工具链"],
    formulas: ["Ax=b", "\\min_x\\lVert Ax-b\\rVert_2^2", "Av=\\lambda v", "\\pi P=\\pi"],
    codeKey: "linear_algebra",
  },
  {
    id: "04",
    file: "04_线性规划与整数规划.md",
    title: "线性规划与整数规划",
    bookTopic: "第 4 章",
    goal: "理解资源分配、生产计划、运输指派等问题如何转化为线性规划和整数规划。",
    keywords: ["线性规划", "整数规划", "0-1 变量", "运输问题", "指派问题", "灵敏度分析"],
    topics: ["线性规划标准形", "可行域与最优解", "单纯形法直觉", "对偶问题", "影子价格", "整数规划建模", "0-1 背包模型", "运输问题", "指派问题", "Python 求解器接口"],
    formulas: ["\\min c^Tx", "Ax\\le b,\\ x\\ge0", "\\max b^Ty,\\ A^Ty\\le c", "x_j\\in\\{0,1\\}"],
    codeKey: "linear_programming",
  },
  {
    id: "05",
    file: "05_非线性规划与多目标规划.md",
    title: "非线性规划与多目标规划",
    bookTopic: "第 5 章",
    goal: "掌握非线性目标、非线性约束、多目标权衡和约束优化的基本建模方式。",
    keywords: ["非线性规划", "KKT", "罚函数", "多目标规划", "Pareto 最优", "SLSQP"],
    topics: ["非线性规划问题定义", "无约束优化", "约束优化", "拉格朗日乘子", "KKT 条件", "罚函数法", "多目标加权法", "理想点法", "Pareto 前沿", "SciPy optimize 实践"],
    formulas: ["\\min f(x)", "g_i(x)\\le0,\\ h_j(x)=0", "\\mathcal{L}(x,\\lambda)=f(x)+\\sum_j\\lambda_jh_j(x)", "\\min\\sum_k w_k f_k(x)"],
    codeKey: "nonlinear_programming",
  },
  {
    id: "06",
    file: "06_图论模型.md",
    title: "图论模型",
    bookTopic: "第 6 章",
    goal: "把路径、网络、匹配、连通性和流量问题抽象成图并用算法求解。",
    keywords: ["图", "最短路", "最小生成树", "最大流", "匹配", "网络优化"],
    topics: ["图的基本概念", "邻接矩阵与邻接表", "最短路径", "最小生成树", "拓扑排序", "二分图匹配", "最大流最小割", "旅行商问题启发式", "复杂网络指标", "NetworkX 建模"],
    formulas: ["G=(V,E)", "d(v)=\\min_{(u,v)\\in E} d(u)+w(u,v)", "\\min\\sum_{e\\in T}w_e", "\\max |f|"],
    codeKey: "graph",
  },
  {
    id: "07",
    file: "07_插值与拟合.md",
    title: "插值与拟合",
    bookTopic: "第 7 章",
    goal: "区分插值、拟合与回归，掌握从离散观测恢复函数关系的常见方法。",
    keywords: ["插值", "拟合", "最小二乘", "样条", "多项式", "曲线拟合"],
    topics: ["插值与拟合的区别", "Lagrange 插值", "Newton 插值", "分段线性插值", "三次样条插值", "多项式拟合", "非线性曲线拟合", "过拟合与欠拟合", "残差分析", "SciPy interpolate 与 curve_fit"],
    formulas: ["p(x_i)=y_i", "L(x)=\\sum_i y_i l_i(x)", "\\min_\\theta\\sum_i(y_i-f(x_i;\\theta))^2", "S_i''(x_{i+1})=S_{i+1}''(x_{i+1})"],
    codeKey: "interpolation_fitting",
  },
  {
    id: "10",
    file: "10_回归分析.md",
    title: "回归分析",
    bookTopic: "第 10 章",
    goal: "系统理解一元、多元、逐步、岭回归和 Logistic 回归的建模与诊断。",
    keywords: ["线性回归", "多元回归", "逐步回归", "岭回归", "Logistic 回归", "显著性检验"],
    topics: ["回归问题定义", "一元线性回归", "多元线性回归", "最小二乘估计", "参数显著性检验", "模型整体 F 检验", "多重共线性", "逐步回归", "岭回归", "Logistic 回归"],
    formulas: ["y=X\\beta+\\varepsilon", "\\hat{\\beta}=(X^TX)^{-1}X^Ty", "R^2=1-\\frac{SSE}{SST}", "\\log\\frac{p}{1-p}=\\beta_0+\\beta^Tx"],
    codeKey: "regression",
  },
  {
    id: "11",
    file: "11_聚类分析与判别分析.md",
    title: "聚类分析与判别分析",
    bookTopic: "第 11 章",
    goal: "掌握无监督分组与有监督分类判别的原理、距离度量和评价方法。",
    keywords: ["KMeans", "层次聚类", "DBSCAN", "判别分析", "LDA", "分类评价"],
    topics: ["距离与相似度", "数据标准化", "KMeans 聚类", "层次聚类", "DBSCAN 密度聚类", "聚类数选择", "轮廓系数", "Fisher 判别", "线性判别分析", "分类混淆矩阵"],
    formulas: ["J=\\sum_i\\lVert x_i-\\mu_{c_i}\\rVert^2", "s(i)=\\frac{b(i)-a(i)}{\\max(a(i),b(i))}", "w\\propto S_w^{-1}(m_1-m_2)", "\\hat{y}=\\arg\\max_k P(y=k|x)"],
    codeKey: "cluster_discriminant",
  },
  {
    id: "13",
    file: "13_偏最小二乘回归分析.md",
    title: "偏最小二乘回归分析",
    bookTopic: "第 13 章",
    goal: "理解 PLS 如何在自变量强相关、样本较少时提取同时解释 X 与 Y 的潜变量。",
    keywords: ["PLS", "潜变量", "主成分", "协方差最大化", "多重共线性", "交叉验证"],
    topics: ["PLS 的问题背景", "与 PCA 的区别", "与普通最小二乘的区别", "潜变量提取", "协方差最大化", "NIPALS 思想", "成分数选择", "回归系数解释", "交叉验证", "sklearn PLSRegression"],
    formulas: ["X=TP^T+E", "Y=UQ^T+F", "\\max \\operatorname{Cov}(t,u)", "\\hat{Y}=XB+C"],
    codeKey: "pls",
  },
  {
    id: "14",
    file: "14_综合评价方法.md",
    title: "综合评价方法",
    bookTopic: "第 14 章",
    goal: "掌握多指标评价中的标准化、赋权、排序和敏感性分析。",
    keywords: ["综合评价", "熵权法", "TOPSIS", "AHP", "灰色关联", "主成分评价"],
    topics: ["评价指标体系", "指标同向化", "极差标准化", "熵权法", "AHP 层次分析", "TOPSIS", "灰色关联分析", "主成分综合评价", "排序稳定性", "敏感性分析"],
    formulas: ["z_{ij}=\\frac{x_{ij}-\\min x_j}{\\max x_j-\\min x_j}", "e_j=-k\\sum_i p_{ij}\\ln p_{ij}", "C_i=\\frac{D_i^-}{D_i^++D_i^-}", "CI=\\frac{\\lambda_{max}-n}{n-1}"],
    codeKey: "evaluation",
  },
  {
    id: "15",
    file: "15_预测方法.md",
    title: "预测方法",
    bookTopic: "第 15 章",
    goal: "掌握时间序列、灰色预测、指数平滑和机器学习预测的基础流程。",
    keywords: ["时间序列", "移动平均", "指数平滑", "灰色预测", "ARIMA", "预测误差"],
    topics: ["预测问题定义", "训练测试切分", "移动平均", "指数平滑", "趋势外推", "GM(1,1) 灰色预测", "ARIMA 思想", "特征工程预测", "误差指标", "滚动预测验证"],
    formulas: ["\\hat{y}_{t+1}=\\frac{1}{m}\\sum_{i=0}^{m-1}y_{t-i}", "S_t=\\alpha y_t+(1-\\alpha)S_{t-1}", "x^{(1)}(k+1)=\\left(x^{(0)}(1)-\\frac{b}{a}\\right)e^{-ak}+\\frac{b}{a}", "MAPE=\\frac{1}{n}\\sum_i\\left|\\frac{y_i-\\hat{y}_i}{y_i}\\right|"],
    codeKey: "forecasting",
  },
];

const exampleCode = {
  linear_algebra: `import numpy as np

def solve_linear_system():
    A = np.array([[3, 1, -1], [2, 4, 1], [-1, 2, 5]], dtype=float)
    b = np.array([4, 1, 1], dtype=float)
    x = np.linalg.solve(A, b)
    residual = np.linalg.norm(A @ x - b)
    return x, residual

def least_squares_demo():
    x = np.linspace(0, 10, 20)
    y = 2.5 * x + 1.2 + np.random.default_rng(42).normal(0, 1, len(x))
    A = np.column_stack([x, np.ones_like(x)])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    return beta

def markov_stationary_distribution():
    P = np.array([[0.7, 0.3, 0.0],
                  [0.2, 0.6, 0.2],
                  [0.1, 0.2, 0.7]])
    pi = np.array([1.0, 0.0, 0.0])
    for _ in range(100):
        pi = pi @ P
    return pi

if __name__ == "__main__":
    print("Ax=b:", solve_linear_system())
    print("least squares beta:", least_squares_demo())
    print("stationary distribution:", markov_stationary_distribution())
`,
  linear_programming: `import numpy as np
from scipy.optimize import linprog
from scipy.optimize import linear_sum_assignment

def production_plan():
    # maximize 40 x1 + 30 x2 -> minimize negative profit
    c = np.array([-40, -30], dtype=float)
    A = np.array([[2, 1], [1, 1], [1, 0]], dtype=float)
    b = np.array([100, 80, 40], dtype=float)
    res = linprog(c, A_ub=A, b_ub=b, bounds=[(0, None), (0, None)], method="highs")
    return res.x, -res.fun

def assignment_demo():
    cost = np.array([[9, 2, 7], [6, 4, 3], [5, 8, 1]], dtype=float)
    row, col = linear_sum_assignment(cost)
    return list(zip(row, col)), cost[row, col].sum()

if __name__ == "__main__":
    print("production:", production_plan())
    print("assignment:", assignment_demo())
`,
  nonlinear_programming: `import numpy as np
from scipy.optimize import minimize

def constrained_nlp():
    def f(x):
        return (x[0] - 1) ** 2 + (x[1] - 2) ** 2

    constraints = [
        {"type": "ineq", "fun": lambda x: x[0] + x[1] - 2},
        {"type": "eq", "fun": lambda x: x[0] - x[1] + 1},
    ]
    res = minimize(f, x0=np.array([0.0, 0.0]), constraints=constraints, method="SLSQP")
    return res.x, res.fun, res.success

def weighted_multi_objective(weight=0.6):
    def f1(x):
        return (x[0] - 1) ** 2 + x[1] ** 2

    def f2(x):
        return x[0] ** 2 + (x[1] - 1) ** 2

    def objective(x):
        return weight * f1(x) + (1 - weight) * f2(x)

    res = minimize(objective, x0=np.array([0.5, 0.5]), method="BFGS")
    return res.x, res.fun

if __name__ == "__main__":
    print("constrained:", constrained_nlp())
    print("multi objective:", weighted_multi_objective())
`,
  graph: `import networkx as nx

def shortest_path_demo():
    G = nx.Graph()
    edges = [
        ("A", "B", 4), ("A", "C", 2), ("B", "C", 1),
        ("B", "D", 5), ("C", "D", 8), ("C", "E", 10),
        ("D", "E", 2), ("D", "F", 6), ("E", "F", 3),
    ]
    G.add_weighted_edges_from(edges)
    path = nx.shortest_path(G, "A", "F", weight="weight")
    length = nx.shortest_path_length(G, "A", "F", weight="weight")
    tree = nx.minimum_spanning_tree(G, weight="weight")
    return path, length, list(tree.edges(data=True))

def max_flow_demo():
    G = nx.DiGraph()
    G.add_edge("s", "a", capacity=8)
    G.add_edge("s", "b", capacity=5)
    G.add_edge("a", "b", capacity=3)
    G.add_edge("a", "t", capacity=4)
    G.add_edge("b", "t", capacity=7)
    return nx.maximum_flow(G, "s", "t")

if __name__ == "__main__":
    print("shortest/mst:", shortest_path_demo())
    print("max flow:", max_flow_demo())
`,
  interpolation_fitting: `import numpy as np
from scipy.interpolate import interp1d, CubicSpline
from scipy.optimize import curve_fit

def interpolation_demo():
    x = np.array([0, 1, 2, 3, 4], dtype=float)
    y = np.array([1.0, 2.0, 1.5, 3.2, 2.8])
    xs = np.linspace(0, 4, 50)
    linear = interp1d(x, y, kind="linear")
    spline = CubicSpline(x, y)
    return xs, linear(xs), spline(xs)

def nonlinear_fit_demo():
    rng = np.random.default_rng(42)
    x = np.linspace(0, 5, 40)
    y = 3.0 * np.exp(-0.7 * x) + 0.5 + rng.normal(0, 0.08, len(x))

    def model(x, a, b, c):
        return a * np.exp(-b * x) + c

    params, cov = curve_fit(model, x, y, p0=[2, 0.5, 0])
    return params, np.sqrt(np.diag(cov))

if __name__ == "__main__":
    print("interpolation arrays:", [arr.shape for arr in interpolation_demo()])
    print("fit params:", nonlinear_fit_demo())
`,
  regression: `import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression, RidgeCV
from sklearn.metrics import accuracy_score

def ols_demo():
    rng = np.random.default_rng(42)
    X = rng.normal(size=(120, 3))
    y = 1.5 + X @ np.array([2.0, -1.0, 0.5]) + rng.normal(0, 0.5, 120)
    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const).fit()
    return model.params, model.rsquared, model.pvalues

def ridge_demo():
    rng = np.random.default_rng(7)
    X = rng.normal(size=(100, 5))
    y = X @ np.array([1, 1, 0, 0, 0.5]) + rng.normal(0, 0.3, 100)
    model = RidgeCV(alphas=[0.01, 0.1, 1, 10]).fit(X, y)
    return model.alpha_, model.coef_

def logistic_demo():
    rng = np.random.default_rng(11)
    X = rng.normal(size=(150, 2))
    y = (X[:, 0] - 0.8 * X[:, 1] + rng.normal(0, 0.5, 150) > 0).astype(int)
    clf = LogisticRegression().fit(X, y)
    pred = clf.predict(X)
    return clf.coef_, clf.intercept_, accuracy_score(y, pred)

if __name__ == "__main__":
    print("OLS:", ols_demo())
    print("Ridge:", ridge_demo())
    print("Logistic:", logistic_demo())
`,
  cluster_discriminant: `import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.datasets import make_blobs
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import silhouette_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def clustering_demo():
    X, _ = make_blobs(n_samples=240, centers=3, cluster_std=0.8, random_state=42)
    Xs = StandardScaler().fit_transform(X)
    km = KMeans(n_clusters=3, random_state=42, n_init="auto").fit(Xs)
    score = silhouette_score(Xs, km.labels_)
    return km.cluster_centers_, score

def lda_demo():
    X, y = make_blobs(n_samples=180, centers=3, cluster_std=1.2, random_state=10)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, stratify=y)
    lda = LinearDiscriminantAnalysis().fit(X_train, y_train)
    pred = lda.predict(X_test)
    return lda.coef_, confusion_matrix(y_test, pred)

if __name__ == "__main__":
    print("cluster:", clustering_demo())
    print("lda:", lda_demo())
`,
  pls: `import numpy as np
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import cross_val_score, KFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def pls_demo():
    rng = np.random.default_rng(42)
    latent = rng.normal(size=(80, 2))
    X = latent @ np.array([[1, 0.8, 0.6, 0.2, 0.1],
                           [0.1, 0.3, 0.5, 0.8, 1.0]]) + rng.normal(0, 0.05, (80, 5))
    y = latent @ np.array([2.0, -1.0]) + rng.normal(0, 0.1, 80)
    pipe = Pipeline([
        ("scale", StandardScaler()),
        ("pls", PLSRegression(n_components=2)),
    ])
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    score = cross_val_score(pipe, X, y, cv=cv, scoring="neg_root_mean_squared_error")
    pipe.fit(X, y)
    return -score.mean(), pipe.named_steps["pls"].coef_.ravel()

if __name__ == "__main__":
    print("PLS:", pls_demo())
`,
  evaluation: `import numpy as np

def minmax_positive(X):
    X = np.asarray(X, dtype=float)
    return (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0) + 1e-12)

def entropy_weight(X):
    Z = minmax_positive(X) + 1e-12
    P = Z / Z.sum(axis=0, keepdims=True)
    n = X.shape[0]
    E = -(P * np.log(P)).sum(axis=0) / np.log(n)
    D = 1 - E
    return D / D.sum()

def topsis(X, weights=None):
    Z = minmax_positive(X)
    norm = Z / (np.sqrt((Z ** 2).sum(axis=0, keepdims=True)) + 1e-12)
    if weights is None:
        weights = entropy_weight(X)
    V = norm * weights
    best = V.max(axis=0)
    worst = V.min(axis=0)
    d_pos = np.sqrt(((V - best) ** 2).sum(axis=1))
    d_neg = np.sqrt(((V - worst) ** 2).sum(axis=1))
    score = d_neg / (d_pos + d_neg + 1e-12)
    return score, np.argsort(-score)

if __name__ == "__main__":
    X = np.array([[80, 70, 90], [90, 65, 85], [75, 95, 80], [88, 82, 78]], dtype=float)
    print("weights:", entropy_weight(X))
    print("topsis:", topsis(X))
`,
  forecasting: `import numpy as np

def moving_average(y, window=3):
    y = np.asarray(y, dtype=float)
    return np.array([y[i-window:i].mean() for i in range(window, len(y) + 1)])

def simple_exp_smoothing(y, alpha=0.4):
    y = np.asarray(y, dtype=float)
    s = [y[0]]
    for t in range(1, len(y)):
        s.append(alpha * y[t] + (1 - alpha) * s[-1])
    return np.array(s)

def gm11_forecast(x0, steps=3):
    x0 = np.asarray(x0, dtype=float)
    x1 = np.cumsum(x0)
    z1 = 0.5 * (x1[1:] + x1[:-1])
    B = np.column_stack([-z1, np.ones(len(z1))])
    Y = x0[1:]
    a, b = np.linalg.lstsq(B, Y, rcond=None)[0]

    def x1_hat(k):
        return (x0[0] - b / a) * np.exp(-a * k) + b / a

    total = len(x0) + steps
    x1_pred = np.array([x1_hat(k) for k in range(total)])
    x0_pred = np.r_[x0[0], np.diff(x1_pred)]
    return x0_pred

def mape(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    return np.mean(np.abs((y_true - y_pred) / (y_true + 1e-12)))

if __name__ == "__main__":
    y = np.array([10, 12, 13, 15, 18, 20, 23, 25], dtype=float)
    print("MA:", moving_average(y))
    print("SES:", simple_exp_smoothing(y))
    print("GM11:", gm11_forecast(y, steps=2))
`,
};

function addLines(lines, list) {
  for (const item of list) lines.push(item);
}

function examOverview(ch) {
  const lines = [];
  lines.push("## 考试复习总览");
  lines.push("");
  lines.push("这一章复习时要按“识别题型、写出模型、说明算法、解释结果”的顺序准备。考试或课程报告通常不会只考一个 API，而是考你能不能把文字问题转成可计算模型。");
  lines.push("");
  lines.push("### 高频考点");
  lines.push("");
  addLines(lines, [
    `- 能识别 ${ch.title} 适合处理什么类型的问题。`,
    "- 能写出变量、参数、目标函数、约束条件或评价指标。",
    "- 能解释公式中每个符号的现实含义，而不是只抄公式。",
    "- 能判断数据是否需要标准化、同向化、缺失值处理或时间顺序切分。",
    "- 能选择 Python 中合适的函数或库，并说明为什么这样求解。",
    "- 能根据输出结果写出一句清楚的建模结论。",
    "- 能指出模型至少两个局限，并提出改进方向。",
  ]);
  lines.push("");
  lines.push("### 题型识别信号");
  lines.push("");
  addLines(lines, [
    "- 题目出现“最优、最大、最小、成本、收益、资源、约束”，优先考虑优化模型。",
    "- 题目出现“节点、道路、路径、网络、运输、连通”，优先考虑图论模型。",
    "- 题目出现“多个指标、综合排名、评价对象、权重”，优先考虑综合评价模型。",
    "- 题目出现“历史数据、趋势、未来、预测”，优先考虑预测模型。",
    "- 题目出现“影响因素、解释变量、因变量、显著性”，优先考虑回归分析。",
    "- 题目出现“分类、相似、分组、判别”，优先考虑聚类分析或判别分析。",
    "- 题目出现“离散点、补全曲线、函数关系”，优先考虑插值与拟合。",
    "- 题目出现“多重共线性、少样本、多指标解释响应”，优先考虑偏最小二乘。",
  ]);
  lines.push("");
  lines.push("### 答题固定结构");
  lines.push("");
  addLines(lines, [
    "1. 先写“设……”：定义变量、样本、指标、节点或时间点。",
    "2. 再写“建立模型如下”：列出目标、约束、公式或算法流程。",
    "3. 然后写“求解方法”：说明使用的算法、库函数和关键参数。",
    "4. 接着写“结果分析”：解释最优解、排名、预测值、分类结果或误差。",
    "5. 最后写“模型评价”：说明优点、缺点、适用条件和改进方向。",
  ]);
  lines.push("");
  lines.push("### 公式速查");
  lines.push("");
  for (const formula of ch.formulas) {
    lines.push(`- $${formula}$`);
  }
  lines.push("");
  lines.push("### 考前自测");
  lines.push("");
  addLines(lines, [
    "- 不看笔记，能否在 3 分钟内写出本章适用场景？",
    "- 不看代码，能否写出核心 Python 调用的输入和输出？",
    "- 给一组小数据，能否手算或半手算一个结果用于校验程序？",
    "- 能否解释为什么要标准化、同向化或加入约束？",
    "- 能否说明模型失败时最先检查哪三件事？",
  ]);
  lines.push("");
  return lines;
}

function examAnswerTemplate(ch, topic) {
  const lines = [];
  lines.push("### 考试答题模板");
  lines.push("");
  lines.push(`如果题目考到“${topic}”，可以按下面这段结构组织答案：`);
  lines.push("");
  addLines(lines, [
    `1. 识别：本题属于 ${ch.title} 中的“${topic}”类问题，目标是把实际问题转化为可计算模型。`,
    "2. 变量：设 $x_i$ 表示第 $i$ 个决策变量、评价值、状态量或待估参数。",
    "3. 数据：将题目给出的表格整理为矩阵 $X$、向量 $y$、约束矩阵 $A$ 或图 $G$。",
    "4. 模型：根据题意写出目标函数、约束条件、距离度量、递推公式或评价函数。",
    "5. 求解：使用对应算法求解，并检查维度、可行性、收敛状态和误差。",
    "6. 解释：把数学结果翻译回现实语言，例如最优方案、排名、预测趋势或分类结论。",
    "7. 检验：用残差、误差、敏感性分析、交叉验证或可行性检查说明结果可靠性。",
  ]);
  lines.push("");
  lines.push("### 快速判分点");
  lines.push("");
  addLines(lines, [
    "- 有没有清楚写出变量含义。",
    "- 有没有写出核心公式，而不是只说“用 Python 求”。",
    "- 有没有说明约束或指标方向。",
    "- 有没有给出结果解释。",
    "- 有没有指出模型局限。",
  ]);
  lines.push("");
  return lines;
}

function workedExamples(ch) {
  const lines = [];
  lines.push("## 典型题型与解题套路");
  lines.push("");
  const examples = [
    {
      name: "概念辨析题",
      prompt: `说明 ${ch.title} 适合解决什么问题，并给出不适用的情况。`,
      steps: [
        "先写适用场景。",
        "再写模型输入和输出。",
        "然后写关键公式。",
        "最后写局限：数据要求、假设条件、计算限制。",
      ],
    },
    {
      name: "建模推导题",
      prompt: "给出一段文字背景，要求建立数学模型。",
      steps: [
        "划出题目中的可控量、已知量和评价目标。",
        "定义变量和参数。",
        "写出目标函数或评价函数。",
        "逐条翻译约束条件。",
        "说明求解方法和结果解释方式。",
      ],
    },
    {
      name: "代码实现题",
      prompt: "给出数据表，要求用 Python 求解并输出结果。",
      steps: [
        "读入数据并检查缺失值。",
        "根据模型需要做标准化、同向化或矩阵转换。",
        "调用 NumPy、SciPy、scikit-learn、statsmodels 或 NetworkX。",
        "输出核心结果，不只打印对象。",
        "用一个误差或可行性指标检查结果。",
      ],
    },
    {
      name: "结果分析题",
      prompt: "给出模型输出，要求解释含义并评价模型。",
      steps: [
        "先解释数值含义。",
        "再联系原问题给出结论。",
        "然后检查约束、误差或排序稳定性。",
        "最后指出局限和改进方向。",
      ],
    },
  ];
  for (const example of examples) {
    lines.push(`### ${example.name}`);
    lines.push("");
    lines.push(`题目特征：${example.prompt}`);
    lines.push("");
    lines.push("答题步骤：");
    lines.push("");
    example.steps.forEach((step, idx) => lines.push(`${idx + 1}. ${step}`));
    lines.push("");
  }
  lines.push("### 小型模拟题");
  lines.push("");
  ch.topics.slice(0, 6).forEach((topic, idx) => {
    lines.push(`${idx + 1}. 已知一组与“${topic}”有关的数据，请建立模型、写出核心公式、给出 Python 求解思路，并说明如何检验结果。`);
  });
  lines.push("");
  return lines;
}

function examChecklist(ch) {
  const lines = [];
  lines.push("## 考前最后检查表");
  lines.push("");
  addLines(lines, [
    `- 我能说出 ${ch.title} 的适用题型和不适用题型。`,
    "- 我能默写本章核心公式并解释符号。",
    "- 我能把题目文字翻译成变量、参数和数据矩阵。",
    "- 我能说明为什么需要标准化、同向化、权重或约束。",
    "- 我能写出至少一个 Python 最小求解模板。",
    "- 我能解释求解器输出中的最优值、参数、误差或标签。",
    "- 我能写出两条模型局限。",
    "- 我能做一个简单的敏感性分析。",
    "- 我能区分训练误差、预测误差、拟合误差和评价分数。",
    "- 我能在报告中把公式、代码、表格和结论连起来。",
  ]);
  lines.push("");
  return lines;
}

function theorySection(ch, topic, index) {
  const lines = [];
  lines.push(`## ${ch.id}.${String(index).padStart(2, "0")} ${topic}`);
  lines.push("");
  lines.push("### 问题意识");
  lines.push("");
  lines.push(`${topic}在数学建模中通常不是为了展示算法，而是为了把一个现实问题压缩成“变量、约束、目标、数据、评价”五件事。`);
  lines.push("遇到任何建模题，先不要急着套包，先判断：哪些量可控，哪些量只能观测，哪些量是必须满足的约束，哪些量只是希望越大或越小越好。");
  lines.push("");
  lines.push("### 建模步骤");
  lines.push("");
  addLines(lines, [
    "1. 明确研究对象：写出样本、节点、时间点、指标或决策变量。",
    "2. 明确输入数据：检查量纲、缺失值、异常点和数据来源可靠性。",
    "3. 明确数学对象：判断使用矩阵、函数、图、概率模型、优化模型还是评价模型。",
    "4. 建立目标函数或评价指标：说明为什么这个目标符合题意。",
    "5. 加入约束条件：区分硬约束、软约束和经验假设。",
    "6. 选择算法求解：优先使用稳定、可解释、可复现的算法。",
    "7. 做结果解释：输出不只是数值，还要说明变量含义和现实建议。",
    "8. 做敏感性分析：改变关键参数或数据扰动，观察结论是否稳定。",
  ]);
  lines.push("");
  lines.push("### 原理讲解");
  lines.push("");
  addLines(lines, [
    `- ${topic}的核心是把现实语言转换成数学语言，转换质量往往比算法复杂度更重要。`,
    "- 如果变量定义不清楚，后面的公式即使正确也没有解释力。",
    "- 如果约束条件漏掉，模型可能给出数学最优但现实不可执行的方案。",
    "- 如果目标函数选错，算法会非常努力地优化一个错误方向。",
    "- 建模时要保留单位和量纲意识，避免把不同尺度的数据直接相加。",
    "- 计算结果要回到原问题解释，不能只给出矩阵、曲线或求解器状态。",
    "- 对比赛或课程作业来说，清晰的假设、可复现代码和图表解释同样重要。",
    "- 对工程问题来说，模型还需要考虑数据更新、运行时间和异常输入。",
  ]);
  lines.push("");
  lines.push("### 数学表达");
  lines.push("");
  lines.push("本节常见表达可以统一写成：");
  lines.push("");
  lines.push("$$");
  lines.push("\\text{data}\\ \\longrightarrow\\ \\text{model}\\ \\longrightarrow\\ \\text{solution}\\ \\longrightarrow\\ \\text{decision}");
  lines.push("$$");
  lines.push("");
  for (const formula of ch.formulas) {
    lines.push("$$");
    lines.push(formula);
    lines.push("$$");
    lines.push("");
  }
  lines.push("符号解释：");
  lines.push("");
  addLines(lines, [
    "- $x$ 通常表示待求变量或特征向量。",
    "- $A$ 通常表示系数矩阵、约束矩阵或邻接矩阵。",
    "- $b$ 通常表示资源上限、观测值或右端项。",
    "- $f(x)$ 通常表示目标函数、误差函数或评价函数。",
    "- $\\theta$ 通常表示需要估计的模型参数。",
    "- $\\hat{y}$ 表示模型给出的预测值或拟合值。",
  ]);
  lines.push("");
  lines.push("### 推导线索");
  lines.push("");
  addLines(lines, [
    "1. 从现实问题抽取变量，先写出变量表。",
    "2. 根据变量关系写出等式、不等式或递推关系。",
    "3. 把多个关系整理成矩阵形式，便于计算和检查维度。",
    "4. 如果方程组无精确解，就转向最小误差原则。",
    "5. 如果有多个目标，就用加权、分层或 Pareto 思想处理冲突。",
    "6. 如果结果依赖主观权重，就必须做权重敏感性分析。",
    "7. 如果模型含随机性，就固定随机种子并多次运行。",
    "8. 如果算法可能陷入局部最优，就尝试多初值或全局搜索。",
  ]);
  lines.push("");
  lines.push("### Python 实现模板");
  lines.push("");
  lines.push("```python");
  lines.push("import numpy as np");
  lines.push("");
  lines.push(`def section_${ch.id}_${index}_check_array(X):`);
  lines.push("    X = np.asarray(X, dtype=float)");
  lines.push("    if np.isnan(X).any():");
  lines.push("        raise ValueError('input contains NaN')")
  lines.push("    if np.isinf(X).any():");
  lines.push("        raise ValueError('input contains Inf')")
  lines.push("    return X");
  lines.push("");
  lines.push(`def section_${ch.id}_${index}_standardize(X):`);
  lines.push(`    X = section_${ch.id}_${index}_check_array(X)`);
  lines.push("    mu = X.mean(axis=0)");
  lines.push("    sigma = X.std(axis=0) + 1e-12");
  lines.push("    return (X - mu) / sigma, mu, sigma");
  lines.push("");
  lines.push(`def section_${ch.id}_${index}_report(name, value):`);
  lines.push("    print(f'{name}: {value}')");
  lines.push("```");
  lines.push("");
  lines.push("### 结果解释");
  lines.push("");
  addLines(lines, [
    "- 先解释最重要的变量或指标，不要先堆代码输出。",
    "- 再解释为什么这个结果符合或不符合直觉。",
    "- 接着说明约束是否全部满足。",
    "- 然后报告误差、残差、最优值、排序分数或预测区间。",
    "- 最后写出模型局限：数据量、假设、参数、算法、外推风险。",
  ]);
  lines.push("");
  lines.push("### 易错点");
  lines.push("");
  addLines(lines, [
    "1. 没有统一量纲，导致大尺度指标支配结果。",
    "2. 忘记检查可行性，直接相信求解器输出。",
    "3. 把相关性解释成因果关系。",
    "4. 用训练误差替代预测能力。",
    "5. 没有说明主观权重来源。",
    "6. 图模型中把有向边和无向边混用。",
    "7. 优化模型中漏写非负约束或整数约束。",
    "8. 预测模型中随机打乱了时间序列。",
  ]);
  lines.push("");
  lines.push(...examAnswerTemplate(ch, topic));
  return lines;
}

function codeBlock(ch) {
  const lines = [];
  lines.push("## 本章完整 Python 示例");
  lines.push("");
  lines.push(`示例文件：[\`${ch.id}_${ch.codeKey}.py\`](../examples/${ch.id}_${ch.codeKey}.py)`);
  lines.push("");
  lines.push("```python");
  lines.push(exampleCode[ch.codeKey].trimEnd());
  lines.push("```");
  lines.push("");
  return lines;
}

function generateChapter(ch) {
  const lines = [];
  lines.push(`# ${ch.bookTopic} ${ch.title}`);
  lines.push("");
  lines.push(`> 这份笔记是针对《Python数学建模算法与应用》${ch.bookTopic}主题的原创学习讲解，重点放在原理、建模步骤和 Python 实现。`);
  lines.push("");
  lines.push("---");
  lines.push("");
  lines.push("## 学习目标");
  lines.push("");
  lines.push(ch.goal);
  lines.push("");
  lines.push("完成本章后，你应该能够：");
  lines.push("");
  addLines(lines, [
    "1. 根据题目文字识别对应的数学模型类型。",
    "2. 写出变量、约束、目标函数或评价指标。",
    "3. 推导关键公式，并解释每个符号的现实含义。",
    "4. 使用 Python 完成最小可运行求解。",
    "5. 对结果做解释、检验和敏感性分析。",
  ]);
  lines.push("");
  lines.push("## 关键词");
  lines.push("");
  for (const kw of ch.keywords) lines.push(`- ${kw}`);
  lines.push("");
  lines.push("## 先记住的核心公式");
  lines.push("");
  for (const formula of ch.formulas) {
    lines.push("$$");
    lines.push(formula);
    lines.push("$$");
    lines.push("");
  }
  lines.push("## 本章学习地图");
  lines.push("");
  lines.push("```text");
  lines.push("现实问题 -> 变量定义 -> 数学模型 -> 算法求解 -> Python 实现 -> 结果解释 -> 稳健性检查");
  lines.push("```");
  lines.push("");
  lines.push(...examOverview(ch));
  lines.push("## 章节目录");
  lines.push("");
  ch.topics.forEach((topic, i) => lines.push(`${i + 1}. ${topic}`));
  lines.push("");
  lines.push("---");
  lines.push("");
  ch.topics.forEach((topic, idx) => lines.push(...theorySection(ch, topic, idx + 1)));
  lines.push(...codeBlock(ch));
  lines.push(...workedExamples(ch));
  lines.push("## 建模报告写作模板");
  lines.push("");
  addLines(lines, [
    "1. 问题重述：用自己的话写清楚研究对象和任务。",
    "2. 模型假设：列出简洁、必要、可辩护的假设。",
    "3. 符号说明：变量、参数、数据来源、单位。",
    "4. 模型建立：给出目标函数、约束、评价指标或递推关系。",
    "5. 模型求解：说明算法、软件包、关键参数和随机种子。",
    "6. 结果展示：用表格、图像和文字解释结果。",
    "7. 检验分析：残差、误差、可行性、敏感性、稳定性。",
    "8. 模型评价：优点、缺点、可改进方向。",
  ]);
  lines.push("");
  lines.push("## 复习题");
  lines.push("");
  for (let i = 1; i <= 20; i++) {
    const topic = ch.topics[(i - 1) % ch.topics.length];
    lines.push(`${i}. 围绕“${topic}”设计一个小型数学建模问题，写出变量、公式、求解方法和 Python 检验方式。`);
  }
  lines.push("");
  lines.push(...examChecklist(ch));
  return lines.join("\n");
}

function generateReadme() {
  const lines = [];
  lines.push("# Python 数学建模算法与应用学习讲义");
  lines.push("");
  lines.push("> 针对《Python数学建模算法与应用》（国防工业出版社）部分章节主题整理的原创学习笔记。");
  lines.push("> 内容覆盖原理讲解、公式推导、建模步骤、Python 代码实现、考试题型和复习题。");
  lines.push("");
  lines.push("## 覆盖章节");
  lines.push("");
  lines.push("| 教材章节 | 本讲义文件 | 主题 |");
  lines.push("|----------|------------|------|");
  for (const ch of chapters) {
    lines.push(`| ${ch.bookTopic} | [${ch.file}](chapters/${ch.file}) | ${ch.title} |`);
  }
  lines.push("");
  lines.push("## 目录结构");
  lines.push("");
  lines.push("```text");
  lines.push("Mathematical Modeling(Python)/");
  lines.push("├── README.md");
  lines.push("├── chapters/");
  for (const ch of chapters) lines.push(`│   ├── ${ch.file}`);
  lines.push("├── examples/");
  for (const ch of chapters) lines.push(`│   ├── ${ch.id}_${ch.codeKey}.py`);
  lines.push("└── tools/");
  lines.push("    └── generate_modeling_notes.mjs");
  lines.push("```");
  lines.push("");
  lines.push("## 推荐学习顺序");
  lines.push("");
  lines.push("1. 先学第 3 章线性代数模型，建立矩阵思维。");
  lines.push("2. 再学第 4、5、6 章，掌握优化模型和图论模型。");
  lines.push("3. 接着学第 7、10、11、13 章，处理数据拟合、回归、分类和降维。");
  lines.push("4. 最后学第 14、15 章，完成综合评价和预测类建模题。");
  lines.push("");
  lines.push("## Python 环境建议");
  lines.push("");
  lines.push("```bash");
  lines.push("pip install numpy scipy pandas matplotlib scikit-learn statsmodels networkx");
  lines.push("```");
  lines.push("");
  lines.push("## 使用方式");
  lines.push("");
  lines.push("- 先读对应章节 Markdown。");
  lines.push("- 考前优先看每章的“考试复习总览”“典型题型与解题套路”“考前最后检查表”。");
  lines.push("- 再运行 `examples/` 中的同章 Python 文件。");
  lines.push("- 最后把模板替换成自己的数据，补上结果解释和敏感性分析。");
  lines.push("");
  return lines.join("\n");
}

mkdirSync(join(root, "chapters"), { recursive: true });
mkdirSync(join(root, "examples"), { recursive: true });
mkdirSync(join(root, "projects"), { recursive: true });

writeFileSync(join(root, "README.md"), generateReadme(), "utf8");
for (const ch of chapters) {
  writeFileSync(join(root, "chapters", ch.file), generateChapter(ch), "utf8");
  writeFileSync(join(root, "examples", `${ch.id}_${ch.codeKey}.py`), exampleCode[ch.codeKey], "utf8");
}
writeFileSync(join(root, "projects", "README.md"), "# 数学建模项目实践\n\n建议基于各章 examples 扩展成完整建模报告。\n", "utf8");

console.log(`Generated ${chapters.length} modeling chapters.`);
