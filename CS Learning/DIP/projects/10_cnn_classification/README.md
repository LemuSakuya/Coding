# 项目 10：CNN 图像分类（PyTorch 迁移学习）

> 对应章节：第 12 章
> 目标：用 PyTorch + 预训练 ResNet18 做 CIFAR-10 / 自定义图像集分类，完成深度学习闭环。

## 包含内容

- CIFAR-10 自动下载与数据增强
- 预训练 ResNet18 迁移学习（冻结底层或微调全部）
- 训练 / 验证循环 + 学习率调度
- 保存 / 加载 `best.pt`
- 单张图推理

## 运行

```bash
# 训练 (默认 CIFAR-10, 5 epoch)
python main.py --mode train --epochs 5 --batch 128

# 从保存权重继续
python main.py --mode train --resume checkpoints/best.pt

# 推理
python main.py --mode predict --image cat.jpg
```

## 预期效果

- CPU 5 epoch：约 10 分钟，Top-1 ~82%
- GPU (RTX 3060) 20 epoch：约 10 分钟，Top-1 ~92%

## 延伸题目

- 切换 `ResNet50`、`ConvNeXt-Tiny`、`ViT-B/16`，对比参数与精度
- 开启 MixUp / CutMix / RandAugment
- 部署：导出 ONNX → TensorRT 推理
- 训练自己的数据集：把图片按 `data/train/class_name/*.jpg`, `data/val/class_name/*.jpg` 组织，改 `--dataset folder --data-dir data`
