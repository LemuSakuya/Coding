import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from model import SimpleCIFARNet


def evaluate(model, device, loader, criterion):
    model.eval()
    total_loss = 0.0
    total_correct = 0
    total = 0
    with torch.no_grad():
        for X,y in loader:
            X, y = X.to(device), y.to(device)
            logits = model(X)
            loss = criterion(logits, y)
            total_loss += loss.item() * X.size(0)
            preds = logits.argmax(dim=1)
            total_correct += (preds == y).sum().item()
            total += X.size(0)
    return total_loss/total, total_correct/total


if __name__ == '__main__':
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    transform_test = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.4914,0.4822,0.4465),(0.247,0.243,0.261))])
    test_ds = datasets.CIFAR10(root='./data', train=False, download=True, transform=transform_test)
    test_loader = DataLoader(test_ds, batch_size=256, shuffle=False, num_workers=2)

    model = SimpleCIFARNet().to(device)
    criterion = nn.CrossEntropyLoss()

    loss, acc = evaluate(model, device, test_loader, criterion)
    print(f"Eval: loss={loss:.4f}, acc={acc:.4f}")
