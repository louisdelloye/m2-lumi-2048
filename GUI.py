"""GUI module for our 2048 application"""

#--------------------- IMPORTS ---------------------
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QStackedLayout, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt5 import QtCore, QtWidgets, QtGui

import sys
import numpy as np
from random import randint

# from main import * #import game module (actually better to do that the other way around (import GUI in main))
import colors as c



#--------------------- MAIN ---------------------
class MainWindow(QMainWindow):

	def __init__(self):
		super().__init__()
		self.size = 600
		self.setWindowTitle("2048")

		# Set BG color
		self.setAutoFillBackground(True)
		palette = self.palette()
		palette.setColor(QtGui.QPalette.Window, QtGui.QColor('#ffecd1'))
		self.setPalette(palette)

		z_layout = QStackedLayout() #create stacked layout for alerts and whatevs

		# Display Board
		self.board = Board(self.size)
		z_layout.addWidget(self.board)

		#TODO : add stacked alerts when winning / losing

		# Display app
		widget = QWidget()
		widget.setLayout(z_layout)
		self.setCentralWidget(widget)
		self.setContentsMargins(10, 10, 10, 10)


class WLMessage(QWidget):
	"""Alert Message to announce win/loss and restart new game"""

	def __init__(self):
		super().__init__()

		layout = QVBoxLayout()
		layout.addWidget(QLabel)


class Board(QWidget):
	"""Main Grid Widget"""

	def __init__(self, size):
		super().__init__()

		grid = QGridLayout()
		board = np.zeros((4,4))
		for i in range(4):
			for j in range(4):
				grid.addWidget(Tile(randint(1, 11), size), i, j)

		grid.setContentsMargins(0, 0, 0, 0)
		self.setLayout(grid)





	#--------- EventHandlers ---------
	def keyPressEvent(self, event):
		key = event.key()
		# Handle key bindind
		if key == QtCore.Qt.Key_Up: self.up()
		elif key == QtCore.Qt.Key_Down: self.down()
		elif key == QtCore.Qt.Key_Left: self.left()
		elif key == QtCore.Qt.Key_Right: self.right()

	def left(self):
		print("left")
	
	def right(self):
		print("right")
	
	def up(self):
		print("up")
	
	def down(self):
		print("down")




class Tile(QWidget):
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
		palette.setColor(QtGui.QPalette.Window, QtGui.QColor(c.CELL_COLORS[2**value]))
		self.setPalette(palette)


	


#--------------------- RUN ---------------------

app = QApplication(sys.argv)

# window = MainWidget()
window = MainWindow()
window.show()

app.exec_()