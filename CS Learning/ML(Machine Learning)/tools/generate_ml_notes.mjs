import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const root = dirname(here);

const chapters = [
  {
    id: "01",
    file: "01_机器学习总览_数学基础与实验范式.md",
    title: "机器学习总览、数学基础与实验范式",
    goal: "建立机器学习全局地图，理解数据、模型、损失、优化、泛化之间的闭环。",
    keywords: ["监督学习", "无监督学习", "经验风险", "泛化误差", "向量化", "实验复现"],
    topics: ["机器学习任务分类", "数据集与样本空间", "特征向量与标签", "经验风险最小化", "训练集验证集测试集", "向量化计算", "损失函数", "优化算法", "泛化与归纳偏置", "实验记录与复现"],
    formulas: ["\\hat{y}=f(x;\\theta)", "\\mathcal{R}_{emp}(\\theta)=\\frac{1}{n}\\sum_{i=1}^{n}\\ell(f(x_i;\\theta),y_i)", "\\theta_{t+1}=\\theta_t-\\eta\\nabla_\\theta J(\\theta_t)"],
    implementation: "baseline",
  },
  {
    id: "02",
    file: "02_数据预处理_特征工程与模型评估.md",
    title: "数据预处理、特征工程与模型评估",
    goal: "掌握从原始数据到可靠评估的完整前处理流水线。",
    keywords: ["缺失值", "标准化", "编码", "交叉验证", "混淆矩阵", "AUC"],
    topics: ["数据清洗", "缺失值处理", "异常值识别", "数值特征缩放", "类别特征编码", "文本与稀疏特征", "数据泄漏", "分类指标", "回归指标", "交叉验证"],
    formulas: ["z=\\frac{x-\\mu}{\\sigma}", "Precision=\\frac{TP}{TP+FP}", "RMSE=\\sqrt{\\frac{1}{n}\\sum_{i=1}^{n}(y_i-\\hat{y}_i)^2}"],
    implementation: "preprocess",
  },
  {
    id: "03",
    file: "03_线性回归_最小二乘与梯度下降.md",
    title: "线性回归、最小二乘与梯度下降",
    goal: "从闭式解和梯度下降两条路线理解最基础的回归模型。",
    keywords: ["线性模型", "最小二乘", "正规方程", "梯度下降", "残差", "R2"],
    topics: ["一元线性回归", "多元线性回归", "残差平方和", "正规方程推导", "梯度下降推导", "学习率选择", "多项式回归", "岭回归", "Lasso 回归", "回归诊断"],
    formulas: ["\\hat{y}=Xw+b", "J(w)=\\frac{1}{2n}\\lVert Xw-y\\rVert_2^2", "w^*=(X^TX)^{-1}X^Ty"],
    implementation: "linear",
  },
  {
    id: "04",
    file: "04_逻辑回归_广义线性模型与分类边界.md",
    title: "逻辑回归、广义线性模型与分类边界",
    goal: "理解分类概率建模、对数似然、交叉熵和决策边界。",
    keywords: ["Sigmoid", "Softmax", "最大似然", "交叉熵", "分类边界", "多分类"],
    topics: ["二分类建模", "Sigmoid 函数", "伯努利似然", "交叉熵推导", "梯度公式", "正则化逻辑回归", "多分类 Softmax", "类别不平衡", "阈值移动", "校准概率"],
    formulas: ["p(y=1|x)=\\sigma(w^Tx+b)", "\\sigma(z)=\\frac{1}{1+e^{-z}}", "J(w)=-\\frac{1}{n}\\sum_i[y_i\\log p_i+(1-y_i)\\log(1-p_i)]"],
    implementation: "logistic",
  },
  {
    id: "05",
    file: "05_朴素贝叶斯_概率建模与生成式分类.md",
    title: "朴素贝叶斯、概率建模与生成式分类",
    goal: "理解条件概率、贝叶斯公式、条件独立假设和生成式分类器。",
    keywords: ["先验", "似然", "后验", "条件独立", "拉普拉斯平滑", "文本分类"],
    topics: ["概率基础", "贝叶斯公式", "生成式与判别式", "朴素条件独立", "GaussianNB", "MultinomialNB", "BernoulliNB", "拉普拉斯平滑", "对数概率计算", "错误分析"],
    formulas: ["P(y|x)=\\frac{P(x|y)P(y)}{P(x)}", "P(x|y)=\\prod_{j=1}^{d}P(x_j|y)", "\\log P(y|x)=\\log P(y)+\\sum_j\\log P(x_j|y)+C"],
    implementation: "bayes",
  },
  {
    id: "06",
    file: "06_KNN_距离度量_核方法入门.md",
    title: "KNN、距离度量与核方法入门",
    goal: "理解基于相似性的学习思想，以及距离、核函数和局部决策。",
    keywords: ["KNN", "欧氏距离", "曼哈顿距离", "余弦相似度", "核函数", "局部平均"],
    topics: ["实例学习", "欧氏距离", "曼哈顿距离", "余弦相似度", "K 值选择", "加权 KNN", "KD Tree 思想", "核函数直觉", "RBF 核", "高维距离问题"],
    formulas: ["d_2(x,z)=\\sqrt{\\sum_j(x_j-z_j)^2}", "K(x,z)=\\exp(-\\gamma\\lVert x-z\\rVert^2)", "\\hat{y}=\\operatorname{mode}\\{y_i:i\\in N_k(x)\\}"],
    implementation: "knn",
  },
  {
    id: "07",
    file: "07_决策树_随机森林与集成学习.md",
    title: "决策树、随机森林与集成学习",
    goal: "掌握树模型的划分准则、剪枝思想和集成学习框架。",
    keywords: ["信息熵", "基尼指数", "剪枝", "Bagging", "随机森林", "Boosting"],
    topics: ["树模型直觉", "信息熵", "信息增益", "基尼指数", "连续特征切分", "预剪枝与后剪枝", "Bagging", "随机森林", "Boosting", "特征重要性"],
    formulas: ["H(Y)=-\\sum_kp_k\\log p_k", "Gini(D)=1-\\sum_kp_k^2", "Gain(D,A)=H(D)-\\sum_v\\frac{|D_v|}{|D|}H(D_v)"],
    implementation: "tree",
  },
  {
    id: "08",
    file: "08_SVM_最大间隔分类与核技巧.md",
    title: "SVM、最大间隔分类与核技巧",
    goal: "理解间隔最大化、软间隔、拉格朗日对偶和核技巧。",
    keywords: ["最大间隔", "支持向量", "Hinge Loss", "对偶问题", "核技巧", "软间隔"],
    topics: ["线性可分 SVM", "几何间隔", "函数间隔", "最大间隔优化", "拉格朗日乘子", "KKT 条件", "软间隔", "Hinge Loss", "核技巧", "参数 C 与 gamma"],
    formulas: ["\\min_{w,b}\\frac{1}{2}\\lVert w\\rVert^2", "y_i(w^Tx_i+b)\\ge1", "\\ell(y,f(x))=\\max(0,1-yf(x))"],
    implementation: "svm",
  },
  {
    id: "09",
    file: "09_聚类_降维_PCA_GMM与EM算法.md",
    title: "聚类、降维、PCA、GMM 与 EM 算法",
    goal: "理解无监督学习中的结构发现、表示压缩和潜变量估计。",
    keywords: ["KMeans", "PCA", "协方差矩阵", "特征值分解", "GMM", "EM"],
    topics: ["无监督学习目标", "KMeans 目标函数", "KMeans 更新推导", "层次聚类", "DBSCAN", "PCA 最大方差", "PCA 最小重构误差", "GMM", "EM 算法", "聚类评估"],
    formulas: ["J=\\sum_i\\lVert x_i-\\mu_{c_i}\\rVert^2", "S=\\frac{1}{n}X^TX", "Q(\\theta,\\theta^{old})=\\mathbb{E}_{Z|X,\\theta^{old}}[\\log P(X,Z|\\theta)]"],
    implementation: "unsupervised",
  },
  {
    id: "10",
    file: "10_模型选择_正则化_泛化理论与调参.md",
    title: "模型选择、正则化、泛化理论与调参",
    goal: "建立调参和泛化分析能力，能解释模型为什么过拟合或欠拟合。",
    keywords: ["偏差方差", "L1", "L2", "交叉验证", "学习曲线", "网格搜索"],
    topics: ["训练误差与泛化误差", "偏差方差分解", "L2 正则化", "L1 正则化", "早停", "交叉验证", "网格搜索", "随机搜索", "贝叶斯优化直觉", "学习曲线诊断"],
    formulas: ["E[(y-\\hat{f}(x))^2]=Bias^2+Var+\\sigma^2", "J_\\lambda(\\theta)=J(\\theta)+\\lambda\\lVert\\theta\\rVert_2^2", "\\theta^*=\\arg\\min_\\theta \\mathcal{R}_{val}(\\theta)"],
    implementation: "model_selection",
  },
  {
    id: "11",
    file: "11_推荐系统_时间序列与异常检测.md",
    title: "推荐系统、时间序列与异常检测",
    goal: "把基础 ML 方法迁移到推荐、序列预测和异常检测三类常见业务问题。",
    keywords: ["协同过滤", "矩阵分解", "滑动窗口", "时间序列", "Isolation Forest", "异常分数"],
    topics: ["推荐系统问题定义", "用户物品矩阵", "矩阵分解", "隐式反馈", "召回与排序", "时间序列切分", "滑动窗口特征", "趋势与季节性", "异常检测", "业务指标"],
    formulas: ["\\hat{r}_{ui}=p_u^Tq_i+b_u+b_i+\\mu", "\\min_{P,Q}\\sum_{(u,i)\\in\\Omega}(r_{ui}-p_u^Tq_i)^2+\\lambda(\\lVert p_u\\rVert^2+\\lVert q_i\\rVert^2)", "score(x)=-\\log p(x)"],
    implementation: "applications",
  },
  {
    id: "12",
    file: "12_机器学习工程_MLOps_解释性与综合实战.md",
    title: "机器学习工程、MLOps、解释性与综合实战",
    goal: "把模型训练推进到可复现、可部署、可监控、可解释的工程闭环。",
    keywords: ["Pipeline", "模型保存", "版本管理", "漂移监控", "SHAP", "模型卡"],
    topics: ["项目结构", "数据版本", "实验追踪", "Pipeline 封装", "模型序列化", "批量推理", "在线推理", "漂移检测", "解释性方法", "模型卡与复盘"],
    formulas: ["PSI=\\sum_b(p_b-q_b)\\log\\frac{p_b}{q_b}", "SHAP_i=\\sum_{S\\subseteq F\\setminus\\{i\\}}\\frac{|S|!(M-|S|-1)!}{M!}[v(S\\cup\\{i\\})-v(S)]", "Risk=Impact\\times Probability"],
    implementation: "mlops",
  },
];

