# 加载数据集并划分数据集和测试集
import torch
from torch.utils.data import Dataset, DataLoader, random_split
import pandas as pd
from sklearn.preprocessing import StandardScaler


# 自定义一个数据集类
class CustomDataset(Dataset):
    def __init__(self, csv_file, transform=None):
        self.data = pd.read_csv(csv_file, encoding='GBK')
        self.transform = transform

        # 提取特征和目标变量
        self.X = self.data.drop(columns=['当日票房(万)'])  # 除了目标剩下的都是特征
        self.Y = self.data['当日票房(万)']  # 目标

        # 使用StandardScaler对数据进行标准化处理，以确保训练过程中的数值稳定性（可选）
        # pd.DataFrame()函数，可以将数据从不同的数据源（如列表、字典、NumPy数组等）转换成数据帧
        self.scaler = StandardScaler()
        self.X = pd.DataFrame(self.scaler.fit_transform(self.X), columns=self.X.columns)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        # 从self.X中选择索引为idx的行，并将其赋值给X_sample
        X_sample = self.X.iloc[idx]
        Y_sample = self.Y.iloc[idx]

        # 特征数据和标签数据都被转换为float32类型的PyTorch张量。
        sample = {'X': torch.tensor(X_sample.values, dtype=torch.float32),
                  'Y': torch.tensor(Y_sample, dtype=torch.float32)}

        # 在这里进行数据预处理，如果需要的话
        if self.transform:
            sample = self.transform(sample)

        return sample


def load_data():
    # 读取CSV文件
    csv_file = 'D:/WORK/大三下/影评项目预测/数据处理/all_movie_one_year.csv'

    # 创建数据集实例
    custom_dataset = CustomDataset(csv_file)

    # 划分训练集和测试集
    train_size = int(0.9 * len(custom_dataset))  # 训练集占比90%
    test_size = len(custom_dataset) - train_size  # 测试集占比10%
    train_dataset, test_dataset = random_split(custom_dataset, [train_size, test_size])  # 按照比例随机划分

    # 创建数据加载器
    # batch_size参数用于指定每个批次（batch）中包含的样本数量。
    # 通常情况下，较大的batch_size可以加快训练速度，但可能会占用更多的内存资源。
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    # 检查数据加载器
    for batch in train_loader:
        print(batch['X'].shape, batch['Y'].shape)
        break

    return train_loader, test_loader, custom_dataset
