import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import gym

# 超参数
BATCH_SIZE = 32 # 批训练的数据个数
LR = 0.01 # 学习率
EPSILON = 0.9 # 贪婪度 greedy policy
GAMMA = 0.9 # 奖励递减值
TARGET_REPLACE_ITER = 100 # Q 现实网络的更新频率
MEMORY_CAPACITY = 2000 # 记忆库大小
env = gym.make('CartPole-v0').unwrapped # 创建游戏环境,使用gym库中的环境：CartPole，且打开封装
N_ACTIONS = env.action_space.n # 获取动作的个数(2),输出维度
N_STATES = env.observation_space.shape[0] # 获取状态的个数(4),输入维度

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(N_STATES, 50)
        self.fc1.weight.data.normal_(0, 0.1) # initialization
        #用均值为 0，标准差为 0.1 的正态分布来初始化神经网络的第一个全连接层（fc1）的权重。这是一种用于初始化神经网络权重的常见技术，用于打破对称性并防止 0 梯度。通过以这种方式初始化权重，模型能够更有效地学习。
        self.out = nn.Linear(50, N_ACTIONS)
        self.out.weight.data.normal_(0, 0.1) # initialization

    # 给第一个全连接层（self.fc1），然后在第二行使用 F.relu 函数对输出结果进行 ReLU 激活。ReLU（Rectified Linear Unit）是一种常用的神经网络激活函数，它对输入值取 max(0, x)，即取 0 和输入值的最大值。ReLU 函数可以帮助模型更快地收敛并有更好的性能。
    # 最后，代码的第三行将 ReLU 激活的输出结果传递给输出层（self.out）并返回最终的输出结果 actions_value。
    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        actions_value = self.out(x)
        return actions_value

    #定义DQN类，主线思路是围绕eval_net和target_net两个网络展开，定义choose_action函数实现部分贪婪策略选择action，store_transition函数实现经验的存储管理，最核心的函数是learn函数，当经验池中存放满了经验之后，智能体开始在池中随机抽取经验进行学习，每次抽取BATCH_SIZE的行数，经过整理后得到b_s,b_a,b_r,b_s_四个可以被送入神经网络的张量
class DQN(object):
    def __init__(self):
        self.eval_net, self.target_net = Net(), Net() # 定义两个网络，eval_net用于选择action，target_net用于计算target
        self.learn_step_counter = 0 # 用于 target 更新计时
        self.memory_counter = 0 # 记忆库记数
        self.memory = np.zeros((MEMORY_CAPACITY, N_STATES * 2 + 2)) # 初始化记忆库
        self.optimizer = torch.optim.Adam(self.eval_net.parameters(), lr=LR) # torch 的优化器
        self.loss_func = nn.MSELoss() # 损失函数

    def choose_action(self, x):
        x = torch.unsqueeze(torch.FloatTensor(x), 0) # 将输入的状态转换成tensor, 并防止维度不匹配
        # 随机探索,使用随机数来决定是否进行探索。如果随机数小于 EPSILON，则模型会选择随机动作；否则，模型会选择估值最大的动作。
        if np.random.uniform() < EPSILON: # 从区间 [0,1) 中随机取一个数，并且这个数小于某个阈值 EPSILON，则这一条件成立
            action_value = self.eval_net.forward(x) # 通过 eval_net 选择动作
            action = torch.max(action_value, 1)[1].data.numpy() # 选择估值最大的动作
            action = action[0]
        else:
            action = np.random.randint(0, N_ACTIONS) # 随机选择动作
        return action

    # 存储记忆
    def store_transition(self, s, a, r, s_):
        transition = np.hstack((s, [a, r], s_))
        # 如果记忆库满了则覆盖旧的
        index = self.memory_counter % MEMORY_CAPACITY
        self.memory[index, :] = transition
        self.memory_counter += 1

    # 学习
    def learn(self):
        # 更新目标网络
        if self.learn_step_counter % TARGET_REPLACE_ITER == 0: # 每隔一段时间更新一次 target_net 的参数
            self.target_net.load_state_dict(self.eval_net.state_dict()) # 将 eval_net 的参数复制到 target_net
        self.learn_step_counter += 1 # 计数器加一

        # 抽取记忆库中的数据
        sample_index = np.random.choice(MEMORY_CAPACITY, BATCH_SIZE) # 随机抽取记忆库中的 BATCH_SIZE 个数据
        b_memory = self.memory[sample_index, :] # 从记忆库中抽取出来的数据
        # 将32个s抽出，转为32-bit floating point形式，并存储到b_s中，b_s为32行4列
        b_s = torch.FloatTensor(b_memory[:, :N_STATES]) # 抽取出来的状态,从数组 b_memory 中选取状态信息，并将其转换为 PyTorch 的 tensor
        # 将32个a抽出，转为64-bit integer (signed)形式，并存储到b_a中 (之所以为LongTensor类型，是为了方便后面torch.gather的使用)，b_a为32行1列
        b_a = torch.LongTensor(b_memory[:, N_STATES:N_STATES+1].astype(int)) # 抽取出来的动作
        # 将32个r抽出，转为32-bit floating point形式，并存储到b_s中，b_r为32行1列
        b_r = torch.FloatTensor(b_memory[:, N_STATES+1:N_STATES+2]) # 抽取出来的奖励
        # 将32个s_抽出，转为32-bit floating point形式，并存储到b_s中，b_s_为32行4列
        b_s_ = torch.FloatTensor(b_memory[:, -N_STATES:]) # 抽取出来的下一个状态

        # 获取32个transition的评估值和目标值，并利用损失函数和优化器进行评估网络参数更新
        # eval_net(b_s)通过评估网络输出32行每个b_s对应的一系列动作值，然后.gather(1, b_a)代表对每行对应索引b_a的Q值提取进行聚合
        q_eval = self.eval_net(b_s).gather(1, b_a) # 通过 eval_net 选择动作
        # q_next不进行反向传递误差，所以detach；q_next表示通过目标网络输出32行每个b_s_对应的一系列动作值
        q_next = self.target_net(b_s_).detach() # 通过 target_net 选择动作
        # q_target表示32个transition的目标值，
        # q_next.max(1)[0]表示只返回每一行的最大值，不返回索引(长度为32的一维张量)；
        # .view()表示把前面所得到的一维张量变成(BATCH_SIZE, 1)的形状；最终通过公式得到目标值
        q_target = b_r + GAMMA * q_next.max(1)[0].view(BATCH_SIZE, 1) #
        # 计算损失函数
        loss = self.loss_func(q_eval, q_target)
        # 优化器优化
        self.optimizer.zero_grad() # 清空上一步的残余更新参数值
        loss.backward() # 误差反向传播，计算参数更新值
        self.optimizer.step() # 更新评估网络的所有参数,将参数更新值施加到 eval_net 的 parameters 上

