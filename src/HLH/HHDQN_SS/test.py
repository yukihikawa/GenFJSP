import torch
from src.HLH.HHDQN_SS import net_ss
import time

dqn = net_ss.DQN()
dqn.eval_net.load_state_dict(torch.load('eval_model.pth'))

print(torch.cuda.is_available())

s = net_ss.myenv.reset()

round = 0
while True:
    # print("Round: %s" % round)
    # net.myenv.render()
    a = dqn.choose_action(s)
    # print('a: ', a)
    s_, r, done, info = net_ss.myenv.step(a)

    round += 1

    s = s_  #



    if round == 5000:
        net_ss.myenv.render()
        break

net_ss.myenv.render()
