from typing import Dict
from ..enums import NodeEnum
from ..models import User


class BitDict(dict):
  dict: Dict[str, int] = {}
  
  def __init__(self, user: User):
    self.user = user
    data = user._bits.split(';')
    
    for i, node in enumerate(NodeEnum):
      self[node.name] = data[i]

  def __setitem__(self, key: str, item: int):
    self.dict[key] = item

    self.user._bits = ';'.join(str(i) for i in self.dict.values())

  def __getitem__(self, key: str):
    return self.dict[key]
    
  def __str__(self):
    return str(self.dict)

  def __repr__(self):
    return repr(self.dict)

  def __len__(self):
    return len(self.dict)

  def __delitem__(self, key: str):
    return

  def clear(self):
    return

  def copy(self):
    return self.dict.copy()

  def has_key(self, k: str):
    return k in self.dict

  def update(self, *args, **kwargs):
    return self.dict.update(*args, **kwargs)

  def keys(self):
    return self.dict.keys()

  def values(self):
    return self.dict.values()

  def items(self):
    return self.dict.items()

  def pop(self, *args):
    return

  def __cmp__(self, dict_: Dict):
    return self.__cmp__(self.dict, dict_)

  def __contains__(self, item):
    return item in self.dict
