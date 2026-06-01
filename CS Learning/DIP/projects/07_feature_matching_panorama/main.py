"""项目 07：特征匹配 + 全景拼接"""
from __future__ import annotations

import argparse

import cv2
import matplotlib.pyplot as plt
import numpy as np


def make_demo_pair() -> tuple[np.ndarray, np.ndarray]:
    """把 skimage astronaut 裁为两张 50% 重叠图。"""
    from skimage import data
    img = cv2.cvtColor(data.astronaut(), cv2.COLOR_RGB2BGR)
    h, w = img.shape[:2]
    left = img[:, : int(w * 0.65)]
    right = img[:, int(w * 0.35):]
    return left, right


# ---------- 特征与匹配 ---------- #

def detect(img: np.ndarray, method: str = 'orb'):
    if method.lower() == 'orb':
        det = cv2.ORB_create(2000)
        kp, des = det.detectAndCompute(img, None)
        norm = cv2.NORM_HAMMING
    else:
        det = cv2.SIFT_create(2000)
        kp, des = det.detectAndCompute(img, None)
        norm = cv2.NORM_L2
    return kp, des, norm


def match(des1, des2, norm):
    bf = cv2.BFMatcher(norm, crossCheck=False)
    raw = bf.knnMatch(des1, des2, k=2)
    good = [m for m, n in raw if m.distance < 0.75 * n.distance]
    return good


# ---------- 单应与拼接 ---------- #

def find_H(kp1, kp2, matches):
    src = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    H, mask = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
    return H, mask


def blend_two(left: np.ndarray, right: np.ndarray, method: str = 'orb') -> np.ndarray:
    """left 对齐到 right 坐标系并与之拼接。"""
    g1 = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)
    kp1, des1, norm = detect(g1, method)
    kp2, des2, _ = detect(g2, method)
    good = match(des1, des2, norm)
    print(f'{len(good)} good matches')
    if len(good) < 10:
        raise RuntimeError('not enough matches')
    H, mask = find_H(kp1, kp2, good)

    # 可视化匹配
    match_img = cv2.drawMatches(left, kp1, right, kp2, good[:80], None,
                                matchesMask=mask.ravel().tolist(),
                                flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    plt.figure(figsize=(12, 5))
    plt.title(f'{method.upper()} matches (after RANSAC)')
    plt.imshow(cv2.cvtColor(match_img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

    # 拼接画布
    h1, w1 = left.shape[:2]
    h2, w2 = right.shape[:2]
    canvas_w = w1 + w2
    canvas_h = max(h1, h2)
    warped = cv2.warpPerspective(left, H, (canvas_w, canvas_h))
    out = warped.copy()
    out[:h2, :w2] = right  # 简单覆盖；右图为基准
    return out


# ---------- 多张 ---------- #

def stitch_multi(images: list[np.ndarray]) -> np.ndarray:
    stitcher = cv2.Stitcher_create()
    status, pano = stitcher.stitch(images)
    if status != cv2.Stitcher_OK:
        raise RuntimeError(f'Stitcher error {status}')
    return pano


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--demo', action='store_true')
    parser.add_argument('--left', type=str)
    parser.add_argument('--right', type=str)
    parser.add_argument('--stitch', nargs='+', help='multi images for Stitcher')
    parser.add_argument('--method', choices=['orb', 'sift'], default='orb')
    args = parser.parse_args()

    if args.stitch:
        imgs = [cv2.imread(p) for p in args.stitch]
        pano = stitch_multi(imgs)
    elif args.left and args.right:
        left = cv2.imread(args.left)
        right = cv2.imread(args.right)
        pano = blend_two(left, right, args.method)
    else:
        left, right = make_demo_pair()
        pano = blend_two(left, right, args.method)

    plt.figure(figsize=(12, 5))
    plt.title('Panorama')
    plt.imshow(cv2.cvtColor(pano, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    main()
