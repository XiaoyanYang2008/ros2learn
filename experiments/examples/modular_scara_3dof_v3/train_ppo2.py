import gym
import gym_gazebo
import tensorflow as tf
import argparse
import copy
import sys
import numpy as np

from baselines import bench, logger

from baselines.common import set_global_seeds
from baselines.common.vec_env.vec_normalize import VecNormalize
from baselines.ppo2 import ppo2
from baselines.ppo2.policies import MlpPolicy
import tensorflow as tf
from baselines.common.vec_env.dummy_vec_env import DummyVecEnv
import multiprocessing

import os

#parser
# parser = argparse.ArgumentParser()
# parser.add_argument('--slowness', dest='slowness', type=int, default=1)
# parser.add_argument('--slowness_unit', dest='slowness_unit', type=str, default='sec')
# args = parser.parse_args()

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--slowness', help='time for executing trajectory', type=int, default=1)
parser.add_argument('--slowness-unit', help='slowness unit',type=str, default='sec')
# parser.add_argument('--num-timesteps', type=int, default=int(1e6))
args = parser.parse_args()


ncpu = multiprocessing.cpu_count()
if sys.platform == 'darwin': ncpu //= 2

print("ncpu: ", ncpu)
# ncpu = 1
config = tf.ConfigProto(allow_soft_placement=True,
                        intra_op_parallelism_threads=ncpu,
                        inter_op_parallelism_threads=ncpu,
                        log_device_placement=False)
config.gpu_options.allow_growth = True #pylint: disable=E1101

tf.Session(config=config).__enter__()
def make_env():
    env = gym.make('GazeboModularScara3DOF-v3')
    env.init_time(slowness= args.slowness, slowness_unit=args.slowness_unit)
    print("slowness unit is: ",args.slowness_unit)
    logdir = '/tmp/rosrl/' + str(env.__class__.__name__) +'/ppo2/' + str(args.slowness) + '_' + str(args.slowness_unit) + '/'
    logger.configure(os.path.abspath(logdir))
    print("logger.get_dir(): ", logger.get_dir() and os.path.join(logger.get_dir()))
    env = bench.MonitorRobotics(env, logger.get_dir() and os.path.join(logger.get_dir()), allow_early_resets=True)
    env.render()
    return env

env = DummyVecEnv([make_env])
env = VecNormalize(env)

initial_observation = env.reset()
print("Initial observation: ", initial_observation)
# env.render()
seed = 0
set_global_seeds(seed)
policy = MlpPolicy
ppo2.learn(policy=policy, env=env, nsteps=2048, nminibatches=32,
    lam=0.95, gamma=0.99, noptepochs=10, log_interval=1,
    ent_coef=0.0,
    lr=3e-4,
    cliprange=0.2,
    total_timesteps=1e6, save_interval=10, outdir=logger.get_dir())