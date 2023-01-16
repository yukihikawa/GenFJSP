import torch

from src.HLH.HHDQN import net

dqn = net.DQN()
print(torch.cuda.is_available())
for epoch in range(400):
    print("<<<<<<<<<<<<<<Epoch: %s" % epoch)
    # 初始化环境
    s = net.myenv.reset()

    round = 0
    while True:
        # print("Round: %s" % round)
        # net.myenv.render()
        a = dqn.choose_action(s)
        s_, r, done, info = net.myenv.step(a)

        dqn.store_transition(s, a, r, s_)
        round += 1

        s = s_  #

        if dqn.memory_counter > net.MEMORY_CAPACITY:
            dqn.learn()
            if(round % 100 == 0):
                print('loss = ', dqn.p_loss)



        if round == 1000:
            net.myenv.render()
            break
torch.save(dqn.eval_net.state_dict(), 'eval_model.pth')
torch.save(dqn.target_net.state_dict(), 'target_model.pth')
net.myenv.render()