const notesByImplementation = {
  baseline: [
    "本章代码不追求复杂模型，而追求把数据、指标、随机种子、训练循环连接起来。",
    "你可以把它当作任何机器学习项目的最小骨架。",
  ],
  preprocess: [
    "本章代码重点是 Pipeline：预处理必须只在训练集拟合，再应用到验证集和测试集。",
    "这样可以避免把测试集统计量泄漏进训练过程。",
  ],
  linear: [
    "线性回归适合从零实现，因为它的损失、梯度和闭式解都非常清晰。",
    "建议同时比较正规方程和梯度下降的结果。",
  ],
  logistic: [
    "逻辑回归虽然名字带回归，但本质是概率分类模型。",
    "实现时要特别注意 sigmoid 的数值稳定性和交叉熵中的 log(0)。",
  ],
  bayes: [
    "朴素贝叶斯的关键不是复杂优化，而是概率估计和对数空间计算。",
    "文本分类中使用拉普拉斯平滑可以避免未见词导致概率为 0。",
  ],
  knn: [
    "KNN 的训练成本低，但预测时要计算距离，因此工程上常需要索引结构或近似搜索。",
    "特征缩放对 KNN 极其重要，因为距离会被量纲大的特征支配。",
  ],
  tree: [
    "树模型把复杂决策拆成一系列局部规则，优点是可解释，缺点是单棵树容易过拟合。",
    "随机森林通过样本随机和特征随机降低方差。",
  ],
  svm: [
    "SVM 的思想是先找决策边界，再最大化边界到最近样本的距离。",
    "核技巧让模型在高维特征空间中线性分类，而不必显式构造高维特征。",
  ],
  unsupervised: [
    "无监督学习没有标签，评估更依赖任务目标、可视化和外部业务信号。",
    "PCA、KMeans、GMM 都可以从优化目标推导出更新公式。",
  ],
  model_selection: [
    "调参不是玄学，而是围绕验证集误差、复杂度、方差和计算预算做搜索。",
    "学习曲线通常比单个分数更能解释模型下一步该怎么改。",
  ],
  applications: [
    "推荐、时间序列和异常检测都不是单个算法，而是一组数据建模方式。",
    "切分数据时要尊重时间顺序和业务可用信息。",
  ],
  mlops: [
    "工程化机器学习的目标不是把 notebook 跑通，而是让训练、推理、监控、复盘都能重复。",
    "模型上线后的数据分布可能变化，因此监控和再训练策略同样重要。",
  ],
};

