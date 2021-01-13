"""Main module for 2048 game"""

#--------------------- IMPORTS ---------------------
import numpy as np
import time
from random import randint, choice



#--------------------- METHODS ---------------------

class main():
	def __init__(self, DEBUG=False):
		self.DEBUG = DEBUG
		self.matrix = np.zeros((4,4))
		self.score = 0
		self.start()

	def start(self):
		self.matrix = np.zeros((4,4))
		self.score = 0

		#add 2 random 2
		row = randint(0,3)
		col = randint(0,3)
		self.matrix[row,col] = 2
		while self.matrix[row, col] != 0: #make sure we don't update twice the same tile
			row = randint(0,3)
			col = randint(0,3)
		self.matrix[row,col] = 2
		self.update_GUI()



	#--------- ACTIONS ON MATRIX ---------
	def stack(self):
		stacked_matrix = np.zeros((4,4))

		for i in range(4):
			pos = 0
			for j in range(4):
				if self.matrix[i,j] != 0: 										#if there is a tile
					stacked_matrix[i,pos] = self.matrix[i,j] #then we move it all the way down the row
					pos +=1
		
		self.matrix = stacked_matrix


	def recombine(self):
		for i in range(4):
			for j in range(3):
				if (self.matrix[i,j] != 0) and (self.matrix[i,j] == self.matrix[i,j+1]): #if tile not empty and equal to one next ot it then combine them
					self.matrix[i,j] *= 2
					self.score += self.matrix[i,j] #we have now reached a higher score
					self.matrix[i,j+1] = 0

	def reverse(self):
		self.matrix = np.flip(self.matrix, axis=1)

	def transpose(self):
		self.matrix = np.transpose(self.matrix)



	#--------- UPDATES ---------
	def add_tile(self):
		row = randint(0,3)
		col = randint(0,3)
		while self.matrix[row, col] != 0: #make sure we don't erase a non-empty tile
			row = randint(0,3)
			col = randint(0,3)
		self.matrix[row,col] = choice([2, 4]) #add randomly a 2 or a 4


	def update_GUI(self):
		if self.DEBUG:
			print(self.matrix) # Show game in console, only for debugging purposes
			time.sleep(2) #wait 2 seconds
			actions = [self.left, self.right, self.up, self.down]
			actions[randint(0,3)]() #simulate an action
		self.u_dead_yet()


	def u_stuck_yet_H(self, m):
		#check for possible moves in horizontal direction
		for i in range(4):
			for j in range(3):
				if m[i,j] == m[i,j+1]: return False
		return True

	def u_stuck_yet_V(self, m):
		#check for possible moves in the vertical direction
		self.u_stuck_yet_H(np.transpose(m))

	def u_dead_yet(self):
		if not any(0 in row for row in self.matrix) and self.u_stuck_yet_H(self.matrix) and self.u_stuck_yet_V(self.matrix):
			#then GAME OVER you lost you can't move anymore
			if self.DEBUG: print("GAME OVER")
			pass #TODO
		elif any(2048 in row for row in self.matrix):
			#then you won congratulations
			if self.DEBUG: print("YOU WON")
			pass #TODO


	#--------- MOVES ---------
	def left(self):
		if self.DEBUG: print("left")

		# Move all to left
		self.stack()
		self.recombine()
		self.stack()
		self.add_tile() # add random tile
		self.update_GUI()
		

	def right(self):
		if self.DEBUG: print("right")

		# Move all to right
		self.reverse() #by flipping it we just have to the same as for left()
		self.stack()
		self.recombine()
		self.stack()
		self.reverse()
		self.add_tile() # add random tile
		self.update_GUI()

	def up(self):
		if self.DEBUG: print("up")

		# Move all to top
		self.transpose()
		self.stack()
		self.recombine()
		self.stack()
		self.transpose()
		self.add_tile() # add random tile
		self.update_GUI()

	def down(self):
		if self.DEBUG: print("down")

		# Move all to bottom
		self.transpose()
		self.reverse() 
		self.stack()
		self.recombine()
		self.stack()
		self.reverse()
		self.transpose()
		self.add_tile() # add random tile
		self.update_GUI()


# print("NEW GAME")
# game = main(DEBUG=True)
# print(game.matrix)
# game.start()
# print(game.matrix)
# game.left()
# print(game.matrix)

game = main(DEBUG=True)