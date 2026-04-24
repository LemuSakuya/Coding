"""项目 02：空间域滤波对比

加入噪声 → 各滤波 → 评价 PSNR/SSIM。
"""
from __future__ import annotations

import argparse

import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage import data
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim


# ---------- 噪声 ---------- #

def add_gaussian(img: np.ndarray, sigma: float = 20) -> np.ndarray:
    noise = np.random.normal(0, sigma, img.shape).astype(np.float32)
    return np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)


def add_salt_pepper(img: np.ndarray, amount: float = 0.05) -> np.ndarray:
    out = img.copy()
    n = int(amount * img.size / 2)
    coords_s = tuple(np.random.randint(0, d, n) for d in img.shape)
    coords_p = tuple(np.random.randint(0, d, n) for d in img.shape)
    out[coords_s] = 255
    out[coords_p] = 0
    return out


# ---------- 平滑滤波 ---------- #

def mean_filter(img: np.ndarray, k: int = 5) -> np.ndarray:
    return cv2.blur(img, (k, k))


def gaussian_filter(img: np.ndarray, k: int = 5, sigma: float = 1.0) -> np.ndarray:
    return cv2.GaussianBlur(img, (k, k), sigma)


def median_filter(img: np.ndarray, k: int = 5) -> np.ndarray:
    return cv2.medianBlur(img, k)


def bilateral(img: np.ndarray, d: int = 9, sc: float = 75, ss: float = 75) -> np.ndarray:
    return cv2.bilateralFilter(img, d, sc, ss)


def nlm(img: np.ndarray, h: float = 10) -> np.ndarray:
    return cv2.fastNlMeansDenoising(img, None, h=h, templateWindowSize=7, searchWindowSize=21)


# ---------- 锐化 ---------- #

def sobel_mag(img: np.ndarray) -> np.ndarray:
    gx = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=3)
    mag = np.sqrt(gx ** 2 + gy ** 2)
    return np.clip(mag, 0, 255).astype(np.uint8)


def laplacian_sharpen(img: np.ndarray) -> np.ndarray:
    lap = cv2.Laplacian(img, cv2.CV_32F, ksize=3)
    sharp = img.astype(np.float32) - lap
    return np.clip(sharp, 0, 255).astype(np.uint8)


def unsharp_mask(img: np.ndarray, sigma: float = 1.5, k: float = 1.5) -> np.ndarray:
    blur = cv2.GaussianBlur(img, (0, 0), sigma)
    sharp = cv2.addWeighted(img, 1 + k, blur, -k, 0)
    return sharp


# ---------- 评价 ---------- #

def evaluate(ref: np.ndarray, pred: np.ndarray, name: str) -> None:
    p = psnr(ref, pred, data_range=255)
    s = ssim(ref, pred, data_range=255)
    print(f'{name:>18s}  PSNR={p:5.2f} dB  SSIM={s:.4f}')


# ---------- 可视化 ---------- #

def show_grid(imgs: dict[str, np.ndarray]) -> None:
    n = len(imgs)
    cols = 3
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 3.5 * rows))
    for ax, (t, im) in zip(axes.ravel(), imgs.items()):
        ax.imshow(im, cmap='gray', vmin=0, vmax=255)
        ax.set_title(t)
        ax.axis('off')
    for ax in axes.ravel()[n:]:
        ax.axis('off')
    plt.tight_layout()
    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, default=None)
    parser.add_argument('--noise', choices=['gauss', 'sp', 'both'], default='both')
    args = parser.parse_args()

    if args.image:
        clean = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)
        if clean is None:
            raise FileNotFoundError(args.image)
    else:
        clean = data.camera()

    if args.noise == 'gauss':
        noisy = add_gaussian(clean, 20)
    elif args.noise == 'sp':
        noisy = add_salt_pepper(clean, 0.05)
    else:
        noisy = add_salt_pepper(add_gaussian(clean, 15), 0.03)

    results = {
        'Clean': clean,
        'Noisy': noisy,
        'Mean 5x5': mean_filter(noisy, 5),
        'Gaussian 5x5, σ=1': gaussian_filter(noisy, 5, 1.0),
        'Median 5x5': median_filter(noisy, 5),
        'Bilateral': bilateral(noisy),
        'NLM': nlm(noisy),
    }
    show_grid(results)

    print('\n=== Denoising Metrics ===')
    for name, im in results.items():
        if name == 'Clean':
            continue
        evaluate(clean, im, name)

    # 锐化对比
    sharp_results = {
        'Clean': clean,
        'Sobel Magnitude': sobel_mag(clean),
        'Laplacian Sharpen': laplacian_sharpen(clean),
        'Unsharp Mask': unsharp_mask(clean),
    }
    show_grid(sharp_results)


if __name__ == '__main__':
    main()
