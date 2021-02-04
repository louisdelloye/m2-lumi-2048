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

#--------------------- Base Agent ---------------------
class AgentBase():
	def __init__(self, gui=None, speed=0.05):
		self.speed = speed
		self.gui = gui
		self.matrix_unchanged = 1

	def update_gui(self, matrix):
		if self.gui:
			self.gui.Board.board = matrix
			self.gui.Board.board_updated.emit(matrix)
			time.sleep(self.speed)
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
		if any(0 in r for r in matrix):
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

	# EVAL
	def probe_moves(self, matrix):
		self.matrix_unchanged = True
		smv = np.zeros(4)

		left_m = self.left(matrix)
		smv[0] = self.smoothness(left_m)

		right_m = self.right(matrix)
		smv[1] = self.smoothness(right_m)

		up_m = self.up(matrix)
		smv[2] = self.smoothness(up_m)

		down_m = self.down(matrix)
		smv[3] = self.smoothness(down_m)

		return np.argmax(smv)

	def smoothness(self, matrix):
		smoothness = 0
		for i in range(4):
			for j in range(4):
				if matrix[i,j]:
					value = np.log(matrix[i,j]) / np.log(2) if matrix[i,j] != 0 else 1
					for direction in np.array([[1,0], [0, 1]]):
						vector = direction
						k,l = i,j
						while (k<3 and l<3) and (matrix[k,l] != 0):
								k += direction[0]
								l += direction[1]

						if matrix[k,l] != 0:
							target = np.log(matrix[k,l]) / np.log(2)
							smoothness += np.abs(value - target)
		return smoothness

	def monolithic(self, matrix):
		mono = 0
		totals = [0, 0, 0, 0]

		# up/down direction
		for x in range(4):
			current = 0
			nextc = current+1
			while nextc<4:
				while nextc<4 and matrix[x,nextc] != 0:
					nextc += 1

				if nextc >= 4: nextc -= 1
				currentValue = np.log(matrix[x][current]) / np.log(2) if matrix[x,current] != 0 else 0
				nextcValue = np.log(matrix[x][nextc]) / np.log(2) if matrix[x,nextc] != 0 else 0

				if currentValue > nextcValue:
					totals[0] += nextcValue - currentValue
				elif nextcValue > currentValue:
					totals[1] += currentValue - nextcValue
				
				current = nextc
				nextc += 1
		
		# left/right direction
		for y in range(4):
			current = 0
			nextc = current+1
			while nextc < 4:
				while nextc < 4 and matrix[nextc,y] != 0:
					nextc += 1

				if nextc >= 4: nextc -= 1
				currentValue = np.log(matrix[current,y]) / np.log(2) if matrix[current,y] != 0 else 0
				nextcValue = np.log(matrix[nextc,y]) / np.log(2) if matrix[nextc,y] != 0 else 0

				if currentValue > nextcValue:
					totals[2] += nextcValue - currentValue
				elif nextcValue > currentValue:
					totals[3] += currentValue - nextcValue
				
				current = nextc
				nextc += 1
				
		return max(totals[0], totals[1]) + max(totals[2], totals[3])


#--------------------- Random Agent ---------------------
class RandomAgent(AgentBase):
	def __init__(self, gui=None, speed=0.05):
		super().__init__(gui, speed)

	def run(self, game=main()):
		#Randomly plays the game
		while game.u_dead_yet()==0:
			move=np.random.randint(4)
			if move == 0: game.up()
			if move == 1: game.down()
			if move == 2: game.left()
			if move == 3: game.right()
			super().update_gui(game.matrix)

	def simulate(self, N):
		score=np.zeros(N)
		maxitile=np.zeros(N)
		for i in range(N):
			game = main()
			self.run(game=game)
			score[i]=game.score
			maxitile[i]=game.matrix.max()
		return score, maxitile
	
	def silent_simu(self, N):
		bins=[0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000]
		score,_ = self.simulate(N)
		plt.hist(score, bins=bins)
		plt.xticks(bins)
		plt.show()


#--------------------- Basic Strategy Agent ---------------------
class PrioAgent(AgentBase):
	def __init__(self, gui=None, speed=0.05):
		super().__init__(gui, speed)

	def run(self, game=main()):
		while game.u_dead_yet() == 0: 
			game.right()
			super().update_gui(game.matrix)
			if game.matrix_unchanged:
				game.up()
				super().update_gui(game.matrix)
			if game.matrix_unchanged:
				game.down()
				super().update_gui(game.matrix)
			if game.matrix_unchanged:
				game.left()
				super().update_gui(game.matrix)

	def simulate(self, N):
		score=np.zeros(N)
		maxitile=np.zeros(N)
		for i in range(N):
			game = main()
			self.run(game=game)
			score[i]=game.score
			maxitile[i]=game.matrix.max()
		return score, maxitile
	
	def silent_simu(self, N):
		bins=[0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000]
		tilebins=[4,8,16,32,64,128,256,512,1024,2048,4096]
		#simulates and plots the results
		score, maxitile = self.simulate(N)
		#plots the score
		# plt.hist(score, bins = bins)
		# plt.xticks(bins)

		#plots the maximum tiles
		# maxitile_repartition=np.zeros(len(tilebins))
		# for i in range(len(tilebins)):
		# 	maxitile_repartition[i]=np.sum(maxitile == tilebins[i])
		# plt.bar(tilebins,maxitile_repartition)

		plt.hist(maxitile)
		plt.show()


#--------------------- Other Strategy Agent ---------------------
class OtherAgent(AgentBase):
	def __init__(self, gui=None, speed=0.05):
		super().__init__(gui, speed)

	def run(self, game=main()):
		while game.u_dead_yet() == 0: 
			game.left()
			# print(best_moves)
			super().update_gui(game.matrix)
			if game.matrix_unchanged:
				best_move = super().probe_moves(game.matrix)
				print(best_move)
				if best_move == 0: #then go back to prio
					if game.matrix_unchanged:
						game.up()
						super().update_gui(game.matrix)
					if game.matrix_unchanged:
						game.down()
						super().update_gui(game.matrix)
					if game.matrix_unchanged:
						game.right()
						super().update_gui(game.matrix)
				elif best_move == 1:
					game.right()
					super().update_gui(game.matrix)
				elif best_move == 2:
					game.up()
					super().update_gui(game.matrix)
				elif best_move == 3:
					game.down()
					super().update_gui(game.matrix)

	def simulate(self, N):
		score=np.zeros(N)
		maxitile=np.zeros(N)
		for i in range(N):
			game = main()
			self.run(game=game)
			score[i]=game.score
			maxitile[i]=game.matrix.max()
		return score, maxitile

	def silent_simu(self, N):
		score, maxitile = self.simulate(N)
		plt.hist(maxitile)
		plt.show()





if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	agent = PrioAgent(gui=window, speed=0.05)
	window.mutlithread_this(agent.simulate, 10)
	app.exec_()