const codeBlocks = {
  baseline: [
    "import numpy as np",
    "from sklearn.datasets import make_classification",
    "from sklearn.model_selection import train_test_split",
    "from sklearn.preprocessing import StandardScaler",
    "from sklearn.linear_model import LogisticRegression",
    "from sklearn.metrics import accuracy_score, log_loss",
    "",
    "RANDOM_STATE = 42",
    "",
    "X, y = make_classification(",
    "    n_samples=1000, n_features=12, n_informative=8,",
    "    n_redundant=2, random_state=RANDOM_STATE",
    ")",
    "",
    "X_train, X_tmp, y_train, y_tmp = train_test_split(",
    "    X, y, test_size=0.4, stratify=y, random_state=RANDOM_STATE",
    ")",
    "X_val, X_test, y_val, y_test = train_test_split(",
    "    X_tmp, y_tmp, test_size=0.5, stratify=y_tmp, random_state=RANDOM_STATE",
    ")",
    "",
    "scaler = StandardScaler().fit(X_train)",
    "X_train_s = scaler.transform(X_train)",
    "X_val_s = scaler.transform(X_val)",
    "X_test_s = scaler.transform(X_test)",
    "",
    "model = LogisticRegression(max_iter=1000)",
    "model.fit(X_train_s, y_train)",
    "",
    "for name, X_part, y_part in [('val', X_val_s, y_val), ('test', X_test_s, y_test)]:",
    "    prob = model.predict_proba(X_part)[:, 1]",
    "    pred = (prob >= 0.5).astype(int)",
    "    print(name, accuracy_score(y_part, pred), log_loss(y_part, prob))",
  ],
  preprocess: [
    "import numpy as np",
    "import pandas as pd",
    "from sklearn.compose import ColumnTransformer",
    "from sklearn.impute import SimpleImputer",
    "from sklearn.metrics import classification_report",
    "from sklearn.model_selection import train_test_split",
    "from sklearn.pipeline import Pipeline",
    "from sklearn.preprocessing import OneHotEncoder, StandardScaler",
    "from sklearn.linear_model import LogisticRegression",
    "",
    "df = pd.DataFrame({",
    "    'age': [18, 21, np.nan, 35, 42, 29, 51, 33],",
    "    'income': [3.2, 4.1, 5.0, np.nan, 9.2, 6.1, 10.5, 7.2],",
    "    'city': ['A', 'B', 'A', 'C', 'B', None, 'C', 'A'],",
    "    'label': [0, 0, 0, 1, 1, 0, 1, 1],",
    "})",
    "",
    "X = df.drop(columns='label')",
    "y = df['label']",
    "num_cols = ['age', 'income']",
    "cat_cols = ['city']",
    "",
    "numeric_pipe = Pipeline([",
    "    ('impute', SimpleImputer(strategy='median')),",
    "    ('scale', StandardScaler()),",
    "])",
    "categorical_pipe = Pipeline([",
    "    ('impute', SimpleImputer(strategy='most_frequent')),",
    "    ('onehot', OneHotEncoder(handle_unknown='ignore')),",
    "])",
    "preprocess = ColumnTransformer([",
    "    ('num', numeric_pipe, num_cols),",
    "    ('cat', categorical_pipe, cat_cols),",
    "])",
    "clf = Pipeline([('prep', preprocess), ('model', LogisticRegression())])",
    "X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)",
    "clf.fit(X_train, y_train)",
    "print(classification_report(y_test, clf.predict(X_test), zero_division=0))",
  ],
  linear: [
    "import numpy as np",
    "",
    "class LinearRegressionGD:",
    "    def __init__(self, lr=0.05, epochs=2000):",
    "        self.lr = lr",
    "        self.epochs = epochs",
    "        self.w = None",
    "        self.b = 0.0",
    "        self.losses = []",
    "",
    "    def fit(self, X, y):",
    "        X = np.asarray(X, dtype=float)",
    "        y = np.asarray(y, dtype=float)",
    "        n, d = X.shape",
    "        self.w = np.zeros(d)",
    "        self.b = 0.0",
    "        for _ in range(self.epochs):",
    "            pred = X @ self.w + self.b",
    "            err = pred - y",
    "            loss = 0.5 * np.mean(err ** 2)",
    "            grad_w = (X.T @ err) / n",
    "            grad_b = np.mean(err)",
    "            self.w -= self.lr * grad_w",
    "            self.b -= self.lr * grad_b",
    "            self.losses.append(loss)",
    "        return self",
    "",
    "    def predict(self, X):",
    "        return np.asarray(X) @ self.w + self.b",
    "",
    "rng = np.random.default_rng(42)",
    "X = rng.normal(size=(200, 3))",
    "true_w = np.array([2.0, -1.0, 0.5])",
    "y = X @ true_w + 0.3 + rng.normal(scale=0.2, size=200)",
    "model = LinearRegressionGD().fit(X, y)",
    "print(model.w, model.b, model.losses[-1])",
  ],
  logistic: [
    "import numpy as np",
    "",
    "class LogisticRegressionGD:",
    "    def __init__(self, lr=0.1, epochs=2000, l2=0.0):",
    "        self.lr = lr",
    "        self.epochs = epochs",
    "        self.l2 = l2",
    "",
    "    @staticmethod",
    "    def sigmoid(z):",
    "        z = np.clip(z, -40, 40)",
    "        return 1.0 / (1.0 + np.exp(-z))",
    "",
    "    def fit(self, X, y):",
    "        X = np.asarray(X, dtype=float)",
    "        y = np.asarray(y, dtype=float)",
    "        n, d = X.shape",
    "        self.w = np.zeros(d)",
    "        self.b = 0.0",
    "        self.losses = []",
    "        for _ in range(self.epochs):",
    "            p = self.sigmoid(X @ self.w + self.b)",
    "            eps = 1e-12",
    "            loss = -np.mean(y*np.log(p+eps) + (1-y)*np.log(1-p+eps))",
    "            loss += self.l2 * np.sum(self.w ** 2)",
    "            grad_w = (X.T @ (p - y)) / n + 2 * self.l2 * self.w",
    "            grad_b = np.mean(p - y)",
    "            self.w -= self.lr * grad_w",
    "            self.b -= self.lr * grad_b",
    "            self.losses.append(loss)",
    "        return self",
    "",
    "    def predict_proba(self, X):",
    "        return self.sigmoid(np.asarray(X) @ self.w + self.b)",
    "",
    "    def predict(self, X, threshold=0.5):",
    "        return (self.predict_proba(X) >= threshold).astype(int)",
  ],
  bayes: [
    "import numpy as np",
    "",
    "class MultinomialNBScratch:",
    "    def __init__(self, alpha=1.0):",
    "        self.alpha = alpha",
    "",
    "    def fit(self, X, y):",
    "        X = np.asarray(X, dtype=float)",
    "        y = np.asarray(y)",
    "        self.classes_ = np.unique(y)",
    "        n_features = X.shape[1]",
    "        self.log_prior_ = []",
    "        self.log_likelihood_ = []",
    "        for c in self.classes_:",
    "            Xc = X[y == c]",
    "            prior = Xc.shape[0] / X.shape[0]",
    "            counts = Xc.sum(axis=0) + self.alpha",
    "            probs = counts / counts.sum()",
    "            self.log_prior_.append(np.log(prior))",
    "            self.log_likelihood_.append(np.log(probs))",
    "        self.log_prior_ = np.array(self.log_prior_)",
    "        self.log_likelihood_ = np.vstack(self.log_likelihood_)",
    "        return self",
    "",
    "    def predict_log_proba(self, X):",
    "        return np.asarray(X) @ self.log_likelihood_.T + self.log_prior_",
    "",
    "    def predict(self, X):",
    "        return self.classes_[np.argmax(self.predict_log_proba(X), axis=1)]",
    "",
    "X = np.array([[2, 1, 0], [1, 0, 1], [0, 2, 3], [0, 1, 4]])",
    "y = np.array(['tech', 'tech', 'sport', 'sport'])",
    "print(MultinomialNBScratch().fit(X, y).predict([[1, 0, 0], [0, 1, 2]]))",
  ],
  knn: [
    "import numpy as np",
    "from collections import Counter",
    "",
    "class KNNClassifier:",
    "    def __init__(self, k=5):",
    "        self.k = k",
    "",
    "    def fit(self, X, y):",
    "        self.X_train = np.asarray(X, dtype=float)",
    "        self.y_train = np.asarray(y)",
    "        return self",
    "",
    "    def _distances(self, x):",
    "        diff = self.X_train - x",
    "        return np.sqrt(np.sum(diff * diff, axis=1))",
    "",
    "    def predict_one(self, x):",
    "        dist = self._distances(x)",
    "        idx = np.argsort(dist)[:self.k]",
    "        votes = Counter(self.y_train[idx])",
    "        return votes.most_common(1)[0][0]",
    "",
    "    def predict(self, X):",
    "        return np.array([self.predict_one(x) for x in np.asarray(X, dtype=float)])",
    "",
    "def rbf_kernel(X, Z, gamma=1.0):",
    "    X2 = np.sum(X * X, axis=1, keepdims=True)",
    "    Z2 = np.sum(Z * Z, axis=1, keepdims=True).T",
    "    dist2 = X2 + Z2 - 2 * X @ Z.T",
    "    return np.exp(-gamma * dist2)",
  ],
  tree: [
    "import numpy as np",
    "",
    "def gini(y):",
    "    values, counts = np.unique(y, return_counts=True)",
    "    p = counts / counts.sum()",
    "    return 1.0 - np.sum(p ** 2)",
    "",
    "def best_stump_split(X, y):",
    "    X = np.asarray(X, dtype=float)",
    "    y = np.asarray(y)",
    "    n, d = X.shape",
    "    best = {'feature': None, 'threshold': None, 'score': np.inf}",
    "    for j in range(d):",
    "        thresholds = np.unique(X[:, j])",
    "        for t in thresholds:",
    "            left = X[:, j] <= t",
    "            right = ~left",
    "            if left.sum() == 0 or right.sum() == 0:",
    "                continue",
    "            score = left.mean() * gini(y[left]) + right.mean() * gini(y[right])",
    "            if score < best['score']:",
    "                best = {'feature': j, 'threshold': t, 'score': score}",
    "    return best",
    "",
    "X = np.array([[0.1, 1.0], [0.2, 0.8], [0.8, 0.3], [0.9, 0.2]])",
    "y = np.array([0, 0, 1, 1])",
    "print(best_stump_split(X, y))",
  ],
  svm: [
    "import numpy as np",
    "",
    "class LinearSVM:",
    "    def __init__(self, lr=0.01, epochs=2000, C=1.0):",
    "        self.lr = lr",
    "        self.epochs = epochs",
    "        self.C = C",
    "",
    "    def fit(self, X, y):",
    "        X = np.asarray(X, dtype=float)",
    "        y = np.where(np.asarray(y) > 0, 1.0, -1.0)",
    "        n, d = X.shape",
    "        self.w = np.zeros(d)",
    "        self.b = 0.0",
    "        for _ in range(self.epochs):",
    "            margins = y * (X @ self.w + self.b)",
    "            active = margins < 1",
    "            grad_w = self.w - self.C * (X[active].T @ y[active]) / n",
    "            grad_b = -self.C * np.sum(y[active]) / n",
    "            self.w -= self.lr * grad_w",
    "            self.b -= self.lr * grad_b",
    "        return self",
    "",
    "    def decision_function(self, X):",
    "        return np.asarray(X) @ self.w + self.b",
    "",
    "    def predict(self, X):",
    "        return np.where(self.decision_function(X) >= 0, 1, -1)",
  ],
  unsupervised: [
    "import numpy as np",
    "",
    "def kmeans(X, k, steps=50, seed=42):",
    "    rng = np.random.default_rng(seed)",
    "    X = np.asarray(X, dtype=float)",
    "    centers = X[rng.choice(len(X), size=k, replace=False)].copy()",
    "    for _ in range(steps):",
    "        dist2 = ((X[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)",
    "        label = np.argmin(dist2, axis=1)",
    "        new_centers = np.vstack([X[label == c].mean(axis=0) for c in range(k)])",
    "        if np.allclose(new_centers, centers, equal_nan=False):",
    "            break",
    "        centers = new_centers",
    "    return centers, label",
    "",
    "def pca_project(X, n_components=2):",
    "    X = np.asarray(X, dtype=float)",
    "    Xc = X - X.mean(axis=0)",
    "    cov = Xc.T @ Xc / len(Xc)",
    "    values, vectors = np.linalg.eigh(cov)",
    "    order = np.argsort(values)[::-1]",
    "    W = vectors[:, order[:n_components]]",
    "    return Xc @ W, W, values[order]",
  ],
  model_selection: [
    "import numpy as np",
    "from sklearn.datasets import make_regression",
    "from sklearn.linear_model import Ridge",
    "from sklearn.model_selection import GridSearchCV, KFold",
    "from sklearn.pipeline import Pipeline",
    "from sklearn.preprocessing import StandardScaler, PolynomialFeatures",
    "",
    "X, y = make_regression(n_samples=300, n_features=5, noise=12.0, random_state=42)",
    "pipe = Pipeline([",
    "    ('poly', PolynomialFeatures(include_bias=False)),",
    "    ('scale', StandardScaler()),",
    "    ('model', Ridge()),",
    "])",
    "param_grid = {",
    "    'poly__degree': [1, 2, 3],",
    "    'model__alpha': [0.01, 0.1, 1.0, 10.0, 100.0],",
    "}",
    "cv = KFold(n_splits=5, shuffle=True, random_state=42)",
    "search = GridSearchCV(pipe, param_grid, cv=cv, scoring='neg_root_mean_squared_error')",
    "search.fit(X, y)",
    "print(search.best_params_, -search.best_score_)",
  ],
  applications: [
    "import numpy as np",
    "",
    "class MatrixFactorization:",
    "    def __init__(self, k=8, lr=0.03, reg=0.02, epochs=50):",
    "        self.k = k",
    "        self.lr = lr",
    "        self.reg = reg",
    "        self.epochs = epochs",
    "",
    "    def fit(self, triples, n_users, n_items):",
    "        rng = np.random.default_rng(42)",
    "        self.P = 0.1 * rng.normal(size=(n_users, self.k))",
    "        self.Q = 0.1 * rng.normal(size=(n_items, self.k))",
    "        self.mu = np.mean([r for _, _, r in triples])",
    "        for _ in range(self.epochs):",
    "            for u, i, r in triples:",
    "                pred = self.mu + self.P[u] @ self.Q[i]",
    "                err = pred - r",
    "                pu = self.P[u].copy()",
    "                qi = self.Q[i].copy()",
    "                self.P[u] -= self.lr * (err * qi + self.reg * pu)",
    "                self.Q[i] -= self.lr * (err * pu + self.reg * qi)",
    "        return self",
    "",
    "    def predict(self, u, i):",
    "        return self.mu + self.P[u] @ self.Q[i]",
  ],
  mlops: [
    "import joblib",
    "import numpy as np",
    "from sklearn.datasets import make_classification",
    "from sklearn.linear_model import LogisticRegression",
    "from sklearn.metrics import roc_auc_score",
    "from sklearn.model_selection import train_test_split",
    "from sklearn.pipeline import Pipeline",
    "from sklearn.preprocessing import StandardScaler",
    "",
    "X, y = make_classification(n_samples=500, n_features=10, random_state=42)",
    "X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, stratify=y)",
    "pipeline = Pipeline([",
    "    ('scale', StandardScaler()),",
    "    ('model', LogisticRegression(max_iter=1000)),",
    "])",
    "pipeline.fit(X_train, y_train)",
    "prob = pipeline.predict_proba(X_test)[:, 1]",
    "metrics = {'auc': float(roc_auc_score(y_test, prob)), 'n_test': int(len(y_test))}",
    "joblib.dump({'pipeline': pipeline, 'metrics': metrics}, 'ml_model.joblib')",
    "loaded = joblib.load('ml_model.joblib')",
    "print(loaded['metrics'])",
  ],
};

