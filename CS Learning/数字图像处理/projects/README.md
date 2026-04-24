# 数字图像处理 · 项目实践总览

本目录提供 **10 个递进式项目**，与 `../chapters/` 的理论章节一一对应。
每个项目都包含：

- `README.md`：背景、目标、知识点、使用方法
- `main.py`：可直接运行的入口脚本
- 必要的工具模块
- （可选）`assets/` 子目录存放专用样图

## 项目列表

| # | 项目 | 对应章节 | 关键技术 |
|---|------|---------|----------|
| 01 | `01_basic_and_histogram/` | Ch 1、3 | 灰度变换、HE、CLAHE、Gamma |
| 02 | `02_spatial_filtering/` | Ch 3 | 均值/高斯/中值/双边/Unsharp |
| 03 | `03_frequency_filtering/` | Ch 4 | FFT、LP/HP、陷波、同态 |
| 04 | `04_edge_and_hough/` | Ch 10 | Canny、Hough 直线与圆 |
| 05 | `05_morphology/` | Ch 9 | 腐蚀膨胀、开闭、Top-hat、分水岭 |
| 06 | `06_segmentation/` | Ch 10 | Otsu、分水岭、GrabCut、K-Means |
| 07 | `07_feature_matching_panorama/` | Ch 11 | ORB/SIFT + RANSAC + 拼接 |
| 08 | `08_license_plate_recognition/` | Ch 3、9、10、11 综合 | 颜色+形态学+透视+OCR |
| 09 | `09_face_detection/` | Ch 12 传统部分 | Haar 级联 / DNN SSD |
| 10 | `10_cnn_classification/` | Ch 12 | PyTorch + ResNet 迁移学习 |

## 环境准备

```bash
cd "CS Learning/数字图像处理/projects"
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 通用说明

- 所有脚本默认使用 `skimage.data` 内置样图，无需额外下载。
- 若要测试自己的图片，把文件放入各项目的 `assets/` 子目录或传 `--image` 参数：
  ```bash
  python main.py --image path/to/my.jpg
  ```
- 运行中会弹出 matplotlib 窗口展示结果；可加 `--save out.png` 直接保存。
- 项目 10 (CNN) 建议有 GPU；CPU 也能跑但慢。

## 学习建议

1. **先通读对应章节**，再跑代码，最后修改关键参数观察变化。
2. **自问**：把高斯 σ 从 1 调到 5，细节保留度如何变化？
3. **排错**：若弹窗闪退，大多是 backend 问题，尝试 `matplotlib.use('TkAgg')`。
4. **扩展**：每个 README 末尾都有"延伸题目"，对应工程中的真实场景。

祝玩得开心！
