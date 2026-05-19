import torch
import torch.nn as nn
import torch.optim as optim

# This is a template train script. It expects a prepared dataset object that yields (input_ids, label).
# Running requires torch and a simple dataset implementation.

def train_one_epoch(model, loader, criterion, optimizer, device):
    model.train()
    total, correct = 0, 0
    for X,y in loader:
        X, y = X.to(device), y.to(device)
        optimizer.zero_grad()
        logits = model(X)
        loss = criterion(logits, y)
        loss.backward()
        optimizer.step()
        preds = logits.argmax(dim=1)
        total += X.size(0)
        correct += (preds == y).sum().item()
    return correct/total

if __name__ == '__main__':
    print('This is a template. Prepare a DataLoader and call train_one_epoch')
