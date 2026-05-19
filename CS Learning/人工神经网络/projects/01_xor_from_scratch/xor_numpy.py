import numpy as np

X = np.array([[0,0],[0,1],[1,0],[1,1]], dtype=np.float64)
y = np.array([0,1,1,0], dtype=np.int64)

np.random.seed(0)

def sigmoid(x):
    return 1/(1+np.exp(-x))

def sigmoid_grad(x):
    s = sigmoid(x)
    return s*(1-s)

class TwoLayerNet:
    def __init__(self, D, H):
        self.W1 = np.random.randn(D, H) * 0.1
        self.b1 = np.zeros((1, H))
        self.W2 = np.random.randn(H, 1) * 0.1
        self.b2 = np.zeros((1,1))

    def forward(self, X):
        self.Z1 = X.dot(self.W1) + self.b1
        self.A1 = np.tanh(self.Z1)
        self.Z2 = self.A1.dot(self.W2) + self.b2
        self.probs = sigmoid(self.Z2).reshape(-1)
        return self.probs

    def loss_and_grads(self, X, y):
        N = X.shape[0]
        probs = self.forward(X)
        eps = 1e-12
        loss = -np.mean(y * np.log(probs+eps) + (1-y) * np.log(1-probs+eps))

        dZ2 = (probs - y).reshape(-1,1) / N
        dW2 = self.A1.T.dot(dZ2)
        db2 = np.sum(dZ2, axis=0, keepdims=True)

        dA1 = dZ2.dot(self.W2.T)
        dZ1 = dA1 * (1 - np.tanh(self.Z1)**2)
        dW1 = X.T.dot(dZ1)
        db1 = np.sum(dZ1, axis=0, keepdims=True)

        grads = {'W1':dW1, 'b1':db1, 'W2':dW2, 'b2':db2}
        return loss, grads

    def step(self, grads, lr=0.1):
        self.W1 -= lr * grads['W1']
        self.b1 -= lr * grads['b1']
        self.W2 -= lr * grads['W2']
        self.b2 -= lr * grads['b2']


def train():
    net = TwoLayerNet(2, 4)
    epochs = 10000
    lr = 0.1
    for e in range(epochs):
        loss, grads = net.loss_and_grads(X, y)
        net.step(grads, lr)
        if e % 1000 == 0:
            preds = (net.forward(X) > 0.5).astype(int)
            acc = np.mean(preds == y)
            print(f"Epoch {e}, loss={loss:.6f}, acc={acc:.3f}")
    preds = (net.forward(X) > 0.5).astype(int)
    acc = np.mean(preds == y)
    print('Final acc:', acc)

if __name__ == '__main__':
    train()
