import torch
import torch.nn as nn
import numpy as np
import os

batch_size = 64
lr = 1e-4
epochs = 30
window_size = 30
feature_num = 21

data = np.load("../data/processed_train.npz")
x_train = data["x_train"]
y_train = data["y_train"]

x_tensor = torch.from_numpy(x_train).float()
y_tensor = torch.from_numpy(y_train).float().unsqueeze(-1)

dataset = torch.utils.data.TensorDataset(x_tensor, y_tensor)
dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

class LstmRUL(nn.Module):
    def __init__(self, input_size, hidden_size=64):
        super(LstmRUL, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)
    def forward(self, x):
        out, _ = self.lstm(x)
        last_step = out[:, -1, :]
        return self.fc(last_step)

model = LstmRUL(feature_num)
loss_fn = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=lr)

for epoch in range(1, epochs + 1):
    model.train()
    total_loss = 0.0
    for batch_x, batch_y in dataloader:
        optimizer.zero_grad()
        pred = model(batch_x)
        loss = loss_fn(pred, batch_y)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.8)
        optimizer.step()
        total_loss += loss.item()
    avg_loss = total_loss / len(dataloader)
    print(f"epoch:{epoch:2d} | loss:{avg_loss:.4f}")

os.makedirs("../output", exist_ok=True)
torch.save(model.state_dict(), "../output/model.pth")
print("训练结束，模型保存至 ../output/model.pth")
