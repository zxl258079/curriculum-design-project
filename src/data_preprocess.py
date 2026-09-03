import pandas as pd
import numpy as np
import os

def load_data(filepath):
    df = pd.read_csv(filepath, sep="\s+", header=None)
    df.columns = ["unit_id","cycle","setting1","setting2","setting3"] + [f"s{i}" for i in range(1,22)]
    return df

def preprocess(df):
    # 简单缺失值填充
    df = df.fillna(df.mean())
    # 归一化
    cols = [f"s{i}" for i in range(1,22)]
    df[cols] = (df[cols] - df[cols].mean()) / df[cols].std()
    return df

def create_sequences(df, window=30):
    seq = []
    for uid in df["unit_id"].unique():
        u_df = df[df["unit_id"]==uid].sort_values("cycle")
        arr = u_df[[f"s{i}" for i in range(1,22)]].values
        for i in range(window, len(arr)):
            seq.append(arr[i-window:i])
    return np.array(seq, dtype=np.float32)

if __name__ == "__main__":
    data_path = "../data/train_FD001.txt"
    df = load_data(data_path)
    df = preprocess(df)
    seqs = create_sequences(df, window=30)
    print(f"生成样本：{seqs.shape}")
    np.save("../output/x_scale.npy", seqs)
