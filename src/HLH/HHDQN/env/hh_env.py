import math

import gym
import numpy as np
from gym import spaces
import src.LLH.encoding as encoding
import src.LLH.decoding as decoding
from src.utils import parser, gantt
import src.LLH.lowlevelheuristic as llh

PROBLEM_STR = "C:\\Users\emg\PycharmProjects\GenFJSP\src\HLH\HHDQN\env\Mk02.fjs"
LLH_HOLDER = llh.LLHolder()
class hh_env(gym.Env):
    def __init__(self):
        #self.factory = parser.parse(PROBLEM_STR)
        #self.solution = encoding.initializeResult(self.factory)
        #self.iter = 0
        #self.prevTime = 0
        # 定义动作空间
        self.action_space = spaces.Discrete(10)
        # 定义状态空间
        self.observation_space = spaces.Box(low=-float('inf'), high=float('inf'), shape=(1,))
        # self.state = None
        self.env_name = 'hh_env'  # the name of this env.
        self.prev_loss = 0
        # self.state_dim = self.observation_space.shape[0]  # feature number of state
        # self.action_dim = self.action_space.n  # feature number of action
        # self.if_discrete = True  # discrete action or continuous action

    def step(self, action):
        function= LLH_HOLDER[action]
        newSolution = function(self.solution, self.factory)
        time = llh.timeTaken(newSolution, self.factory)
        # 状态定义为
        if action in [4, 6, 7]:
            ck = 20
        else:
            ck = 40
        s_ = (self.prevTime - time) / self.prevTime + ck
        s_ = np.array([s_], dtype=float)
        FLAG = 1
        # 奖励函数
        if self.prevTime > time:
            self.solution = newSolution
            self.prevTime = time
            reward = 1
            FLAG = 1
        else:
            if self.prevTime == time:
                reward = 0
            else:
                reward = -1
            p = math.exp((self.prevTime - time) / (0.01 * FLAG))
            if np.random.rand() < p:
                self.solution = newSolution
                self.prevTime = time
                FLAG = 1
            else:
                FLAG += 1
        return s_, reward, False, {}

    def reset(self, **kwargs):
        self.factory = parser.parse(PROBLEM_STR)
        self.solution = encoding.initializeResult(self.factory)
        self.iter = 0
        self.prevTime = llh.timeTaken(self.solution, self.factory)
        return np.zeros(1, dtype=float)

    def render(self, mode='human'):
        print("finish time: ", self.prevTime)
        #gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(self.factory, self.solution[0], self.solution[1]))
        #gantt.draw_chart(gantt_data)

    def close(self):
        pass