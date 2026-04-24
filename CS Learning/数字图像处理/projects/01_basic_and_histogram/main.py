"""项目 01：基础操作 + 直方图处理

演示：灰度变换、HE、CLAHE、直方图匹配。
"""
from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage import data, exposure


def load_image(path: str | None) -> np.ndarray:
    """读入灰度图。若未指定 path 使用 skimage 内置 moon 图。"""
    if path is None:
        img = data.moon()
    else:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise FileNotFoundError(path)
    return img


# ---------- 灰度变换 ---------- #

def negative(img: np.ndarray) -> np.ndarray:
    return 255 - img


def log_transform(img: np.ndarray, c: float | None = None) -> np.ndarray:
    f = img.astype(np.float32)
    if c is None:
        c = 255.0 / np.log1p(f.max())
    out = c * np.log1p(f)
    return np.clip(out, 0, 255).astype(np.uint8)


def gamma_transform(img: np.ndarray, gamma: float = 0.5) -> np.ndarray:
    f = img.astype(np.float32) / 255.0
    out = np.power(f, gamma) * 255.0
    return np.clip(out, 0, 255).astype(np.uint8)


def contrast_stretch(img: np.ndarray, r1: int = 70, r2: int = 170) -> np.ndarray:
    """分段线性：将 [r1, r2] 拉伸到 [0, 255]。"""
    table = np.zeros(256, dtype=np.uint8)
    for r in range(256):
        if r < r1:
            s = 0.5 * r
        elif r < r2:
            s = 255.0 * (r - r1) / max(r2 - r1, 1)
        else:
            s = 255.0
        table[r] = np.clip(s, 0, 255)
    return table[img]


# ---------- 直方图均衡 ---------- #

def my_equalize_hist(img: np.ndarray) -> np.ndarray:
    hist, _ = np.histogram(img.flatten(), 256, [0, 256])
    cdf = hist.cumsum().astype(np.float32)
    cdf = (cdf - cdf.min()) * 255.0 / (cdf.max() - cdf.min() + 1e-8)
    return cdf.astype(np.uint8)[img]


def clahe(img: np.ndarray, clip: float = 2.0, tile: int = 8) -> np.ndarray:
    c = cv2.createCLAHE(clipLimit=clip, tileGridSize=(tile, tile))
    return c.apply(img)


def hist_match(src: np.ndarray, ref: np.ndarray) -> np.ndarray:
    """把 src 的直方图映射为 ref 的直方图。"""
    return exposure.match_histograms(src, ref).astype(np.uint8)


# ---------- 可视化 ---------- #

def plot_results(imgs: dict[str, np.ndarray], save: str | None) -> None:
    n = len(imgs)
    cols = 3
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 3.5 * rows))
    for ax, (title, im) in zip(axes.ravel(), imgs.items()):
        ax.imshow(im, cmap='gray', vmin=0, vmax=255)
        ax.set_title(title)
        ax.axis('off')
    for ax in axes.ravel()[len(imgs):]:
        ax.axis('off')
    plt.tight_layout()
    if save:
        plt.savefig(save, dpi=150)
        print(f"saved -> {save}")
    plt.show()


def plot_hist(img: np.ndarray, eq: np.ndarray, clahe_img: np.ndarray) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(12, 3))
    for ax, im, name in zip(
        axes,
        [img, eq, clahe_img],
        ['Original', 'HE', 'CLAHE'],
    ):
        ax.hist(im.ravel(), bins=256, range=(0, 256), color='steelblue', alpha=0.8)
        ax.set_title(f'Hist - {name}')
        ax.set_xlim(0, 255)
    plt.tight_layout()
    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, default=None)
    parser.add_argument('--save', type=str, default=None)
    args = parser.parse_args()

    img = load_image(args.image)

    results = {
        'Original': img,
        'Negative': negative(img),
        'Log': log_transform(img),
        'Gamma 0.5': gamma_transform(img, 0.5),
        'Gamma 2.0': gamma_transform(img, 2.0),
        'Contrast Stretch': contrast_stretch(img),
        'HE (my)': my_equalize_hist(img),
        'HE (cv2)': cv2.equalizeHist(img),
        'CLAHE': clahe(img),
    }
    plot_results(results, args.save)

    # 直方图可视化
    plot_hist(img, results['HE (cv2)'], results['CLAHE'])

    # 直方图匹配示例：把 moon 匹配为 camera 的亮度分布
    try:
        ref = data.camera()
        matched = hist_match(img, ref)
        plot_results({'Src': img, 'Ref': ref, 'Matched': matched}, None)
    except Exception as e:  # 用户自传图时可能尺寸不匹配，忽略
        print(f'histogram matching skipped: {e}')


if __name__ == '__main__':
    main()
