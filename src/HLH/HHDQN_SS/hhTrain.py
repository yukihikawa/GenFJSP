import torch
import config
from src.HLH.HHDQN_SS import net_ss

dqn = net_ss.DQN()
print(torch.cuda.is_available())
dqn.eval_net.load_state_dict(torch.load('eval_model 01.pth'))
for epoch in range(config.EPOCH_TRAIN):
    print("<<<<<<<<<<<<<<Epoch: %s" % epoch)
    # 初始化环境
    s = net_ss.myenv.reset()
    count = [0 for i in range(10)]
    round = 0
    while True:
        # print("Round: %s" % round)
        # net.myenv.render()
        a = dqn.choose_action(s)
        # print('a: ', a)
        count[a] += 1
        s_, r, done, info = net_ss.myenv.step(a)

        dqn.store_transition(s, a, r, s_)
        round += 1

        s = s_  #

        if dqn.memory_counter > net_ss.MEMORY_CAPACITY:
            dqn.learn()
            if(round % (config.INNER_ITER / 10) == 0):
                print('loss = ', dqn.p_loss)



        if round == config.INNER_ITER:
            net_ss.myenv.render()
            print(count)
            break
    if epoch % 100 == 0:
        torch.save(dqn.eval_net.state_dict(), 'eval_model 02' + str(epoch) +'.pth')
torch.save(dqn.eval_net.state_dict(), 'eval_model 02.pth')
torch.save(dqn.target_net.state_dict(), 'target_model 02.pth')
net_ss.myenv.render()