function slugVar(text, idx) {
  return `topic_${idx}_${text.length}`;
}

function addWrapped(lines, prefix, text) {
  const chunks = text.split("。").filter(Boolean);
  for (const chunk of chunks) {
    lines.push(`${prefix}${chunk}。`);
  }
}

function section(ch, topic, idx) {
  const lines = [];
  const v = slugVar(topic, idx);
  lines.push(`## ${ch.id}.${String(idx).padStart(2, "0")} ${topic}`);
  lines.push("");
  lines.push("### 学习目标");
  lines.push("");
  lines.push(`1. 能用自己的话解释“${topic}”解决什么问题。`);
  lines.push(`2. 能写出本节最核心的数学表达式，并知道每个符号的含义。`);
  lines.push(`3. 能把公式翻译成 NumPy 或 Scikit-learn 代码。`);
  lines.push(`4. 能判断本节方法在什么数据条件下会失效。`);
  lines.push("");
  lines.push("### 核心概念");
  lines.push("");
  const conceptText = [
    `${topic}不是孤立技巧，而是数据、假设、目标函数和优化过程共同作用的结果`,
    `学习时先问输入是什么、输出是什么、模型假设是什么、评价指标是什么`,
    `如果模型假设与数据生成机制差距过大，即使优化过程正确，泛化效果也可能很差`,
    `如果数据预处理方式错误，后续再复杂的模型也会把错误放大`,
    `机器学习的关键习惯是把每个结论落到可观测实验，而不是只记名称`,
    `本节涉及的变量都默认按矩阵形式组织，这样便于向量化实现`,
    `向量化不仅让代码更快，也让推导更贴近线性代数表达`,
    `训练误差下降不等于模型可用，必须同时观察验证集或交叉验证结果`,
    `当模型表现异常时，优先检查数据切分、标签、尺度、缺失值和随机种子`,
    `真正掌握一个算法，至少要能说清目标函数、优化变量、更新规则和适用边界`,
  ];
  for (const item of conceptText) lines.push(`- ${item}。`);
  lines.push("");
  lines.push("### 数学符号");
  lines.push("");
  lines.push(`- $X\\in\\mathbb{R}^{n\\times d}$：包含 $n$ 个样本、$d$ 个特征的设计矩阵。`);
  lines.push(`- $x_i\\in\\mathbb{R}^{d}$：第 $i$ 个样本的特征向量。`);
  lines.push(`- $y_i$：第 $i$ 个样本的监督信号，可能是类别、实数或排序反馈。`);
  lines.push(`- $\\theta$：模型中需要学习的参数集合。`);
  lines.push(`- $\\ell(\\hat{y}_i,y_i)$：单个样本上的损失函数。`);
  lines.push(`- $J(\\theta)$：所有样本损失与正则项组成的优化目标。`);
  lines.push(`- $\\eta$：学习率，控制每次参数更新的步长。`);
  lines.push(`- ${ch.formulas.map((f) => `$${f}$`).join("；")}。`);
  lines.push("");
  lines.push("### 推导 1：从预测函数到经验风险");
  lines.push("");
  lines.push(`1. 设模型对样本 $x_i$ 的预测为 $\\hat{y}_i=f(x_i;\\theta)$。`);
  lines.push(`2. 用损失函数度量预测与真实值的差异：$\\ell_i=\\ell(\\hat{y}_i,y_i)$。`);
  lines.push(`3. 训练集上共有 $n$ 个样本，因此平均损失写作：`);
  lines.push("");
  lines.push("$$");
  lines.push("\\mathcal{R}_{emp}(\\theta)=\\frac{1}{n}\\sum_{i=1}^{n}\\ell(f(x_i;\\theta),y_i)");
  lines.push("$$");
  lines.push("");
  lines.push(`4. 如果加入正则项 $\\Omega(\\theta)$，目标函数变为：`);
  lines.push("");
  lines.push("$$");
  lines.push("J(\\theta)=\\mathcal{R}_{emp}(\\theta)+\\lambda\\Omega(\\theta)");
  lines.push("$$");
  lines.push("");
  lines.push(`5. ${topic}中的建模选择，本质上是在改变 $f$、$\\ell$ 或 $\\Omega$ 的具体形式。`);
  lines.push(`6. 当 $\\lambda=0$ 时，模型只关心训练误差，可能更容易过拟合。`);
  lines.push(`7. 当 $\\lambda$ 太大时，模型过度偏向简单参数，可能欠拟合。`);
  lines.push(`8. 因此学习过程需要在拟合能力和复杂度约束之间取平衡。`);
  lines.push("");
  lines.push("### 推导 2：梯度下降的一般形式");
  lines.push("");
  lines.push(`1. 对目标函数 $J(\\theta)$ 求导，得到当前位置最陡上升方向 $\\nabla_\\theta J(\\theta)$。`);
  lines.push(`2. 为了让损失下降，参数沿负梯度方向移动：`);
  lines.push("");
  lines.push("$$");
  lines.push("\\theta_{t+1}=\\theta_t-\\eta\\nabla_\\theta J(\\theta_t)");
  lines.push("$$");
  lines.push("");
  lines.push(`3. 若 $\\eta$ 太小，收敛缓慢；若 $\\eta$ 太大，损失可能震荡或发散。`);
  lines.push(`4. 批量梯度下降使用全部样本估计梯度，稳定但每步较慢。`);
  lines.push(`5. 随机梯度下降使用单个或小批量样本估计梯度，噪声更大但更新更频繁。`);
  lines.push(`6. 小批量梯度下降是深度学习和大规模机器学习中最常见的折中。`);
  lines.push(`7. 如果目标函数是凸函数，合适学习率下可收敛到全局最优或其附近。`);
  lines.push(`8. 如果目标函数非凸，训练结果还会受到初始化、批量顺序和优化器影响。`);
  lines.push("");
  lines.push("### 推导 3：矩阵形式的好处");
  lines.push("");
  lines.push(`1. 单样本计算清晰，但循环写法容易慢，也容易隐藏维度错误。`);
  lines.push(`2. 把样本堆叠成矩阵后，预测可统一写成 $\\hat{y}=f(X;\\theta)$。`);
  lines.push(`3. 对线性部分，常见形式是 $z=Xw+b\\mathbf{1}$。`);
  lines.push(`4. 对损失函数，常见形式是所有样本损失取均值。`);
  lines.push(`5. 对梯度，常见形式会出现 $X^T$，因为每个特征都要累加所有样本的误差信号。`);
  lines.push(`6. 维度检查是推导中的保险：$X^T e$ 的形状是 $d\\times1$，正好对应 $w$。`);
  lines.push(`7. 代码实现时，优先让数组形状与公式保持一致。`);
  lines.push(`8. 如果广播规则让代码“刚好能跑”，也要检查它是否真的表达了公式。`);
  lines.push("");
  lines.push("### 代码实现：本节最小实验");
  lines.push("");
  lines.push("```python");
  lines.push("import numpy as np");
  lines.push("");
  lines.push(`def ${v}_standardize(X_train, X_test):`);
  lines.push("    X_train = np.asarray(X_train, dtype=float)");
  lines.push("    X_test = np.asarray(X_test, dtype=float)");
  lines.push("    mu = X_train.mean(axis=0)");
  lines.push("    sigma = X_train.std(axis=0) + 1e-12");
  lines.push("    return (X_train - mu) / sigma, (X_test - mu) / sigma");
  lines.push("");
  lines.push(`def ${v}_mse(y_true, y_pred):`);
  lines.push("    y_true = np.asarray(y_true, dtype=float)");
  lines.push("    y_pred = np.asarray(y_pred, dtype=float)");
  lines.push("    return np.mean((y_true - y_pred) ** 2)");
  lines.push("");
  lines.push(`def ${v}_train_linear_baseline(X, y, lr=0.05, epochs=300):`);
  lines.push("    X = np.asarray(X, dtype=float)");
  lines.push("    y = np.asarray(y, dtype=float)");
  lines.push("    n, d = X.shape");
  lines.push("    w = np.zeros(d)");
  lines.push("    b = 0.0");
  lines.push("    history = []");
  lines.push("    for step in range(epochs):");
  lines.push("        pred = X @ w + b");
  lines.push("        err = pred - y");
  lines.push("        loss = 0.5 * np.mean(err ** 2)");
  lines.push("        grad_w = X.T @ err / n");
  lines.push("        grad_b = np.mean(err)");
  lines.push("        w -= lr * grad_w");
  lines.push("        b -= lr * grad_b");
  lines.push("        if step % 20 == 0:");
  lines.push("            history.append(float(loss))");
  lines.push("    return w, b, history");
  lines.push("");
  lines.push("# 运行建议：把本节函数接入真实数据，再比较训练集和验证集误差。");
  lines.push("```");
  lines.push("");
  lines.push("### 实验检查点");
  lines.push("");
  lines.push(`- 检查输入矩阵是否存在缺失值、无穷值或明显异常量纲。`);
  lines.push(`- 检查训练集和验证集是否使用同一个随机种子可复现切分。`);
  lines.push(`- 检查只在训练集拟合标准化参数，再应用到验证集和测试集。`);
  lines.push(`- 检查损失曲线是否整体下降，而不是一开始就发散。`);
  lines.push(`- 检查模型在训练集和验证集上的差距，判断是否过拟合。`);
  lines.push(`- 检查预测结果的分布是否符合任务常识。`);
  lines.push(`- 检查指标是否和业务目标一致，例如排序任务不要只看准确率。`);
  lines.push(`- 检查是否记录了数据版本、代码版本、参数和随机种子。`);
  lines.push("");
  lines.push("### 常见错误");
  lines.push("");
  lines.push(`1. 把测试集参与特征选择、标准化拟合或调参，造成数据泄漏。`);
  lines.push(`2. 只报告最好的单次结果，不报告随机种子和方差。`);
  lines.push(`3. 没有确认标签含义，导致把反向标签当成正向标签。`);
  lines.push(`4. 忽略类别不平衡，在极端数据上被准确率误导。`);
  lines.push(`5. 不看残差、不看混淆矩阵、不看错误样本，只盯一个总分。`);
  lines.push(`6. 公式会背，但写代码时没有做维度检查。`);
  lines.push(`7. 训练集表现很好就停止分析，没有解释泛化能力。`);
  lines.push(`8. 不保存实验配置，导致结果无法复现。`);
  lines.push("");
  lines.push("### 小结");
  lines.push("");
  addWrapped(lines, "", `${topic}这一节要把概念、公式、代码和实验四件事连起来`);
  addWrapped(lines, "", `如果只能记住一个原则，就是任何模型选择都要回到数据假设和评价目标`);
  addWrapped(lines, "", `当你能从目标函数推到梯度，再从梯度写出更新代码，本节就算真正过关`);
  lines.push("");
  return lines;
}

