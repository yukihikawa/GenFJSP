#!/usr/bin/env python
import random
# This script contains a high level overview of the proposed hybrid algorithm
# The code is strictly mirroring the section 4.1 of the attached paper

import sys
import time

from src.HLH import highLevelStrategy
from src.utils import parser, gantt
from src.LLH import encoding, decoding, lowlevelheuristic
from src import config


# Beginning
# Parameters Setting
strs = '/Users/wurifu/PycharmProjects/GenFJSP/test_data/Brandimarte_Data/Text/Mk02.fjs'
para = parser.parse(strs) # 导入数据




# Initialize the Population
os = encoding.generateOS(para)
ms = encoding.generateMS(para)
result = (os, ms)
oriTime = lowlevelheuristic.timeTaken(result, para)
print('time:', oriTime)


# lastBest = highLevelStrategy.randomStrategy(result, para, config.iter)
lastBest = highLevelStrategy.greedyStrategy(result, para, config.iter)
# lastBest = highLevelStrategy.saStrategy(result, para, config.iter)

# Termination Criteria Satisfied ?
gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(para, lastBest[0], lastBest[1]))
print('time:', oriTime)
print('final Best time:', lowlevelheuristic.timeTaken(lastBest, para))

if config.latex_export:
    gantt.export_latex(gantt_data)
else:
    gantt.draw_chart(gantt_data)


