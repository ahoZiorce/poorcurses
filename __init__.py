import os
import sys
import termios

if os.name == 'nt':
  from ctypes import windll, create_string_buffer

from poorcurses.dyn import Dyn
from poorcurses.exceptions import CursorOutOfBounds

class Terminal:
  def __init__(self):
    self.bufferc_x = 0
    self.bufferc_y = 0
    self.initted = False
    self._nclear = False
    self.buffer = Dyn(fill_value = ' ')
  
  try:
    import tty, termios
  except ImportError:
    try:
      import msvcrt
    except ImportError:
      raise ImportError('getch not available')
    else:
      getch = msvcrt.getch
  else:
    def getch(self):
      import tty, termios
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
      raise CursorOutOfBounds("Fuck you")
    elif x < 0 or y < 0:
      raise CursorOutOfBounds("Fuck you")
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
      self.bufferc_x += 0
      if (self._maxx % self.bufferc_x) == 0:
        sys.stdout.write('\n')
    sys.stdout.write('\n')
    self._nclear = False


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
        except OSError as e:
          print(e)
      finally:
        return (maxy, maxx)
  
  def clear(self):
    self.render_x = 0
    self.render_y = 0
    os.system('cls' if os.name == 'nt' else 'clear')

"""t = Terminal()
r = t.getch()
print(r)
t.getch()
t.initscr()
t.move(2, 9)
t.addstr('LOL')
t.render()

text = 'Welcome to Poorcurses'
t.move(int(t._maxy / 2),int(t._maxx / 2) - len(text))
t.addstr(text)
t.render()

x = 0
y = 0
t.move(y, x)
t.addstr('@')
t.render()
t.getch()
while True:
  c = t.getch()
  t.move(y, x)
  t.addstr(' ')
  t.render()
  if c == 's':
    y += 1
  elif c == 'z':
    y -= 1
  elif c == 'd':
    x += 1
  elif c == 'q':
    x -= 1
  elif c == 'p':
    t.endwin()
    print(str(x) + ' and ' + str(y))
    sys.exit(0)
  t.move(y, x)
  t.addstr('@')
  t.render()"""