import os
import sys

from poorcurses.dyn import Dyn

from poorcurses.exceptions import CursorOutOfBounds
from poorcurses.exceptions import UnsuportedEnvironment

try:
  import tty
  import termios
  OSTYPE = 'unix'
except ImportError:
  try:
    import msvcrt
    import struct
    from ctypes import windll
    from ctypes import create_string_buffer
    OSTYPE = 'nt'
  except ImportError:
    OSTYPE = 'unknown'
    raise UnsuportedEnvironment('The current environment is not supported by this version of poorcurses, please check your os or your python version')


class Terminal:
  def __init__(self):
    self.bufferc_x = 0
    self.bufferc_y = 0
    self._nclear = False
    self.buffer = Dyn(fill_value = ' ')
  
  if OSTYPE == 'nt':
    def getch(self):
      res = str(msvcrt.getch())
      res = res[:-1]
      res = res[2:]
      return res
  elif OSTYPE == 'unix':
    def getch(self):
      fd = sys.stdin.fileno()
      old_settings = termios.tcgetattr(fd)
      try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
      finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
      return ch

  def initscr(self):
    self._maxy, self._maxx = self.getmaxyx()
    self.buffer[self._maxx * self._maxy] = ' '
    self.clear()
    self.initted = True

  def endwin(self):
    self.clear()

  def move(self, y, x):
    real_y = y + 2
    real_x = x + 1
    if x > self._maxx - 2 or y > self._maxy:
      raise CursorOutOfBounds('Fuck you')
    elif x < 0 or y < 0:
      raise CursorOutOfBounds('Fuck you')
    self.bufferc_y = real_y
    self.bufferc_x = real_x
  
  def addstr(self, text):
    for i in text:
      self.buffer[self.bufferc_y * self._maxx + self.bufferc_x] = i
      self.bufferc_x += 1

  def render(self):
    self.clear()
    for i in self.buffer:
      sys.stdout.write(str(i))
      self.bufferc_x += 1
    sys.stdout.write('\n')

  if OSTYPE == 'nt':
    def getmaxyx(self):
      h = windll.kernel32.GetStdHandle(-12)
      csbi = create_string_buffer(22)
      res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
      if res:
          (bufx, bufy, curx, cury, wattr,
          left, top, right, bottom, maxx, maxy) = struct.unpack('hhhhHhhhhhh', csbi.raw)
          sizex = right - left + 1
          sizey = bottom - top + 1
      else:
          sizex, sizey = 80, 25
      return (sizey, sizex)
  elif OSTYPE == 'unix':
    def getmaxyx(self):
      try:
        maxx, maxy = os.get_terminal_size(0)
      except OSError:
        try:
          maxx, maxy = os.get_terminal_size(1)
        except OSError as e:
          print(e)
      finally:
        return (maxy, maxx)
  
  if OSTYPE == 'nt':
    def clear(self):
      os.system('cls')
      sys.stdout.flush()
  elif OSTYPE == 'unix':
    def clear(self):
      os.system('clear')
      sys.stdout.flush()
