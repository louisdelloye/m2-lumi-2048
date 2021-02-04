#--------------------- Imports ---------------------
import numpy as np
from main import main
import matplotlib.pyplot as plt
import pandas as pd
import time

import sys
from PyQt5.QtWidgets import QApplication
from GUI import MainWindow

def update_gui(gui, board, speed=0.25):
	if gui:
		gui.Board.board = board
		gui.Board.board_updated.emit(board)
		time.sleep(speed)
	else: pass

#--------------------- Random Agent ---------------------
bins=[0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000]
tilebins=[4,8,16,32,64,128,256,512,1024,2048,4096]

def random_agent(jeu, gui=None):
	#Randomly plays the game
	while jeu.u_dead_yet()==0:
		move=np.random.randint(4)
		if move == 0: jeu.up()
		if move == 1: jeu.down()
		if move == 2: jeu.left()
		if move == 3: jeu.right()
		update_gui(gui, jeu.matrix)

def simulate_random(N, gui=None):
	score=np.zeros(N)
	for i in range(N):
		game=main()
		random_agent(game, gui)
		score[i]=game.score
	return score
def plot_random(N):
	score = simulate_random(N)
	plt.hist(score, bins=bins)
	plt.xticks(bins)
	plt.show()


#--------------------- Basic Strategy Agent ---------------------
def prio_agent(jeu, gui=None):
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


def simulate_prio(N, gui=None):
	score=np.zeros(N)
	maxitile=np.zeros(N)
	for i in range(N):
		game=main()
		prio_agent(game, gui)
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








"""
if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.mutlithread_this(simulate_prio, 100, window)
	app.exec_()"""