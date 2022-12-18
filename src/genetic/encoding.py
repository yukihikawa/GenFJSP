# This module creates a population of random OS and MS chromosomes

import random
from src import config

# 生成工序码
def generateOS(parameters):
    jobs = parameters['jobs'] # 从dict中取出

    OS = []
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
    for job in jobs:
        for op in job:
            randomMachine = random.randint(0, len(op) - 1)
            MS.append(randomMachine)
    return MS

def initializePopulation(parameters):
    gen1 = []

    for i in range(config.popSize):
        OS = generateOS(parameters)
        MS = generateMS(parameters)
        gen1.append((OS, MS))

    return gen1