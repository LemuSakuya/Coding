"""
分子性质预测脚本
主要功能：使用训练好的模型预测分子性质
"""

import csv
import numpy as np
from fpgnn.tool import set_predict_argument, get_scaler, load_args, load_data, load_model
from fpgnn.train import predict
from fpgnn.data import MoleDataSet

def predicting(args):
    """执行分子性质预测
    
    Args:
        args: 参数对象，包含预测配置
    """
    # 加载模型参数和数据标准化器
    print('Load args.')
    scaler = get_scaler(args.model_path)  # 获取数据标准化器
    print('scaler', scaler)
    train_args = load_args(args.model_path)  # 加载训练参数
    
    # 合并参数
    for key, value in vars(train_args).items():
        if not hasattr(args, key):
            setattr(args, key, value)

    # 加载测试数据
    print('Load data.')
    test_data = load_data(args.predict_path, args)
    
    # 加载模型并进行预测
    print('Load model')
    model = load_model(args.model_path, args.cuda)  # 加载训练好的模型
    test_pred = predict(model, test_data, args.batch_size, scaler)  # 执行预测
    
    # 验证预测结果
    assert len(test_data) == len(test_pred)
    test_pred = np.array(test_pred)
    test_pred = test_pred.tolist()  # 转换为列表格式
    
    # 将预测结果写入CSV文件
    print('Write result.')
    write_smile = test_data.smile()  # 获取分子SMILES字符串
    with open(args.result_path, 'w', newline='') as file:
        writer = csv.writer(file)
        
        # 写入表头
        line = ['Smiles']  # 第一列为SMILES
        line.extend(args.task_names)  # 添加任务名称作为列名
        writer.writerow(line)
        
        # 写入每行数据
        for i in range(len(test_data)):
            line = []
            line.append(write_smile[i])  # 添加SMILES
            line.extend(test_pred[i])  # 添加预测结果
            writer.writerow(line)

if __name__ == '__main__':
    # 主程序入口
    args = set_predict_argument()  # 获取预测参数
    predicting(args)  # 执行预测
    