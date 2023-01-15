import gym

import numpy as np
from env import hh_env
myenv = gym.make('hh_env-v0', new_step_api = True)
print(myenv.action_space.n)



# 默认为浮点数
x = np.zeros(1)
print(x)
