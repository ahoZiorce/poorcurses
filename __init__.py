import os

from poorcurses.dyn import Dyn

class Terminal:
  def __init__(self):
    self.render_y = 0
    self.render_x = 0
    self._maxy, self._maxx = self.getmaxyx()
    self.buffery = Dyn(fill_value = Dyn(fill_value = " "))
    self.buffery.append(Dyn(fill_value = " "))
    self.buffery[5]
  
  def initscr(self):
    self.clear()

  def getmaxyx(self):
    maxx, maxy = os.get_terminal_size(0)
    return (maxy, maxx)
  
  def clear(self):
    self.render_x = 0
    self.render_y = 0
    os.system('cls' if os.name == 'nt' else 'clear')

t = Terminal()
t.initscr()
print(str(t._maxx) + " and " + str(t._maxy))
