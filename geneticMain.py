#!/usr/bin/env python

# This script contains a high level overview of the proposed hybrid algorithm
# The code is strictly mirroring the section 4.1 of the attached paper

import sys
import time

from src.utils import parser, gantt
from src.genetic import encoding, decoding, genetic, termination
from src import config

# Beginning
ss = 'test_data/Brandimarte_Data/Text/Mk06.fjs'
# Parameters Setting
parameters = parser.parse(ss)  # 导入数据

t0 = time.time()

# Initialize the Population
population = encoding.initializePopulation(parameters)  # 设置种群
gen = 1  # 标记代数

# Evaluate the population
while not termination.shouldTerminate(population, gen):  # 迭代
    # Genetic Operators 选择,交叉,变异
    population = genetic.selection(population, parameters)
    population = genetic.crossover(population, parameters)
    population = genetic.mutation(population, parameters)
    print("gen: " + str(gen))
    gen = gen + 1

sortedPop = sorted(population, key=lambda cpl: genetic.timeTaken(cpl, parameters))  # 选出最优

t1 = time.time()
total_time = t1 - t0
print("Finished in {0:.2f}s".format(total_time))

# Termination Criteria Satisfied ?
gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(parameters, sortedPop[0][0], sortedPop[0][1]))

print(genetic.timeTaken((sortedPop[0][0], sortedPop[0][1]), parameters))

if config.latex_export:
    gantt.export_latex(gantt_data)
else:
    gantt.draw_chart(gantt_data)
