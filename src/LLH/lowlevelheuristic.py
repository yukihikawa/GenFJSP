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

### 改变指定机器码序列位置的机器码 已测
def changeMsRandom(machineIdx, ms, parameters):
    jobs = parameters['jobs'] # 作业的集合
    # jobIdx = os[machineIdx] # 指定的位置所属的作业序号 错误在此
    mcLength = 0 # 工具人
    jobIdx = -1 # 所属工作号

    for job in jobs:
        jobIdx += 1

        if mcLength + len(job) >= machineIdx + 1:
            break
        else:
            mcLength += len(job)

    opIdx = machineIdx - mcLength# 指定位置对应的 在工件中的工序号

    # print('belongs to: job', jobIdx, ' op: ', opIdx, ' ava machine: ', len(jobs[jobIdx][opIdx]))
    newMachine = random.randint(0, len(jobs[jobIdx][opIdx]) - 1)
    newMs = ms.copy()
    newMs[machineIdx] = newMachine
    return newMs

# 获取指定 os 位置工序在 ms 中的位置
def getMachineIdx(jobIdx, os, parameters):
    jobNum = os[jobIdx] # 工件号
    jobs = parameters['jobs'] # 工件集合
    machineIdx = 0 # 在 ms 中的位置
    for i in range(0, jobNum): #
        machineIdx += len(jobs[i])
    for i in range(0, jobIdx):
        if os[i] == jobNum:
            machineIdx += 1
    return machineIdx


# =====================启发式操作++++++++++++++++++
# 1. 随机交换两个工序码, 返回新的工序码 已测
def heuristic1(os):
    # 随机选择两个不同机器码
    ida = idb = random.randint(0, len(os) - 1)
    while ida == idb:
        idb = random.randint(0, len(os) - 1)

    newOs = os.copy()
    newOs[ida], newOs[idb] = newOs[idb], newOs[ida]
    return newOs

# 2. 随机反转工序码子序列 已测
def heuristic2(os):
    ida = idb = random.randint(0, len(os) - 2)
    while ida == idb:
        idb = random.randint(0, len(os) - 1)

    if ida > idb:
        ida, idb = idb, ida

    rev = os[ida:idb + 1]
    rev.reverse()
    newOs = os[:ida] + rev + os[idb + 1:]

    return newOs

# 3. 随机前移工序码子序列 已测
def heuristic3(os):
    ida = idb = random.randint(0, len(os) - 2)
    while ida == idb:
        idb = random.randint(0, len(os) - 1)

    if ida > idb:
        ida, idb = idb, ida

    newOs =os[ida:idb + 1] + os[:ida] + os[idb + 1:]

    return newOs

# 4. 对 os 简化领域搜索
def heuristic4(os):
    pass

# 5. 随机改变单个机器码 已测
def heuristic5(ms, parameters):
    machineIdx = random.randint(0, len(ms) - 1)
    print('selected idx : ', machineIdx)
    return changeMsRandom(machineIdx, ms, parameters)

# 6. 机器码简化领域搜索
def heuristic6(ms, parameters):
    pass

# 7. 并行简化领域搜索
def heuristic7(os, ms, parameters):
    pass

# 8. 工序码随机交换同时随机改变对应位置机器码 已测
def heuristic8(os, ms, parameters):
    jobs = parameters['jobs']
    newOs = os.copy()
    newMs = ms.copy()

    ida = idb = random.randint(0, len(os) - 1)
    while ida == idb:
        idb = random.randint(0, len(os) - 1)

    newOs[ida], newOs[idb] = newOs[idb], newOs[ida] # 工序码交换完成
    machineIda = getMachineIdx(ida, os, parameters)
    machineIdb = getMachineIdx(idb, os, parameters)

    newMs = changeMsRandom(machineIda, newMs, parameters)
    newMs = changeMsRandom(machineIdb, newMs, parameters)

    return (newOs, newMs)

# 9. 工序码随机反转子序列并同时随机改变对应位置机器码 已测
def heuristic9(os, ms, parameters):
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

    return newOs, newMs

# 10. 随机前移工序码子序列, 并改变对应位置的机器码 已测
def heuristic10(os, ms, parameters):
    ida = idb = random.randint(0, len(os) - 2)
    while ida == idb:
        idb = random.randint(0, len(os) - 1)

    if ida > idb:
        ida, idb = idb, ida

    newOs =os[ida:idb + 1] + os[:ida] + os[idb + 1:]
    newMs = ms.copy()
    for i in range(0, idb - ida + 1):
        newMs = changeMsRandom(i, newMs, parameters)

    return newOs, newMs