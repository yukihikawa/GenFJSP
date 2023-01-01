from src.utils import parser, gantt
from src.LLH import lowlevelheuristic
from src.LLH import decoding
from src.LLH import encoding
from src.LLH.lowlevelheuristic import LLHolder
llh = LLHolder()
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
historyBestTime = lowlevelheuristic.timeTaken(lastBest, para)
print(llh[10])
for i in range(0, 20):
    print('===================')
    # print(i, ' history Best Time:', lowlevelheuristic.timeTaken(lastBest, para))
    newResult = llh[10](lastBest, para)
    # print(i, ' history Best Time:', lowlevelheuristic.timeTaken(lastBest, para))
    nt = lowlevelheuristic.timeTaken(newResult, para)
    # print(i, ' history Best Time:', lowlevelheuristic.timeTaken(lastBest, para))
    if nt < historyBestTime:
        lastBest = newResult
        historyBestTime = nt
        print(i, ' new Best time:', nt)
    print(i, ' new time:', lowlevelheuristic.timeTaken(newResult, para))
    # print(i, ' history Best Time:', lowlevelheuristic.timeTaken(lastBest, para))
    print(i, ' history Best Time:', lowlevelheuristic.timeTaken(lastBest, para))
    # decoding.decode(para, newResult[0], newResult[1])

print('ori time:', oriTime)
print('final Best time:', lowlevelheuristic.timeTaken(lastBest, para))
print('final Best time 2:', lowlevelheuristic.timeTaken(lastBest, para))
gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(para, lastBest[0], lastBest[1]))
gantt.draw_chart(gantt_data)