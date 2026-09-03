import numpy as np
import torch
import matplotlib.pyplot as plt
from train import LstmRUL

if __name__ == "__main__":
    model_path = "../output/model.pth"
    data_file = "../data/processed_train.npz"

    data = np.load(data_file)
    x_test = data["x_train"][:200].astype(np.float32)
    y_true = data["y_train"][:200]

    model = LstmRUL(input_dim=23,hidden_dim=64)
    model.load_state_dict(torch.load(model_path))
    model.eval()

    x_t = torch.from_numpy(x_test)
    with torch.no_grad():
        y_pred = model(x_t).numpy().flatten()

    #绘图
    plt.figure(figsize=(10,4))
    plt.plot(y_true,label="真实RUL")
    plt.plot(y_pred,label="预测RUL")
    plt.legend()
    plt.title("RUL预测对比结果")
    plt.savefig("../output/predict_result.png")
    plt.show()

    mae = np.mean(np.abs(y_pred - y_true))
    print(f"MAE平均绝对误差:{mae:.2f}")
    print("预测图像保存 output/predict_result.png")
