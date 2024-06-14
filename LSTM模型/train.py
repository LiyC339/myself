import torch
from torch import nn
import load_data
import LSTMmodel as lstm
import torch.optim as optim


def evaluate_model(model, data_loader, criterion):
    # 评估模块
    model.eval()
    total_loss = 0
    with torch.no_grad():
        for batch in data_loader:
            X_batch = batch['X'].unsqueeze(1).to('cuda')
            Y_batch = batch['Y'].unsqueeze(1).to('cuda')

            outputs = model(X_batch)
            loss = criterion(outputs, Y_batch)
            total_loss += loss.item()
    return total_loss / len(data_loader)


def main():
    # 加载训练集和测试集和对应的数据加载器
    train_loader, test_loader, custom_dataset = load_data.load_data()

    # 设置超参数
    input_size = len(custom_dataset.X.columns)  # 特征数量
    hidden_size = 32  # 隐藏层大小
    # 隐藏层大小是指每个LSTM单元中的隐藏状态向量的维度，它在很大程度上影响了模型的表示能力和性能
    # 如果隐藏层太大，模型可能会过拟合训练数据，对测试数据表现不佳。
    # 如果隐藏层太小，模型可能无法捕捉到足够的信息，导致欠拟合。

    output_size = 1  # 输出大小（预测当日票房）

    num_layers = 4  # LSTM层数
    # 单层LSTM：适用于简单的序列建模任务，结构简单，计算效率高。
    # 多层LSTM：适用于复杂的序列建模任务，能够捕捉更复杂的模式和长距离依赖，但需要更多的计算资源。
    # 层数选择：需要通过实验来确定，考虑任务复杂度、数据量和计算资源。

    learning_rate = 0.01  # 学习率
    # 对于较小的网络或简单任务，较大的学习率（如 0.01)可能是合适的。
    # 对于较深的网络或复杂任务，较小的学习率（如 0.0001)可能是必要的。

    # 实例化模型、损失函数和优化器
    model = lstm.LSTMModel(input_size, hidden_size, output_size, num_layers).to('cuda')  # 在GPU上训练
    criterion = nn.SmoothL1Loss()  # 均方误差损失函数
    # 回归损失函数
    # torch.nn.MSELoss 用于回归任务，计算预测值与目标值之间的均方误差。
    # torch.nn.L1Loss 用于回归任务，计算预测值与目标值之间的平均绝对误差。
    # torch.nn.SmoothL1Loss 结合了 L1Loss 和 MSELoss 的优点，对于回归任务更为稳健。

    optimizer = optim.RMSprop(model.parameters(), lr=learning_rate)
    # model.parameters()，获取模型中所有需要训练的参数（权重和偏置）
    # SGD：适合大规模数据和需要较好泛化性能的任务，可以通过调节学习率和添加动量（Momentum）来改进。
    # RMSprop：适合处理非平稳目标，可以自动调整学习率。
    # Adam：适用于大多数情况，特别是有噪声的梯度和稀疏梯度的情形。

    # 训练模型
    try:
        epoch = 0
        model.train()  # 将模型设置为训练模型
        while True:
            for batch in train_loader:
                X_batch = batch['X'].unsqueeze(1).to('cuda')  # 增加序列维度
                Y_batch = batch['Y'].unsqueeze(1).to('cuda')

                # 前向传播
                outputs = model(X_batch)  # 经过LSTM层，全连接层，生成输出
                loss = criterion(outputs, Y_batch)  # 计算模型输出与目标值之间的损失

                # 反向传播及优化
                optimizer.zero_grad()  # 梯度清零，防止堆积

                # 反向传播PyTorch会自动计算损失相对于模型参数的梯度
                # 在这一步中，PyTorch会执行以下操作：
                # 从损失开始，沿计算图的反向方向计算梯度。
                # 对于LSTM层，这意味着计算损失相对于LSTM权重和偏置的梯度。LSTM层的反向传播包括计算输入门、遗忘门、输出门和候选记忆细胞的梯度。
                # 对于全连接层（Linear layer），计算损失相对于线性层权重和偏置的梯度。
                loss.backward()

                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)  # 添加梯度裁剪，防止梯度爆炸

                # 调用优化器的step函数，使用计算得到的梯度来更新模型参数
                # 优化器会使用学习率来缩放梯度。
                # 对于每个参数，优化器会减去相应的梯度乘以学习率，从而更新参数。
                optimizer.step()

            if (epoch + 1) % 20 == 0:
                # 每20epoch使用测试集计算一次损失,并保存模型
                test_loss = evaluate_model(model, test_loader, criterion)
                print(f'Epoch [{epoch + 1}], Train Loss: {loss.item():.4f}, Test Loss: {test_loss:.4f}')
                # 保存模型
                torch.save(model.state_dict(), f'D:/WORK/大三下/影评项目预测/LSTM模型/训练好的模型/lstm_model_{epoch+1}.pth')
                print(f"训练完成并保存模型(lstm_model_{epoch+1}.pth)。")
                model.train()
            else:
                print(f'Epoch [{epoch + 1}], Train Loss: {loss.item():.4f}')

            epoch += 1

    except KeyboardInterrupt:
        # ctrl+c中止训练
        print("训练已中止。")


if __name__ == "__main__":
    main()
