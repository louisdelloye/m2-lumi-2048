#--------------------- Imports ---------------------
import numpy as np
from main import main
import matplotlib.pyplot as plt
import pandas as pd

#--------------------- Random Agent ---------------------

def random_agent(jeu):
	#Randomly plays the game
	while jeu.u_dead_yet()==0:
		move=np.random.randint(4)
		if move == 0: jeu.up()
		if move == 1: jeu.down()
		if move == 2: jeu.left()
		if move == 3: jeu.right()

def simulate_random(N):
	score=np.zeros(N)
	for i in range(N):
		game=main()
		random_agent(game)
		score[i]=game.score
	return score
def plot_random(N):
	bins=[0, 500, 1000, 1500, 2000, 2500, 3000]
	score = simulate_random(N)
	plt.hist(score, bins=bins)
	plt.xticks(bins)
	plt.show()


#--------------------- Basic Strategy Agent ---------------------
def prio_agent(jeu):
	#Player who follows priorities: right > up > down > left
	while jeu.u_dead_yet() == 0: 
		jeu.right()
		if jeu.matrix_unchanged:
			jeu.up()
		if jeu.matrix_unchanged:
			jeu.down()
		if jeu.matrix_unchanged:
			jeu.left()

def simulate_prio(N):
	score=np.zeros(N)
	for i in range(N):
		game=main()
		prio_agent(game)
		score[i]=game.score
	return score
def plot_prio(N):
	bins=[0, 500, 1000, 1500, 2000, 2500, 3000]
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