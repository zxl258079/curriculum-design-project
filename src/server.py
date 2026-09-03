from flask import Flask, request, jsonify, render_template
import sqlite3
import torch
import numpy as np
import os

app = Flask(__name__)

DB_PATH = "../output/rul_system.db"
MODEL_PATH = "../output/model.pth"
SCALER_PATH = "../output/y_scale.npz"


def get_db_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# 首页网页路由
@app.route("/")
def index():
    return render_template("index.html")


# 1.录入设备
@app.route("/api/add_device", methods=["POST"])
def add_device():
    data = request.get_json()
    equip_name = data.get("equip_name", "")
    equip_model = data.get("equip_model", "")
    if not equip_name:
        return jsonify({"code": -1, "msg": "设备名称不能为空"}), 400
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO device(equip_name,equip_model,create_time) VALUES(?,?,datetime('now'))",
                (equip_name, equip_model))
    conn.commit()
    equip_id = cur.lastrowid
    conn.close()
    return jsonify({"code": 0, "equip_id": equip_id, "msg": "设备录入成功"})


# 2.RUL预测接口
@app.route("/api/predict_rul", methods=["POST"])
def predict_rul():
    req = request.get_json()
    equip_id = req.get("equip_id")
    sample = req.get("sample")
    if equip_id is None or sample is None:
        return jsonify({"code": -1, "msg": "参数缺失"}),400

    # 加载模型与归一化参数
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        return jsonify({"code":-2,"msg":"模型文件不存在，请先运行train.py训练模型"}),500

    checkpoint = torch.load(MODEL_PATH, map_location=torch.device("cpu"))
    model = checkpoint["model"]
    model.eval()
    scale_data = np.load(SCALER_PATH, allow_pickle=True)
    y_mean = scale_data["y_mean"]
    y_std = scale_data["y_std"]

    input_tensor = torch.tensor(sample, dtype=torch.float32)
    with torch.no_grad():
        pred_norm = model(input_tensor)
    pred_norm_val = float(pred_norm.numpy()[0][0])
    pred_rul = pred_norm_val * y_std + y_mean

    # 生成运维建议
    if pred_rul <= 30:
        suggestion = "剩余寿命较低，建议立即停机检修"
    elif pred_rul <= 80:
        suggestion = "进入预警区间，建议加强巡检，择机维护"
    else:
        suggestion = "设备状态良好，继续正常运行"

    # 写入数据库
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO predict_record(equip_id,rul_result,suggestion,predict_time) VALUES(?,?,?,datetime('now'))",
                (equip_id, float(pred_rul), suggestion))
    conn.commit()
    conn.close()

    return jsonify({
        "code":0,
        "predict_rul": round(float(pred_rul),2),
        "predict_norm": round(pred_norm_val,4),
        "suggestion": suggestion
    })


# 3.查询历史记录
@app.route("/api/get_history", methods=["GET"])
def get_history():
    equip_id = request.args.get("equip_id")
    if equip_id is None:
        return jsonify({"code":-1,"msg":"缺少equip_id"}),400
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.id as record_id,d.equip_name,r.rul_result,r.suggestion,r.predict_time
        FROM predict_record r LEFT JOIN device d ON r.equip_id=d.equip_id
        WHERE r.equip_id=? ORDER BY r.predict_time DESC
    """,(equip_id,))
    rows = cur.fetchall()
    res = []
    for row in rows:
        res.append({
            "record_id":row["record_id"],
            "equip_name":row["equip_name"],
            "predict_rul":row["rul_result"],
            "suggestion":row["suggestion"],
            "time":row["predict_time"]
        })
    conn.close()
    return jsonify({"code":0,"data":res})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
