import torch

from src.HLH.HHDQN import net

dqn = net.DQN()

for epoch in range(400):
    print("<<<<<<<<<<<<<<Epoch: %s" % epoch)
    # 初始化环境
    s = net.myenv.reset()

    round = 0
    while True:
        # net.myenv.render()
        a = dqn.choose_action(s)
        s_, r, done, other, info = net.myenv.step(a)

        dqn.store_transition(s, a, r, s_)
        round += 1

        s = s_  #

        if dqn.memory_counter > net.MEMORY_CAPACITY:
            dqn.learn()

        if round % 20 == 0:
            net.myenv.render()
        if round == 100:
            break
torch.save(dqn.eval_net.state_dict(), 'eval_model.pth')
torch.save(dqn.target_net.state_dict(), 'target_model.pth')
net.myenv.render()