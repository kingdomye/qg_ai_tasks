import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import pandas as pd


# 定义神经网络
class BinaryClassifier(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(BinaryClassifier, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = x.float()
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.sigmoid(out)
        return out


# 准备数据
dataset = pd.read_csv('./banana.dat', header=None)
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values
y = np.where(y < 0, 0, 1)

X_tensor = torch.from_numpy(X)
y_tensor = torch.from_numpy(y)
dataset = TensorDataset(X_tensor, y_tensor)
dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

# 初始化网络
input_size = 2
hidden_size = 10
output_size = 1
model = BinaryClassifier(input_size, hidden_size, output_size)

# 定义损失函数和优化器
criterion = nn.BCELoss()
optimizer = optim.SGD(model.parameters(), lr=0.005)

# 训练网络
epochs = 100
for epoch in range(epochs):
    for inputs, targets in dataloader:
        outputs = model(inputs)
        outputs = outputs.squeeze()
        targets = targets.float()
        if outputs.shape != targets.shape:
            outputs = outputs.view_as(targets)
        loss = criterion(outputs, targets)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f"Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}")
    if loss.item() < 0.0025:
        break

# 测试网络
model.eval()
with torch.no_grad():
    predictions = model(X_tensor)
    predicted_labels = (predictions > 0.5).float()

true_numbers = 0
for i in range(len(predicted_labels)):
    if int(predicted_labels[i].item()) == int(y_tensor[i].item()):
        true_numbers += 1

print(f"Accuracy: {true_numbers / len(predicted_labels) * 100}%")
