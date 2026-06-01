# 项目 01：基础操作与直方图处理

> 对应章节：第 1、3 章
> 目标：熟悉图像的读入/显示/保存、灰度变换、直方图均衡与匹配。

## 包含内容

1. 图像读取、灰度转换、通道拆分
2. 灰度反转、对数变换、Gamma 校正
3. 分段线性拉伸
4. 直方图、CDF
5. 全局直方图均衡 (HE)
6. CLAHE（限制对比度自适应）
7. 直方图匹配（指定 CDF）

## 运行

```bash
python main.py                    # 使用 skimage 的 'moon' 图
python main.py --image my.jpg    # 自定义图
python main.py --save out.png    # 保存可视化结果
```

## 预期输出

一个 3×3 的网格图，依次展示：原图、反转、对数、Gamma、对比度拉伸、HE、CLAHE、匹配结果、以及对应的直方图/CDF 曲线。

## 延伸题目

- 实现自己的 `my_equalize_hist`，对比 OpenCV `cv2.equalizeHist` 的性能与结果差异。
- 把 CLAHE 应用到彩色图：直接对 BGR 三通道分别 vs 只对 Lab 的 L 通道 vs HSV 的 V 通道，观察哪种保色更好。
