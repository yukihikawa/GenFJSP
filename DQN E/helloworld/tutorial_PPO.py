import os
import gym
from config import Config, get_gym_env_args
from agent import AgentPPO
from run import train_agent, render_agent
from env import PendulumEnv

gym.logger.set_level(40)  # Block warning


def train_ppo_for_pendulum(gpu_id=0):
    agent_class = AgentPPO  # DRL algorithm name
    env_class = PendulumEnv  # run a custom env: PendulumEnv, which based on OpenAI pendulum
    env_args = {
        'env_name': 'Pendulum',  # Apply torque on the free end to swing a pendulum into an upright position
        # Reward: r = -(theta + 0.1 * theta_dt + 0.001 * torque)

        'state_dim': 3,  # the x-y coordinates of the pendulum's free end and its angular velocity.
        'action_dim': 1,  # the torque applied to free end of the pendulum
        'if_discrete': False  # continuous action space, symbols → direction, value → force
    }
    get_gym_env_args(env=PendulumEnv(), if_print=True)  # return env_args

    args = Config(agent_class, env_class, env_args)  # see `config.py Arguments()` for hyperparameter explanation
    args.break_step = int(2e5)  # break training if 'total_step > break_step'
    args.net_dims = (64, 32)  # the middle layer dimension of MultiLayer Perceptron
    args.gpu_id = gpu_id  # the ID of single GPU, -1 means CPU
    args.gamma = 0.97  # discount factor of future rewards
    args.repeat_times = 16  # repeatedly update network using ReplayBuffer to keep critic's loss small

    train_agent(args)


def train_ppo_for_lunar_lander(gpu_id=0):
    agent_class = AgentPPO  # DRL algorithm name
    env_class = gym.make
    env_args = {
        'env_name': 'LunarLanderContinuous-v2',  # A lander learns to land on a landing pad
        # Reward: Lander moves to the landing pad and come rest +100; lander crashes -100.
        # Reward: Lander moves to landing pad get positive reward, move away gets negative reward.
        # Reward: Firing the main engine -0.3,  side engine -0.03 each frame.

        'state_dim': 8,  # coordinates xy, linear velocities xy, angle, angular velocity, two booleans
        'action_dim': 2,  # fire main engine or side engine.
        'if_discrete': False  # continuous action space, symbols → direction, value → force
    }
    get_gym_env_args(env=gym.make('LunarLanderContinuous-v2'), if_print=True)  # return env_args

    args = Config(agent_class, env_class, env_args)  # see `config.py Arguments()` for hyperparameter explanation
    args.break_step = int(4e5)  # break training if 'total_step > break_step'
    args.net_dims = (64, 32)  # the middle layer dimension of MultiLayer Perceptron
    args.gpu_id = gpu_id  # the ID of single GPU, -1 means CPU
    args.repeat_times = 32  # repeatedly update network using ReplayBuffer to keep critic's loss small
    args.lambda_entropy = 0.04  # the lambda of the policy entropy term in PPO

    train_agent(args)
    if input("| Press 'y' to load actor.pth and render:"):
        actor_name = sorted([s for s in os.listdir(args.cwd) if s[-4:] == '.pth'])[-1]
        actor_path = f"{args.cwd}/{actor_name}"
        render_agent(env_class, env_args, args.net_dims, agent_class, actor_path)


if __name__ == "__main__":
    GPU_ID = 0
    train_ppo_for_pendulum(GPU_ID)
    train_ppo_for_lunar_lander(GPU_ID)
