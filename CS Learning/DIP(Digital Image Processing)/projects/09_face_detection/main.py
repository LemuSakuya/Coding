"""项目 09：人脸检测（Haar vs DNN SSD）"""
from __future__ import annotations

import argparse
import os
import urllib.request
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np


MODEL_DIR = Path(__file__).parent / 'models'
PROTOTXT_URL = ('https://raw.githubusercontent.com/opencv/opencv/master/'
                'samples/dnn/face_detector/deploy.prototxt')
CAFFEMODEL_URL = ('https://raw.githubusercontent.com/opencv/opencv_3rdparty/'
                  'dnn_samples_face_detector_20170830/'
                  'res10_300x300_ssd_iter_140000.caffemodel')


def download(url: str, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        return
    print(f'downloading {url}\n -> {dst}')
    urllib.request.urlretrieve(url, dst)


# ---------- Haar 级联 ---------- #

def haar_detect(img: np.ndarray) -> list[tuple[int, int, int, int]]:
    path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    det = cv2.CascadeClassifier(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = det.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return [(x, y, w, h) for x, y, w, h in faces]


# ---------- DNN SSD ---------- #

_net_cache = None


def get_dnn():
    global _net_cache
    if _net_cache is not None:
        return _net_cache
    proto = MODEL_DIR / 'deploy.prototxt'
    weights = MODEL_DIR / 'res10_300x300_ssd_iter_140000.caffemodel'
    try:
        download(PROTOTXT_URL, proto)
        download(CAFFEMODEL_URL, weights)
    except Exception as e:
        raise RuntimeError(f'model download failed: {e}. 请手动下载放入 {MODEL_DIR}')
    _net_cache = cv2.dnn.readNetFromCaffe(str(proto), str(weights))
    return _net_cache


def dnn_detect(img: np.ndarray, conf_thresh: float = 0.5) -> list:
    net = get_dnn()
    h, w = img.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0,
                                 (300, 300), (104, 177, 123))
    net.setInput(blob)
    dets = net.forward()
    results = []
    for i in range(dets.shape[2]):
        conf = float(dets[0, 0, i, 2])
        if conf < conf_thresh:
            continue
        x1, y1, x2, y2 = (dets[0, 0, i, 3:7] * np.array([w, h, w, h])).astype(int)
        results.append((x1, y1, x2 - x1, y2 - y1, conf))
    return results


# ---------- 绘制 ---------- #

def draw(img: np.ndarray, boxes, color=(0, 255, 0)) -> np.ndarray:
    out = img.copy()
    for b in boxes:
        if len(b) == 5:
            x, y, w, h, c = b
            cv2.rectangle(out, (x, y), (x + w, y + h), color, 2)
            cv2.putText(out, f'{c:.2f}', (x, y - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        else:
            x, y, w, h = b
            cv2.rectangle(out, (x, y), (x + w, y + h), color, 2)
    return out


def run_image(img_path: str | None, detector: str) -> None:
    if img_path:
        img = cv2.imread(img_path)
    else:
        # 下载 OpenCV 自带测试人脸图
        path = MODEL_DIR / 'people.jpg'
        try:
            download('https://raw.githubusercontent.com/opencv/opencv/master/samples/data/aero3.jpg', path)
            img = cv2.imread(str(path))
        except Exception:
            img = np.full((400, 500, 3), 160, np.uint8)
            cv2.putText(img, 'please provide --image', (20, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    panels = {'Original': img}
    if detector in ('all', 'haar'):
        panels['Haar'] = draw(img, haar_detect(img), (0, 255, 0))
    if detector in ('all', 'dnn'):
        try:
            panels['DNN SSD'] = draw(img, dnn_detect(img), (0, 0, 255))
        except Exception as e:
            print(f'DNN failed: {e}')

    fig, axes = plt.subplots(1, len(panels), figsize=(5 * len(panels), 5))
    for ax, (t, im) in zip(np.array(axes).ravel(), panels.items()):
        ax.imshow(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
        ax.set_title(t)
        ax.axis('off')
    plt.tight_layout()
    plt.show()


def run_camera(idx: int, detector: str) -> None:
    cap = cv2.VideoCapture(idx)
    if not cap.isOpened():
        print(f'cannot open camera {idx}')
        return
    print('按 q 退出')
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if detector == 'haar':
            frame = draw(frame, haar_detect(frame))
        else:
            frame = draw(frame, dnn_detect(frame), (0, 0, 255))
        cv2.imshow('face', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str)
    parser.add_argument('--camera', type=int)
    parser.add_argument('--detector', choices=['haar', 'dnn', 'all'], default='all')
    args = parser.parse_args()
    if args.camera is not None:
        run_camera(args.camera,
                   'haar' if args.detector == 'all' else args.detector)
    else:
        run_image(args.image, args.detector)


if __name__ == '__main__':
    main()
