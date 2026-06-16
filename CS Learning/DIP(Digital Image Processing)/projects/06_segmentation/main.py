"""项目 06：图像分割方法对比"""
from __future__ import annotations

import argparse

import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage import data, segmentation, color


def show(imgs: dict, ncols=3):
    n = len(imgs)
    rows = (n + ncols - 1) // ncols
    fig, axes = plt.subplots(rows, ncols, figsize=(4 * ncols, 3.5 * rows))
    for ax, (t, im) in zip(np.array(axes).ravel(), imgs.items()):
        if im.ndim == 2:
            ax.imshow(im, cmap='gray')
        else:
            ax.imshow(im)
        ax.set_title(t)
        ax.axis('off')
    for ax in np.array(axes).ravel()[n:]:
        ax.axis('off')
    plt.tight_layout()
    plt.show()


# ---------- 阈值 ---------- #

def otsu(gray: np.ndarray) -> np.ndarray:
    _, bin_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return bin_img


def adaptive(gray: np.ndarray) -> np.ndarray:
    return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 25, 5)


# ---------- K-Means ---------- #

def kmeans_seg(bgr: np.ndarray, K: int = 4, use_lab: bool = True) -> np.ndarray:
    img = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB) if use_lab else bgr
    data_f = img.reshape(-1, 3).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.5)
    _, labels, centers = cv2.kmeans(data_f, K, None, criteria, 5, cv2.KMEANS_PP_CENTERS)
    quant = centers[labels.flatten()].reshape(img.shape).astype(np.uint8)
    if use_lab:
        quant = cv2.cvtColor(quant, cv2.COLOR_LAB2BGR)
    return cv2.cvtColor(quant, cv2.COLOR_BGR2RGB)


# ---------- Watershed ---------- #

def watershed(bgr: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    op = cv2.morphologyEx(th, cv2.MORPH_OPEN, se, iterations=2)
    sure_bg = cv2.dilate(op, se, iterations=3)
    dist = cv2.distanceTransform(op, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist, 0.4 * dist.max(), 255, 0)
    sure_fg = sure_fg.astype(np.uint8)
    unknown = cv2.subtract(sure_bg, sure_fg)
    _, markers = cv2.connectedComponents(sure_fg)
    markers += 1
    markers[unknown == 255] = 0
    markers = cv2.watershed(bgr, markers)
    out = bgr.copy()
    out[markers == -1] = (0, 0, 255)
    return cv2.cvtColor(out, cv2.COLOR_BGR2RGB)


# ---------- GrabCut ---------- #

def grabcut(bgr: np.ndarray, rect: tuple[int, int, int, int]) -> np.ndarray:
    mask = np.zeros(bgr.shape[:2], np.uint8)
    bgdM, fgdM = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
    cv2.grabCut(bgr, mask, rect, bgdM, fgdM, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype(np.uint8)
    result = bgr * mask2[:, :, None]
    return cv2.cvtColor(result, cv2.COLOR_BGR2RGB)


# ---------- SLIC ---------- #

def slic_superpixel(bgr: np.ndarray, n_segments: int = 200) -> np.ndarray:
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    segs = segmentation.slic(rgb, n_segments=n_segments, compactness=10, start_label=1)
    out = color.label2rgb(segs, rgb, kind='avg', bg_label=0)
    return (out * 255).astype(np.uint8)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, default=None)
    parser.add_argument('--method', choices=['all', 'threshold', 'kmeans',
                        'watershed', 'grabcut', 'slic'], default='all')
    parser.add_argument('--rect', nargs=4, type=int,
                        default=[50, 50, 400, 400], help='GrabCut rect x y w h')
    args = parser.parse_args()

    if args.image:
        bgr = cv2.imread(args.image)
        if bgr is None:
            raise FileNotFoundError(args.image)
    else:
        bgr = cv2.cvtColor(data.astronaut(), cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    if args.method in ('all', 'threshold'):
        show({
            'Gray': gray,
            'Otsu': otsu(gray),
            'Adaptive Gaussian': adaptive(gray),
        })

    if args.method in ('all', 'kmeans'):
        show({
            'Original': cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB),
            'K-Means K=3 RGB': kmeans_seg(bgr, 3, use_lab=False),
            'K-Means K=4 Lab': kmeans_seg(bgr, 4, use_lab=True),
        })

    if args.method in ('all', 'watershed'):
        show({
            'Original': cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB),
            'Watershed': watershed(bgr),
        })

    if args.method in ('all', 'grabcut'):
        x, y, w, h = args.rect
        show({
            'Original': cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB),
            f'GrabCut rect={args.rect}': grabcut(bgr, (x, y, w, h)),
        })

    if args.method in ('all', 'slic'):
        show({
            'Original': cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB),
            'SLIC Superpixels': slic_superpixel(bgr),
        })


if __name__ == '__main__':
    main()
