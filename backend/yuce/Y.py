import tensorflow as tf
import numpy as np
import pandas as pd


def yuce_func(file_path):
    # (1) 读取数据集
    # filepath = 'climate.csv'
    filepath = file_path  # 预测文件路径
    data = pd.read_csv(filepath)
    print(data.head())

    # (2) 特征选择
    feat = data.iloc[:, 1:11]
    date = data.iloc[:, 0]  # 获取日期

    # 预处理
    train_num = 20000
    val_num = 23000

    # 每个特征列的均值和标准差
    feat_mean = feat[:train_num].mean(axis=0)
    feat_std = feat[:train_num].std(axis=0)

    # 标准化
    feat = (feat - feat_mean) / feat_std

    targets = feat.iloc[:, 1]  # 取标准化后的气温数据作为标签

    def TimeSeries(dataset, start_index, history_size, end_index, step, target_size, point_time, true):
        data = []
        labels = []

        start_index = start_index + history_size  # 第一次的取值范围[0:start_index]

        if end_index is None:
            end_index = len(dataset) - target_size

        for i in range(start_index, end_index):
            index = range(i - history_size, i, step)  # 第一次相当于range(0, start_index, 6)
            data.append(dataset.iloc[index])
            if point_time:  # 预测某一个时间点
                labels.append(true[i + target_size])
            else:  # 预测某一时间区间
                labels.append(true[i:i + target_size])

        return np.array(data), np.array(labels)

    history_size = 5 * 24 * 6  # 每个滑窗取5天的数据量=720
    target_size = 0  # 预测未来下一个时间点的气温值
    step = 1  # 步长1

    # 构造测试集
    x_test, y_test = TimeSeries(dataset=feat, start_index=val_num, history_size=history_size, end_index=25000,
                                step=step, target_size=target_size, point_time=True, true=targets)

    # 加载保存的模型
    model = tf.keras.models.load_model('climate_model.h5')

    # 预测阶段
    x_predict = x_test[:200]  # 用测试集的前200组特征数据来预测
    y_true = y_test[:200]  # 每组特征对应的标签值

    y_predict = model.predict(x_predict)  # 对测试集的特征进行预测
    date1 = []
    for i in date[val_num:val_num + len(y_true)][:200]:
        # print(i)
        date1.append(str(i))
    yuce = []
    for i in y_predict:
        yuce.append(float(i[0]))
        # yuce.append('%.6f' % i[0])
    yuanshi = []
    for i in y_true:
        yuanshi.append(float(i))

    # 保存预测结果到 CSV 文件
    results_df = pd.DataFrame({
        'Date': date[val_num:val_num + len(y_true)][:200],  # 对应的日期
        'Actual': y_true.flatten(),  # 真实值
        'Predicted': y_predict.flatten()  # 预测值
    })
    import os
    os.makedirs('static', exist_ok=True)
    results_df.to_csv('static/predictions.csv', index=False)
    print("预测结果已保存为 'predictions.csv'")
    return {
        'date': date1,
        'yuanshi': yuanshi,
        'yuce': yuce,
    }
    #

# yuce_func('climate.csv')
