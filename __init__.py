import os
import sys
import termios

if os.name == 'nt':
  from ctypes import windll, create_string_buffer

from poorcurses.dyn import Dyn

class Terminal:
  def __init__(self):
    self.render_y = 0
    self.render_x = 0
    self.bufferc_x = 0
    self.bufferc_y = 0
    self.initted = False
    self._nclear = False
    self._maxy, self._maxx = self.getmaxyx()
    self.buffer = Dyn(fill_value = ' ')
  

  try:
    import tty, termios
  except ImportError:
    # Probably Windows.
    try:
      import msvcrt
    except ImportError:
      # FIXME what to do on other platforms?
      # Just give up here.
      raise ImportError('getch not available')
    else:
      getch = msvcrt.getch
  else:
    def getch(self):
      import tty, termios
      """getch() -> key character

      Read a single keypress from stdin and return the resulting character. 
      Nothing is echoed to the console. This call will block if a keypress 
      is not already available, but will not wait for Enter to be pressed. 

      If the pressed key was a modifier key, nothing will be detected; if
      it were a special function key, it may return the first character of
      of an escape sequence, leaving additional characters in the buffer.
      """
      fd = sys.stdin.fileno()
      old_settings = termios.tcgetattr(fd)
      try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
      finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
      return ch

  def initscr(self):
    self.clear()
    self.initted = True

  def move(self, y, x):
    self.bufferc_y = y
    self.bufferc_x = x
  
  def addstr(self, text):
    for i in text:
      self.buffer[self.bufferc_y * self._maxx + self.bufferc_x] = i
      self.bufferc_x += 1
    if self.bufferc_x > self._maxx:
      raise OSError
    if self.bufferc_y <= self.render_y:
      self._nclear = True

  def render(self):
    if self._nclear:
      self.clear()
    for i in self.buffer:
      sys.stdout.write(str(i))
      self.render_x += 1
      if (self._maxx % self.render_x) == 0:
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
t.move(0, 5)
t.addstr("lol")
t.move(1, 5)
t.addstr("lol")
t.render()
t.getch()