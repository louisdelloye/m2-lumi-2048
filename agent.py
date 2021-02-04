from main import main
from GUI import MainWindow
import Non_AI

import time
import sys
from PyQt5.QtWidgets import QApplication


class Agent():
  """
  Class that contains all types of AI
  """

  def __init__(self, agent, speed=0):
    self.game = main()
    self.speed = speed

    if agent == "random":
      self.run_loop(Non_AI.simulate_random, 100)

    elif agent == "prio":
      self.run_loop(Non_AI.simulate_prio, 100)

    elif agent == "montecarlo":
      pass

    elif agent == "gym":
      pass

  def run_loop(self, func, *args):
      app = QApplication(sys.argv)
      window = MainWindow()
      window.mutlithread_this(func, *args, window, self.speed)
      app.exec_()

  # def update_gui(self, gui, board, speed=0.25):
  #   if gui:
  #     gui.Board.board = board
  #     gui.Board.board_updated.emit(board)
  #     time.sleep(speed)
  #   else: pass


if __name__ == "__main__":
  Agent("prio")