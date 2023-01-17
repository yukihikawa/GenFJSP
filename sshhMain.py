#!/usr/bin/env python
import random
# This script contains a high level overview of the proposed hybrid algorithm
# The code is strictly mirroring the section 4.1 of the attached paper

import sys
import time

from src.HLH import sshh
from src.utils import parser, gantt
from src.LLH import encoding, decoding, lowlevelheuristic
from src import config


# Beginning
# Parameters Setting
strs = 'test_data/Brandimarte_Data/Text/Mk09.fjs'
para = parser.parse(strs) # 导入数据
ss = sshh.SequenceSelection()



# Initialize the Population
ss.best_solution = solution = (encoding.generateOS(para), encoding.generateMS(para))

ss.prevTime = oriTime = lowlevelheuristic.timeTaken(ss.best_solution, para)
print('Ori time:', oriTime)

for epoch in range(0, 5000):
    print('epoch:', epoch)
    solution = ss.update_solution(solution, para)
    time = lowlevelheuristic.timeTaken(solution, para)
    print('time:', time)


# Termination Criteria Satisfied ?
gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(para, ss.best_solution[0], ss.best_solution[1]))
print('time:', oriTime)
print('final Best time:', lowlevelheuristic.timeTaken(ss.best_solution, para))
print(ss.transition_matrix)

if config.latex_export:
    gantt.export_latex(gantt_data)
else:
    gantt.draw_chart(gantt_data)


