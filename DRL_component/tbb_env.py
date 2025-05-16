import gymnasium as gym
from gymnasium import spaces
import pydirectinput
import numpy as np
import dxcam
from utils import resize_img, get_setting

HEIGHT = 1080
WIDTH = 1920
RESCALE_FACTOR = 8

class TBBEnv(gym.Env):
    def __init__(self):
        super().__init__()
        # left, right, jump/fly, attack, hook, m(mouse).x -/+, m.x bit 1...7, m(mouse).y -/+, m.y bit 1...7
        self.action_space=gym.spaces.MultiBinary(21)
        self.observation_space = spaces.Box(0, 255, shape=(HEIGHT // RESCALE_FACTOR, WIDTH // RESCALE_FACTOR, 3), dtype=np.uint8)
        self.total_steps = 0
        self.episode_steps = 0
        self.pre_reward_accumulant = 0
        self.screen_grabber = dxcam.create(output_idx=1)
        self.pre_screen = np.zeros((HEIGHT // RESCALE_FACTOR, WIDTH // RESCALE_FACTOR, 3), dtype=np.uint8)

    def reset(self, seed=None, options=None):
        pydirectinput.press('r')  # r is ingame input that resets the state
        pydirectinput.press('1')  # select weapon
        pydirectinput.moveTo(WIDTH//2, HEIGHT//2) # mouse to middle of screen
        #input keys up
        pydirectinput.keyUp('a')
        pydirectinput.keyUp('d')
        pydirectinput.keyUp(' ')
        pydirectinput.mouseUp()
        pydirectinput.keyUp('e')

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
            pydirectinput.keyDown('a') if action[0] else pydirectinput.keyUp('a')
            pydirectinput.keyDown('d') if action[1] else pydirectinput.keyUp('d')
            pydirectinput.keyDown(' ') if action[2] else pydirectinput.keyUp(' ')
            pydirectinput.mouseDown() if action[3] else pydirectinput.mouseUp()
            pydirectinput.keyDown('e') if action[4] else pydirectinput.keyUp('e')

            horizontal_move=0
            for i in range(6, 13):
                if action[i]:
                    horizontal_move|=(1<<(i-6))
            horizontal_move*=10

            vertical_move=0
            for i in range(14, 21):
                if action[i]:
                    vertical_move |= (1<<(i-14))
            vertical_move*=10

            if action[5]: horizontal_move*=-1
            if action[13]: vertical_move*=-1

            if get_setting("restrain_cursor_from_side_monitor"):
                pydirectinput.moveTo(max(min(cur_x+horizontal_move,WIDTH),0), max(min(cur_y+vertical_move,HEIGHT),0))
            else:
                pydirectinput.moveTo(cur_x + horizontal_move, cur_y + vertical_move)

        screen = self.screen_grabber.grab()
        if screen is None:
            print(f"Screen idle at episode step {self.episode_steps}, total step {self.total_steps}.")
            obs = self.pre_screen
        else:
            obs = resize_img(screen, WIDTH // RESCALE_FACTOR, HEIGHT // RESCALE_FACTOR)
            self.pre_screen = obs

        finished = False
        with open("reward_accumulant.txt", "r") as f:
            cur_reward_accumulant = f.read()
        if len(cur_reward_accumulant) >= 8 and cur_reward_accumulant[:8] == 'Inactive':
            finished = True
            if cur_reward_accumulant[8:] == ' Player died.':
                reward = get_setting("lose_reward")
            elif cur_reward_accumulant[8:] == ' Boss defeated.':
                reward = get_setting("win_reward")
            else:
                reward = 0
            reward += (self.pre_reward_accumulant if get_setting("account_previous_reward_at_final_state") else 0)
        else:
            reward = int(cur_reward_accumulant) - self.pre_reward_accumulant
            self.pre_reward_accumulant = int(cur_reward_accumulant)

        self.total_steps += 1
        self.episode_steps += 1
        return obs, reward, finished, False, {}