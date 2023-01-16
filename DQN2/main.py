import torch

import net
print(torch.cuda.is_available())
print(torch.__version__)
dqn = net.DQN()
# dqn.eval_net.load_state_dict(torch.load('eval_model.pth'))
# 训练 400 个 episode
for episode in range(400):
    print("<<<<<<<<<<<<<<Episode: %s" % episode)
    # 初始化环境
    s = net.env.reset()
    # 记录每个 episode 的步数
    episode_reward_sum = 0

    while True:
        net.env.render() # 刷新环境
        a = dqn.choose_action(s) # 选择行动
        s_, r, done, done1, info = net.env.step(a) # 执行行动, 得到下一状态, 奖励, 是否终止

        # 修改奖励
        x, x_dot, theta, theta_dot = s_
        r1 = (net.env.x_threshold - abs(x)) / net.env.x_threshold - 0.8 # 奖励函数
        r2 = (net.env.theta_threshold_radians - abs(theta)) / net.env.theta_threshold_radians - 0.5 # 奖励函数
        new_r = r1 + r2

        dqn.store_transition(s, a, new_r, s_) # 存储记忆
        episode_reward_sum += new_r # 记录每个 episode 的步数

        s = s_ # 下一步,更新状态

        # 如果累计的transition数量超过了记忆库的固定容量2000
        if dqn.memory_counter > net.MEMORY_CAPACITY:
            # 开始学习
            dqn.learn()
        if done:
            print('episode%s---reward_sum: %s' % (episode, round(episode_reward_sum, 2)))
            break
torch.save(dqn.eval_net.state_dict(), 'eval_model neo.pth')
torch.save(dqn.target_net.state_dict(), 'target_model neo.pth')
# 关闭环境
net.env.close()