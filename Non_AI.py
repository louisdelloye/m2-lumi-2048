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
	for i in range(N):
		game=main()
		prio_agent(game, gui)
		score[i]=game.score
	return score

def plot_prio(N):
	score = simulate_prio(N)
	plt.hist(score, bins=bins)
	plt.xticks(bins)
	plt.show()





"""
def basic_move(self):
    if self.u_stuck_yet_H
    #Does a move in a random direction
    move=np.random.randint(4)
    if move == 0: self.up()
    if move == 1: self.down()
    if move == 2: self.left()
    if move == 3: self.right()

def basic_agent(jeu):
    while jeu.u_dead_yet()==0:
        jeu.basic_move()

def simulate_basic(N):
    score=np.zeros(N)
    for i in range(N):
        game=main()
        basic_agent(game)
        score[i]=game.score
def plot_basic(N):
    bins=[0, 500, 1000, 1500, 2000, 2500, 3000]
    simulate_basic(N)"""



if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.mutlithread_this(simulate_prio, 100, window)
	app.exec_()