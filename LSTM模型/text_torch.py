# 这是一个测试程序，检查torch是否安装成功
import torch

# 创建一个大小为5x3的张量（tensor），其中的元素是在0到1之间均匀分布的随机数
x = torch.rand(5, 3)
print(x)

# 打印版本号
print(torch.__version__)  # pytorch版本
print(torch.version.cuda)  # cuda版本
print(torch.cuda.is_available())  # 查看cuda是否可用（GPU训练）
