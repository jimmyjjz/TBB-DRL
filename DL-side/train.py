import tbb_env
import os
import atexit
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecFrameStack
from stable_baselines3.common.env_util import make_vec_env
from utils import get_setting

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

stride=get_setting("stride")

using_checkpoint=False
initial_timestep=0
env=None
model=None

if get_setting("use_checkpoint"):
    checkpoint=get_setting("checkpoint_to_use")
    checkpoint_path = "checkpoint/"+str(checkpoint)+".zip"
    if os.path.isfile(checkpoint_path):
        print(f"Checkpoint {checkpoint} found. Using checkpoint {checkpoint}.")
        initial_timestep = checkpoint
        env = VecFrameStack(make_vec_env(tbb_env.TBBEnv, n_envs=1), n_stack=4)
        model = PPO.load(checkpoint_path)
        model.set_env(env)
        using_checkpoint=True
    else:
        print(f"Checkpoint {checkpoint} not found.")

if not using_checkpoint:
    print("Fresh start.")
    env = VecFrameStack(make_vec_env(tbb_env.TBBEnv, n_envs=1), n_stack=4)
    model = PPO("CnnPolicy", env, verbose=1, n_steps=stride, tensorboard_log="checkpoint/tensorboard")

atexit.register(env.close)

amount_of_strides=get_setting("amount_of_strides")
for i in range(1,get_setting("amount_of_strides")+1):
    print(f"Stride {i+1}.")
    model = model.learn(total_timesteps=stride, reset_num_timesteps=False)
    model.save(f"checkpoint/{initial_timestep+(stride*i)}")
    print(f"Current model saved as checkpoint.")

