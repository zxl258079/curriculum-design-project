from flask import Flask, request, jsonify
import sqlite3
import numpy as np
import torch
import os

app = Flask(__name__)
db_path = "../output/rul_system.db"

# --------模型加载，和你现有项目保持一致--------
feature_num = 21
window_size = 30

class LstmRUL(torch.nn.Module):
    def __init__(self, input_size, hidden_size=64):
        super().__init__()
        self.lstm = torch.nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = torch.nn.Linear(hidden_size,1)
    def forward(self,x):
        out,_ = self.lstm(x)
        last = out[:,-1,:]
        return self.fc(last)

model = LstmRUL(feature_num,64)
model_weight_path = "../output/model.pth"
if os.path.exists(model_weight_path):
    model.load_state_dict(torch.load(model_weight_path,map_location=torch.device("cpu")))
model.eval()

# 运维建议阈值
def get_suggestion(rul):
    if rul>80:
        return "设备健康，正常运行，常规巡检"
    elif 30<rul<=80:
        return "状态下降，增加巡检频次，密切监控传感器数据"
    else:
        return "剩余寿命不足，建议停机开展维护检修"

# ----------------API接口----------------
@app.route("/api/upload_data",methods=["POST"])
def upload_data():
    """模拟上传设备与传感器数据"""
    data = request.get_json()
    equip_name = data.get("equip_name","涡轮发动机‑001")
    equip_type = data.get("equip_type","航空涡轮发动机")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("INSERT INTO equipment_info(equip_name,equip_type) VALUES (?,?)",(equip_name,equip_type))
    equip_id = cur.lastrowid
    conn.commit()
    conn.close()
    return jsonify({"code":0,"msg":"设备信息入库成功","equip_id":equip_id})


@app.route("/api/predict_rul",methods=["POST"])
def predict_rul():
    """执行RUL预测"""
    req = request.get_json()
    equip_id = req.get("equip_id")
    sample_np = np.array(req["sample"],dtype=np.float32)
    tensor_x = torch.from_numpy(sample_np).float()

    with torch.no_grad():
        pred_norm = model(tensor_x).item()
    pred_rul = pred_norm * 130
    suggestion = get_suggestion(pred_rul)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO predict_record(equip_id,predict_rul,suggestion) VALUES (?,?,?)
    ''',(equip_id,pred_rul,suggestion))
    conn.commit()
    conn.close()

    return jsonify({
        "code":0,
        "predict_norm":round(pred_norm,4),
        "predict_rul":round(pred_rul,2),
        "suggestion":suggestion
    })


@app.route("/api/get_history",methods=["GET"])
def get_history():
    equip_id = request.args.get("equip_id")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''
    SELECT pr.id,ei.equip_name,pr.predict_rul,pr.suggestion,pr.create_time
    FROM predict_record pr
    LEFT JOIN equipment_info ei ON pr.equip_id=ei.id
    WHERE pr.equip_id=?
    ORDER BY pr.create_time DESC
    ''',(equip_id,))
    rows = cur.fetchall()
    conn.close()
    res = []
    for r in rows:
        res.append({
            "record_id":r[0],
            "equip_name":r[1],
            "predict_rul":r[2],
            "suggestion":r[3],
            "time":r[4]
        })
    return jsonify({"code":0,"data":res})


if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5000,debug=False)
