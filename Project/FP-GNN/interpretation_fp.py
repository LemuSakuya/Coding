import csv
import numpy as np
from fpgnn.tool import set_interfp_argument, set_log, get_scaler, load_args, load_data, load_model, rmse
from fpgnn.train import predict
from fpgnn.data import MoleDataSet

def make_fp_interpretation(args, log):
    """执行指纹解释性分析
    
    Args:
        args: 参数对象，包含分析配置
        log: 日志记录器，用于输出分析信息
    """
    info = log.info  # 获取日志记录方法
    
    # 加载模型参数
    info('Load args.')
    scaler = get_scaler(args.model_path)  # 获取数据标准化器
    train_args = load_args(args.model_path)  # 加载训练参数
    
    # 合并参数
    for key, value in vars(train_args).items():
        if not hasattr(args, key):
            setattr(args, key, value)

    # 加载测试数据
    info('Load data.')
    test_data = load_data(args.predict_path, args)
    test_label = test_data.label()
    test_label = np.squeeze(np.array(test_label))  # 处理标签形状
    
    # 初始化结果存储
    result = []
    orig_score = 0
    
    # 确定指纹类型和长度
    if hasattr(args, 'fp_type'):
        fp_type = args.fp_type
    else:
        fp_type = 'mixed'  # 默认使用混合指纹
    
    fp_length = 1490 if fp_type == 'mixed' else 1025  # 设置指纹长度
    
    # 遍历每个指纹位点进行分析
    for fp_changebit in range(fp_length):
        args.fp_changebit = fp_changebit  # 设置当前修改的指纹位点
        model = load_model(args.model_path, args.cuda, pred_args=args)  # 加载模型
        model_pred = predict(model, test_data, args.batch_size, scaler)  # 获取预测结果
        model_pred = np.array(model_pred)
        
        if fp_changebit == 0:
            # 原始指纹(未修改)的基准结果
            info('Original fingerprint. Nothing changed.')
            orig_score = rmse(test_label, model_pred)  # 计算原始RMSE
        else:
            # 修改指纹位点后的结果
            info(f'Change fingerprint bit : {fp_changebit}')
            change_score = rmse(test_label, model_pred)  # 计算修改后的RMSE
            res = orig_score - change_score  # 计算重要性分数
            info(f'Change Importance: {res}')
            result.append([fp_changebit, res])  # 存储结果
    
    # 将结果写入CSV文件
    with open(args.result_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['No_of_Bit_Changed', 'Importance'])  # 写入表头
        for row in result:
            writer.writerow(row)  # 写入每行结果

if __name__ == '__main__':
    # 主程序入口
    args = set_interfp_argument()  # 获取分析参数
    log = set_log('inter_fp', args.log_path)  # 初始化日志
    make_fp_interpretation(args, log)  # 执行指纹解释性分析
