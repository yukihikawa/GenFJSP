# This module creates a population of random OS and MS chromosomes

import random
from src import config


# 生成工序码:
def generateOS(parameters):
    jobs = parameters['jobs']  # 从dict中取出,jobs 为包含所有任务/工件的 list

    OS = [] # 任务的标号
    i = 0
    for job in jobs:
        for op in job:
            OS.append(i)
        i = i + 1

    random.shuffle(OS)  # 随机打乱位置

    return OS


# 生成机器码
def generateMS(parameters):
    jobs = parameters['job']

    MS = []
    for job in jobs: # 遍历每个工序
        for op in job: # 遍历工序的可选机器列表
            randomMachine = random.randint(0, len(op) - 1) # 随机选取一个可选机器
            MS.append(randomMachine)
    return MS


def initializePopulation(parameters): # 初始化种群
    gen1 = []

    for i in range(config.popSize):
        OS = generateOS(parameters)
        MS = generateMS(parameters)
        gen1.append((OS, MS))

    return gen1
