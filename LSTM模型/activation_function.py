# 定义各个激活函数以及对应的导数
import numpy as np


class SigmoidActivator(object):
    # gate的激活函数为sigmoid函数(Logistic函数，将输出的值固定在0-1之间)
    # 前向
    def forward(self, weighted_input):
        return 1.0 / (1.0 + np.exp(-weighted_input))

    # 反向（导数）
    def backward(self, output):
        return output * (1 - output)


class TanhActivator(object):
    # 输出的激活函数为tanh，在输出ct之前需要tanh激活
    # 前向
    def forward(self, weighted_input):
        return 2.0 / (1.0 + np.exp(-2 * weighted_input)) - 1.0

    # 反向（导数）
    def backward(self, output):
        return 1 - output * output


class ReluActivator(object):
    # relu激活函数
    def forward(self, weighted_input):
        # return weighted_input
        return max(0, weighted_input)

    def backward(self, output):
        return 1 if output > 0 else 0


class IdentityActivator(object):
    # 恒等映射，不对输入进行任何变换或操作，只是简单地将输入返回作为输出
    def forward(self, weighted_input):
        return weighted_input

    def backward(self, output):
        return 1