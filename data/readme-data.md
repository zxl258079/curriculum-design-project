# 数据集说明
本项目采用 **IMS‑NASA IMS 轴承加速寿命数据集 2nd‑test**，是故障预测领域经典公开基准数据集。

原始数据文件 `2nd_test.mat` 体积约850MB，GitHub单文件上传上限25MB，因此不在仓库上传完整原始数据。

官方下载地址：
https://data.nist.gov/od/id/mds2-2422
非官方：https://blog.csdn.net/ynn4818172/article/details/113914718
## 数据预处理流程
1. 读取振动时序信号 `text_data`；
2. 设置滑动窗口长度1024，滑动步长512；
3. 提取时域特征：有效值RMS、峭度kurtosis、均值mean、标准差std、峰值peak；
4. 输出结构化CSV特征数据集，用于寿命预测模型训练。

仓库内 `sample_500.csv` 为**预处理后采样子集（前500条）**，用于演示格式；完整数据集可下载原始文件运行预处理脚本生成。
