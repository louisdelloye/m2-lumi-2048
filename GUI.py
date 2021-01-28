"""GUI module for our 2048 application"""

#--------------------- IMPORTS ---------------------
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDialog, QStackedLayout, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt5 import QtCore, QtWidgets, QtGui, Qt

import sys
import numpy as np
from random import randint

import main as m #import game module (actually better to do that the other way around (import GUI in main) ?)
import colors as c



#--------------------- MAIN ---------------------
class MainWindow(QMainWindow):
	# replay_demanded = QtCore.pyqtSignal()
	# quitting = QtCore.pyqtSignal()

	def __init__(self, game=m.main()):
		super().__init__()
		self.size = 600
		self.setWindowTitle("2048")
		self.game = game
		self.board = self.game.matrix

		# Set BG color
		self.setAutoFillBackground(True)
		palette = self.palette()
		palette.setColor(QtGui.QPalette.Window, QtGui.QColor('#6e645d'))
		self.setPalette(palette)

		self.Board = Board(self.size, self.board) # Display Board

		self.setCentralWidget(self.Board)
		self.setContentsMargins(10, 10, 10, 10)
		self.show()
		
	def restart(self):
		self.game.start()

	#--------- EventHandlers ---------
	def keyPressEvent(self, event):
		key = event.key()

		# Handle key bindind
		if key == QtCore.Qt.Key_Up: self.up()
		elif key == QtCore.Qt.Key_Down: self.down()
		elif key == QtCore.Qt.Key_Left: self.left()
		elif key == QtCore.Qt.Key_Right: self.right()
		elif key == QtCore.Qt.Key_W: self.deal_w_it()
		elif key == QtCore.Qt.Key_L: self.u_die()
		self.Board.board_updated.emit(self.game.matrix) # condition if no moves
		self.show_dialog()

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

	def u_die(self):
		print("die")
		self.game.u_lose()

	def show_dialog(self):
		"""Prompt for dialog"""
		game_state = self.game.u_dead_yet()
		if game_state == 0:
			pass #keep the game going
		else:
			dialog = WLMessage(True if game_state == 1 else False, self)
			dialog.exec_()


class WLMessage(QDialog):
	"""Alert message to announce win/loss and restart new game"""

	def __init__(self, has_won, parent_window):
		super().__init__()
		self.setFixedHeight(150) #set size
		self.setFixedWidth(300)

		self.parent_window = parent_window

		# Set color
		self.setAutoFillBackground(True)
		palette = self.palette()
		palette.setColor(QtGui.QPalette.Window, QtGui.QColor('#6e645d'))
		self.setPalette(palette)

		layout = QVBoxLayout()

		#Text info
		info = QLabel()
		info.setText("You won !" if has_won else "You lost")
		info.setAlignment(QtCore.Qt.AlignCenter)
		info.setFont(QtGui.QFont("Helvetica", 20, QtGui.QFont.Bold))
		layout.addWidget(info)

		#Buttons to quit / replay
		h_layout = QHBoxLayout()

		replay = QPushButton()
		replay.setText("Replay")
		replay.setFont(QtGui.QFont("Helvetica", 20, QtGui.QFont.Normal))
		replay.clicked.connect(self.restart_handler)
		replay.setFixedHeight(40)
		replay.setStyleSheet("""QPushButton {
			background-color: '#edc22e';
			border-radius: 5px;
			color: #eee4da;
		}""")
		h_layout.addWidget(replay)

		quitter = QPushButton()
		quitter.setText("Quit")
		quitter.setFont(QtGui.QFont("Helvetica", 20, QtGui.QFont.Normal))
		quitter.clicked.connect(self.quit_handler)
		quitter.setFixedHeight(40)
		quitter.setStyleSheet("""QPushButton {
			background-color: #91857d;
			border-radius: 5px;
		}""")
		h_layout.addWidget(quitter)

		h_widget = QWidget()
		h_widget.setLayout(h_layout)
		layout.addWidget(h_widget)
		
		self.setLayout(layout)
		self.show()

	def restart_handler(self):
		print("restart")
		self.parent_window.restart() #reset board
		self.parent_window.Board.board_updated.emit(self.parent_window.game.matrix) #update GUI
		self.close() #close dialog

	def quit_handler(self):
		print("close")
		QtCore.QCoreApplication.quit() #quit application




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
# window = WLMessage(True)

app.exec_()