function fullCode(ch) {
  const lines = [];
  lines.push("## 本章完整代码实现");
  lines.push("");
  for (const note of notesByImplementation[ch.implementation]) {
    lines.push(`- ${note}`);
  }
  lines.push("");
  lines.push("```python");
  for (const line of codeBlocks[ch.implementation]) lines.push(line);
  lines.push("```");
  lines.push("");
  return lines;
}

function generateChapter(ch) {
  const lines = [];
  lines.push(`# 第 ${Number(ch.id)} 章 ${ch.title}`);
  lines.push("");
  lines.push(`> ${ch.goal}`);
  lines.push("");
  lines.push("---");
  lines.push("");
  lines.push("## 章节定位");
  lines.push("");
  lines.push(`本章属于机器学习知识体系中的第 ${Number(ch.id)} 章。它的任务不是孤立记忆算法名，而是把问题定义、数学推导、代码实现、实验验证和错误分析放在同一个框架里。`);
  lines.push("");
  lines.push("### 本章关键词");
  lines.push("");
  for (const keyword of ch.keywords) lines.push(`- ${keyword}`);
  lines.push("");
  lines.push("### 学习完成标准");
  lines.push("");
  lines.push("1. 能画出本章方法从输入到输出的数据流。");
  lines.push("2. 能写出主要目标函数，并说明每一项的意义。");
  lines.push("3. 能手推至少一个关键梯度或更新公式。");
  lines.push("4. 能用 NumPy 或 Scikit-learn 实现最小可运行实验。");
  lines.push("5. 能解释训练误差、验证误差和测试误差的差别。");
  lines.push("6. 能列出至少三种常见失败原因和对应排查方法。");
  lines.push("");
  lines.push("### 学习路线");
  lines.push("");
  lines.push("```text");
  lines.push("概念定义 -> 数学符号 -> 目标函数 -> 推导更新 -> 代码实现 -> 实验诊断 -> 复盘");
  lines.push("```");
  lines.push("");
  lines.push("### 先记住的三个公式");
  lines.push("");
  for (const f of ch.formulas) {
    lines.push("$$");
    lines.push(f);
    lines.push("$$");
    lines.push("");
  }
  lines.push("### 本章目录");
  lines.push("");
  ch.topics.forEach((topic, i) => {
    lines.push(`${i + 1}. ${topic}`);
  });
  lines.push("");
  lines.push("---");
  lines.push("");
  ch.topics.forEach((topic, i) => {
    lines.push(...section(ch, topic, i + 1));
  });
  lines.push(...fullCode(ch));
  lines.push("## 复习题");
  lines.push("");
  for (let i = 1; i <= 20; i++) {
    const topic = ch.topics[(i - 1) % ch.topics.length];
    lines.push(`${i}. 解释“${topic}”中的输入、输出、参数和评价指标。`);
    lines.push(`   - 写出一个可能的数据泄漏场景。`);
    lines.push(`   - 写出一个可运行的最小实验设计。`);
  }
  lines.push("");
  lines.push("## 章节复盘模板");
  lines.push("");
  lines.push("- 我真正理解的公式：");
  lines.push("- 我能独立写出的代码：");
  lines.push("- 我还容易混淆的概念：");
  lines.push("- 我在实验中观察到的现象：");
  lines.push("- 下次遇到类似任务时的第一步：");
  lines.push("");
  return lines.join("\n");
}

