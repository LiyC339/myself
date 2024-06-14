import torch
import torch.nn as nn

# input_size输入特征的维度
# hidden_size隐藏层的维度，即每个LSTM单元的隐藏状态向量的维度。
# output_size：输出的维度。
# num_layers：LSTM层的数量，默认为1。


class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers=1):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # 定义lsmt层
        # batch_first=True表示输入数据的形状是(batch_size, sequence_length, input_size)
        # 而不是默认的(sequence_length, batch_size, input_size)。
        # batch_size是指每个训练批次中包含的样本数量
        # sequence_length是指输入序列的长度
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)

        # 定义全连接层，将LSTM层的输出映射到最终的输出空间。
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        # 初始化了隐藏状态h0和细胞状态c0，并将其设为零向量。
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)

        # LSTM层前向传播
        # 将输入数据x以及初始化的隐藏状态和细胞状态传入LSTM层
        # 得到输出out和更新后的状态。
        # out的形状为(batch_size, sequence_length, hidden_size)。
        out, _ = self.lstm(x, (h0, c0))

        # 全连接层前向传播
        # 使用LSTM层的最后一个时间步的输出out[:, -1, :]（形状为(batch_size, hidden_size)）作为全连接层的输入，得到最终的输出。
        out = self.fc(out[:, -1, :])

        return out
