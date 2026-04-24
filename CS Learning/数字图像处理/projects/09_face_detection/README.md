# 项目 09：人脸检测 (Haar 级联 + DNN SSD)

> 对应章节：第 12 章（传统 + 现代）
> 目标：对比 Viola-Jones Haar 级联（传统）与 DNN (Caffe SSD / ResNet-SSD) 两种人脸检测方法。

## 包含内容

- OpenCV 自带 Haar 级联检测
- OpenCV DNN 模块加载 Caffe SSD（首次运行自动下载模型）
- 网络摄像头实时检测
- 对比二者在同一张图上的检出率与误检

## 运行

```bash
# 静态图
python main.py --image assets/family.jpg

# 使用摄像头
python main.py --camera 0

# 选择检测器
python main.py --detector haar
python main.py --detector dnn
```

## 模型自动下载

首次运行 DNN 模式时，脚本会自动从 OpenCV GitHub 下载：
- `deploy.prototxt`
- `res10_300x300_ssd_iter_140000.caffemodel`

若无网络，请手动下载放入 `models/`。

## 延伸题目

- 替换为 MTCNN / RetinaFace / YOLOv8-Face，观察精度与速度。
- 加入人脸关键点检测（Dlib 68 点 / Mediapipe 478 点）。
