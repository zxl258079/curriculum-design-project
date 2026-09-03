import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class SimpleRULModel(nn.Module):
    def __init__(self, input_dim=21, hidden_dim=64):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim,1)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:,-1,:])

def main():
    x = np.load("../output/x_scale.npy")
    # 模拟标签，课设演示
    y = np.random.randint(25,120,size=(x.shape[0],1)).astype(np.float32)

    x_tensor = torch.from_numpy(x).to(device)
    y_tensor = torch.from_numpy(y).to(device)

    model = SimpleRULModel().to(device)
    loss_fn = nn.MSELoss()
    opt = optim.Adam(model.parameters(), lr=1e-3)

    epochs = 10
    for epoch in range(epochs):
        model.train()
        pred = model(x_tensor)
        loss = loss_fn(pred, y_tensor)
        opt.zero_grad()
        loss.backward()
        opt.step()
        print(f"epoch:{epoch+1}, loss:{loss.item():.2f}")

    torch.save(model.state_dict(), "../output/model.pth")
    np.savez("../output/y_scale.npz", y=y)
    print("模型训练完成，已保存到output")

if __name__ == "__main__":
    main()
