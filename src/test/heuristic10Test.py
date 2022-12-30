import random

from src.utils import parser, gantt
from src.LLH import lowlevelheuristic
from src.LLH import decoding
from src.LLH import encoding
# 载入册数数据
str = '/Users/wurifu/PycharmProjects/GenFJSP/test_data/Brandimarte_Data/Text/Mk01.fjs'
para = parser.parse(str)
print('test 9')
jobs = para['jobs']
os = encoding.generateOS(para)
ms = encoding.generateMS(para)
print('OS: ', os)
print('ms: ', ms)
print('time:', lowlevelheuristic.timeTaken((os, ms), para))
gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(para, os, ms))
gantt.draw_chart(gantt_data)

newOs, newMs = lowlevelheuristic.heuristic10(os, ms, para)
print('MS: ', ms)
print('MS: ', newMs)
oriTime = lowlevelheuristic.timeTaken((os, newMs), para)
print('time:', oriTime)
gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(para, os, newMs))
gantt.draw_chart(gantt_data)

lastBest = ms
historyBestTime = 10000
for i in range(0, 1000):
    newOs, newMs = lowlevelheuristic.heuristic10(os, ms, para)
    nt = lowlevelheuristic.timeTaken((newOs, newMs), para)
    lt = lowlevelheuristic.timeTaken((os, ms), para)
    if nt < lt:
        ms = newMs
        if nt < historyBestTime:
            lastBest = ms
            historyBestTime = nt
            print(i, ' new Best time:', nt)
    # else:
    #     if random.randint(0, 10) >= 5:
    #         print('random accept')
    #         ms = newMs
    print(i, ' new time:', lowlevelheuristic.timeTaken((os, ms), para))
    decoding.decode(para, newOs, newMs)

print('ori time:', oriTime)
print('Best time:', lowlevelheuristic.timeTaken((os, lastBest), para))
gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(para, os, lastBest))
gantt.draw_chart(gantt_data)