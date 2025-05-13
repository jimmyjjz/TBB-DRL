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

class TBBEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.action_space = gym.spaces.Tuple((
            gym.spaces.MultiBinary(4),# left, right, jump/fly, attack
            gym.spaces.Box(low=0, high=WIDTH, shape=(1,), dtype=np.float32), # horizontal mouse placement
            gym.spaces.Box(low=0, high=HEIGHT, shape=(1,), dtype=np.float32) # vertical mouse placement
        ))
        self.observation_space = spaces.Box(0,255,shape=(HEIGHT//RESCALE_FACTOR, WIDTH//RESCALE_FACTOR, 3), dtype=np.uint8)
        self.total_step=0
        self.episode_steps=0
        self.screen_grabber = dxcam.create(output_idx=0)
        self.text_reader = easyocr.Reader(['en'])
        pyautogui.press('r') # r is ingame input that resets the state
        pyautogui.press('1') # select weapon

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
        pyautogui.moveTo(action[1], action[2])

        try:
            screen = self.screen_grabber.grab()
        except:
            raise Exception(f'Screen cannot be grabbed at step {self.total_step}')

        #.//not in a runnable state currently

    def render(self, mode="human", close=False):
        pass