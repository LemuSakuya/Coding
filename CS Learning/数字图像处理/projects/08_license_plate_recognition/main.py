"""项目 08：车牌定位 + 字符分割（传统图像处理流水线）"""
from __future__ import annotations

import argparse
from typing import List, Optional

import cv2
import matplotlib.pyplot as plt
import numpy as np


def synth_plate() -> np.ndarray:
    """合成一张蓝底白字的"车牌嵌入风景"图，便于无输入演示。"""
    bg = np.full((400, 700, 3), (60, 90, 40), dtype=np.uint8)
    cv2.rectangle(bg, (100, 120), (220, 280), (120, 160, 100), -1)
    cv2.circle(bg, (550, 110), 50, (180, 190, 210), -1)
    plate = np.full((80, 260, 3), (180, 60, 30), dtype=np.uint8)  # 蓝色
    cv2.putText(plate, 'A88888', (15, 60), cv2.FONT_HERSHEY_SIMPLEX,
                1.6, (255, 255, 255), 3)
    # 旋转
    M = cv2.getRotationMatrix2D((130, 40), -8, 1.0)
    plate = cv2.warpAffine(plate, M, (260, 90), borderValue=(180, 60, 30))
    bg[250:340, 330:590] = plate
    return bg


def find_plate_candidates(img: np.ndarray) -> List[np.ndarray]:
    """颜色 + 形态学 + 长宽比，返回候选车牌区域的四点坐标。"""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_blue = cv2.inRange(hsv, (100, 80, 40), (130, 255, 255))
    mask_yellow = cv2.inRange(hsv, (15, 80, 80), (40, 255, 255))
    mask = cv2.bitwise_or(mask_blue, mask_yellow)

    se = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, se, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,
                            cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates = []
    for c in contours:
        rect = cv2.minAreaRect(c)
        (cx, cy), (w, h), angle = rect
        if w == 0 or h == 0:
            continue
        ratio = max(w, h) / min(w, h)
        area = w * h
        if 2 < ratio < 6 and 1500 < area < 50000:
            box = cv2.boxPoints(rect)
            candidates.append((rect, box.astype(np.float32)))
    return candidates


def order_points(pts: np.ndarray) -> np.ndarray:
    """左上、右上、右下、左下。"""
    rect = np.zeros((4, 2), dtype=np.float32)
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1).ravel()
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def warp_plate(img: np.ndarray, box: np.ndarray,
               out_w: int = 300, out_h: int = 90) -> np.ndarray:
    src = order_points(box)
    dst = np.array([[0, 0], [out_w - 1, 0],
                    [out_w - 1, out_h - 1], [0, out_h - 1]], np.float32)
    H = cv2.getPerspectiveTransform(src, dst)
    return cv2.warpPerspective(img, H, (out_w, out_h))


def segment_chars(plate: np.ndarray) -> List[np.ndarray]:
    """字符分割：二值 + 连通域 + 过滤。"""
    gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
    # 深色牌底，白字 → 直接 OTSU 即为字
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(bw)
    chars = []
    for i in range(1, n):
        x, y, w, h, area = stats[i]
        if h / plate.shape[0] < 0.4:
            continue
        if w / plate.shape[1] > 0.5:
            continue
        if area < 30:
            continue
        chars.append((x, plate[y:y + h, x:x + w]))
    chars.sort(key=lambda c: c[0])
    return [c[1] for c in chars]


def try_ocr(img: np.ndarray) -> Optional[str]:
    try:
        import pytesseract  # type: ignore
    except ImportError:
        return None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    text = pytesseract.image_to_string(bw,
        config='--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return text.strip()


def show(imgs: dict, ncols: int = 3):
    n = len(imgs)
    rows = (n + ncols - 1) // ncols
    fig, axes = plt.subplots(rows, ncols, figsize=(4 * ncols, 3.5 * rows))
    for ax, (t, im) in zip(np.array(axes).ravel(), imgs.items()):
        if im.ndim == 2:
            ax.imshow(im, cmap='gray')
        else:
            ax.imshow(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
        ax.set_title(t)
        ax.axis('off')
    for ax in np.array(axes).ravel()[n:]:
        ax.axis('off')
    plt.tight_layout()
    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, default=None)
    args = parser.parse_args()

    img = cv2.imread(args.image) if args.image else synth_plate()
    if img is None:
        raise FileNotFoundError(args.image)

    cands = find_plate_candidates(img)
    print(f'找到 {len(cands)} 个候选')

    vis = img.copy()
    for _, box in cands:
        cv2.polylines(vis, [box.astype(int)], True, (0, 255, 0), 2)

    if not cands:
        show({'Original': img, 'Detected': vis})
        return

    # 取最大者
    rect, box = max(cands, key=lambda x: x[0][1][0] * x[0][1][1])
    plate = warp_plate(img, box)
    chars = segment_chars(plate)
    print(f'分割出 {len(chars)} 个字符')

    ocr = try_ocr(plate)
    title = f'Plate (OCR="{ocr}")' if ocr else 'Plate'

    show({
        'Original': img,
        'Detected': vis,
        title: plate,
    }, ncols=3)

    if chars:
        fig, axes = plt.subplots(1, len(chars), figsize=(2 * len(chars), 2))
        for ax, c in zip(np.array(axes).ravel(), chars):
            ax.imshow(c, cmap='gray' if c.ndim == 2 else None)
            ax.axis('off')
        plt.suptitle('Segmented characters')
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    main()
