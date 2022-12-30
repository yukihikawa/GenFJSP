import random

from src.utils import parser, gantt
from src.LLH import lowlevelheuristic
from src.LLH import decoding
from src.LLH import encoding

str = '/Users/wurifu/PycharmProjects/GenFJSP/test_data/Brandimarte_Data/Text/Mk01.fjs'
para = parser.parse(str)
print(para)

os = encoding.generateOS(para)
ms = encoding.generateMS(para)
print('OS: ', os)
print('ms: ', ms)
print('time:', lowlevelheuristic.timeTaken((os, ms), para))
gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(para, os, ms))
gantt.draw_chart(gantt_data)

newOs = lowlevelheuristic.heuristic2(os)
print('OS: ', os)
print('OS: ', newOs)
oriTime = lowlevelheuristic.timeTaken((newOs, ms), para)
print('time:', oriTime)
gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(para, newOs, ms))
gantt.draw_chart(gantt_data)

lastBest = os
historyBestTime = 10000
for i in range(0, 100000):
    newos = lowlevelheuristic.heuristic3(os)
    nt = lowlevelheuristic.timeTaken((newos, ms), para)
    lt = lowlevelheuristic.timeTaken((os, ms), para)
    if nt < lt:
        os= newos
        if nt < historyBestTime:
            lastBest = os
            historyBestTime = nt
            print(i, ' new Best time:', nt)
    else:
        if random.randint(0, 10) >= 5:
            print('random accept')
            os = newos
    print(i, ' new time:', lowlevelheuristic.timeTaken((os, ms), para))
    decoding.decode(para, newOs, ms)

print('ori time:', oriTime)
print('Best time:', lowlevelheuristic.timeTaken((lastBest, ms), para))
gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(para, lastBest, ms))
gantt.draw_chart(gantt_data)