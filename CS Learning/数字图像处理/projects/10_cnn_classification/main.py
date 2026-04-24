"""项目 10：PyTorch CNN 图像分类（CIFAR-10 / 自定义 ImageFolder）"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import torch
from torch import nn, optim
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms
from tqdm import tqdm


CKPT_DIR = Path(__file__).parent / 'checkpoints'
CKPT_DIR.mkdir(exist_ok=True)


# ---------- 数据 ---------- #

def get_loaders(dataset: str, data_dir: str, batch: int, img_size: int = 224):
    train_tf = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(0.2, 0.2, 0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
    ])
    val_tf = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
    ])

    if dataset == 'cifar10':
        train_ds = datasets.CIFAR10(data_dir, train=True, download=True, transform=train_tf)
        val_ds = datasets.CIFAR10(data_dir, train=False, download=True, transform=val_tf)
        classes = train_ds.classes
    elif dataset == 'folder':
        train_ds = datasets.ImageFolder(Path(data_dir) / 'train', transform=train_tf)
        val_ds = datasets.ImageFolder(Path(data_dir) / 'val', transform=val_tf)
        classes = train_ds.classes
    else:
        raise ValueError(dataset)

    train_loader = DataLoader(train_ds, batch_size=batch, shuffle=True,
                              num_workers=2, pin_memory=True)
    val_loader = DataLoader(val_ds, batch_size=batch, shuffle=False,
                            num_workers=2, pin_memory=True)
    return train_loader, val_loader, classes


# ---------- 模型 ---------- #

def build_model(num_classes: int, freeze_backbone: bool = False) -> nn.Module:
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    if freeze_backbone:
        for p in model.parameters():
            p.requires_grad = False
    in_f = model.fc.in_features
    model.fc = nn.Linear(in_f, num_classes)
    return model


# ---------- 训练 ---------- #

def train_epoch(model, loader, criterion, optimizer, device) -> tuple[float, float]:
    model.train()
    loss_sum, correct, total = 0.0, 0, 0
    for x, y in tqdm(loader, desc='train', leave=False):
        x, y = x.to(device), y.to(device)
        out = model(x)
        loss = criterion(out, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        loss_sum += loss.item() * x.size(0)
        correct += (out.argmax(1) == y).sum().item()
        total += x.size(0)
    return loss_sum / total, correct / total


@torch.no_grad()
def eval_epoch(model, loader, criterion, device) -> tuple[float, float]:
    model.eval()
    loss_sum, correct, total = 0.0, 0, 0
    for x, y in tqdm(loader, desc='val', leave=False):
        x, y = x.to(device), y.to(device)
        out = model(x)
        loss = criterion(out, y)
        loss_sum += loss.item() * x.size(0)
        correct += (out.argmax(1) == y).sum().item()
        total += x.size(0)
    return loss_sum / total, correct / total


def save_ckpt(model, classes, path: Path) -> None:
    torch.save({
        'state_dict': model.state_dict(),
        'classes': classes,
    }, path)


def run_train(args) -> None:
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'device={device}')

    train_loader, val_loader, classes = get_loaders(
        args.dataset, args.data_dir, args.batch)
    model = build_model(len(classes), args.freeze).to(device)
    if args.resume and Path(args.resume).exists():
        state = torch.load(args.resume, map_location=device)
        model.load_state_dict(state['state_dict'])
        print(f'resumed from {args.resume}')

    criterion = nn.CrossEntropyLoss(label_smoothing=0.05)
    optimizer = optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)

    best_acc = 0.0
    for epoch in range(args.epochs):
        tl, ta = train_epoch(model, train_loader, criterion, optimizer, device)
        vl, va = eval_epoch(model, val_loader, criterion, device)
        scheduler.step()
        print(f'[{epoch + 1:02d}/{args.epochs}] '
              f'train loss={tl:.4f} acc={ta:.4f} | val loss={vl:.4f} acc={va:.4f}')
        if va > best_acc:
            best_acc = va
            save_ckpt(model, classes, CKPT_DIR / 'best.pt')
            print(f'  best saved (acc={va:.4f})')
    print(f'training done. best val acc = {best_acc:.4f}')


# ---------- 推理 ---------- #

def run_predict(args) -> None:
    from PIL import Image
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    ckpt = torch.load(CKPT_DIR / 'best.pt', map_location=device)
    classes = ckpt['classes']
    model = build_model(len(classes)).to(device)
    model.load_state_dict(ckpt['state_dict'])
    model.eval()

    tf = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    img = Image.open(args.image).convert('RGB')
    x = tf(img).unsqueeze(0).to(device)
    with torch.no_grad():
        prob = torch.softmax(model(x), dim=1).cpu().numpy()[0]
    top = prob.argsort()[::-1][:5]
    print('Top-5:')
    for i in top:
        print(f'  {classes[i]:20s}  {prob[i] * 100:6.2f}%')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['train', 'predict'], default='train')
    parser.add_argument('--dataset', choices=['cifar10', 'folder'], default='cifar10')
    parser.add_argument('--data-dir', type=str, default='./data')
    parser.add_argument('--epochs', type=int, default=5)
    parser.add_argument('--batch', type=int, default=128)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--freeze', action='store_true',
                        help='freeze backbone, only train fc')
    parser.add_argument('--resume', type=str, default=None)
    parser.add_argument('--image', type=str, help='for predict mode')
    args = parser.parse_args()

    if args.mode == 'train':
        run_train(args)
    else:
        if not args.image:
            raise SystemExit('--image required for predict mode')
        run_predict(args)


if __name__ == '__main__':
    main()
