# 项目 06：图像分割综合

> 对应章节：第 10 章
> 目标：综合对比阈值、K-Means、分水岭、GrabCut 分割方法。

## 包含内容

- Otsu / 自适应阈值 / 多阈值
- K-Means（RGB 和 Lab 空间）
- 标记控制分水岭
- GrabCut（矩形框交互）
- SLIC 超像素

## 运行

```bash
python main.py                # 默认 coffee + astronaut
python main.py --image my.jpg --method grabcut  --rect 50 50 300 300
```

## 延伸题目

- 用 SLIC 超像素 + 区域邻接图（RAG）合并，得到语义级分割。
- 在 GrabCut 上加入笔刷式前/背景 mark（通过鼠标回调）。
