"""项目 04：边缘检测与霍夫变换"""
from __future__ import annotations

import argparse

import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage import data


def load_line_image(path: str | None) -> np.ndarray:
    if path:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise FileNotFoundError(path)
        return img
    # 默认合成：方格 + 噪声
    img = np.full((300, 400), 30, dtype=np.uint8)
    cv2.rectangle(img, (50, 50), (350, 250), 220, 2)
    cv2.line(img, (50, 50), (350, 250), 200, 2)
    cv2.line(img, (350, 50), (50, 250), 200, 2)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    return img


def load_circle_image(path: str | None) -> np.ndarray:
    if path:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise FileNotFoundError(path)
        return img
    return data.coins()


# ---------- 边缘算子对比 ---------- #

def edges_compare(img: np.ndarray) -> dict[str, np.ndarray]:
    f = img.astype(np.float32)
    kernels = {
        'Roberts X': np.array([[1, 0], [0, -1]], dtype=np.float32),
        'Roberts Y': np.array([[0, 1], [-1, 0]], dtype=np.float32),
        'Prewitt X': np.array([[-1, 0, 1]] * 3, dtype=np.float32),
        'Prewitt Y': np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float32),
    }
    gx_r = cv2.filter2D(f, cv2.CV_32F, kernels['Roberts X'])
    gy_r = cv2.filter2D(f, cv2.CV_32F, kernels['Roberts Y'])
    gx_p = cv2.filter2D(f, cv2.CV_32F, kernels['Prewitt X'])
    gy_p = cv2.filter2D(f, cv2.CV_32F, kernels['Prewitt Y'])
    sobel = cv2.magnitude(cv2.Sobel(f, cv2.CV_32F, 1, 0),
                          cv2.Sobel(f, cv2.CV_32F, 0, 1))
    scharr = cv2.magnitude(cv2.Scharr(f, cv2.CV_32F, 1, 0),
                           cv2.Scharr(f, cv2.CV_32F, 0, 1))
    lap = np.abs(cv2.Laplacian(f, cv2.CV_32F, ksize=3))
    log = np.abs(cv2.Laplacian(cv2.GaussianBlur(img, (5, 5), 1.0), cv2.CV_32F))
    canny = cv2.Canny(img, 80, 160, L2gradient=True)

    def norm(x):
        x = np.clip(x, 0, 255)
        return x.astype(np.uint8)

    return {
        'Original': img,
        'Roberts': norm(np.hypot(gx_r, gy_r)),
        'Prewitt': norm(np.hypot(gx_p, gy_p)),
        'Sobel': norm(sobel),
        'Scharr': norm(scharr),
        'Laplacian': norm(lap),
        'LoG': norm(log),
        'Canny': canny,
    }


# ---------- Hough 直线 ---------- #

def hough_lines(img: np.ndarray) -> np.ndarray:
    edges = cv2.Canny(img, 80, 160)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=120)
    color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if lines is not None:
        for rho, theta in lines[:30, 0]:
            a, b = np.cos(theta), np.sin(theta)
            x0, y0 = a * rho, b * rho
            x1, y1 = int(x0 + 1000 * (-b)), int(y0 + 1000 * a)
            x2, y2 = int(x0 - 1000 * (-b)), int(y0 - 1000 * a)
            cv2.line(color, (x1, y1), (x2, y2), (0, 0, 255), 1)
    return cv2.cvtColor(color, cv2.COLOR_BGR2RGB)


def hough_lines_p(img: np.ndarray) -> np.ndarray:
    edges = cv2.Canny(img, 80, 160)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=60,
                            minLineLength=50, maxLineGap=8)
    color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if lines is not None:
        for x1, y1, x2, y2 in lines[:, 0]:
            cv2.line(color, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return cv2.cvtColor(color, cv2.COLOR_BGR2RGB)


# ---------- Hough 圆 ---------- #

def hough_circles(img: np.ndarray) -> np.ndarray:
    blur = cv2.medianBlur(img, 5)
    circles = cv2.HoughCircles(
        blur, cv2.HOUGH_GRADIENT, dp=1, minDist=30,
        param1=100, param2=30, minRadius=15, maxRadius=80,
    )
    color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if circles is not None:
        for x, y, r in circles[0].astype(int):
            cv2.circle(color, (x, y), r, (0, 255, 255), 2)
            cv2.circle(color, (x, y), 2, (0, 0, 255), 3)
    return cv2.cvtColor(color, cv2.COLOR_BGR2RGB)


# ---------- 展示 ---------- #

def show(imgs: dict, cmap='gray') -> None:
    n = len(imgs)
    cols = 3
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 3.5 * rows))
    for ax, (t, im) in zip(axes.ravel(), imgs.items()):
        if im.ndim == 2:
            ax.imshow(im, cmap=cmap, vmin=0, vmax=255)
        else:
            ax.imshow(im)
        ax.set_title(t)
        ax.axis('off')
    for ax in axes.ravel()[n:]:
        ax.axis('off')
    plt.tight_layout()
    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, default=None)
    parser.add_argument('--task', choices=['all', 'edge', 'line', 'circle'], default='all')
    args = parser.parse_args()

    if args.task in ('all', 'edge'):
        img = load_line_image(args.image)
        show(edges_compare(img))

    if args.task in ('all', 'line'):
        img = load_line_image(args.image)
        show({
            'Original': img,
            'HoughLines': hough_lines(img),
            'HoughLinesP': hough_lines_p(img),
        })

    if args.task in ('all', 'circle'):
        img = load_circle_image(args.image)
        show({'Original': img, 'HoughCircles': hough_circles(img)})


if __name__ == '__main__':
    main()
