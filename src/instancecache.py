# Copyright 2011 Andrea Lattuada <utaaal@gmail.com>

class _InstanceCacheMetaclass(type):
  def __new__(cls, name, bases, attrs):
    if name != 'InstanceCache':
      assert '_dict' in attrs
    return super(_InstanceCacheMetaclass, cls).__new__(
        cls, name, bases, attrs)

class InstanceCache(object):
  __metaclass__ = _InstanceCacheMetaclass

  def __init__(self, *init_params, **init_dict):
    self._init_params = init_params
    self._init_dict = init_dict
    self._instances = {}

  @classmethod
  def Has(cls, name):
    return name in cls._dict

  def Get(self, name):
    if name in self._instances:
      ret = self._instances[name]
    else:
      ret = self._instances[name] = self.__class__._dict[name](
          *self._init_params, **self._init_dict)
    return ret

