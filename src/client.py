import requests

base = "http://127.0.0.1:5000"

def test():
    # 添加设备
    r1 = requests.post(f"{base}/api/add_device", json={"equip_name":"轴承‑01","equip_model":"IMS‑B01"})
    print(r1.json())
    dev_id = r1.json()["device_id"]

    # 预测
    r2 = requests.post(f"{base}/api/predict_rul", json={"device_id":dev_id})
    print(r2.json())

    # 查询
    r3 = requests.post(f"{base}/api/query_history", json={})
    print(r3.json())

if __name__ == "__main__":
    test()
