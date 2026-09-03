import sqlite3
import os

db_path = "../output/rul_system.db"

def init_db():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 1.设备信息表
    cur.execute('''
    CREATE TABLE IF NOT EXISTS equipment_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        equip_name TEXT NOT NULL,
        equip_type TEXT,
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 2.传感器时序数据表
    cur.execute('''
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        equip_id INTEGER,
        cycle INTEGER,
        s1 REAL,s2 REAL,s3 REAL,s4 REAL,s5 REAL,
        s6 REAL,s7 REAL,s8 REAL,s9 REAL,s10 REAL,
        s11 REAL,s12 REAL,s13 REAL,s14 REAL,s15 REAL,
        s16 REAL,s17 REAL,s18 REAL,s19 REAL,s20 REAL,s21 REAL,
        FOREIGN KEY(equip_id) REFERENCES equipment_info(id)
    )
    ''')

    #3.预测运维记录表
    cur.execute('''
    CREATE TABLE IF NOT EXISTS predict_record (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        equip_id INTEGER,
        predict_rul REAL,
        suggestion TEXT,
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(equip_id) REFERENCES equipment_info(id)
    )
    ''')

    conn.commit()
    conn.close()
    print(f"数据库初始化完成，数据库文件：{db_path}")

if __name__ == "__main__":
    init_db()
