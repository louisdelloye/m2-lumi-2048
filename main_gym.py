import sys
import numpy as np
import math
import random

import gym
from openai import gym_game

from PyQt5.QtWidgets import QApplication
from GUI import MainWindow

def simulate(g):
	global epsilon, epsilon_decay
	for episode in range(MAX_EPISODES):

		# Init environment
		state = env.reset()
		total_reward = 0

		# AI tries up to MAX_TRY times
		for t in range(MAX_TRY):

			# In the beginning, do random action to learn
			if random.uniform(0, 1) < epsilon:
				action = env.action_space.sample()
			else:
				action = np.argmax(q_table[state])

			# Do action and get result
			next_state, reward, done, _ = env.step(action)
			total_reward += reward

			# print("linlsed")
			# Get correspond q value from state, action pair
			q_value = q_table[state][action]
			best_q = np.max(q_table[next_state])

			# Q(state, action) <- (1 - a)Q(state, action) + a(reward + rmaxQ(next state, all actions))
			q_table[state][action] = (1 - learning_rate) * q_value + learning_rate * (reward + gamma * best_q)

			# Set up for the next iteration
			state = next_state

			# Draw games
			env.render()
			g.Board.board = env.pygame.game.matrix
			g.Board.board_updated.emit(env.pygame.game.matrix)
			# When episode is done, print reward
			if done or t >= MAX_TRY - 1:
				print("Episode %d finished after %i time steps with total reward = %f." % (episode, t, total_reward))
				break

		# exploring rate decay
		if epsilon >= 0.005:
			epsilon *= epsilon_decay
			print(epsilon)


if __name__ == "__main__":
	env = gym.make("2048-v0")
	MAX_EPISODES = 999 #9999
	MAX_TRY = 100 #1000
	epsilon = 1
	epsilon_decay = 0.99
	learning_rate = 0.2
	gamma = 0.6
	num_box = tuple((env.observation_space.high + np.ones(env.observation_space.shape)).astype(int)) #TODO modify astype ? because I think it should rather be float32 
	print(num_box)
	q_table = np.zeros(num_box + (env.action_space.n,))#, dtype=np.float128)
	
	app = QApplication(sys.argv)
	window = MainWindow()
	window.mutlithread_this(simulate, window)
	app.exec_()
