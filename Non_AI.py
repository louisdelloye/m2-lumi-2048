#--------------------- Imports ---------------------
import numpy as np
from main import main
import matplotlib.pyplot as plt
import pandas as pd
import time
from random import randint

import sys
from PyQt5.QtWidgets import QApplication
from GUI import MainWindow

#--------------------- Base Agent ---------------------
class AgentBase():
	def __init__(self, gui=None, speed=0.05):
		self.speed = speed
		self.gui = gui
		self.matrix_unchanged = True
		self.silent = False

	def update_gui(self, matrix):
		if self.gui:
			self.gui.Board.board = matrix
			self.gui.Board.board_updated.emit(matrix)
			if not self.silent: time.sleep(self.speed)
		else: pass

	def move(self, best_move, game):
		if best_move == 0: 
			game.left()
			self.update_gui(game.matrix)
		elif best_move == 1:
			game.right()
			self.update_gui(game.matrix)
		elif best_move == 2:
			game.up()
			self.update_gui(game.matrix)
		elif best_move == 3:
			game.down()
			self.update_gui(game.matrix)

	def action(self, action, matrix):
		if action == 0: 
			return self.left(matrix)
		elif action == 1:
			return self.right(matrix)
		elif action == 2:
			return self.up(matrix)
		elif action == 3:
			return self.down(matrix)

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
			new_matrix[row,col] = np.random.choice([2, 4], p=[0.9, 0.1]) #add randomly a 2 or a 4
		return new_matrix

	def stack_AND_combine(self, matrix):
		old = np.copy(matrix)
		new = self.stack(matrix)
		new = self.recombine(new)
		new = self.stack(new)
		if not np.allclose(old, new):
			new = self.add_tile(new) # add random tile if changes happened
			self.matrix_unchanged = False
		else: self.matrix_unchanged = True
		return new

	def left(self, matrix):
			# Move all to left
			return self.stack_AND_combine(matrix)
		
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


#--------------------- Evaluate next move using prefered tiles Agent ---------------------
class FutureSerpentin(AgentBase):
	def __init__(self, gui=None, speed=0.05):
		super().__init__(gui, speed)	

	def future_best_move(self, matrix):
		self.matrix_unchanged = True
		smv = np.zeros(4)

		left_m = self.left(matrix)
		smv[0] = self.evaluate(left_m)

		right_m = self.right(matrix)
		smv[1] = self.evaluate(right_m)

		up_m = self.up(matrix)
		smv[2] = self.evaluate(up_m)

		down_m = self.down(matrix)
		smv[3] = self.evaluate(down_m)

		return np.argsort(smv) # The order of the best moves


	# Evaluation of a matrix with priority tiles
	def evaluate(self, matrix):
		rating_matrix = np.array(([0,8,10,500],[1,6,25,300],[2,5,35,150],[3,4,50,80]))
		return np.sum(rating_matrix * matrix)

	def run(self, game=main()):
		count=3
		while (game.u_dead_yet() == 0):
			best_move = self.future_best_move(game.matrix)[count]
			if best_move == 0:
				game.left()
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
			if game.matrix_unchanged == 0:
				count = 3
			elif game.matrix_unchanged == 1:
				count -= 1 
			if count == -1:
				count = 3

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
		tilebins=[4,8,16,32,64,128,256,512,1024,2048,4096]
		score, maxitile = self.simulate(N)
		plt.hist(maxitile)
		plt.show()
	
