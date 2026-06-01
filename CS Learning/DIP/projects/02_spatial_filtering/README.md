# 项目 02：空间域滤波

> 对应章节：第 3 章
> 目标：对比各种平滑与锐化滤波器，理解参数对效果的影响。

## 包含内容

- 加入**高斯噪声** / **椒盐噪声**
- 平滑：均值、高斯、中值、双边、非局部均值 (NLM)
- 锐化：Sobel、Laplacian、Unsharp Masking
- 定量指标：PSNR / SSIM 对比

## 运行

```bash
python main.py                # 默认 cameraman + 混合噪声
python main.py --noise gauss  # 只高斯
python main.py --noise sp     # 只椒盐
python main.py --image my.jpg
```

## 输出

- 噪声图 vs 各种滤波结果的网格对比
- 命令行打印 PSNR / SSIM
- 锐化对比图

## 延伸题目

- 固定 σ=1，调整高斯核尺寸 3/5/9/15，看窗口过大时的过平滑。
- 对比 `cv2.bilateralFilter` 不同 `sigmaColor` / `sigmaSpace` 的效果。
- 把 Unsharp Masking 的高斯核换成双边（保边锐化），用于人像磨皮后锐化。
