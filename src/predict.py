import torch
import numpy as np
from train import SimpleRULModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_path = "../output/model.pth"

model = SimpleRULModel().to(device)
model.load_state_dict(torch.load(model_path, map_location=device))
model.eval()

def get_rul_pred():
    # 课设演示：模拟输入一段时序，输出RUL
    dummy_seq = np.random.randn(1,30,21).astype(np.float32)
    x = torch.from_numpy(dummy_seq).to(device)
    with torch.no_grad():
        pred = model(x).item()
    rul = np.clip(pred,25,120)

    if rul < 40:
        status = "故障风险高"
        advice = "尽快停机检修"
    elif 40 <= rul <80:
        status = "状态一般"
        advice = "加强巡检"
    else:
        status = "状态良好"
        advice = "正常运行"
    return {"rul":round(rul,1), "health_status":status, "advice":advice}

if __name__ == "__main__":
    res = get_rul_pred()
    print(res)
