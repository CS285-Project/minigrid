# This script generates textual prompt. The prompt could then be fed to GPT.

import gymnasium as gym
from minigrid.core.constants import *
import matplotlib.pyplot as plt
from .gpt_interface import *
import random
import re

IDX_TO_STATE = {v: k for k, v in STATE_TO_IDX.items()}
DIR_TO_STR = {0: "right", 1: "down", 2: "left", 3: "up"}
ACTION_TO_STR = {0: "turn left", 1: "turn right", 2: "move forward", 3: "pick up the object in front", 4: "drop the object in front", 5: "toggle the object in front", 6: "finish the environment"}

def get_relative_position(i, j, img):
    center = img.shape[0] // 2
    dist_h = img.shape[1] - j - 1
    dist_v = i - center
    if dist_v < 0:
        return f"{dist_h} steps in front, {-dist_v} steps to the left"
    elif dist_v > 0:
        return f"{dist_h} steps in front, {dist_v} steps to the right"
    else:
        return f"{dist_h} steps directly in front"

def img_to_str(img):
    result = ""
    for j in range(img.shape[1]):
        for i in range(img.shape[0]):
            obj = IDX_TO_OBJECT[img[i, j, 0]]
            color = IDX_TO_COLOR[img[i, j, 1]]
            state = IDX_TO_STATE[img[i, j, 2]]
            obj_info = ""
            if obj in ["ball", "box", "key"]:
                obj_info = f"{color} {obj}"
            elif obj in ["door"]:
                obj_info = f"{color} {state} {obj}"
            else:
                continue
            result += f"There's a {obj_info} {get_relative_position(i, j, img)}. "
    if len(result) == 0:
        result += "All you see are floors, walls, and blocked objects. "
    return result

def get_reward_prompt_str(obs, action):
    image, direction, mission = img_to_str(obs['image']), DIR_TO_STR[obs['direction']], obs['mission']
    act = ACTION_TO_STR[action.item()]
    return f'''
You are an agent in a Minigrid environment. Your mission is {mission}. Your agent's direction is currently {direction}.
Your agent can only see in front of itself. It cannot see blocked objects.
{image}

Your agent would like to {act}. Evaluate how this state and action is helpful for achieving the goal, using a number between -1 and 1. Please only return that single number, and do not return anything else. Do not explain your reasoning, just provide a reward.
'''

def get_planning_prompt_str(obs_img, mission_txt):
    image, mission = img_to_str(obs_img), mission_txt
    return f'''You are an agent in a Minigrid environment. Your mission is {mission}. Your agent can only see in front of itself. It cannot see blocked objects. Here is the vision of your agent: {image}
You have the following skills at your disposal:
Skill 0: Go to Object in the same room
Skill 1: Open door in the same room
Skill 2: Pickup an item in the same room
Skill 3: Put an item next to an item in the same room
Skill 4: Unlock a door in the same room
Skill 5: Find an object in a random room
Skill 6: Go to an object in a random room

Based on the skills, determine which skill is the most appropriate to use. Use the format "Answer: Skill [a number from 0 to 6]". Do not say anything else.
'''

def gpt_skill_planning(obs, mission_txt):
    prompt = get_planning_prompt_str(obs, mission_txt)
    response = interact_with_gpt(prompt)
    match = re.search(r'Answer: Skill (\d)', response)
    if match:
        skill = int(match.group(1))
    return skill


class GPTRewardFunction():
    def __init__(self, query_gpt_prob, ask_every, gpt_prob_decay=1):
        self.query_gpt_prob = query_gpt_prob
        self.ask_interval = ask_every
        self.gpt_prob_decay = gpt_prob_decay
        self.counter = 0

    def should_ask_gpt(self):
        if self.query_gpt_prob == -1:
            if self.counter <= 0:
                self.counter = self.ask_interval
                return True
            else:
                self.counter -= 1
                return False
        else:
            return random.random() < self.query_gpt_prob

    def reshape_reward(self, observation, action, reward, done):
        if self.should_ask_gpt():
            gpt_reward = gpt_reward_func(observation, action)
            print(f"gpt reward is {gpt_reward}")
            shaped_reward = reward + gpt_reward
        else:
            shaped_reward = reward
        # self.query_gpt_prob *= self.gpt_prob_decay
        return shaped_reward
            
def gpt_reward_func(obs, action):
    prompt = get_reward_prompt_str(obs, action)
    return float(interact_with_gpt(prompt))


# The things below are dry run test code
if __name__ == "__main__":
    env = gym.make("BabyAI-GoToImpUnlock-v0", render_mode='rgb_array')
    # Reset the environment to get the initial state
    obs = env.reset()
    # Take some actions and continue displaying the state
    for _ in range(1):
        action = env.action_space.sample()  # Replace with your desired action
        obs, reward, terminated, truncated, info = env.step(action)
        plt.figure()
        plt.imshow(env.render())
        print(obs)
        print(get_planning_prompt_str(obs['image'], obs['mission']))
    plt.show()

