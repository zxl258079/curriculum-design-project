import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler,MinMaxScaler

def load_data(file_path):
    col_names = ["engine_id","cycle","setting1","setting2","setting3"] + [f"s{i}" for i in range(1,24)]
    df = pd.read_csv(file_path, sep=',', names=col_names, index_col=False)
    print("读取文件行数：",len(df))
    print(df.head(2))
    return df


def sliding_window(data,window_size=30):
    x_list = []
    y_list = []
    engines = data["engine_id"].unique()
    for eng in engines:
        eng_data = data[data["engine_id"]==eng].copy()
        rul = eng_data["RUL"].values
        sensor = eng_data.loc[:,[f"s{i}" for i in range(1,22)]].values
        for i in range(window_size,len(eng_data)):
            x_list.append(sensor[i-window_size:i,:])
            y_list.append(rul[i])
    return np.array(x_list),np.array(y_list)


if __name__ == "__main__":
    data_dir = "../data"
    train_raw = load_data(os.path.join(data_dir,"train_FD001.txt"))

    sensor_cols = [f"s{i}" for i in range(1,22)]
    train_raw[sensor_cols] = train_raw[sensor_cols].fillna(0.0)

    max_cycle = train_raw.groupby("engine_id")["cycle"].max()
    rul_table = []
    for eid in train_raw["engine_id"].unique():
        mc = max_cycle[eid]
        part = train_raw[train_raw.engine_id==eid].copy()
        part["RUL"] = mc - part["cycle"]
        rul_table.append(part)
    train_df = pd.concat(rul_table)

    scaler_x = StandardScaler()
    train_df[sensor_cols] = scaler_x.fit_transform(train_df[sensor_cols])

    x_train,y_train = sliding_window(train_df,window_size=30)

    scaler_y = MinMaxScaler(feature_range=(0,1))
    y_train = scaler_y.fit_transform(y_train.reshape(-1,1)).flatten()

    np.savez(os.path.join(data_dir,"processed_train.npz"),
             x_train=x_train,
             y_train=y_train)

    print(f"训练样本shape:{x_train.shape}")
    print(f"y范围：{y_train.min():.2f} ~ {y_train.max():.2f}")
