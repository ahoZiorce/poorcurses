import os
import sys

if os.name == 'nt':
  from ctypes import windll, create_string_buffer

from poorcurses.dyn import Dyn

class Terminal:
  def __init__(self):
    self.render_y = 0
    self.render_x = 0
    self._maxy, self._maxx = self.getmaxyx()
    self.buffery = Dyn(fill_value = Dyn(fill_value = ''))
    self.buffery.append(Dyn(fill_value = 54326543254325432))
    self.buffery[0][self._maxx * self._maxy] = 54
  
  def initscr(self):
    self.clear()

  def getmaxyx(self):
    if os.name == 'nt':
      h = windll.kernel32.GetStdHandle(-12)
      csbi = create_string_buffer(22)
      res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
      if res:
          import struct
          (bufx, bufy, curx, cury, wattr,
          left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
          sizex = right - left + 1
          sizey = bottom - top + 1
      else:
          sizex, sizey = 80, 25 # can't determine actual size - return default values
      return (sizey, sizex)
    else:
      try:
        maxx, maxy = os.get_terminal_size(0)
      except OSError:
        try:
          maxx, maxy = os.get_terminal_size(1)
        except OSError:
          raise OSError
      finally:
        return (maxy, maxx)
  
  def clear(self):
    self.render_x = 0
    self.render_y = 0
    os.system('cls' if os.name == 'nt' else 'clear')

t = Terminal()
t.initscr()
print(str(t._maxx) + " and " + str(t._maxy))
"""stringg = ''.join(map(str, t.buffery[0][0][0][0][0].to_list()))
print(' lol' + stringg)"""