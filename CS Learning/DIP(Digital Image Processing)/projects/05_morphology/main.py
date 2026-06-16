"""项目 05：形态学操作与分水岭应用"""
from __future__ import annotations

import argparse

import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage import data


def show(imgs: dict, cmap='gray', ncols=3):
    n = len(imgs)
    rows = (n + ncols - 1) // ncols
    fig, axes = plt.subplots(rows, ncols, figsize=(4 * ncols, 3.5 * rows))
    for ax, (t, im) in zip(np.array(axes).ravel(), imgs.items()):
        if im.ndim == 2:
            ax.imshow(im, cmap=cmap, vmin=0, vmax=255)
        else:
            ax.imshow(im)
        ax.set_title(t)
        ax.axis('off')
    for ax in np.array(axes).ravel()[n:]:
        ax.axis('off')
    plt.tight_layout()
    plt.show()


def basic_morph(binary: np.ndarray) -> dict[str, np.ndarray]:
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    return {
        'Binary': binary,
        'Erosion': cv2.erode(binary, se),
        'Dilation': cv2.dilate(binary, se),
        'Opening': cv2.morphologyEx(binary, cv2.MORPH_OPEN, se),
        'Closing': cv2.morphologyEx(binary, cv2.MORPH_CLOSE, se),
        'Gradient': cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, se),
        'Top-hat': cv2.morphologyEx(binary, cv2.MORPH_TOPHAT, se),
        'Black-hat': cv2.morphologyEx(binary, cv2.MORPH_BLACKHAT, se),
    }


def skeleton(binary: np.ndarray) -> np.ndarray:
    """基于反复腐蚀-开-取差的简易骨架。"""
    skel = np.zeros_like(binary)
    img = binary.copy()
    se = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    while True:
        opened = cv2.morphologyEx(img, cv2.MORPH_OPEN, se)
        temp = cv2.subtract(img, opened)
        eroded = cv2.erode(img, se)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded
        if cv2.countNonZero(img) == 0:
            break
    return skel


def watershed_coins(color: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    # 去噪
    opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, se, iterations=2)
    # 确定背景
    sure_bg = cv2.dilate(opening, se, iterations=3)
    # 距离变换 → 确定前景
    dist = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist, 0.5 * dist.max(), 255, 0)
    sure_fg = sure_fg.astype(np.uint8)
    unknown = cv2.subtract(sure_bg, sure_fg)

    _, markers = cv2.connectedComponents(sure_fg)
    markers += 1
    markers[unknown == 255] = 0
    markers = cv2.watershed(color, markers)
    out = color.copy()
    out[markers == -1] = (0, 0, 255)

    # 标号
    ids = [i for i in np.unique(markers) if i > 1]
    print(f'检测到 {len(ids)} 枚硬币')
    for i in ids:
        mask = (markers == i).astype(np.uint8)
        M = cv2.moments(mask)
        if M['m00'] > 0:
            cx, cy = int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])
            cv2.putText(out, str(i - 1), (cx - 10, cy + 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    return cv2.cvtColor(out, cv2.COLOR_BGR2RGB)


def tophat_illumination(img: np.ndarray) -> dict[str, np.ndarray]:
    """通过大尺寸 Top-hat 校正缓慢光照变化。"""
    se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (51, 51))
    tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, se)
    bg = cv2.morphologyEx(img, cv2.MORPH_OPEN, se)
    norm = cv2.normalize(tophat, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    return {
        'Original': img,
        'Estimated Background (open)': bg,
        'Top-hat (Corrected)': norm,
    }


def binarize(img: np.ndarray) -> np.ndarray:
    _, bw = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return bw


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, default=None)
    args = parser.parse_args()

    # 基础形态学：文字图
    if args.image:
        gray = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)
    else:
        # 合成：黑底白字
        gray = np.zeros((200, 500), dtype=np.uint8)
        cv2.putText(gray, 'Morphology', (30, 130),
                    cv2.FONT_HERSHEY_SIMPLEX, 3, 255, 5)
    bw = binarize(gray)
    show(basic_morph(bw))

    # 骨架
    sk = skeleton(bw)
    show({'Binary': bw, 'Skeleton': sk}, ncols=2)

    # 分水岭分硬币
    coins = data.coins()
    color = cv2.cvtColor(coins, cv2.COLOR_GRAY2BGR)
    ws = watershed_coins(color)
    show({'Coins': coins, 'Watershed': ws}, ncols=2)

    # 光照校正
    moon = data.moon()
    show(tophat_illumination(moon))


if __name__ == '__main__':
    main()