function generateReadme() {
  const lines = [];
  lines.push("# 机器学习完全学习手册");
  lines.push("");
  lines.push("> 面向机器学习课程、数学推导、实验代码和工程实践的系统笔记。");
  lines.push("> 本目录采用和 ANN、DIP、Algorithm 类似的组织方式：总览 README + 分章知识笔记 + 项目实践。");
  lines.push("");
  lines.push("---");
  lines.push("");
  lines.push("## 目录结构");
  lines.push("");
  lines.push("```text");
  lines.push("ML(Machine Learning)/");
  lines.push("├── README.md");
  lines.push("├── chapters/");
  for (const ch of chapters) lines.push(`│   ├── ${ch.file}`);
  lines.push("├── projects/");
  lines.push("│   └── README.md");
  lines.push("└── tools/");
  lines.push("    └── generate_ml_notes.mjs");
  lines.push("```");
  lines.push("");
  lines.push("## 推荐学习顺序");
  lines.push("");
  lines.push("| 周次 | 阅读章节 | 实验重点 | 目标 |");
  lines.push("|------|----------|----------|------|");
  chapters.forEach((ch, idx) => {
    lines.push(`| 第 ${idx + 1} 周 | Ch ${ch.id} | ${ch.keywords.slice(0, 3).join("、")} | ${ch.goal} |`);
  });
  lines.push("");
  lines.push("## 章节入口");
  lines.push("");
  chapters.forEach((ch, idx) => {
    lines.push(`${idx + 1}. [${ch.title}](chapters/${ch.file})`);
  });
  lines.push("");
  lines.push("## 学习原则");
  lines.push("");
  lines.push("1. 先明确任务，再选择模型。");
  lines.push("2. 先写最小 baseline，再堆复杂方法。");
  lines.push("3. 先看数据，再看指标。");
  lines.push("4. 先防止数据泄漏，再讨论调参。");
  lines.push("5. 每个算法至少掌握一条数学推导和一份可运行代码。");
  lines.push("6. 每次实验都记录随机种子、数据切分、指标和结论。");
  lines.push("");
  lines.push("## 与 ANN 笔记的关系");
  lines.push("");
  lines.push("传统机器学习重点是小中规模数据、特征工程、可解释模型和经典优化。ANN 笔记重点是神经网络、反向传播、深度结构和大规模训练。建议先学本目录前 10 章，再进入 ANN 目录。");
  lines.push("");
  return lines.join("\n");
}

