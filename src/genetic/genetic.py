# 遗传操作的实现
# The code is strictly mirroring the section 4.3 of the attached paper

import random
import itertools
from src import config
from src.genetic import decoding


def timeTaken(os_ms, pb_instance):  # 最大完成时间
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


# 选择操作
def elitistSelection(population, parameters):  # 精英选拔,选择最佳的一部分个体
    # population 中的元素是一个 OS MS 元组
    keptPopSize = int(config.pr * len(population))  # 选择的数量
    sortedPop = sorted(population, key=lambda cpl: timeTaken(cpl, parameters))
    # 使用 lambda 表达式,按照 种群中每个元素 (cpl) 的 timeTaken 排列
    return sortedPop[:keptPopSize]


def tournamentSelection(population, parameters):  # 锦标赛选拔,随机选择规模为B的个体,并选出最好的
    b = 2

    selectIndividuals = []
    for i in range(b):
        randomIndividual = random.randint(0, len(population) - 1)
        selectIndividuals.append(population[randomIndividual])

    return min(selectIndividuals, key=lambda cpl: timeTaken(cpl, parameters))


def selection(population, parameters):  # 新一代先用精英策略选择,剩下的用锦标赛策略填满
    newPop = elitistSelection(population, parameters)
    while len(newPop) < len(population):
        newPop.append(tournamentSelection(population, parameters))

    return newPop


# 交叉操作
def precedenceOperationCrossover(p1, p2, parameters):  # 优先操作交叉
    J = parameters['jobs']
    jobNumber = len(J)
    jobRange = range(1, jobNumber + 1)
    sizeJobset1 = random.randint(0, jobNumber)  # 选多少个 job

    jobset1 = random.sample(jobRange, sizeJobset1)  # 随机,返回从总体序列或集合中选择的唯一元素的 k 长度列表。 用于无重复的随机抽样。
    # 从 jobRange 中选出 sizeJobset1 个 job
    # P1中属于Jobset1的任何元素被附加到O1中的相同位置，并在P1中被删除；P2中属于Jobset1的任何元素被附加到O2中的相同位置，并在P2中被删除；
    o1 = []
    p1kept = []
    for i in range(len(p1)):
        e = p1[i]
        if e in jobset1:
            o1.append(e)
        else:
            o1.append(-1)
            p1kept.append(e)

    o2 = []
    p2kept = []
    for i in range(len(p2)):
        e = p2[i]
        if e in jobset1:
            o2.append(e)
        else:
            o2.append(-1)
            p2kept.append(e)

    # P2中的剩余元素被附加到O1序列中的剩余空位置；并且P1中的剩余元素被附加到O2序列中的剩余空位置。
    for i in range(len(o1)):
        if o1[i] == -1:
            o1[i] = p2kept.pop(0)

    for i in range(len(o2)):
        if o2[i] == -1:
            o2[i] = p1kept.pop(0)

    return (o1, o2)


def jobBasedCrossOver(p1, p2, parameters):  # 基于作业的交叉
    J = parameters['jobs']
    jobNumber = len(J)
    jobsRange = range(0, jobNumber)
    sizeJobset1 = random.randint(0, jobNumber)

    # 随机分为两组Jobset1和Jobset2
    jobset1 = random.sample(jobsRange, sizeJobset1)
    jobset2 = [item for item in jobsRange if item not in jobset1]

    o1 = []
    p1kept = []
    for i in range(len(p1)):
        e = p1[i]
        if e in jobset1:
            o1.append(e)
            p1kept.append(e)
        else:
            o1.append(-1)

    o2 = []
    p2kept = []
    for i in range(len(p2)):
        e = p2[i]
        if e in jobset2:
            o2.append(e)
            p2kept.append(e)
        else:
            o2.append(-1)

    for i in range(len(o1)):
        if o1[i] == -1:
            o1[i] = p2kept.pop(0)

    for i in range(len(o2)):
        if o2[i] == -1:
            o2[i] = p1kept.pop(0)

    return (o1, o2)

