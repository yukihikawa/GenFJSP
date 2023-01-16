import math
import random
from src.LLH import decoding, genetic

def LLHolder():
    llh = []
    llh.append(heuristic1)
    llh.append(heuristic2)
    llh.append(heuristic3)
    llh.append(heuristic4)
    llh.append(heuristic5)
    llh.append(heuristic6)
    llh.append(heuristic7)
    llh.append(heuristic8)
    llh.append(heuristic9)
    llh.append(heuristic10)
    llh.append(heuristic11)

    return llh

def LLHolder2():
    llh = []
    llh.append(heuristic4)
    llh.append(heuristic6)
    llh.append(heuristic7)
    llh.append(heuristic11)

    return llh
def LLHolder3():
    llh = []
    llh.append(heuristic1)
    llh.append(heuristic2)
    llh.append(heuristic3)
    llh.append(heuristic5)
    llh.append(heuristic8)
    llh.append(heuristic9)
    llh.append(heuristic10)

    return llh

# 以模拟退火机制, 调用 function,参数为 solution 和 parameters.
# 如果 solution 的 timeTaken(solution, parameters) 比原来的小,则接受新的 solution
# 否则以一定概率接受新的 solution,并存储历史上的最优值
# 降温过程结束后返回历史最优解
def SAWarapper(function, solution, parameters, maxTemp=100, minTemp=0.01, coolingRate=0.9):
    bestSolution = solution
    bestTime = timeTaken(bestSolution, parameters)
    currentSolution = solution
    currentTemp = maxTemp
    while currentTemp > minTemp:
        newSolution = function(currentSolution, parameters)
        newTime = timeTaken(newSolution, parameters)
        if newTime < bestTime:
            bestSolution = newSolution
            bestTime = newTime
        else:
            p = math.exp(-(newTime - bestTime) / currentTemp)
            if random.random() < p:
                currentSolution = newSolution
        currentTemp *= coolingRate
    return bestSolution

#
def SAWarapper2(function, solution, parameters, maxTemp=100, minTemp=0.01, coolingRate=0.9):
    bestSolution = solution
    bestTime = timeTaken(bestSolution, parameters)
    currentSolution = solution
    currentTemp = maxTemp
    FLAG = 0
    while currentTemp > minTemp:
        newSolution = function(currentSolution, parameters)
        newTime = timeTaken(newSolution, parameters)
        if newTime < bestTime:
            bestSolution = newSolution
            bestTime = newTime
            FLAG = 0
        else:
            p = math.exp(-(newTime - bestTime) / FLAG)
            if random.random() < p:
                currentSolution = newSolution
                FLAG = 0
            else:
                FLAG += 1
        currentTemp *= coolingRate
    return bestSolution

# ================== 工具方法 ===================
# 最大完成时间
def timeTaken(os_ms, pb_instance):
    (os, ms) = os_ms  # 元组
    decoded = decoding.decode(pb_instance, os, ms)  # 结构化的问题数据集

    # 每台机器的最大值
    max_per_machine = []
    for machine in decoded:
        max_d = 0
        for job in machine:  # 遍历机器的所有作业
            end = job[3] + job[1]
            if end > max_d:
                max_d = end
        max_per_machine.append(max_d)

    return max(max_per_machine)

# 改变指定机器码序列位置的机器码 已测
def changeMsRandom(machineIdx, ms, parameters):
    jobs = parameters['jobs']  # 作业的集合
    # jobIdx = os[machineIdx] # 指定的位置所属的作业序号 错误在此
    mcLength = 0  # 工具人
    jobIdx = -1  # 所属工作号

    for job in jobs:
        jobIdx += 1

        if mcLength + len(job) >= machineIdx + 1:
            break
        else:
            mcLength += len(job)

    opIdx = machineIdx - mcLength  # 指定位置对应的 在工件中的工序号

    # print('belongs to: job', jobIdx, ' op: ', opIdx, ' ava machine: ', len(jobs[jobIdx][opIdx]))
    newMachine = random.randint(0, len(jobs[jobIdx][opIdx]) - 1)
    newMs = ms.copy()
    newMs[machineIdx] = newMachine
    return newMs

# 获取指定 os 位置工序在 ms 中的位置
def getMachineIdx(jobIdx, os, parameters):
    jobNum = os[jobIdx]  # 工件号
    jobs = parameters['jobs']  # 工件集合
    machineIdx = 0  # 在 ms 中的位置
    for i in range(0, jobNum):  #
        machineIdx += len(jobs[i])
    for i in range(0, jobIdx):
        if os[i] == jobNum:
            machineIdx += 1
    return machineIdx


# =====================启发式操作++++++++++++++++++
# 1. 随机交换两个工序码, 返回新的工序码 已测
def heuristic1(os_ms, parameters):
    # print('1')
    # 随机选择两个不同机器码
    (os, ms) = os_ms
    ida = idb = random.randint(0, len(os) - 1)
    while ida == idb:
        idb = random.randint(0, len(os) - 1)

    newOs = os.copy()
    newOs[ida], newOs[idb] = newOs[idb], newOs[ida]
    return (newOs, ms)


# 2. 随机反转工序码子序列 已测
def heuristic2(os_ms, parameters):
    (os, ms) = os_ms
    ida = idb = random.randint(0, len(os) - 2)
    while ida == idb:
        idb = random.randint(0, len(os) - 1)

    if ida > idb:
        ida, idb = idb, ida

    rev = os[ida:idb + 1]
    rev.reverse()
    newOs = os[:ida] + rev + os[idb + 1:]

    return (newOs, ms)


