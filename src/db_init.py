import sqlite3
import os

def init_db():
    db_path = "cmapss_rul.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 设备表
    cur.execute('''
    CREATE TABLE IF NOT EXISTS device (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        equip_name TEXT NOT NULL,
        equip_model TEXT NOT NULL,
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 预测记录表
    cur.execute('''
    CREATE TABLE IF NOT EXISTS predict_record (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER NOT NULL,
        pred_rul REAL,
        health_status TEXT,
        advice TEXT,
        predict_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(device_id) REFERENCES device(id)
    )
    ''')
    conn.commit()
    conn.close()
    print("数据库初始化完成")

if __name__ == "__main__":
    init_db()
