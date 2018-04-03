class Dyn:
  def __init__(self, def_list = [], fill_value = None):
    self.l = def_list
    self.max = -1
    self.fill_value = fill_value

  def __getitem__(self, key):
    if key > self.max or key < 0:
      return None
    else:
      return self.l[key]

  def __setitem__(self, key, item):
    if key >= 0:
      if key <= self.max:
        self.l[key] = item
      elif key > self.max:
        for i in range(key - self.max - 1):
          self.l.append(self.fill_value)
        self.l.append(item)
        self.max = len(self.l) - 1
  
  def __delitem__(self, key):
    del self.l[key]
    self.max -= 1

  def __str__(self):
    return str(self.l)

  def __len__(self):
    return len(self.l)

  def __iter__(self):
    return self.l.__iter__()

  def append(self, obj):
    return self.l.append(obj)

  def pop(self, obj = None):
    return self.l.pop(obj)

  def to_list(self):
    return self.l
