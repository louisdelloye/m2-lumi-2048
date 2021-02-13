"""Main module for 2048 game"""

#--------------------- IMPORTS ---------------------
import numpy as np
import time
from random import randint

from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDialog, QStackedLayout, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QRunnable, QThreadPool
from PyQt5 import QtCore, QtWidgets, QtGui, Qt

# import keyboard

import sys


#--------------------- METHODS ---------------------

class main():
	def __init__(self, DEBUG=False, no_GUI=False):
		self.DEBUG = DEBUG
		self.matrix = np.zeros((4,4))
		self.score = 0
		self.no_GUI = no_GUI
		self.matrix_unchanged = 0
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
		if self.no_GUI: self.update_GUI()



	#--------- ACTIONS ON MATRIX ---------
	def stack(self):
		stacked_matrix = np.zeros((4,4))
		for i in range(4):
			pos = 0
			for j in range(4):
				if self.matrix[i,j] != 0: 								 #if there is a tile
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
		if any(0 in r for r in self.matrix):
			while self.matrix[row, col] != 0:# and any(0 in r for r in self.matrix): #make sure we don't erase a non-empty tile
				row = randint(0,3)
				col = randint(0,3)
			self.matrix[row,col] = np.random.choice([2, 4], p=[0.9,0.1]) #add randomly a 2 or a 4


	def update_GUI(self):
		# keyboard.is_pressed('up', lambda: print('dick'))
		print(self.matrix) # Show game in console, only for debugging purposes
		if self.DEBUG:
			time.sleep(2) #wait 2 seconds
			actions = [self.left, self.right, self.up, self.down]
			actions[randint(0,3)]() #simulate an action


	def u_stuck_yet_H(self, m):
		#check for possible moves in horizontal direction
		for i in range(4):
			for j in range(3):
				if m[i,j] == m[i,j+1]: return False
		return True

	def u_stuck_yet_V(self, m):
		#check for possible moves in the vertical direction
		return self.u_stuck_yet_H(np.transpose(m))

	def u_dead_yet(self):
		if not any(0 in row for row in self.matrix) and self.u_stuck_yet_H(self.matrix) and self.u_stuck_yet_V(self.matrix):
			#then GAME OVER you lost you can't move anymore
			if self.DEBUG: print("GAME OVER")
			return -1
		elif any(2048 in row for row in self.matrix):
			#then you won congratulations
			if self.DEBUG: print("YOU WON")
			return 1
		return 0


	#--------- MOVES ---------
	def stack_AND_combine(self):
		old = np.copy(self.matrix)
		self.stack()
		self.recombine()
		self.stack()
		if not np.allclose(old, self.matrix):
			self.add_tile() # add random tile if changes happened
			self.matrix_unchanged = 0
		else: self.matrix_unchanged = 1

	def left(self):
		if self.DEBUG: print("left")

		if self.u_dead_yet() not in [-1, 1]:
			# Move all to left
			self.stack_AND_combine()
			self.update_GUI()
		

	def right(self):
		if self.DEBUG: print("right")

		if self.u_dead_yet() not in [-1, 1]:
			# Move all to right
			self.reverse() #by flipping it we just have to the same as for left()
			self.stack_AND_combine()
			self.reverse()
			self.update_GUI()

	def up(self):
		if self.DEBUG: print("up")

		if self.u_dead_yet() not in [-1, 1]:
			# Move all to top
			self.transpose()
			self.stack_AND_combine()
			self.transpose()
			self.update_GUI()

	def down(self):
		if self.DEBUG: print("down")

		if self.u_dead_yet() not in [-1, 1]:
			# Move all to bottom
			self.transpose()
			self.reverse() 
			self.stack_AND_combine()
			self.reverse()
			self.transpose()
			self.update_GUI()

	def boom_i_almost_won(self):
		self.matrix[0,0] = 1024 
		self.matrix[0,1] = 1024 

	def u_lose(self):
		"""Method that creates matrix where u can't do anything"""
		losing_matrix = 2 * np.ones((4,4))
		for i in range(4):
			for j in range(4):
				if (j%2 == 0 and i%2 == 1) or (j%2 == 1 and i%2 == 0):
					losing_matrix[i,j] = 4
		self.matrix = losing_matrix



if __name__ == "__main__":
	class MainWindow(QMainWindow):
		def __init__(self):
			super().__init__()
			self.game = main(no_GUI=True)
			self.show()
			self.setWindowOpacity(0.)
		
		def keyPressEvent(self, event):
			key = event.key()

			# Handle key bindind
			if key == QtCore.Qt.Key_Up: self.game.up()
			elif key == QtCore.Qt.Key_Down: self.game.down()
			elif key == QtCore.Qt.Key_Left: self.game.left()
			elif key == QtCore.Qt.Key_Right: self.game.right()
			elif key == QtCore.Qt.Key_W: self.game.deal_w_it()
			elif key == QtCore.Qt.Key_L: self.game.u_die()
			elif key == QtCore.Qt.Key_Q: QtCore.QCoreApplication.quit() #quit app
	
	app = QApplication(sys.argv)
	window = MainWindow()
	app.exec_()
	# game = main(no_GUI=True)
	# game = main(DEBUG=True)

# independent files