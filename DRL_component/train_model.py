import pydirectinput
import tbb_env
import os
import atexit
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecFrameStack
from stable_baselines3.common.env_util import make_vec_env
from utils import get_setting, print_all_settings

HEIGHT = get_setting("monitor_height")
WIDTH = get_setting("monitor_width")

def train():
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    timesteps_per_checkpoint=get_setting("timesteps_per_checkpoint")

    using_checkpoint=False
    initial_timestep=0
    env=None
    model=None

    print("Using the following settings.")
    print_all_settings()

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
        model = PPO("CnnPolicy",
                    env,
                    ent_coef=get_setting("entropy_coef"),
                    vf_coef=get_setting("value_function_coef"),
                    learning_rate=get_setting("model_learning_rate"),
                    verbose=1,
                    n_steps=get_setting("n_steps"),
                    n_epochs=get_setting("n_epochs"),
                    gamma=get_setting("gamma"),
                    gae_lambda=get_setting("gae_lambda"),
                    clip_range=get_setting("clip_range"),
                    max_grad_norm=get_setting("max_grad_norm"),
                    use_sde=get_setting("use_sde"),
                    tensorboard_log="checkpoint/tensorboard")

    atexit.register(env.close)

    for i in range(1,get_setting("checkpoints_to_go_through")+1):
        print(f"Next checkpoint: {i}.")
        env.reset()
        model.learn(total_timesteps=timesteps_per_checkpoint, reset_num_timesteps=False)
        model.save(f"checkpoint/{initial_timestep+(timesteps_per_checkpoint * i)}")
        print(f"Current model saved as checkpoint {initial_timestep+(timesteps_per_checkpoint * i)}.")

if __name__ == "__main__":
    train()
