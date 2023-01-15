import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from matplotlib import pyplot as plt


class Net(nn.Module):
    def __init__(self, n_states, n_actions):
        super(Net, self).__init__()
        # 两个全连接层,
        self.fc1 = nn.Linear(n_states, 10)
        self.fc2 = nn.Linear(10, n_actions)
        self.fc1.weight.data.normal_(0, 0.1)
        self.fc2.weight.data.normal_(0, 0.1)

    def forward(self, x):
        # 前向传播
        x = self.fc1(x) # 连接第一层
        x = F.relu(x) # 激活
        out = self.fc2(x) # 连接第二层/输出
        return out



class DQN:
    def __init__(self, n_states, n_actions):
        print('<DQN init>')
        # 创建两个 Net, 具有选动作,存经历,学习的功能
        self.eval_net, self.target_net = Net(n_states, n_actions), Net(n_states, n_actions)
        self.loss = nn.MSELoss() # 定义损失函数
        self.optimizer = torch.optim.Adam(self.eval_net.parameters(), lr=0.01) # 定义优化器
        self.n_action = n_actions
        self.n_states = n_states

        # 使用变量
        self.learn_step_counter = 0 # 用于 target 网络学习更新计时
        self.memory_counter = 0 # 记忆库记数
        self.memory = np.zeros((2000, 2 * 2 + 2)) # 初始化记忆库, 2000 行, 2*2+2 列
        self.cost = [] # 记录所有 cost 变化(损失值)

    # 选择行动
    def choose_action(self, x, epsilon):
        x = torch.unsqueeze(torch.FloatTensor(x), 0) # 由x创建张量,并扩展维度
        #
        if np.random.uniform() < epsilon:
            action_value = self.eval_net.forward(x)
            action = torch.max(action_value, 1)[1].data.numpy()
        else:
            action = np.random.randint(0, self.n_action)
        return action

    # 存储记忆
    def store_transition(self, state, action, reward, next_state):
        transition = np.hstack((state, [action, reward], next_state))
        index = self.memory_counter % 200 # 满了就覆盖旧的
        self.memory[index, :] = transition
        self.memory_counter += 1

    def learn(self):
        # target net 更新频率
        if self.learn_step_counter % 200 == 0:
            self.target_net.load_state_dict(self.eval_net.state_dict())
        self.learn_step_counter += 1

        # 抽取记忆库中的批数据
        sample_index = np.random.choice(2000, 32) # 2000 个中随机抽取 32 个作为 batch_size
        memory = self.memory[sample_index, :] # 逐个提取记忆单元
        state = torch.FloatTensor(memory[:, :2])
        action = torch.LongTensor(memory[:, 2:3])
        reward = torch.FloatTensor(memory[:, 3:4])
        next_state = torch.FloatTensor(memory[:, 4:])

        q_eval = self.eval_net(state).gather(1, action) # 选取动作的值
        q_next = self.target_net(next_state).detach() # detach from graph, don't backpropagate
        q_target = reward + 0.9 * q_next.max(1)[0].unsqeeze(1) # shape (batch, 1)
        loss = self.loss(q_eval, q_target)
        self.cost.append(loss)

        # 反向传播更新
        self.optimizer.zero_grad() # 梯度重置
        loss.backward() # 反向求导
        self.optimizer.step() # 更新参数

    def plot_cost(self):
        plt.plot(np.arange(len(self.cost)), self.cost)
        plt.ylabel('Cost')
        plt.xlabel('training steps')
        plt.show()
