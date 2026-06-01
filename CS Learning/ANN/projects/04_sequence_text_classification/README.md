# 项目 04 序列分类与注意力实验

## 项目目标

完成一个简单的序列分类任务，例如情感分析或主题分类，理解 RNN / LSTM / GRU / 注意力机制在序列数据上的作用。

---

## 你将学到什么

1. 如何把文本转成序列输入。
2. 如何使用词表、Embedding 和 padding 处理变长文本。
3. 如何使用 RNN、LSTM 或 GRU 做分类。
4. 如何添加简化注意力机制增强表示能力。
5. 如何分析长序列、罕见词和类别不平衡问题。

---

## 数据建议

你可以选择以下任一类任务：

- 电影评论情感分类
- 新闻主题分类
- 简短句子意图识别
- 时间序列异常分类

数据规模不必太大，重点是把流程走通。

---

## 建议结构

```text
文本 -> 分词/编码 -> Embedding -> RNN/LSTM/GRU -> 分类器
```

也可以加入：

- Attention pooling
- 双向 RNN
- Mask 机制

---

## 实现步骤

### 第 1 步：文本预处理

完成分词、构建词表、将文本映射为 id 序列。

### 第 2 步：处理变长序列

对短句进行 padding，对超长文本进行截断。

### 第 3 步：定义模型

先做一个基础 RNN / GRU 分类器，再加注意力模块。

### 第 4 步：训练与评估

记录训练损失、验证损失、准确率和 F1。

### 第 5 步：分析样本

看看哪些句子容易被错分，是否和长依赖、否定词或歧义有关。

---

## 建议文件结构

```text
dataset.py
model.py
train.py
evaluate.py
notes.md
```

---

## 训练建议

- Embedding 维度不要一开始就设太大。
- 序列任务特别关注 padding 和 mask。
- 如果长依赖明显，可以尝试 LSTM 或注意力。
- 文本任务里类别不平衡时要关注 F1 而不是只看 accuracy。

---

## 常见问题

1. 词表构建错误，导致未知词太多。
2. padding 没处理好，影响模型学习。
3. 序列长度太长，训练速度慢。
4. RNN 容易梯度消失，效果不稳定。
5. 注意力权重没有 mask 掉 padding 部分。

---

## 扩展任务

1. 比较 RNN、LSTM 和 GRU 的效果。
2. 增加双向结构。
3. 加入简化自注意力。
4. 将文本分类改成时间序列预测。

---

## 预期成果

你应该能得到：

- 一个完整的序列分类训练脚本；
- 一份模型对比实验结果；
- 一组注意力或序列权重可视化图；
- 一份关于序列建模难点的总结。

## 快速开始

安装依赖并运行最小示例（模板）：

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
# 准备一个简单 DataLoader 或使用 FakeData 来做前向/训练烟雾测试
python -c "import sys; sys.path.append('e:/VSCode/Coding/CS Learning/人工神经网络/projects/04_sequence_text_classification'); from model import SimpleRNNClassifier; import torch; m=SimpleRNNClassifier(vocab_size=100); x=torch.randint(0,100,(4,10)); out=m(x); print('sequence forward output shape=', out.shape)"
```

> 说明：本项目 README 提供训练模板；请根据具体任务实现 `dataset.py` 或把真实数据预处理成 `(input_ids, label)` 的 DataLoader。
