#!/usr/bin/env python
import random
# This script contains a high level overview of the proposed hybrid algorithm
# The code is strictly mirroring the section 4.1 of the attached paper

import sys
import time

from src.LLH.lowlevelheuristic import LLHolder, LLHolder2
from src.utils import parser, gantt
from src.LLH import encoding, decoding, genetic, lowlevelheuristic
from src import config


# Beginning
# Parameters Setting
strs = '/Users/wurifu/PycharmProjects/GenFJSP/test_data/Brandimarte_Data/Text/Mk01.fjs'
para = parser.parse(strs) # 导入数据
llh = LLHolder()

t0 = time.time()

# Initialize the Population
os = encoding.generateOS(para)
ms = encoding.generateMS(para)
result = (os, ms)
oriTime = lowlevelheuristic.timeTaken(result, para)
print('time:', oriTime)

# Evaluate the population
lastBest = result
historyBestTime = oriTime
for i in range(0, 100):
    idx = random.randint(0, len(llh) - 1)
    print('heuristic ', idx + 1, ' selected, given time: ', lowlevelheuristic.timeTaken(lastBest, para))
    newResult = llh[idx](lastBest, para)
    nt = lowlevelheuristic.timeTaken(newResult, para)
    lt = lowlevelheuristic.timeTaken(result, para)
    if nt < historyBestTime:
        lastBest = newResult
        historyBestTime = nt
        print(i, ' new Best time:', nt)
    print(i, ' new time:', lowlevelheuristic.timeTaken(newResult, para))

t1 = time.time()
total_time = t1 - t0
print("Finished in {0:.2f}s".format(total_time))

# Termination Criteria Satisfied ?
gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(para, lastBest[0], lastBest[1]))

print('final Best time:', lowlevelheuristic.timeTaken(lastBest, para))

if config.latex_export:
    gantt.export_latex(gantt_data)
else:
    gantt.draw_chart(gantt_data)
