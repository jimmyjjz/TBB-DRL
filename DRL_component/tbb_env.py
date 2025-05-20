import math
import gymnasium as gym
from gymnasium import spaces
import pydirectinput
import numpy as np
import dxcam

from utils import resize_img, get_setting

HEIGHT = get_setting("monitor_height")
WIDTH = get_setting("monitor_width")
RESCALE_FACTOR = 8

class TBBEnv(gym.Env):
    def __init__(self):
        super().__init__()
        #left, right, jump, attack, hook, heal, mouse x, mouse y
        self.action_space=gym.spaces.Box(low=-1, high=1, shape=(8,), dtype=np.float32)
        self.observation_space = spaces.Box(0, 255, shape=(HEIGHT // RESCALE_FACTOR, WIDTH // RESCALE_FACTOR, 3), dtype=np.uint8)
        self.total_steps = 0
        self.episode_steps = 0
        self.pre_reward_denoter = 0
        self.screen_grabber = dxcam.create(device_idx=get_setting("dxcam_device_idx"), output_idx=get_setting("dxcam_output_idx"))
        self.pre_screen = np.zeros((HEIGHT // RESCALE_FACTOR, WIDTH // RESCALE_FACTOR, 3), dtype=np.uint8)

    def reset(self, seed=None, options=None):
        print(f"Episode steps {self.episode_steps}. Total steps {self.total_steps}.")
        pydirectinput.press('r')  # r is ingame input that resets the state
        pydirectinput.press('1')  # select weapon
        pydirectinput.press('b') # use buff potions
        pydirectinput.moveTo(WIDTH//2, HEIGHT//2) # mouse to middle of screen
        #input keys up
        pydirectinput.keyUp('a')
        pydirectinput.keyUp('d')
        pydirectinput.keyUp(' ')
        pydirectinput.mouseUp()
        pydirectinput.keyUp('e')
        pydirectinput.keyUp('h')

        screen = self.screen_grabber.grab()
        if screen is None:
            print("Screen idle at reset.")
            obs = self.pre_screen
        else:
            obs = resize_img(screen, WIDTH // RESCALE_FACTOR, HEIGHT // RESCALE_FACTOR)
            self.pre_screen = obs

        self.episode_steps = 0
        return obs, {}

    def step(self, action):
        cur_x, cur_y = pydirectinput.position()
        #print(action)
        if not(get_setting("stop_input_when_cursor_off_main_screen") and (cur_x<0 or cur_x>WIDTH or cur_y<0 or cur_y>HEIGHT)):
            pydirectinput.keyDown('a') if round(action[0],0)!=0.0 else pydirectinput.keyUp('a')
            pydirectinput.keyDown('d') if round(action[1],0)!=0.0 else pydirectinput.keyUp('d')
            pydirectinput.keyDown(' ') if round(action[2],0)!=0.0 else pydirectinput.keyUp(' ')
            pydirectinput.mouseDown() if round(action[3],0)!=0.0 else pydirectinput.mouseUp()
            pydirectinput.keyDown('e') if round(action[4],0)!=0.0 else pydirectinput.keyUp('e')
            pydirectinput.keyDown('h') if round(action[5],0)!=0.0 else pydirectinput.keyUp('h')
            pydirectinput.moveTo(int(round((action[6]+1)*(WIDTH//2), 0)), int(round((action[7]+1)*(HEIGHT//2), 0)))
        else:
            print("Mouse is offscreen.")
        screen = self.screen_grabber.grab()
        if screen is None:
            print(f"Screen idle at episode step {self.episode_steps}, total step {self.total_steps}.")
            obs = self.pre_screen
        else:
            obs = resize_img(screen, WIDTH // RESCALE_FACTOR, HEIGHT // RESCALE_FACTOR)
            self.pre_screen = obs

        finished = False
        with open("reward_denoter.txt", "r") as f:
            cur_reward_denoter = f.read()
        if len(cur_reward_denoter) >= 9 and cur_reward_denoter[1:9] == 'Inactive':
            finished = True
            if cur_reward_denoter[10:] == ' Player died.':
                reward = get_setting("lose_reward")
            elif cur_reward_denoter[10:] == ' Boss defeated.':
                reward = get_setting("win_reward")
            else:
                reward = 0
            reward += (self.pre_reward_denoter if get_setting("account_previous_reward_at_final_state") else 0)
        else:
            try:
                reward = int(cur_reward_denoter[1:]) - self.pre_reward_denoter
                self.pre_reward_denoter = int(cur_reward_denoter[1:])
            except Exception as e:
                print("Tried to add inactive reward denoter. If this occurs very rarely ignore this.")
                reward=0
        try:
            if get_setting("punish_run_away") and cur_reward_denoter[0]=="P":
                reward+=get_setting("run_away_punishment")
        except IndexError as e:
            print("Tried to access idx 0 of empty reward_denoter. If this occurs very rarely ignore this.")

        self.total_steps += 1
        self.episode_steps += 1
        return obs, reward, finished, False, {}