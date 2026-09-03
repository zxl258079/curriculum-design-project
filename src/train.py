import numpy as np
import os
import torch
import torch.nn as nn
import torch.optim as optim

class LstmRUL(nn.Module):
    def __init__(self,input_dim=23,hidden_dim=64):
        super().__init__()
        self.lstm = nn.LSTM(input_size=input_dim,hidden_size=hidden_dim,batch_first=True)
        self.fc = nn.Linear(hidden_dim,1)

    def forward(self,x):
        out,_ = self.lstm(x)
        last_step = out[:,-1,:]
        pred = self.fc(last_step)
        return pred

if __name__ == "__main__":
    data_path = "../data/processed_train.npz"
    save_model_path = "../output/model.pth"
    data = np.load(data_path)
    x_train = data["x_train"].astype(np.float32)
    y_train = data["y_train"].astype(np.float32).reshape(-1,1)

    x_tensor = torch.from_numpy(x_train)
    y_tensor = torch.from_numpy(y_train)

    model = LstmRUL(input_dim=23,hidden_dim=64)
    loss_fn = nn.MSELoss()
    opt = optim.Adam(model.parameters(),lr=1e-3)
    epochs = 30

    print("开始训练···")
    for epoch in range(epochs):
        model.train()
        opt.zero_grad()
        pred = model(x_tensor)
        loss = loss_fn(pred,y_tensor)
        loss.backward()
        opt.step()
        print(f"epoch:{epoch+1:2d} | loss:{loss.item():.2f}")

    os.makedirs("../output",exist_ok=True)
    torch.save(model.state_dict(),save_model_path)
    print(f"训练结束，模型保存:{save_model_path}")
