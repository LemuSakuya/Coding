import torch
import torch.nn as nn

class MNISTMLP(nn.Module):
    def __init__(self, input_dim=784, hidden1=256, hidden2=128, num_classes=10):
        super().__init__()
        self.net = nn.Sequential(
            nn.Flatten(),
            nn.Linear(input_dim, hidden1),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden1, hidden2),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden2, num_classes)
        )

    def forward(self, x):
        return self.net(x)
