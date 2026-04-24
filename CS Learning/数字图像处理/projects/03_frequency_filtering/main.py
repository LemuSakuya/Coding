"""项目 03：频率域滤波"""
from __future__ import annotations

import argparse

import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage import data


def fft_center(img: np.ndarray) -> np.ndarray:
    return np.fft.fftshift(np.fft.fft2(img.astype(np.float32)))


def ifft_center(F: np.ndarray) -> np.ndarray:
    f = np.fft.ifft2(np.fft.ifftshift(F))
    return np.real(f)


def spectrum(F: np.ndarray) -> np.ndarray:
    mag = 20 * np.log1p(np.abs(F))
    mag = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    return mag.astype(np.uint8)


# ---------- 低通 / 高通滤波器 ---------- #

def distance_map(shape: tuple[int, int]) -> np.ndarray:
    M, N = shape
    u = np.arange(M) - M // 2
    v = np.arange(N) - N // 2
    U, V = np.meshgrid(u, v, indexing='ij')
    return np.sqrt(U ** 2 + V ** 2)


def ilpf(shape, D0):  # 理想低通
    D = distance_map(shape)
    return (D <= D0).astype(np.float32)


def blpf(shape, D0, n=2):
    D = distance_map(shape)
    return 1.0 / (1.0 + (D / D0) ** (2 * n))


def glpf(shape, D0):
    D = distance_map(shape)
    return np.exp(-(D ** 2) / (2 * D0 ** 2))


def highpass(H_low):
    return 1 - H_low


# ---------- 同态滤波（简化版） ---------- #

def homomorphic(img: np.ndarray, gl=0.4, gh=1.6, D0=30, c=1) -> np.ndarray:
    f = np.log1p(img.astype(np.float32))
    F = fft_center(f)
    D = distance_map(img.shape)
    H = (gh - gl) * (1 - np.exp(-c * (D ** 2) / (D0 ** 2))) + gl
    G = F * H
    g = np.expm1(ifft_center(G))
    g = cv2.normalize(g, None, 0, 255, cv2.NORM_MINMAX)
    return g.astype(np.uint8)


# ---------- 周期噪声 + 陷波 ---------- #

def add_periodic(img: np.ndarray, freq: int = 30, amp: float = 40) -> np.ndarray:
    h, w = img.shape
    x = np.arange(w)
    stripe = amp * np.sin(2 * np.pi * freq * x / w)
    noisy = img.astype(np.float32) + stripe[None, :]
    return np.clip(noisy, 0, 255).astype(np.uint8)


def notch_reject(shape, centers, D0=5) -> np.ndarray:
    """给定几组 (u, v) 及其对称点，构造 Butterworth 陷波。"""
    H = np.ones(shape, dtype=np.float32)
    M, N = shape
    u = np.arange(M)[:, None] - M // 2
    v = np.arange(N)[None, :] - N // 2
    for uk, vk in centers:
        Dk = np.sqrt((u - uk) ** 2 + (v - vk) ** 2)
        D_k = np.sqrt((u + uk) ** 2 + (v + vk) ** 2)
        H *= 1.0 / (1.0 + (D0 / (Dk + 1e-6)) ** 4)
        H *= 1.0 / (1.0 + (D0 / (D_k + 1e-6)) ** 4)
    return H


def show(imgs: dict[str, np.ndarray], cmap='gray') -> None:
    n = len(imgs)
    cols = 3
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 3.5 * rows))
    for ax, (t, im) in zip(axes.ravel(), imgs.items()):
        ax.imshow(im, cmap=cmap, vmin=0, vmax=255)
        ax.set_title(t)
        ax.axis('off')
    for ax in axes.ravel()[n:]:
        ax.axis('off')
    plt.tight_layout()
    plt.show()


def apply_filter(img: np.ndarray, H: np.ndarray) -> np.ndarray:
    F = fft_center(img)
    g = ifft_center(F * H)
    g = cv2.normalize(g, None, 0, 255, cv2.NORM_MINMAX)
    return g.astype(np.uint8)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, default=None)
    args = parser.parse_args()

    if args.image:
        img = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)
    else:
        img = data.camera()

    # 1. 频谱可视化
    F = fft_center(img)
    show({'Original': img, 'Spectrum (log|F|)': spectrum(F)})

    # 2. 低通三种
    D0 = 30
    H1, H2, H3 = ilpf(img.shape, D0), blpf(img.shape, D0), glpf(img.shape, D0)
    show({
        'Original': img,
        f'ILPF D0={D0}': apply_filter(img, H1),
        f'BLPF D0={D0}, n=2': apply_filter(img, H2),
        f'GLPF D0={D0}': apply_filter(img, H3),
    })

    # 3. 高通锐化
    D0h = 30
    show({
        'Original': img,
        'IHPF': apply_filter(img, highpass(ilpf(img.shape, D0h))),
        'BHPF': apply_filter(img, highpass(blpf(img.shape, D0h))),
        'GHPF': apply_filter(img, highpass(glpf(img.shape, D0h))),
    })

    # 4. 同态滤波
    show({'Original': img, 'Homomorphic': homomorphic(img)})

    # 5. 周期噪声 + 陷波
    noisy = add_periodic(img, freq=30, amp=40)
    F_noisy = fft_center(noisy)
    # 横向条纹 → 频谱两个对称亮斑 (0, ±30)；结合 fftshift 后坐标
    H_notch = notch_reject(img.shape, centers=[(0, 30)], D0=5)
    recovered = apply_filter(noisy, H_notch)
    show({
        'Noisy (periodic)': noisy,
        'Spectrum noisy': spectrum(F_noisy),
        'Notch H': (H_notch * 255).astype(np.uint8),
        'Recovered': recovered,
    })


if __name__ == '__main__':
    main()
