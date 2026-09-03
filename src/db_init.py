import sqlite3
conn = sqlite3.connect("cmapss_rul.db")
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS device(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equip_name TEXT NOT NULL,
    equip_model TEXT NOT NULL,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
cur.execute('''CREATE TABLE IF NOT EXISTS predict_record(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id INTEGER,
    pred_rul REAL,
    health_status TEXT,
    advice TEXT,
    predict_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
conn.commit()
conn.close()
print("数据库初始化完成")
