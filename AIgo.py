import numpy as np
from main import main



class AIplayer:
	def __init__(self, jeu=main()):
		self.jeu = jeu
		self.note=0

	def notation(self):
		#gives a score to the current grid
		corners = ([0,0],[0,3],[3,0],[3,3])
		note = np.sum(self.jeu.matrix)
		if 2048 in self.jeu.matrix: note += 10000
		maxi = np.max(self.jeu.matrix)
		maxi_index = np.where(self.jeu.matrix == maxi)	
		if np.size(maxi_index) == 2: #If there is only 1 max tile
			note += 1.1
			if maxi_index in corners: note *= 1.2
			if (maxi > 2) and (maxi/2 in self.jeu.matrix): #If the next big tile exists
				maxi2_index = np.where(self.jeu.matrix == maxi/2)
#				for i in maxi2_index:
#					if 
		self.note = note

AIgame = AIplayer()