def twoPointCrossover(p1, p2):
    pos1 = random.randint(0, len(p1) - 1)
    pos2 = random.randint(0, len(p2) - 1)

    if pos1 > pos2:
        pos2, pos1 = pos1, pos2

    offspring1 = p1
    if pos1 != pos2:
        offspring1 = p1[:pos1] + p2[pos1:pos2] + p1[pos2:]

    offspring2 = p2
    if pos1 != pos2:
        offspring2 = p2[:pos1] + p1[pos1:pos2] + p2[pos2:]

    return (offspring1, offspring2)


def crossoverOS(p1, p2, parameters):
    if random.choice([True, False]):
        return precedenceOperationCrossover(p1, p2, parameters)
    else:
        return jobBasedCrossOver(p1, p2, parameters)


def crossoverMS(p1, p2):
    return twoPointCrossover(p1, p2)


def crossover(population, parameters):
    newPop = []
    i = 0
    while i < len(population):
        (OS1, MS1) = population[i]
        (OS2, MS2) = population[i + 1]

        if random.random() < config.pc:
            (oOS1, oOS2) = crossoverOS(OS1, OS2, parameters)
            (oMS1, oMS2) = crossoverMS(MS1, MS2)
            newPop.append((oOS1, oMS1))
            newPop.append((oOS2, oMS2))
        else:
            newPop.append((OS1, MS1))
            newPop.append((OS2, MS2))

        i = i + 2

    return newPop



# 变异操作

def swappingMutation(p):
    pos1 = random.randint(0, len(p) - 1)
    pos2 = random.randint(0, len(p) - 1)

    if pos1 == pos2:
        return p

    if pos1 > pos2:
        pos1, pos2 = pos2, pos1

    offspring = p[:pos1] + [p[pos2]] + p[pos1 + 1:pos2] + [p[pos1]] + p[pos2 + 1:]

    return offspring


def neighborhoodMutation(p):
    pos3 = pos2 = pos1 = random.randint(0, len(p) - 1)

    while p[pos2] == p[pos1]:
        pos2 = random.randint(0, len(p) - 1)

    while p[pos3] == p[pos2] or p[pos3] == p[pos1]:
        pos3 = random.randint(0, len(p) - 1)

    sortedPositions = sorted([pos1, pos2, pos3])
    pos1 = sortedPositions[0]
    pos2 = sortedPositions[1]
    pos3 = sortedPositions[2]

    e1 = p[sortedPositions[0]]
    e2 = p[sortedPositions[1]]
    e3 = p[sortedPositions[2]]

    permutations = list(itertools.permutations([e1, e2, e3])) # 全排列
    permutation = random.choice(permutations)

    offspring = p[:pos1] + [permutation[0]] + \
                p[pos1 + 1:pos2] + [permutation[1]] + \
                p[pos2 + 1:pos3] + [permutation[2]] + \
                p[pos3 + 1:]

    return offspring


def halfMutation(p, parameters):
    o = p
    jobs = parameters['jobs']

    size = len(p)
    r = int(size / 2)

    positions = random.sample(range(size), r)

    i = 0
    for job in jobs:
        for op in job:
            if i in positions:
                o[i] = random.randint(0, len(op) - 1)
            i = i + 1

    return o


def mutationOS(p):
    if random.choice([True, False]):
        return swappingMutation(p)
    else:
        return neighborhoodMutation(p)


def mutationMS(p, parameters):
    return halfMutation(p, parameters)


def mutation(population, parameters):
    newPop = []

    for (OS, MS) in population:
        if random.random() < config.pm:
            oOS = mutationOS(OS)
            oMS = mutationMS(MS, parameters)
            newPop.append((oOS, oMS))
        else:
            newPop.append((OS, MS))

    return newPop
