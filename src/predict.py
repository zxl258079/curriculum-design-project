import torch
import torch.nn as nn
import numpy as np
import os

window_size = 30
feature_num = 21
RUL_MAX = 130

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
model.load_state_dict(torch.load("../output/model.pth"))
model.eval()

data = np.load("../data/processed_train.npz")
x_test_sample = data["x_train"][0:1]

x_tensor = torch.from_numpy(x_test_sample).float()

with torch.no_grad():
    pred_norm = model(x_tensor)

pred_rul = pred_norm.item() * RUL_MAX
print(f"归一化输出：{pred_norm.item():.4f}")
print(f"预测剩余寿命RUL：{pred_rul:.1f}")
