from copy import deepcopy as copy

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
          #print(str(self.l))
          self.l.append(copy(self.fill_value))
        self.l.append(copy(item))
        self.max = len(self.l) - 1
  
  def __delitem__(self, key):
    del self.l[key]
    self.max -= 1

  def __str__(self):
    return self.l.__str__()

  def __len__(self):
    return self.l.__len__()

  def __iter__(self):
    return self.l.__iter__()

  def append(self, obj):
    r = self.l.append(copy(obj))
    self.max += 1
    return r

  def pop(self, obj = None):
    r = self.l.pop(copy(obj))
    self.max = len(self.l) - 1
    return r
  
  def exists(self, key):
    if key >= 0 and key <= self.max:
      return True
    else:
      return False

  def to_list(self):
    return self.l
