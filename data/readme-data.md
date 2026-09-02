# 数据集说明：IMS‑Rexnord 滚动轴承全寿命退化数据集

## 1.数据集基本信息
数据集全称：IMS‑Rexnord Bearing Dataset
发布机构：University of Cincinnati, Intelligent Maintenance Systems (IMS) 中心，Rexnord公司合作
官方镜像地址：https://data.nist.gov/od/id/mds2-13WL-B74Z
数据集下载：https://blog.csdn.net/ynn4818172/article/details/113914718
>重要声明：
本项目**未选用C‑MAPSS、AI4I‑2020、NEU、CWRU**等已被本组其他同学选用的数据集，规避选题重复。

## 2.试验平台介绍
试验台安装4个Rexnord ZA‑2115双列滚动轴承，由交流电机带动保持恒定转速 **2000 RPM**，弹簧机构施加 **6000 lbs 的径向载荷**。
使用PCB 353B33高灵敏度石英ICP加速度传感器采集轴承壳体振动，NI DAQ Card 6062E采集卡记录数据。
轴承持续运行直至疲劳失效，总转数超过1亿转，模拟装备长期服役的渐进式退化过程。

## 3.选用子集：Set No.2（2nd_test）
- 采集时间段：2004‑02‑12 10:32:39 — 2004‑02‑19 06:22:39
- 文件数量：984个ASCII格式数据文件
- 采样频率：**20 kHz**
- 每个文件：1秒时长振动快照，包含20480个加速度采样点
- 采样间隔：每10分钟采集一次振动数据
- 通道配置：4个通道，分别对应Bearing1、Bearing2、Bearing3、Bearing4
- 试验结果：试验末期 **Bearing1出现外圈故障**，存在完整的从健康→退化→失效的寿命轨迹，非常适合剩余使用寿命（RUL）预测研究。

>完整原始数据集体积较大，GitHub仓库不存储全部原始文件，仅提供数据集官方获取链接；仓库内仅存放少量采样数据用于代码调试演示。

## 4.本项目数据预处理流程
1. 读取原始ASCII文本（或.mat格式）振动数据；
2. 滑动平均滤波，抑制高频电磁噪声；
3. 3‑σ准则剔除传感器跳变带来的异常采样点；
4. 提取时域退化特征：均方根RMS、峭度、均值、标准差、峰值因子；
5. 根据轴承失效时刻标定近似RUL（剩余使用寿命）标签；
6. 滑动窗口切片，生成LSTM模型所需的定长时序样本；
7. Z‑score标准化，消除量纲差异；
8. 严格按时间顺序划分训练集、验证集、测试集，防止时序数据泄露。

## 5.数据集引用
[1] Lee J, Qiu H, Yu G, et al. IMS‑Rexnord Bearing Dataset[EB/OL]. University of Cincinnati, 2007.
[2] Qiu H, Lee J, Lin J. Wavelet Filter‑based Weak Signature Detection and its Application on Roller Bearing Prognostics[J]. Journal of Sound and Vibration, 2006.
