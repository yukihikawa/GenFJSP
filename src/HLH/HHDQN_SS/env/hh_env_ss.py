import math
import random

import gym
import numpy as np
from gym import spaces
import src.LLH.encoding as encoding
import src.LLH.decoding as decoding
from src.utils import parser, gantt
import src.LLH.lowlevelheuristic as llh
from src.HLH.HHDQN_SS import config

problem_str = config.TRAIN_PROBLEM

# "C:\\Users\emg\PycharmProjects\GenFJSP\src\HLH\HHDQN\env\Mk01.fjs"
class hh_env_ss(gym.Env):
    def __init__(self):
        #self.factory = parser.parse(PROBLEM_STR)
        #self.solution = encoding.initializeResult(self.factory)
        #self.iter = 0
        #self.prevTime = 0
        # 定义动作空间
        self.action_space = spaces.Discrete(10)
        # 定义状态空间, 有 0-9 共 10 个整数状态
        # self.observation_space = spaces.Box(low=0, high=10, shape=(1,), dtype=np.int32)

        # 定义状态空间
        #self.observation_space = spaces.Box(low=-float('inf'), high=float('inf'), shape=(1,))
        self.observation_space = spaces.Tuple((spaces.Discrete(10), spaces.Discrete(float('inf')),
                                                   spaces.Box(-float('inf'), float('inf'), shape=(1,))))

        # self.observation_space = spaces.Discrete(10)
        # self.state = None
        self.env_name = 'hh_env_ss-v0'  # the name of this env.
        self.prev_loss = 0
        self.heuristics = llh.LLHolder()

        # self.state_dim = self.observation_space.shape[0]  # feature number of state
        # self.action_dim = self.action_space.n  # feature number of action
        # self.if_discrete = True  # discrete action or continuous action

    def step(self, action):
        self.ITER += 1
        #print("in env: action: ", action)
        #print(self.heuristics[action])
        newSolution = self.heuristics[action](self.solution, self.parameters)
        # prevTime = llh.timeTaken(self.solution, self.parameters)
        newTime = llh.timeTaken(newSolution, self.parameters)
        # 状态定义为


        # 奖励函数
        if self.prevTime > newTime:
            self.solution = newSolution
            self.prevTime = newTime
            if(self.bestTime > newTime):
                self.best_solution = newSolution
                self.bestTime = newTime
            reward = 3 + self.NOT_IMPROVED * 0.01
            self.NOT_ACCEPTED = 1
            self.NOT_IMPROVED = 1
        else:
            self.NOT_IMPROVED += 1
            if self.prevTime == newTime:
                reward = 0
            else:
                #reward = self.NOT_IMPROVED * 10 / self.ITER
                reward = 2 * math.exp(-(35 / self.NOT_IMPROVED)) - 1
                #reward = -1
                # print("mut reward: ", reward)

            # 解的接受
            p = random.random()
            temp = np.exp(-(newTime - self.prevTime) / (self.NOT_ACCEPTED * 0.01))
            if p < temp:
                #print('accepted!')
                self.solution = newSolution
                self.prevTime = newTime
                self.NOT_ACCEPTED = 1
                self.NOT_IMPROVED = 1
            else:
                self.NOT_ACCEPTED += 1
                self.NOT_IMPROVED += 1
        #print("finish time: ", self.prevTime)
        # 用 action 创建一个一维张量, 并且将其转换为整型
        #s_ = np.array([action], dtype=np.int32)
        if action in [3, 5, 6]:
            ck = 20
        else:
            ck = 40
        delta = (self.prevTime - newTime) / self.prevTime + ck
        s_ = (action, self.NOT_IMPROVED, delta)
        return s_, reward, False, {}

    def stepTest(self, action):
        newSolution = self.heuristics[action](self.solution, self.parameters)
        # prevTime = llh.timeTaken(self.solution, self.parameters)
        newTime = llh.timeTaken(newSolution, self.parameters)
        # 奖励函数
        if self.prevTime > newTime:
            self.solution = newSolution
            self.prevTime = newTime
            if(self.bestTime > newTime):
                self.best_solution = newSolution
                self.bestTime = newTime

            self.NOT_ACCEPTED = 1
        else:
            # 解的接受
            p = random.random()
            temp = np.exp(-(newTime - self.prevTime) / (self.NOT_ACCEPTED * 0.01))
            if p < temp:
                print('accepted!')
                self.solution = newSolution
                self.prevTime = newTime
                self.NOT_ACCEPTED = 1
            else:
                self.NOT_ACCEPTED += 1
                print("NOT ACCEPTED count: ", self.NOT_ACCEPTED)

        if action in [3, 5, 6]:
            ck = 20
        else:
            ck = 40
        s_ = (self.prevTime - newTime) / self.prevTime + ck
        s_ = np.array([s_], dtype=float)
        return s_, 0, False, {}



    def reset(self, **kwargs):
        self.parameters = parser.parse(problem_str)
        self.best_solution = self.solution = encoding.initializeResult(self.parameters)
        self.NOT_ACCEPTED = 1
        self.NOT_IMPROVED = 1
        self.ITER = 1
        self.prevTime = self.bestTime = llh.timeTaken(self.solution, self.parameters)
        self.prevState = random.randint(0, 10)
        # 返回一个一维的整型张量,随机取值,取值范围是[0,10)
        return np.array([self.prevState, self.NOT_IMPROVED, 0])

    def render(self, mode='human'):

        print("finish time: ", self.bestTime)
        #gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(self.parameters, self.best_solution[0], self.best_solution[1]))
        #gantt.draw_chart(gantt_data)

    def close(self):
        pass