# 3. 随机前移工序码子序列 已测
def heuristic3(os_ms, parameters):
    (os, ms) = os_ms
    ida = idb = random.randint(0, len(os) - 2)
    while ida == idb:
        idb = random.randint(0, len(os) - 1)

    if ida > idb:
        ida, idb = idb, ida

    newOs = os[ida:idb + 1] + os[:ida] + os[idb + 1:]

    return (newOs, ms)


# 4. 对 os 简化领域搜索 已测
def heuristic4(os_ms, parameters):
    (os, ms) = os_ms
    tos = os.copy()
    # print(tos)
    idx = random.randint(0, len(tos) - 1)
    bestTime = timeTaken((tos, ms), parameters)
    # print('selected position: ', idx)
    for i in range(0, len(tos)):
        newOs = tos.copy()
        k = newOs[idx]
        newOs = newOs[0:idx] + newOs[idx + 1: len(newOs)]
        newOs = newOs[0: i] + [k] + newOs[i: len(newOs)]
        # print(newOs)
        if bestTime > timeTaken((newOs, ms), parameters):
            tos = newOs
    return (tos, ms)


# 5. 随机改变单个机器码 已测
def heuristic5(os_ms, parameters):
    (os, ms) = os_ms
    machineIdx = random.randint(0, len(ms) - 1)
    # ('selected idx : ', machineIdx)
    return (os, changeMsRandom(machineIdx, ms, parameters))


# 6. 机器码简化领域搜索 已测
def heuristic6(os_ms, parameters):
    (os, ms) = os_ms
    tms = ms.copy()
    bestTime = timeTaken((os, tms), parameters)
    for i in range(0, len(tms)):
        newMs = changeMsRandom(i, ms, parameters)
        if bestTime > timeTaken((os, newMs), parameters):
            tms = newMs

    return (os, tms)


# 7. 并行简化领域搜索
def heuristic7(os_ms, parameters):
    (os, ms) = os_ms
    tos = os.copy()
    tms = ms.copy()
    # print(tos)
    idx = random.randint(0, len(tos) - 1)

    bestTime = timeTaken((tos, ms), parameters)
    # print('selected position: ', idx)
    for i in range(0, len(tos)):
        newOs = tos.copy()
        k = newOs[idx]
        newOs = newOs[0:idx] + newOs[idx + 1: len(newOs)]
        newOs = newOs[0: i] + [k] + newOs[i: len(newOs)]
        machineIdx = getMachineIdx(i, os, parameters)
        newMs = changeMsRandom(machineIdx, ms, parameters)
        # print(newOs)
        if bestTime > timeTaken((newOs, newMs), parameters):
            tos = newOs
            tms = newMs
    return (tos, tms)


# 8. 工序码随机交换同时随机改变对应位置机器码 已测
def heuristic8(os_ms, parameters):
    jobs = parameters['jobs']
    (os, ms) = os_ms
    newOs = os.copy()
    newMs = ms.copy()

    ida = idb = random.randint(0, len(os) - 1)
    while ida == idb:
        idb = random.randint(0, len(os) - 1)

    newOs[ida], newOs[idb] = newOs[idb], newOs[ida]  # 工序码交换完成
    machineIda = getMachineIdx(ida, os, parameters)
    machineIdb = getMachineIdx(idb, os, parameters)

    newMs = changeMsRandom(machineIda, newMs, parameters)
    newMs = changeMsRandom(machineIdb, newMs, parameters)

    return (newOs, newMs)


# 9. 工序码随机反转子序列并同时随机改变对应位置机器码 已测
def heuristic9(os_ms, parameters):
    (os, ms) = os_ms
    ida = idb = random.randint(0, len(os) - 2)
    while ida == idb:
        idb = random.randint(0, len(os) - 1)

    if ida > idb:
        ida, idb = idb, ida

    # print('start: ', ida, ' end: ', idb)

    rev = os[ida:idb + 1]
    rev.reverse()
    newOs = os[:ida] + rev + os[idb + 1:]
    newMs = ms.copy()
    for i in range(ida, idb + 1):
        # print('place: ', i)
        newMs = changeMsRandom(i, newMs, parameters)

    return (newOs, newMs)


# 10. 随机前移工序码子序列, 并改变对应位置的机器码 已测
def heuristic10(os_ms, parameters):
    (os, ms) = os_ms
    ida = idb = random.randint(0, len(os) - 2)
    while ida == idb:
        idb = random.randint(0, len(os) - 1)

    if ida > idb:
        ida, idb = idb, ida

    newOs = os[ida:idb + 1] + os[:ida] + os[idb + 1:]
    newMs = ms.copy()
    for i in range(0, idb - ida + 1):
        newMs = changeMsRandom(i, newMs, parameters)

    return (newOs, newMs)


# 11. 遗传算法
def heuristic11(os_ms, parameters):
    # print('11')
    result = (os_ms[0].copy(), os_ms[1].copy())
    # Initialize the Population
    population = []  # 设置种群
    for i in range(40):
        population.append(result)

    gen = 1  # 标记代数

    # Evaluate the population
    while gen < 5:  # 迭代
        # Genetic Operators 选择,交叉,变异
        population = genetic.selection(population, parameters)
        population = genetic.crossover(population, parameters)
        population = genetic.mutation(population, parameters)
        # print("gen: " + str(gen))
        gen = gen + 1

    sortedPop = sorted(population, key=lambda cpl: genetic.timeTaken(cpl, parameters))  # 选出最优

    return (sortedPop[0][0], sortedPop[0][1])
