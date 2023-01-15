# python标准 GUI 库
import tkinter as tk
import sys
import numpy as np

UNIT = 40  # 像素
MAZE_H = 4  # 格子高
MAZE_W = 4  # 格子宽


class Maze(tk.Tk, object):
    def __init__(self): # 初始化
        # self.rect = None
        print("<env init>")
        super(Maze, self).__init__()
        # 动作空间,定义智能体可选的行为,action = 0-3
        self.action_space = ['u', 'd', 'l', 'r']
        # 使用变量
        self.n_actions = len(self.action_space)
        self.n_states = 2
        # 配置信息
        self.title('maze')
        self.geometry("160x160")
        # 初始化
        self.__build_maze()

    # 渲染
    def render(self):
        # time.sleep(0, 1)
        self.update()

    def reset(self): # 智能体回到初始位置

        # time.sleep(0, 1)
        self.update()
        self.canvas.delete(self.rect)
        origin = np.array([20, 20])
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red'
        )
        # return observation
        return (np.array(self.canvas.coords(self.rect)[:2]) -
                np.array(self.canvas.coords(self.oval)[:2])) / (MAZE_H * UNIT)

    # 智能体移动一步, 返回 next_state, reward, terminal
    def step(self, action): # 输入 action
        s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        # 行动分支
        if action == 0:  # 上
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:  # 下
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:  # 右
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:  # 左
            if s[0] > UNIT:
                base_action[0] -= UNIT

        # 移动
        self.canvas.move(self.rect, base_action[0], base_action[1])

        # next state
        next_coords = self.canvas.coords(self.rect)

        # 奖励函数
        if next_coords == self.canvas.coords(self.oval):
            reward = 1
            print('victory')
            done = True
        elif next_coords in [self.canvas.coords(self.hell1)]:
            reward = -1
            print('defeat')
            done = True
        else:
            reward = 0
            done = False
        s_ = (np.array(next_coords[:2]) - np.array(self.canvas.coords(self.oval)[:2])) / (MAZE_H * UNIT)
        return s_, reward, done

    # 创建迷宫 GUI
    def __build_maze(self):
        # 新建画布
        self.canvas = tk.Canvas(self, bg='white', height=MAZE_H * UNIT, width=MAZE_W * UNIT)

        # 建立格子
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        # 起点
        origin = np.array([20, 20])

        # 创建黑洞
        hell1_center = origin + np.array([UNIT * 2, UNIT])
        self.hell1 = self.canvas.create_rectangle(
            hell1_center[0] - 15, hell1_center[1] - 15,
            hell1_center[0] + 15, hell1_center[1] + 15,
            fill='black'
        )

        # 创建椭圆形
        oval_center = origin + UNIT * 2
        self.oval = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='yellow'
        )
        # 创建三角形
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red'
        )
        self.canvas.pack()
