from src.LLH import lowlevelheuristic
from src.genetic import encoding
from src.utils import parser

list = [1, 2, 3, 4, 5, 6, 7, 8]
print('1')
print(lowlevelheuristic.heuristic1(list))
print('ori ',list)
list = [1, 2, 3, 4, 5, 6, 7, 8]
print('2')
print(lowlevelheuristic.heuristic2(list))
print(list)
list = [1, 2, 3, 4, 5, 6, 7, 8]
print('3')
print(lowlevelheuristic.heuristic3(list))
print(list)

print("=== OS & MS generation ===")
op11 = [{'machine': 0, 'processingTime': 1}, {'machine': 1, 'processingTime': 2}]
op12 = [{'machine': 1, 'processingTime': 1}, {'machine': 2, 'processingTime': 2}]
job1 = [op11, op12]
op21 = [{'machine': 2, 'processingTime': 1}, {'machine': 3, 'processingTime': 2}, {'machine': 4, 'processingTime': 2}, {'machine': 5, 'processingTime': 2}]
op22 = [{'machine': 3, 'processingTime': 1}, {'machine': 4, 'processingTime': 2}, {'machine': 2, 'processingTime': 2}]
job2 = [op21, op22]
op31 = [{'machine': 4, 'processingTime': 1}, {'machine': 5, 'processingTime': 2}]
op32 = [{'machine': 5, 'processingTime': 1}, {'machine': 0, 'processingTime': 2}, {'machine': 4, 'processingTime': 2}]
job3 = [op31, op32]
jobs = [job1, job2, job3]
para = {'machinesNb' : 6, 'jobs': jobs}
str = '/Users/wurifu/PycharmProjects/GenFJSP/test_data/Brandimarte_Data/Text/Mk01.fjs'
para0 = parser.parse(str)
print(para)

os = encoding.generateOS(para)
ms = encoding.generateMS(para)
print('OS: ', os)
print('ms: ', ms)
print("=== 7 ===")
print('new: ', lowlevelheuristic.heuristic5(os, ms, para))

print("=== 8 ===")
print((os, ms))
print(lowlevelheuristic.heuristic8(os, ms, para))