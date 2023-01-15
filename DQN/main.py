import time

from DQN.maze_env import Maze as env
from DQN.RL_brain import DQN as RL

def run_maze():
    print("<run_maze>") # 
    step = 0
    max_episode = 500
    for episode in range(max_episode):
        state = env.reset()
        step_every_episode = 0
        epsilon = episode / max_episode
        while True:
            if episode < 10:
                time.sleep(0.1)
            if episode > 480:
                time.sleep(0.5)
            env.render() # 刷新环境
            action = RL.choose_action(state, epsilon) # 选择行动
            #
            next_state, reward, terminal = env.step(action) # 执行行动, 得到下一状态, 奖励, 是否终止
            RL.store_transition(state, action, reward, next_state) # 存储记忆
            # 控制学习起始时间(先积累记忆)和学习频率
            if (step > 200) and (step % 5 == 0):
                RL.learn()
            state = next_state # 下一步
            if terminal:
                print("episode: %d, step: %d" % (episode, step_every_episode))
                break
            step += 1
            step_every_episode += 1

    # 游戏环境结束
    print("game over")
    env.destroy()

if __name__ == "__main__":
    print("<main>")
    env = env()
    RL = RL(env.n_actions, env.n_states) # 算法模型
    run_maze()
    env.mainloop()
    RL.plot_cost()     # 误差曲线