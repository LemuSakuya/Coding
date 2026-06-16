# 项目 07：特征匹配与全景拼接

> 对应章节：第 11 章
> 目标：从 ORB/SIFT 特征 → 匹配 → RANSAC 估单应 → 图像拼接，完整走完一遍全景生成。

## 包含内容

- ORB / SIFT 特征检测与描述
- 暴力匹配 + Lowe 比率测试
- `findHomography` + RANSAC
- `warpPerspective` 拼接 + 简单羽化融合
- 也可使用 OpenCV 高级 `Stitcher`

## 运行

```bash
# 使用内置样图自动合成两张有重叠的图
python main.py --demo

# 自定义两张有重叠的图
python main.py --left left.jpg --right right.jpg

# 超过 2 张
python main.py --stitch img1.jpg img2.jpg img3.jpg
```

## 输出

- 两图特征点 + 匹配连线
- 拼接后的全景图

## 延伸题目

- 切换 SIFT vs ORB，观察匹配数量与拼接质量差异。
- 用 `cv2.createStitcher` 实现多张拼接。
