from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# 首页 - 直接返回HTML，不依赖templates文件夹
@app.route("/")
def index():
    return '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>航空发动机RUL智能预测系统</title>
    <style>
        body{font-family:Microsoft YaHei;margin:20px;background:#e8f4ff;}
        .box{background:#fff;padding:20px;border-radius:8px;margin-bottom:15px;box-shadow:0 1px 4px #ccc;}
        input{padding:8px;width:260px;margin:6px 0;border:1px solid #aaa;border-radius:4px;}
        button{padding:8px 16px;border:none;border-radius:4px;color:#fff;cursor:pointer;}
        .btn-blue{background:#2b78e4;}
        .btn-green{background:#28a745;}
        .btn-yellow{background:#f0ad4e;color:#222;}
        .tip{margin-top:8px;color:#226622;}
        table{width:100%;border-collapse:collapse;margin-top:10px;}
        th,td{border:1px solid #ccc;padding:8px;text-align:center;}
    </style>
</head>
<body>
<h1 style="text-align:center;">航空发动机剩余寿命RUL智能预测系统</h1>

<div class="box">
    <h3>1.设备信息录入</h3>
    <div>
        <label>设备名称</label><br>
        <input id="equip_name" placeholder="请输入设备名称"><br>
        <label>设备型号</label><br>
        <input id="equip_model" placeholder="请输入设备型号"><br>
        <button id="btn_add" class="btn-blue">录入设备</button>
        <div class="tip" id="add_tip"></div>
    </div>
</div>

<div class="box">
    <h3>2.剩余寿命RUL智能预测</h3>
    <div>
        <label>设备编号</label><br>
        <input id="predict_device_id" placeholder="输入设备编号"><br>
        <button id="btn_predict" class="btn-green">执行智能预测</button>
        <div class="tip" id="predict_tip"></div>
    </div>
</div>

<div class="box">
    <h3>3.历史预测记录查询</h3>
    <div>
        <label>设备编号</label><br>
        <input id="query_device_id" placeholder="输入设备编号(留空查全部)"><br>
        <button id="btn_query" class="btn-yellow">查询历史记录</button>
        <div id="table_wrap"></div>
    </div>
</div>

<script>
document.querySelector("#btn_add").addEventListener("click",async ()=>{
    const name=document.querySelector("#equip_name").value.trim();
    const model=document.querySelector("#equip_model").value.trim();
    const tip=document.querySelector("#add_tip");
    if(!name){tip.innerText="请填写设备名称";return;}
    const res=await fetch("/api/add_device",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({equip_name:name,equip_model:model})
    });
    const data=await res.json();
    if(data.code===0){
        tip.innerText=`设备录入成功，设备编号：${data.device_id}`;
    }else{
        tip.innerText=`录入失败：${data.msg}`;
    }
});

document.querySelector("#btn_predict").addEventListener("click",async ()=>{
    const devId=document.querySelector("#predict_device_id").value.trim();
    const tip=document.querySelector("#predict_tip");
    if(!devId){tip.innerText="请输入设备编号";return;}
    const res=await fetch("/api/predict_rul",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({device_id:devId})
    });
    const data=await res.json();
    if(data.code===0){
        tip.innerText=`预测RUL：${data.data.pred_rul}，健康状态：${data.data.health_status}，运维建议：${data.data.advice}`;
    }else{
        tip.innerText=`预测失败：${data.msg}`;
    }
});

document.querySelector("#btn_query").addEventListener("click",async ()=>{
    const devId=document.querySelector("#query_device_id").value.trim();
    const wrap=document.querySelector("#table_wrap");
    const res=await fetch("/api/query_history",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({device_id:devId})
    });
    const data=await res.json();
    if(data.code!==0){wrap.innerText=`查询失败：${data.msg}`;return;}
    let html=`<table><tr><th>记录ID</th><th>设备名称</th><th>预测RUL</th><th>健康状态</th><th>运维建议</th><th>预测时间</th></tr>`;
    for(let r of data.data){
        html+=`<tr><td>${r.id}</td><td>${r.equip_name}</td><td>${r.pred_rul}</td><td>${r.health_status}</td><td>${r.advice}</td><td>${r.predict_time}</td></tr>`;
    }
    html+=`</table>`;
    wrap.innerHTML=html;
});
</script>
</body>
</html>
'''

def get_db():
    conn = sqlite3.connect("cmapss_rul.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/api/add_device", methods=["POST"])
def add_device():
    data = request.get_json()
    equip_name = data.get("equip_name", "").strip()
    equip_model = data.get("equip_model", "").strip()
    if not equip_name:
        return jsonify({"code": -1, "msg": "设备名称不能为空"}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO device(equip_name,equip_model) VALUES (?,?)", (equip_name, equip_model))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return jsonify({"code": 0, "msg": "ok", "device_id": new_id})

@app.route("/api/predict_rul", methods=["POST"])
def predict_rul():
    data = request.get_json()
    if not data:
        return jsonify({"code": -1, "msg": "请求数据为空"}), 400
    device_id = data.get("device_id", "").strip()
    if not device_id:
        return jsonify({"code": -1, "msg": "设备编号不能为空"}), 400
    import random
    pred_rul = random.randint(25, 120)
    if pred_rul < 40:
        health_status = "故障风险高"
        advice = "尽快停机检修"
    elif pred_rul < 80:
        health_status = "状态一般"
        advice = "加强巡检"
    else:
        health_status = "状态良好"
        advice = "正常运行"
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO predict_record(device_id,pred_rul,health_status,advice) VALUES (?,?,?,?)",
                (device_id, pred_rul, health_status, advice))
    conn.commit()
    conn.close()
    return jsonify({
        "code": 0,
        "msg": "预测完成",
        "data": {"pred_rul": pred_rul, "health_status": health_status, "advice": advice}
    })

@app.route("/api/query_history", methods=["POST"])
def query_history():
    data = request.get_json()
    device_id = data.get("device_id", "").strip()
    conn = get_db()
    cur = conn.cursor()
    if device_id:
        cur.execute("SELECT pr.*,d.equip_name FROM predict_record pr LEFT JOIN device d ON pr.device_id=d.id WHERE pr.device_id=?", (device_id,))
    else:
        cur.execute("SELECT pr.*,d.equip_name FROM predict_record pr LEFT JOIN device d ON pr.device_id=d.id")
    rows = cur.fetchall()
    res = [dict(r) for r in rows]
    conn.close()
    return jsonify({"code": 0, "data": res})

if __name__ == "__main__":
    app.run(debug=True)
