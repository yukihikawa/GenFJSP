import random

from src.utils import parser, gantt
from src.LLH import lowlevelheuristic
from src.LLH import decoding
from src.LLH import encoding

str = '/Users/wurifu/PycharmProjects/GenFJSP/test_data/Brandimarte_Data/Text/Mk01.fjs'
para = parser.parse(str)

print('test1')
os = encoding.generateOS(para)
ms = encoding.generateMS(para)
result = (os, ms)
print('OS: ', os)
print('ms: ', ms)
oriTime = lowlevelheuristic.timeTaken(result, para)
print('time:', oriTime)
gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(para, os, ms))
gantt.draw_chart(gantt_data)

lastBest = result
historyBestTime = 10000
for i in range(0, 100):
    newResult = lowlevelheuristic.heuristic8(lastBest, para)
    nt = lowlevelheuristic.timeTaken(newResult, para)
    lt = lowlevelheuristic.timeTaken(result, para)
    if nt < historyBestTime:
        lastBest = newResult
        historyBestTime = nt
        print(i, ' new Best time:', nt)
    print(i, ' new time:', lowlevelheuristic.timeTaken(newResult, para))
    decoding.decode(para, newResult[0], newResult[1])

print('ori time:', oriTime)
print('final Best time:', lowlevelheuristic.timeTaken(lastBest, para))
gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(para, lastBest[0], lastBest[1]))
gantt.draw_chart(gantt_data)