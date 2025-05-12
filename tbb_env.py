import gymnasium as gym
from gymnasium import spaces
import pyautogui
import numpy as np
import dxcam
import easyocr
from utils import resize_img

HEIGHT=1080
WIDTH=1920
RESCALE_FACTOR=8
#.//resize_img(WIDTH//RESCALE_FACTOR, HEIGHT//RESCALE_FACTOR)

class TBBEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.action_space = gym.spaces.Tuple((
            gym.spaces.Discrete(3), # left, right, jump
            gym.spaces.Box(low=0, high=WIDTH, shape=(1,), dtype=int), # horizontal mouse placement
            gym.spaces.Box(low=0, high=HEIGHT, shape=(1,), dtype=int) # vertical mouse placement
        ))
        self.observation_space = spaces.Box(0,255,shape=(HEIGHT//RESCALE_FACTOR, WIDTH//RESCALE_FACTOR, 3), dtype=np.uint8)
        self.step=0
        self.episode_steps=0
        self.screen_grabber = dxcam.create(output_idx=0)
        self.text_reader = easyocr.Reader(['en'])

    def reset(self, seed=None, options=None):
        pyautogui.press('r')#.//<insert ingame input that resets environment>
        obs = resize_img(self.screen_grabber.grab(), WIDTH // RESCALE_FACTOR, HEIGHT // RESCALE_FACTOR)
        self.episode_steps=0
        return obs, {}

    def step(self, action):
        pass

    def render(self):
        pass