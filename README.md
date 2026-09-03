# 课程设计代码仓库
> 大三课设仓库：涡轮发动机剩余使用寿命RUL预测，基于LSTM时序深度学习

## 环境依赖
- python
- numpy
- pandas
- scikit‑learn
- torch

## 项目目录说明
- **data/**：原始数据集、数据说明文档
- **src/**：项目源代码
  - `data_preprocess.py`：数据集加载、清洗、标准化、滑动窗口样本生成
  - `train.py`：LSTM模型训练，梯度裁剪，保存模型权重
  - `predict.py`：加载训练权重，完成剩余寿命预测推理
- **output/**：训练输出模型权重文件
- **prompt/**：AI辅助开发对话记录json文件
- `选题说明.md`：项目选题、目标、技术方向
- `方案设计.md`：需求分析、方案论证、技术路线、进度计划、参考文献
- `学习笔记.md`：Git、AI工具、模型调研学习笔记

## 本地运行步骤
```bash
# 进入src目录
cd src

# 1.数据预处理
python data_preprocess.py

# 2.模型训练
python train.py

# 3.模型预测推理
python predict.py
