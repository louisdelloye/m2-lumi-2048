#--------------------- Imports ---------------------
import numpy as np
from main import main
import matplotlib.pyplot as plt
import pandas as pd
import time
from random import randint, choice

import sys
from PyQt5.QtWidgets import QApplication
from GUI import MainWindow

def update_gui(gui, board, speed=0.25):
	if gui:
		gui.Board.board = board
		gui.Board.board_updated.emit(board)
		time.sleep(speed)
	else: pass


class AgentBase():
	def __init__(self, gui=None, speed=0.05):
		self.game = game
		self.speed = speed
		self.gui = gui
		self.matrix_unchanged = 1

	def update_gui(self):
		if self.gui:
			self.gui.Board.board = self.game.matrix
			self.gui.Board.board_updated.emit(self.game.matrix)
			time.sleep(speed)
		else: pass
	
	# ACTIONS
	def stack(self, matrix):
		stacked_matrix = np.zeros((4,4))
		for i in range(4):
			pos = 0
			for j in range(4):
				if matrix[i,j] != 0: 								 #if there is a tile
					stacked_matrix[i,pos] = matrix[i,j] #then we move it all the way down the row
					pos +=1
		return stacked_matrix

	def recombine(self, matrix):
		new_m = np.copy(matrix)
		for i in range(4):
			for j in range(3):
				if (matrix[i,j] != 0) and (matrix[i,j] == matrix[i,j+1]): #if tile not empty and equal to one next ot it then combine them
					new_m[i,j] *= 2
					new_m[i,j+1] = 0
		return new_m

	def reverse(self, matrix):
		return np.flip(matrix, axis=1)

	def transpose(self, matrix):
		return np.transpose(matrix)

	def add_tile(self, matrix):
		new_matrix = np.copy(matrix)
		row = randint(0,3)
		col = randint(0,3)
		if any(0 in r for r in self.matrix):
			while new_matrix[row, col] != 0:# and any(0 in r for r in self.matrix): #make sure we don't erase a non-empty tile
				row = randint(0,3)
				col = randint(0,3)
			new_matrix[row,col] = choice([2, 4]) #add randomly a 2 or a 4
		return new_matrix

	def stack_AND_combine(self, matrix):
		old = np.copy(matrix)
		new = self.stack(matrix)
		new = self.recombine(new)
		new = self.stack(new)
		if not np.allclose(old, new):
			new = self.add_tile(new) # add random tile if changes happened
			self.matrix_unchanged = True
		else: self.matrix_unchanged = False
		return new

	def left(self, matrix):
			# Move all to left
			new = self.stack_AND_combine(matrix)
			return new
		
	def right(self, matrix):
		new = self.reverse(matrix) #by flipping it we just have to the same as for left()
		new = self.stack_AND_combine(new)
		new = self.reverse(new)
		return new

	def up(self, matrix):
		new = self.transpose(matrix)
		new = self.stack_AND_combine(new)
		new = self.transpose(new)
		return new

	def down(self, matrix):
		new = self.transpose(matrix)
		new = self.reverse(new) 
		new = self.stack_AND_combine(new)
		new = self.reverse(new)
		new = self.transpose(new)
		return new

	def probe_move(self, matrix, action):
		self.matrix_unchanged = True
		new = np.zeros((4,4))
		if action == 0:
			new = self.left(matrix)
		elif action == 1:
			new = self.right(matrix)
		elif action == 2:
			new = self.up(matrix)
		elif action == 3:
			new = self.down(matrix)

	def smoothness(self, matrix):
		pass

	def monolithic(self, matrix):
		pass




#--------------------- Random Agent ---------------------
bins=[0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000]
tilebins=[4,8,16,32,64,128,256,512,1024,2048,4096]

def random_agent(jeu, gui=None, speed=0):
	#Randomly plays the game
	while jeu.u_dead_yet()==0:
		move=np.random.randint(4)
		if move == 0: jeu.up()
		if move == 1: jeu.down()
		if move == 2: jeu.left()
		if move == 3: jeu.right()
		update_gui(gui, jeu.matrix, speed)

def simulate_random(N, gui=None, speed=0):
	score=np.zeros(N)
	for i in range(N):
		game=main()
		random_agent(game, gui, speed)
		score[i]=game.score
		# time.sleep(speed)
	return score
def plot_random(N):
	score = simulate_random(N)
	plt.hist(score, bins=bins)
	plt.xticks(bins)
	plt.show()


#--------------------- Basic Strategy Agent ---------------------
def prio_agent(jeu, gui=None, speed=0):
	#Player who follows priorities: right > up > down > left
	while jeu.u_dead_yet() == 0: 
		jeu.right()
		update_gui(gui, jeu.matrix, speed)
		if jeu.matrix_unchanged:
			jeu.up()
			update_gui(gui, jeu.matrix, speed)
		if jeu.matrix_unchanged:
			jeu.down()
			update_gui(gui, jeu.matrix, speed)
		if jeu.matrix_unchanged:
			jeu.left()
			update_gui(gui, jeu.matrix, speed)


def simulate_prio(N, gui=None, speed=0):
	score=np.zeros(N)
	maxitile=np.zeros(N)
	for i in range(N):
		game=main()
		prio_agent(game, gui, speed)
		score[i]=game.score
		maxitile[i]=game.matrix.max()
	return score, maxitile

def plot_prio(N):
	#simulates and plots the results
	score, maxitile = simulate_prio(N)	
	#plots the score

	"""plt.hist(score, bins = bins)
	plt.xticks(bins)"""

	#plots the maximum tiles
	"""
	maxitile_repartition=np.zeros(len(tilebins))
	for i in range(len(tilebins)):
		maxitile_repartition[i]=np.sum(maxitile == tilebins[i])
	plt.bar(tilebins,maxitile_repartition)"""

	plt.hist(maxitile)
	plt.show()



#--------------------- Other Strategy Agent ---------------------
class OtherAgent():
	def __init__(self, jeu, speed=0):
		self.jeu = jeu

	def run(self, jeu=self.jeu, gui=None, speed=0):
		#Player who follows priorities: right > up > down > left
		while jeu.u_dead_yet() == 0: 
			jeu.right()
			update_gui(gui, jeu.matrix)
			if jeu.matrix_unchanged:
				jeu.up()
				update_gui(gui, jeu.matrix)
			if jeu.matrix_unchanged:
				jeu.down()
				update_gui(gui, jeu.matrix)
			if jeu.matrix_unchanged:
				jeu.left()
				update_gui(gui, jeu.matrix)

	def simulate(self, N, gui=None, speed=0):
		score=np.zeros(N)
		for i in range(N):
			game = main()
			self.run(game, gui, self.speed)
			score[i] = game.score
			# time.sleep(speed)
		return score







"""
if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.mutlithread_this(simulate_prio, 100, window)
	app.exec_()"""