function generateProjectsReadme() {
  const lines = [];
  lines.push("# 机器学习项目实践");
  lines.push("");
  lines.push("这些项目用于把分章笔记中的公式和代码落到可运行实验。");
  lines.push("");
  lines.push("## 建议项目");
  lines.push("");
  lines.push("1. `01_tabular_baseline`：表格分类 baseline，练习数据切分、Pipeline、指标报告。");
  lines.push("2. `02_linear_regression_from_scratch`：从零实现线性回归，比较闭式解和梯度下降。");
  lines.push("3. `03_logistic_regression_from_scratch`：从零实现逻辑回归，观察交叉熵下降。");
  lines.push("4. `04_text_naive_bayes`：使用词袋模型和朴素贝叶斯完成文本分类。");
  lines.push("5. `05_tree_ensemble`：比较决策树、随机森林和梯度提升。");
  lines.push("6. `06_unsupervised_lab`：用 KMeans、PCA、GMM 做聚类与可视化。");
  lines.push("7. `07_model_selection_lab`：用交叉验证、学习曲线和网格搜索调参。");
  lines.push("8. `08_mlops_mini_pipeline`：训练、保存、加载、监控一个简单模型。");
  lines.push("");
  lines.push("## 每个项目的最低要求");
  lines.push("");
  lines.push("- 有固定随机种子。");
  lines.push("- 有训练集、验证集、测试集或交叉验证。");
  lines.push("- 有至少一个 baseline。");
  lines.push("- 有指标报告和错误样本分析。");
  lines.push("- 有实验结论，不只保存代码。");
  lines.push("");
  return lines.join("\n");
}

mkdirSync(join(root, "chapters"), { recursive: true });
mkdirSync(join(root, "projects"), { recursive: true });

writeFileSync(join(root, "README.md"), generateReadme(), "utf8");
writeFileSync(join(root, "projects", "README.md"), generateProjectsReadme(), "utf8");
for (const ch of chapters) {
  writeFileSync(join(root, "chapters", ch.file), generateChapter(ch), "utf8");
}

console.log(`Generated ${chapters.length} chapters in ${join(root, "chapters")}`);
