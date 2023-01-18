import torch
import net_ss as net
import time


dqn = net.DQN()
dqn.eval_net.load_state_dict(torch.load('eval_model.pth'))


for episode in range(100):
    print("<<<<<<<<<<<<<<Episode: %s" % episode)
    # 初始化环境
    s = net.myenv.reset()
    # 记录每个 episode 的步数
    episode_reward_sum = 0
    t0 = time.time()
    while True:
        net.myenv.render() # 刷新环境
        a = dqn.choose_action(s) # 选择行动
        s_, r, done, info = net.myenv.step(a) # 执行行动, 得到下一状态, 奖励, 是否终止

        # 修改奖励
        x, x_dot, theta, theta_dot = s_
        r1 = (net.myenv.x_threshold - abs(x)) / net.myenv.x_threshold - 0.8 # 奖励函数
        r2 = (net.myenv.theta_threshold_radians - abs(theta)) / net.myenv.theta_threshold_radians - 0.5 # 奖励函数
        new_r = r1 + r2

        dqn.store_transition(s, a, new_r, s_) # 存储记忆
        episode_reward_sum += new_r # 记录每个 episode 的步数

        s = s_ # 下一步,更新状态


        if done:
            print('episode%s---reward_sum: %s' % (episode, round(episode_reward_sum, 2)))
            t1 = time.time()
            total_time = t1 - t0
            print("Made it {0:.2f}s".format(total_time))
            print()
            break

# 关闭环境
