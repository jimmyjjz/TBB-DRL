import atexit
import tbb_env
import os
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecFrameStack
from stable_baselines3.common.env_util import make_vec_env
from utils import get_setting, print_all_settings

def run():
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    env = VecFrameStack(make_vec_env(tbb_env.TBBEnv, n_envs=1), n_stack=4)
    atexit.register(env.close)
    obs = env.reset()
    checkpoint=get_setting("checkpoint_to_use")

    try:
        model = PPO.load("checkpoint/"+str(checkpoint)+".zip")
    except FileNotFoundError:
        raise Exception(f"Checkpoint {checkpoint} not found.")

    print("Using the following settings.")
    print_all_settings()
    print(f"Using checkpoint {checkpoint}.")

    while True:
        action, _states = model.predict(obs, deterministic=False)
        obs, reward, dones, info = env.step(action)

if __name__ == "__main__":
    run()