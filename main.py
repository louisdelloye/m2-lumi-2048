"""Main module for 2048 game"""

#--------------------- IMPORTS ---------------------
import numpy as np




#--------------------- METHODS ---------------------

class main():
	matrix = np.zeros((4,4))

	def show(self):
		"""Show game in console, only for debugging purposes"""

		print(self.matrix)

	def update(self):
		pass

	

	#--------- ACTIONS ---------
	def satck(self):
		pass

	def recombine(self):
		pass

	def transpose(self):
		pass



	#--------- MOVES ---------
	def left(self):
		print("left")

	def right(self):
		print("right")

	def up(self):
		print("up")

	def down(self):
		print("down")