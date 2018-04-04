# Ok so i don't know how this import system works but the module (Terminal class) should be imported here

t = Terminal()
r = t.getch()
print(r)
t.getch()
t.initscr()
t.move(2, 9)
t.addstr('LOL')
t.render()

text = 'Welcome to Poorcurses'
t.move(int(t._maxy / 2),int(t._maxx / 2) - int(len(text) / 2))
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
  t.render()