from flask import Flask, render_template, request, jsonify
import sqlite3
from predict import get_rul_pred

app = Flask(__name__)
DB = "cmapss_rul.db"

def get_conn():
    return sqlite3.connect(DB)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/add_device", methods=["POST"])
def add_device():
    data = request.get_json()
    name = data.get("equip_name","")
    model = data.get("equip_model","")
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO device(equip_name,equip_model) VALUES (?,?)",(name,model))
    conn.commit()
    dev_id = cur.lastrowid
    conn.close()
    return jsonify({"code":0,"device_id":dev_id})

@app.route("/api/predict_rul", methods=["POST"])
def predict_rul():
    data = request.get_json()
    dev_id = data.get("device_id")
    res = get_rul_pred()
    rul = res["rul"]
    status = res["health_status"]
    advice = res["advice"]

    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO predict_record(device_id,pred_rul,health_status,advice)
    VALUES (?,?,?,?)
    ''',(dev_id, rul, status, advice))
    conn.commit()
    conn.close()
    return jsonify({"code":0,**res})

@app.route("/api/query_history", methods=["POST"])
def query_history():
    data = request.get_json()
    dev_id = data.get("device_id")
    conn = get_conn()
    cur = conn.cursor()
    if dev_id:
        cur.execute('''
        SELECT pr.id,d.equip_name,d.equip_model,pr.pred_rul,pr.health_status,pr.advice,pr.predict_time
        FROM predict_record pr LEFT JOIN device d ON pr.device_id=d.id WHERE pr.device_id=?
        ''',(dev_id,))
    else:
        cur.execute('''
        SELECT pr.id,d.equip_name,d.equip_model,pr.pred_rul,pr.health_status,pr.advice,pr.predict_time
        FROM predict_record pr LEFT JOIN device d ON pr.device_id=d.id
        ''')
    rows = cur.fetchall()
    conn.close()
    lst = []
    for r in rows:
        lst.append({
            "id":r[0],
            "equip_name":r[1],
            "equip_model":r[2],
            "pred_rul":r[3],
            "health_status":r[4],
            "advice":r[5],
            "predict_time":r[6]
        })
    return jsonify({"code":0,"data":lst})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
