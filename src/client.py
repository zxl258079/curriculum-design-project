import requests
import numpy as np

base_url = "http://127.0.0.1:5000"

def main():
    print("===== 涡轮发动机智能运维C/S客户端 =====")
    print("1. 注册录入设备信息")
    print("2. 执行设备剩余寿命RUL预测")
    print("3. 查询该设备全部历史预测记录")
    print("0. 退出")
    equip_id = None

    while True:
        op = input("\n请输入功能编号：")
        if op=="0":
            print("客户端退出")
            break
        elif op=="1":
            name = input("输入设备名称：") or "涡轮发动机‑001"
            typ = input("输入设备类型：") or "航空涡轮发动机"
            resp = requests.post(f"{base_url}/api/upload_data",json={
                "equip_name":name,"equip_type":typ
            })
            js = resp.json()
            equip_id = js["equip_id"]
            print(f"✅设备录入成功，equip_id={equip_id}")

        elif op=="2":
            if equip_id is None:
                print("⚠️请先执行1录入设备！")
                continue
            # 取一个30窗口21特征的随机模拟样本，实际项目替换成预处理后真实时序样本
            sample = np.random.randn(1,30,21).tolist()
            payload = {"equip_id":equip_id,"sample":sample}
            res = requests.post(f"{base_url}/api/predict_rul",json=payload)
            ret = res.json()
            print("--------预测结果--------")
            print(f"归一化输出：{ret['predict_norm']}")
            print(f"预测剩余寿命RUL：{ret['predict_rul']}")
            print(f"运维建议：{ret['suggestion']}")

        elif op=="3":
            if equip_id is None:
                print("⚠️请先录入设备")
                continue
            r = requests.get(f"{base_url}/api/get_history",params={"equip_id":equip_id})
            hist = r.json()["data"]
            print("====历史预测记录====")
            for item in hist:
                print(f"时间:{item['time']} | RUL:{item['predict_rul']:.2f} | 建议:{item['suggestion']}")
        else:
            print("输入无效，请重新选择")

if __name__ == "__main__":
    main()
