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

  def __init__(self, selec, silent=False, nb_game=100, speed=0.1, max_depth=5):
    self.game = main()
    self.selec = selec
    self.speed = speed
    self.nb_game = nb_game
    self.max_depth = max_depth
    self.silent = silent
    self.run_loop()

  def run_loop(self):
      if not self.silent:
        app = QApplication(sys.argv)
        window = MainWindow(game=self.game)

      if self.selec == "random":
        if self.silent: agent = Non_AI.RandomAgent(speed=self.speed)
        else: agent = Non_AI.RandomAgent(gui=window, speed=self.speed)

      elif self.selec == "prio":
        if self.silent: agent = Non_AI.PrioAgent(speed=self.speed)
        else: agent = Non_AI.PrioAgent(gui=window, speed=self.speed)
      
      elif self.selec == "serp":
        if self.silent: agent = Non_AI.FutureSerpentin(speed=self.speed)
        else: agent = Non_AI.FutureSerpentin(gui=window, speed=self.speed)

      elif self.selec == "other":
        if self.silent: agent = Non_AI.OtherAgent(speed=self.speed)
        else: agent = Non_AI.OtherAgent(gui=window, speed=self.speed)

      elif self.selec == "carlo":
        if self.silent: agent = Non_AI.CarloAgent(speed=self.speed, max_depth=self.max_depth)
        else: agent = Non_AI.CarloAgent(gui=window, speed=self.speed, max_depth=self.max_depth)

      elif self.selec == "carlosnake":
        if self.silent: agent = Non_AI.CarloTheSnakeAgent(speed=self.speed, max_depth=self.max_depth)
        else: agent = Non_AI.CarloTheSnakeAgent(gui=window, speed=self.speed, max_depth=self.max_depth)

      if self.silent: agent.silent_simu(self.nb_game)
      else: window.mutlithread_this(agent.simulate, self.nb_game)

      if not self.silent: app.exec_()


if __name__ == "__main__":
  Agent("carlosnake", nb_game=10, speed=0.025, silent=True)#, max_depth=5)#, silent=True)