# 项目 04：边缘检测与霍夫变换

> 对应章节：第 10 章
> 目标：对比经典边缘算子，使用 Hough 直线/圆变换检测几何结构。

## 包含内容

- Roberts / Prewitt / Sobel / Scharr / Laplacian / LoG
- Canny（可调双阈值）
- HoughLines + HoughLinesP（概率霍夫）
- HoughCircles

## 运行

```bash
python main.py                    # 用内置 coins/building
python main.py --image my.jpg
python main.py --task circle      # 只看圆检测
python main.py --task line        # 只看直线检测
```

## 延伸题目

- 用 HoughLinesP 做车道线检测（需要 ROI 掩膜 + 角度过滤）。
- 加高斯噪声后观察 Canny 的鲁棒性，调整 `sigma` 找最优。
