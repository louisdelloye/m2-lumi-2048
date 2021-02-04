import gym
from gym import spaces
import numpy as np
from openai.gym_game.envs.pygame_2d import PyGame2D

class CustomEnv(gym.Env):
	def __init__(self):
		self.speed = 0.01
		self.pygame = PyGame2D(self.speed)
		self.action_space = spaces.Discrete(3) #TODO 0 = left, 1 = right, 2 = up, 3 = down
		self.observation_space = spaces.Box(np.array([0,0,0,0,0]), np.array([16,100000, 2048, 3, 3]), dtype=np.int) 
		# self.observation_space = spaces.Box(np.zeros(16).astype(np.int), 2048 * np.ones(16).astype(np.int), dtype=np.int)
		# self.observation_space = spaces.Box(np.zeros((4,4)), 2048 * np.ones((4,4)), shape=(4,4), dtype=np.int)
		# self.observation_space = spaces.Box(np.zeros((4,4)), 2048 * np.zeros((4,4)), dtype=np.int) 
		# self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), np.array([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]), dtype=np.int)  

	def reset(self):
		del self.pygame
		self.pygame = PyGame2D(self.speed)
		obs = self.pygame.observe()
		return obs

	def step(self, action):
		self.pygame.action(action)
		obs = self.pygame.observe()
		reward = self.pygame.evaluate()
		done = self.pygame.is_done()
		return obs, reward, done, {}
	
	def render(self, mode="human", close=False): 			#TODO
		self.pygame.view()
