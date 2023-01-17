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
strs = 'test_data\Brandimarte_Data\Text\Mk02.fjs'
para = parser.parse(strs) # 导入数据




# Initialize the Population
population = encoding.initializePopulation(para)
sortedPop = sorted(population, key=lambda cpl: lowlevelheuristic.timeTaken(cpl, para))  # 选出最优

# Termination Criteria Satisfied ?
gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(para, sortedPop[0][0], sortedPop[0][1]))

print('ori Best time:', lowlevelheuristic.timeTaken((sortedPop[0][0], sortedPop[0][1]), para))
gantt.draw_chart(gantt_data)

gen = 1  # 标记代数

population = highLevelStrategy.populationStrategy(population, para, config.iter)


sortedPop = sorted(population, key=lambda cpl: lowlevelheuristic.timeTaken(cpl, para))  # 选出最优

# Termination Criteria Satisfied ?
gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(para, sortedPop[0][0], sortedPop[0][1]))

print('final Best time:', lowlevelheuristic.timeTaken((sortedPop[0][0], sortedPop[0][1]), para))
gantt.draw_chart(gantt_data)


