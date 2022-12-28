import random
import itertools
from src.LLH import decoding

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

### 改变指定位置的机器码 已测
def changeMs(idx, os, ms, parameters):
    jobs = parameters['jobs'] # 作业的集合
    jobIdx = os[idx] # 指定的位置所属的作业序号
    opIdx = 0 # 指定位置是所属作业的第几道工序
    for index, val in enumerate(os):
        if(index == idx):
            break
        else:
            if val == jobIdx:
                opIdx += 1
    print('belongs to: job', jobIdx + 1, ' op: ', opIdx + 1, ' ava machine: ', len(jobs[jobIdx][opIdx]))
    newMachine = random.randint(0, len(jobs[jobIdx][opIdx]) - 1)
    while ms[idx] == newMachine and len(jobs[jobIdx][opIdx]) > 1:
        newMachine = random.randint(0, len(jobs[jobIdx][opIdx]) - 1)

    newMs = ms.copy()
    print('ori: ', newMs)
    newMs[idx] = newMachine
    return newMs


# =====================启发式操作++++++++++++++++++
# 1. 随机交换两个工序码 已测
def heuristic1(os):
    ida = idb = random.randint(0, len(os) - 1)
    while ida == idb:
        idb = random.randint(0, len(os) - 1)

    newOs = os.copy()
    newOs[ida], newOs[idb] = newOs[idb], newOs[ida]
    return newOs

# 2. 随机反转工序码子序列 已测
def heuristic2(os):
    ida = idb = random.randint(0, len(os) - 2)
    while ida >= idb:
        idb = random.randint(0, len(os) - 1)

    rev = os[ida:idb + 1]
    rev.reverse()
    newOs = os[:ida] + rev + os[idb + 1:]

    return newOs

# 3. 随机前移工序码子序列 已测
def heuristic3(os):
    ida = random.randint(0, len(os) - 1)
    idb = random.randint(0, len(os) - 1)
    while ida > idb:
        idb = random.randint(0, len(os) - 1)

    newOs =os[ida:idb + 1] + os[:ida] + os[idb + 1:]

    return newOs

# 4. 对 os 简化领域搜索
def heuristic4(os):
    pass

# 5. 随机改变单个机器码 已测
def heuristic5(os, ms, parameters):
    machineIdx = random.randint(0, len(ms) - 1)
    print('selected idx : ', machineIdx)
    return changeMs(machineIdx, os, ms, parameters)

# 6. 机器码简化领域搜索
def heuristic6(ms, parameters):
    pass

# 7. 并行简化领域搜索
def heuristic7(os, ms, parameters):
    pass

# 8. 工序码随机交换同时随机改变对应位置机器码
def heuristic8(os, ms, parameters):
    jobs = parameters['jobs']
    newOs = os.copy()
    newMs = ms.copy()

    ida = idb = random.randint(0, len(os) - 1)
    while ida == idb:
        idb = random.randint(0, len(os) - 1)

    newOs[ida], newOs[idb] = newOs[idb], newOs[ida] # 工序码交换完成

    jobIda = os[ida]
    jobIdb = os[idb]

    newMachineA = random.randint(0, len(jobs[jobIda]) - 1)
    while ms[ida] == newMachineA:
        newMachineA = random.randint(0, len(jobs[jobIda]) - 1)

    newMachineB = random.randint(0, len(jobs[jobIdb]) - 1)
    while ms[idb] == newMachineB:
        newMachineB = random.randint(0, len(jobs[jobIdb]) - 1)

    newMs[ida], newMs[idb] = newMachineA, newMachineB

    return (newOs, newMs)