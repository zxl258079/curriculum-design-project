import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler

def load_data(file_path):
    col_names = ["engine_id","cycle","setting1","setting2","setting3"] + [f"s{i}" for i in range(1,24)]
    df = pd.read_csv(file_path, names=col_names, index_col=False)
    return df

def sliding_window(data,window_size=30):
    x_list = []
    y_list = []
    engines = data["engine_id"].unique()
    for eng in engines:
        eng_data = data[data["engine_id"]==eng].copy()
        rul = eng_data["RUL"].values
        sensor = eng_data.loc[:,[f"s{i}" for i in range(1,24)]].values
        for i in range(window_size,len(eng_data)):
            x_list.append(sensor[i-window_size:i,:])
            y_list.append(rul[i])
    return np.array(x_list),np.array(y_list)

if __name__ == "__main__":
    data_dir = "../data"
    train_raw = load_data(os.path.join(data_dir,"sample_500.csv"))

    #构造RUL标签
    max_cycle = train_raw.groupby("engine_id")["cycle"].max()
    rul_table = []
    for eid in train_raw["engine_id"].unique():
        mc = max_cycle[eid]
        part = train_raw[train_raw.engine_id==eid].copy()
        part["RUL"] = mc - part["cycle"]
        rul_table.append(part)
    train_df = pd.concat(rul_table)

    #标准化
    sensor_cols = [f"s{i}" for i in range(1,24)]
    scaler = StandardScaler()
    train_df[sensor_cols] = scaler.fit_transform(train_df[sensor_cols])

    x_train,y_train = sliding_window(train_df,window_size=30)
    np.savez(os.path.join(data_dir,"processed_train.npz"),x_train=x_train,y_train=y_train)
    print("预处理完成，输出保存至data/processed_train.npz")
    print(f"训练样本shape:{x_train.shape}")
