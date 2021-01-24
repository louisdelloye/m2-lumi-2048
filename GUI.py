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
		palette.setColor(QtGui.QPalette.Window, QtGui.QColor('#6e645d'))
		self.setPalette(palette)

		z_layout = QStackedLayout() #create stacked layout for alerts and whatevs
		
		self.Board = Board(self.size, self.board) # Display Board
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
		elif key == QtCore.Qt.Key_W: self.deal_w_it()
		self.Board.board_updated.emit(self.game.matrix) # condition if no moves

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

	def deal_w_it(self):
		print("hehe")
		self.game.boom_i_almost_won()




class WLMessage(QWidget):
	"""Alert Message to announce win/loss and restart new game"""

	def __init__(self):
		super().__init__()

		layout = QVBoxLayout()
		layout.addWidget(QLabel)




class Board(QWidget):
	"""Main Grid Widget"""
	board_updated = QtCore.pyqtSignal(np.ndarray) # slot

	def __init__(self, size, board):
		super().__init__()

		grid = QGridLayout()
		self.board = board
		for i in range(4):
			for j in range(4):
				grid.addWidget(Tile(self.board[i,j], size, self, i, j), i, j)

		grid.setContentsMargins(0, 0, 0, 0)
		self.setLayout(grid)




class Tile(QLabel):
	"""1 number Tile"""
	def __init__(self, value, size, parent, i, j):
		super().__init__()
		self.i = i
		self.j = j
		self.board = parent
		self.board.board_updated.connect(self.update_tile)
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

	def update_tile(self, matrix):
		self.value = matrix[self.i,self.j] # TODO #doesn't work cause

		# Set color
		self.setAutoFillBackground(True)
		palette = self.palette()
		palette.setColor(QtGui.QPalette.Window, QtGui.QColor(c.CELL_COLORS[int(self.value)]))
		self.setPalette(palette)

		if self.value != 0: 
			self.setText(f"{int(self.value)}")
			self.setAlignment(QtCore.Qt.AlignCenter)
			self.setFont(QtGui.QFont("Helvetica", 40, QtGui.QFont.Bold))
		else: self.setText("")
		self.show()
		


#--------------------- RUN ---------------------



app = QApplication(sys.argv)

window = MainWindow()

app.exec_()
