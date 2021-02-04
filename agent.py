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

  def __init__(self, agent, nb_game=100, speed=0.1):
    self.game = main()
    self.speed = speed

    if agent == "random":
      self.run_loop(Non_AI.simulate_random, nb_game)

    elif agent == "prio":
      self.run_loop(Non_AI.simulate_prio, nb_game)

    elif agent == "montecarlo":
      pass

    elif agent == "gym":
      pass

  def run_loop(self, func, *args):
      app = QApplication(sys.argv)
      window = MainWindow()
      window.mutlithread_this(func, *args, window, self.speed)
      app.exec_()


if __name__ == "__main__":
  Agent("prio", nb_game=10, speed=0.05)