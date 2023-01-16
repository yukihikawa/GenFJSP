import math
import random
import time

import numpy as np

from src.LLH import lowlevelheuristic as llh
from src.LLH.encoding import initializeResult

heuristics = llh.LLHolder()
heuristics2 = llh.LLHolder2()
heuristics3 = llh.LLHolder3()

#基于种群的优化策略
def populationStrategy(population, parameters, iter):
    t0 = time.time()
    # Evaluate the population

    for i in range(0, iter):
        # 输出当前循环号
        print('iter ', i)

        # 用索引遍历population
        for j in range(0, len(population)):
            function = heuristics[random.randint(0, len(heuristics) - 1)]

            newS = function(population[j], parameters)
            if llh.timeTaken(newS, parameters) < llh.timeTaken(population[j], parameters):
                population[j] = newS
            #population[j] = llh.SAWarapper(function, population[j], parameters, 100, 1, 0.9)


    t1 = time.time()
    total_time = t1 - t0
    print("Finished in {0:.2f}s".format(total_time))

    return population

# 纯随机选择策略
def randomStrategy(result, parameters, iter):
    t0 = time.time()
    # Evaluate the population
    lastBest = result
    historyBestTime = llh.timeTaken(result, parameters)
    for i in range(0, iter):
        idx = random.randint(0, len(heuristics) - 1)
        print('heuristic ', idx + 1, ' selected, given time: ', llh.timeTaken(lastBest, parameters))
        newResult = heuristics[idx](lastBest, parameters)
        #newResult = llh.SAWarapper(heuristics[idx], lastBest, parameters)
        nt = llh.timeTaken(newResult, parameters)
        #lt = llh.timeTaken(result, parameters)
        if nt < historyBestTime:
            lastBest = newResult
            historyBestTime = nt
            print(i, ' new Best time:', nt)
        print(i, ' new time:', llh.timeTaken(newResult, parameters))

    t1 = time.time()
    total_time = t1 - t0
    print("Finished in {0:.2f}s".format(total_time))

    return lastBest

def greedyStrategy(result, parameters, iter):
    t0 = time.time()
    # Evaluate the population
    lastBest = result
    randomAccept = result
    initResult = result
    flag = False
    historyBestTime = llh.timeTaken(result, parameters)
    for i in range(0, iter):
    # while historyBestTime > 32:
        results = []
        initResult = result
        if flag:
            initResult = initializeResult(parameters)
        for heuristic in heuristics:
            results.append(heuristic(lastBest, parameters))
            if flag:
                results.append(heuristic(randomAccept, parameters))
                results.append(heuristic(initResult, parameters))
        flag = False
        newResult = sorted(results, key=lambda cpl: llh.timeTaken(cpl, parameters))[0]
        nt = llh.timeTaken(newResult, parameters)
        # lt = llh.timeTaken(result, parameters)
        if nt < historyBestTime:
            lastBest = newResult
            historyBestTime = nt
            print(' new Best time:', nt)
        else:
            if random.randint(0, 9) < 3:
                randomAccept = newResult
                flag = True
                print('random accepted')
        print(' new time:', llh.timeTaken(newResult, parameters))

    t1 = time.time()
    total_time = t1 - t0
    print("Finished in {0:.2f}s".format(total_time))

    return lastBest

def saStrategy(result, parameters, iter):
    t0 = time.time()
    # Evaluate the population
    last = best = result

    lastTime = BestTime = llh.timeTaken(result, parameters)


    T = 100000
    t = 0
    L = 100
    k = 2
    Tmin = 1

    while T > Tmin:
        for i in range(L):
            idx = random.randint(0, len(heuristics) - 1)
            print('heuristic ', idx + 1, ' selected, given time: ', llh.timeTaken(last, parameters))
            newResult = heuristics[idx](last, parameters)
            nt = llh.timeTaken(newResult, parameters)
            if nt < BestTime:
                best = newResult
                BestTime = nt
            if nt < lastTime:
                last = newResult
                lastTime = nt
                print(' new Best time:', nt)
            else:
                p = math.exp(-(nt - lastTime) / T)
                r = np.random.uniform(low=0, high=1)
                if r < p:
                    last = newResult
        t += 1
        T *= 0.9

    t1 = time.time()
    total_time = t1 - t0
    print("Finished in {0:.2f}s".format(total_time))

    return best

# 使用遗传算法对 LLH 进行选择
def geneticStrategy(result, parameters, iter):
    t0 = time.time()
    # 初始化种群
    alo = []
    for i in range(0, 100):
        solution = []
        for j in range(0, 50):
            solution.append(random.randint(0, len(heuristics) - 1))

# 遗传算法中解的变异操作
def mutation(solution):
    idx = random.randint(0, len(solution) - 1)
    solution[idx] = random.randint(0, len(heuristics) - 1)
    return solution

# 遗传算法中基础解的交叉操作
def crossover(solution1, solution2):
    idx = random.randint(0, len(solution1) - 1)
    return solution1[0:idx] + solution2[idx:]

# 将 solution 代表的 LLH 依次应用到 result 上
def applyHeuristics(solution, result, parameters):
    for i in solution:
        result = heuristics[i](result, parameters)
    return result

# 遗传算法中解的选择操作,选择的对象是 solution, 选择依据是solution 所代表的 LLH 依次应用到 result 上,用 timeTaken() 计算时间
def selection(solutions, result, parameters):

    return sorted(solutions, key=lambda solution: llh.timeTaken(applyHeuristics(solution, result, parameters), parameters))[0:10]
