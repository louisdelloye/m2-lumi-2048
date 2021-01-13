"""GUI module for our 2048 application"""

#--------------------- IMPORTS ---------------------
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QStackedLayout, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt5 import QtCore, QtWidgets, QtGui, Qt

import sys
import numpy as np
from random import randint

import main as m #import game module (actually better to do that the other way around (import GUI in main) ?)
import colors as c



#--------------------- MAIN ---------------------
class MainWindow(QMainWindow):

	def __init__(self):
		super().__init__()
		self.size = 600
		self.setWindowTitle("2048")
		self.game = m.main()
		self.board = self.game.matrix

		# Set BG color
		self.setAutoFillBackground(True)
		palette = self.palette()
		palette.setColor(QtGui.QPalette.Window, QtGui.QColor('#ffecd1'))
		self.setPalette(palette)

		z_layout = QStackedLayout() #create stacked layout for alerts and whatevs

		# Display Board
		self.Board = Board(self.size, self.board)
		z_layout.addWidget(self.Board)

		#TODO : add stacked alerts when winning / losing

		# Display app
		widget = QWidget()
		widget.setLayout(z_layout)
		self.setCentralWidget(widget)
		self.setContentsMargins(10, 10, 10, 10)
		self.show()
	

	#--------- EventHandlers ---------
	def keyPressEvent(self, event):
		key = event.key()

		# Handle key bindind
		if key == QtCore.Qt.Key_Up: self.up()
		elif key == QtCore.Qt.Key_Down: self.down()
		elif key == QtCore.Qt.Key_Left: self.left()
		elif key == QtCore.Qt.Key_Right: self.right()

		print(self.game.matrix)
		# self.update()
		self.Board.update()

	def left(self):
		print("left")
		self.game.left()
	
	def right(self):
		print("right")
		self.game.right()
	
	def up(self):
		print("up")
		self.game.up()
	
	def down(self):
		print("down")
		self.game.down()




class WLMessage(QWidget):
	"""Alert Message to announce win/loss and restart new game"""

	def __init__(self):
		super().__init__()

		layout = QVBoxLayout()
		layout.addWidget(QLabel)




class Board(QWidget):
	"""Main Grid Widget"""

	def __init__(self, size, board):
		super().__init__()

		grid = QGridLayout()
		self.board = board
		for i in range(4):
			for j in range(4):
				grid.addWidget(Tile(self.board[i,j], size), i, j)

		grid.setContentsMargins(0, 0, 0, 0)
		self.setLayout(grid)




class Tile(QLabel):
	"""1 number Tile"""
	def __init__(self, value, size):
		super().__init__()
		self.size = size / 4
		self.setContentsMargins(2, 2, 2, 2)
		self.value = value #set value of Tile
		self.setFixedHeight(self.size - 4) #set size
		self.setFixedWidth(self.size - 4)

		# Set color
		self.setAutoFillBackground(True)
		palette = self.palette()
		palette.setColor(QtGui.QPalette.Window, QtGui.QColor(c.CELL_COLORS[int(value)]))
		self.setPalette(palette)

		if self.value != 0: 
			self.setText(f"{int(self.value)}")
			self.setAlignment(QtCore.Qt.AlignCenter)
			self.setFont(QtGui.QFont("Helvetica", 40, QtGui.QFont.Bold))
		


	


#--------------------- RUN ---------------------



app = QApplication(sys.argv)

window = MainWindow()
# window = Board(400)
# window = Tile(11, 400)
# window.show()

app.exec_()
