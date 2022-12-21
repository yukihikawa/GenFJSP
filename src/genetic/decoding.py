# 解码

import sys


def split_ms(pb_instance, ms):
    jobs = []
    current = 0

    for index, job in enumerate(pb_instance['jobs']): # 遍历工序(和序号
        jobs.append(ms[current:current + len(job)]) # 切片
        current += len(job)

    return jobs


def get_processing_time(ob_by_machine, machine_nb):  # 根据序号获取在某个机器的加工时间
    for op in ob_by_machine:
        if op['machine'] == machine_nb:
            return op['processingTime']
    print("[ERROR] Machine {} doesn't to be able to process this task.".format(machine_nb))
    sys.exit(-1)


def is_free(tab, start, duration):  # 查找 tab 列表是否可用(时间区间
    for k in range(start, start + duration):
        if not tab[k]:
            return False
    return True


def find_first_available_place(start_ctr, duration, machine_jobs):  # 查找第一个可用位置
    max_duration_list = []
    max_duration = start_ctr + duration

    # max_duration is either the start_ctr + duration or the max(possible starts) + duration
    # max_duration是start_ctr+持续时间或最大（可能开始）+持续时间
    if machine_jobs:  # 非空
        for job in machine_jobs:
            max_duration_list.append(job[3] + job[1])

        max_duration = max(max(max_duration_list), start_ctr) + duration

    machine_used = [True] * max_duration  # 构建包含 max_duration 个 True 的列表

    # 更新数组
    for job in machine_jobs:
        start = job[3]
        len = job[1]
        for k in range(start, start + len):
            machine_used[k] = False

    # 找第一个符合约束的空位
    for k in range(start_ctr, len(machine_used)):
        if is_free(machine_used, k, duration):
            return k;


def decode(pb_instance, os, ms):
    o = pb_instance['jobs'] # 取出操作列表
    machine_operations = [[] for i in range(pb_instance['machineNb'])] # 生成一个包含所有机器序号的列表

    ms_s = split_ms(pb_instance, ms) # 每个操作的机器

    indexes = [0] * len(ms_s)
    start_task_cstr = [0] * len(ms_s)

    # 迭代 OS 获取任务执行顺序
    # MS 获取机器码
    for job in os:
        index_machine = ms_s[job][indexes[job]]
        machine = o[job][indexes[job]][index_machine]['machine']
        prcTime = o[job][indexes[job]][index_machine]['processingTime']



def translate_decoded_to_gantt(machine_operations):
    pass
