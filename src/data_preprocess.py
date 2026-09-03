import pandas as pd
import numpy as np
import os

def load_data(filepath):
    # 逗号分隔读取csv
    df = pd.read_csv(filepath, sep=",", header=None)
    print(f"读取文件，行数:{df.shape[0]}, 列数:{df.shape[1]}")
    df.columns = ["unit_id","cycle","setting1","setting2","setting3"] + [f"s{i}" for i in range(1,22)]
    return df

def preprocess(df):
    df = df.fillna(df.mean())
    sensor_cols = [f"s{i}" for i in range(1,22)]
    df[sensor_cols] = (df[sensor_cols] - df[sensor_cols].mean()) / df[sensor_cols].std()
    return df

def create_sequences(df, window=30):
    seq = []
    sensor_cols = [f"s{i}" for i in range(1,22)]
    for uid in df["unit_id"].unique():
        u_df = df[df["unit_id"]==uid].sort_values("cycle")
        arr = u_df[sensor_cols].values
        if len(arr) > window:
            for i in range(window, len(arr)):
                seq.append(arr[i-window:i])
    return np.array(seq, dtype=np.float32)

if __name__ == "__main__":
    # ⚠️这里写csv后缀！！
    data_path = "../data/train_FD001.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"找不到文件：{data_path}，确认data目录存在train_FD001.csv")
    df = load_data(data_path)
    df = preprocess(df)
    seqs = create_sequences(df, window=30)
    print(f"生成时序样本 shape = {seqs.shape}")
    os.makedirs("../output", exist_ok=True)
    np.save("../output/x_scale.npy", seqs)
    print("✅预处理完成，已保存到output/x_scale.npy")