class OtherAgent(AgentBase):
	def __init__(self, gui=None, speed=0.05):
		super().__init__(gui, speed)

	def run(self, game=main()):
		while game.u_dead_yet() == 0: 
			best_move = self.probe_moves(game)
			super().move(best_move, game)
	
	def probe_moves(self, game, func=None):
		self.matrix_unchanged = True
		# prio_weight = np.array([0.27, 0.26, 0.25, 0.22])
		smv_weight = 0 #0.1
		mono_weight = 0 #3.0
		non_z_weight = 0 #10 #3.7
		max_pos_weight = 0 #5
		min_pos_weight = 0 #5
		serp_weight = 1
		func_eval_weight = 1.0

		smv = np.zeros(4)
		mono = np.zeros(4)
		non_z = np.zeros(4)
		serp = np.zeros(4)
		max_pos = np.zeros((4,2))
		min_pos = np.zeros((4,2))
		if func: func_eval = np.zeros(4)
		all_eval = np.zeros(4)

		m = game.matrix
		for i in range(4):
			if i == 0:
				m = super().left(m)
			elif i == 1:
				m = super().right(m)
			elif i == 2:
				m = super().up(m)
			elif i == 3:
				m = super().down(m)
			
			smv[i] = super().smoothness(m)
			mono[i] = super().monolithic(m)
			non_z[i] = np.count_nonzero(m)
			serp[i] = self.serpent(m)
			max_pos[i] = np.argmax(m)
			min_pos[i] = np.argmin(m)
			# max_pos[i] = np.unravel_index(np.argmax(m), shape=(4,4))
			# min_pos[i] = np.unravel_index(np.argmin(m), shape=(4,4))
			if func: func_eval[i] = func(m)

			m = game.matrix # reset for next iteration

		all_eval = - smv_weight * smv + mono_weight * mono - non_z_weight * non_z - max_pos_weight * (max_pos[:,0] + max_pos[:,1]) - min_pos_weight * (8 - min_pos[:,0] + min_pos[:,1]) + serp_weight + serp
		if func: all_eval += func_eval_weight * func_eval
		best_move = np.argmax(all_eval)# * prio_weight)

		print(all_eval)
		tst = super().action(best_move, game.matrix)
		while self.matrix_unchanged:
			np.put(all_eval, best_move, -1e18)
			best_move = np.argmax(all_eval)
			tst = super().action(best_move, game.matrix)

		return best_move
	
	def serpent(self, matrix):
		m = np.ones((4,4))
		for i in range(4):
			for j in range(4):
				if i % 2 == 0:
				# 	m[i,j] *= (15-i-j)
				# else: m[i,3-j] *= (15-i-3+j)
					m[i,j] = 0.1**(i+j)
				else: m[i,3-j] = 0.1**(i+3-j)
				# 	m[i,j] = 2**(15-i-j)
				# else: m[i,3-j] = 2**(15-i-3+j)
		return np.sum(matrix * m)

	def simulate(self, N):
		score=np.zeros(N)
		maxitile=np.zeros(N)
		for i in range(N):
			print(f"game {i} done")
			game = main()
			self.run(game=game)
			score[i]=game.score
			maxitile[i]=game.matrix.max()
		return score, maxitile

	def silent_simu(self, N):
		self.silent = True
		score, maxitile = self.simulate(N)
		self.silent = False
		plt.hist(maxitile)
		plt.show()


#--------------------- Monte Carlo Strategy Agent ---------------------
class CarloAgent(AgentBase):
	def __init__(self, gui=None, speed=0.05, max_depth=1):
		super().__init__(gui, speed)
		self.max_depth = max_depth
	
	def run(self, game=main()):
		while game.u_dead_yet() == 0: 
			best_move = self.probe_move(game.matrix)
			super().move(best_move, game)

	def simulate(self, N):
		score=np.zeros(N)
		maxitile=np.zeros(N)
		for i in range(N):
			print(f"game {i} done")
			game = main()
			self.run(game=game)
			score[i]=game.score
			maxitile[i]=game.matrix.max()
		return score, maxitile

	def silent_simu(self, N):
		self.silent = True
		score, maxitile = self.simulate(N)
		self.silent = False
		plt.hist(maxitile)
		plt.show()

	def go_deep(self, matrix, depth):
		if depth == self.max_depth:
			return self.final_score(matrix)
		
		total = 0
		for i,j in np.argwhere(matrix == 0):
			#simulate placing random 2 with 0.9 proba
			matrix_w2 = np.copy(matrix)
			matrix_w2[i,j] = 2
			score_w2 = self.calc_score(matrix_w2, depth)
			total += 0.9 * score_w2

			#simulate placing random 4 with 0.1 proba
			matrix_w4 = np.copy(matrix)
			matrix_w4[i,j] = 4
			score_w4 = self.calc_score(matrix_w4, depth)
			total += 0.1 * score_w4
		return total

	def calc_score(self, matrix, depth):
		score = -1e18
		best_score = -1e18
		for i in range(4):
			m = super().action(i, matrix)
			if not np.allclose(matrix, m):
				score = self.go_deep(m, depth + 1)
				best_score = max(score, best_score) 
		return best_score

	def is_unchanged(self, matrix, move):
		if np.allclose(super().action(move, matrix), matrix):
			return -1e18
		else: return self.go_deep(matrix, 0)

	def probe_move(self, matrix):
		self.matrix_unchanged = True
		depth = 0
		score = -1e18
		best_score = -1e18
		best_move = 0
		m = matrix
		for i in range(4):
			m = super().action(i, matrix)
			score = self.is_unchanged(matrix, i)
			if score > best_score:
				best_score = score
				best_move = i
		return best_move
			
	def final_score(self, matrix):
		nz_weight = 10 #10
		max_weight = 3 #1
		max_pos_weight = 0
		smv_weight = 0.1
		mono_weight = 1
		return np.max(matrix) * max_weight - np.count_nonzero(matrix) * nz_weight \
			+ np.argmax(matrix) * max_pos_weight - smv_weight * super().smoothness(matrix) \
			+ mono_weight * super().monolithic(matrix)
	



agent = FutureSerpentin()
agent.silent_simu(100)

# if __name__ == "__main__":
# 	app = QApplication(sys.argv)
# 	window = MainWindow()
# 	agent = FutureSerpentin(gui=window, speed=0.025)
# 	window.mutlithread_this(agent.simulate, 10)
# 	app.exec_()