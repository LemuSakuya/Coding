# 项目 03 CIFAR-10 卷积神经网络训练

## 项目目标

在 CIFAR-10 上训练一个基础 CNN，理解卷积网络如何处理彩色图像，并体会“卷积先验 + 数据增强 + 归一化”对视觉任务的重要性。

---

## 你将学到什么

1. CNN 在图像任务上的结构优势。
2. 如何计算卷积层输出尺寸与参数量。
3. 如何使用数据增强提升泛化能力。
4. 如何通过 BatchNorm、Dropout 和学习率调度稳定训练。
5. 如何分析 CIFAR-10 上的类别混淆。

---

## 数据集

CIFAR-10 包含 10 个类别，每张图像大小为 32x32 彩色图片。

常见类别包括：

- airplane
- automobile
- bird
- cat
- deer
- dog
- frog
- horse
- ship
- truck

---

## 建议结构

```text
Conv -> ReLU -> Conv -> ReLU -> Pool -> Conv -> ReLU -> Pool -> FC -> FC
```

你也可以加上：

- BatchNorm
- Dropout
- Global Average Pooling
- Residual block

---

## 实现步骤

### 第 1 步：准备数据

完成训练集增强和测试集标准化。

### 第 2 步：定义 CNN

先做一个基础版本，确保可以正常跑通。

### 第 3 步：训练模型

记录 loss、accuracy 和每类召回情况。

### 第 4 步：比较不同结构

对比纯 MLP 与 CNN 的效果差异。

### 第 5 步：做错误分析

观察哪些类别最容易混淆，例如猫和狗、汽车和卡车。

---

## 建议文件结构

```text
model.py
train.py
evaluate.py
visualize.py
notes.md
```

---

## 训练建议

- 使用 Adam 或 SGD + Momentum。
- 使用数据增强：随机裁剪、翻转、颜色扰动。
- 合理使用学习率衰减。
- 观察验证集曲线，防止过拟合。

---

## 快速开始

安装依赖并运行最小训练：

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python train.py
```

如果 CIFAR-10 无法下载，可使用 FakeData 进行烟雾测试：

```bash
python -c "import sys; sys.path.append('e:/VSCode/Coding/CS Learning/人工神经网络/projects/03_cifar10_cnn'); from model import SimpleCIFARNet; import torch; from torchvision.datasets import FakeData; from torchvision import transforms; from torch.utils.data import DataLoader; transform=transforms.Compose([transforms.ToTensor()]); ds=FakeData(size=256, image_size=(3,32,32), num_classes=10, transform=transform); loader=DataLoader(ds,batch_size=64); device=torch.device('cpu'); model=SimpleCIFARNet().to(device); opt=torch.optim.SGD(model.parameters(), lr=1e-2); crit=torch.nn.CrossEntropyLoss(); X,y=next(iter(loader)); X,y=X.to(device),y.to(device); opt.zero_grad(); logits=model(X); loss=crit(logits,y); loss.backward(); opt.step(); print('CIFAR fake train batch done, loss=',loss.item())"
```


## 常见问题

1. 输入通道数写错，导致卷积层报错。
2. 卷积输出尺寸计算不一致。
3. 数据增强过强，反而伤害训练。
4. 没有 BatchNorm 时训练容易不稳定。
5. 只追求训练集准确率，忽视测试集效果。

---

## 扩展任务

1. 实现一个更深的 CNN。
2. 使用残差连接改进模型。
3. 尝试轻量卷积网络。
4. 比较不同增强策略的效果。

---

## 预期成果

你应该能得到：

- 一个可复现的 CIFAR-10 CNN 训练脚本；
- 一组训练曲线和混淆矩阵；
- 一份关于 CNN 视觉先验的总结；
- 一个与 MLP 的横向对比实验。
