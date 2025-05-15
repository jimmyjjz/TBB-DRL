import gymnasium as gym
from gymnasium import spaces
import pyautogui
import numpy as np
import dxcam
from utils import resize_img, get_setting

HEIGHT=1080
WIDTH=1920
RESCALE_FACTOR=8

class TBBEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.action_space = spaces.Tuple((
            gym.spaces.MultiBinary(5),# left, right, jump/fly, attack, hook
            gym.spaces.Box(low=0, high=WIDTH, shape=(1,), dtype=np.float32), # horizontal mouse placement
            gym.spaces.Box(low=0, high=HEIGHT, shape=(1,), dtype=np.float32) # vertical mouse placement
        ))
        self.observation_space = spaces.Box(0,255,shape=(HEIGHT//RESCALE_FACTOR, WIDTH//RESCALE_FACTOR, 3), dtype=np.uint8)
        self.total_step=0
        self.episode_steps=0
        self.pre_reward_accumulant=0
        self.screen_grabber = dxcam.create(output_idx=1)
        pyautogui.press('r') # r is ingame input that resets the state
        pyautogui.press('1') # select weaponr1

    def reset(self, seed=None, options=None):
        pyautogui.press('r') # r is ingame input that resets the state
        pyautogui.press('1') # select weapon
        try:
            screen = self.screen_grabber.grab()
        except:
            raise Exception('Screen cannot be grabbed at reset operation')
        obs = resize_img(screen, WIDTH // RESCALE_FACTOR, HEIGHT // RESCALE_FACTOR)
        self.episode_steps=0
        return obs, {}

    def step(self, action):
        pyautogui.keyDown('a') if action[0][0] else pyautogui.keyUp('a')
        pyautogui.keyDown('d') if action[0][1] else pyautogui.keyUp('d')
        pyautogui.keyDown(' ') if action[0][2] else pyautogui.keyUp(' ')
        if action[0][3]:
            pyautogui.leftClick()
        if action[0][4]:
            pyautogui.press('e')
        pyautogui.moveTo(action[1], action[2])

        try:
            screen = self.screen_grabber.grab()
            obs = resize_img(screen, WIDTH // RESCALE_FACTOR, HEIGHT // RESCALE_FACTOR)
        except Exception as e:
            print(f'Screen cannot be grabbed at step {self.total_step}. {e}')
            obs = np.zeros((HEIGHT//RESCALE_FACTOR, WIDTH//RESCALE_FACTOR, 3), dtype=np.uint8)
            #raise Exception(f'Screen cannot be grabbed at step {self.total_step}. {e}')

        finished=False
        with open("reward_accumulant.txt","r") as f:
            cur_reward_accumulant = f.read()
        if len(cur_reward_accumulant)>=8 and cur_reward_accumulant[:8]=='Inactive':
            finished = True
            if cur_reward_accumulant[8:]==' Player died.':
                reward=get_setting("lose_reward")
            elif cur_reward_accumulant[8:]==' Boss defeated.':
                reward = get_setting("win_reward")
            else:
                reward=0
            reward+=(self.pre_reward_accumulant if get_setting("account_previous_reward_at_final_state") else 0)
        else:
            reward=int(cur_reward_accumulant)-self.pre_reward_accumulant
            self.pre_reward_accumulant=int(cur_reward_accumulant)
        return obs, reward, finished, {}