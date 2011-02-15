# Copyright 2011 Andrea Lattuada <utaaal@gmail.com>

class _InstanceCacheMetaclass(type):
  def __new__(cls, name, bases, attrs):
    if name != 'InstanceCache':
      class_dict = attrs['_dict']
      def _GetClassOrNone(self, name):
        return (class_dict[name] if name in class_dict else None)
      attrs['_GetClassOrNone'] = _GetClassOrNone
    return super(_InstanceCacheMetaclass, cls).__new__(
        cls, name, bases, attrs)

class InstanceCache(object):
  __metaclass__ = _InstanceCacheMetaclass

  def __init__(self, *init_params, **init_dict):
    self._init_params = init_params
    self._init_dict = init_dict
    self._instances = {}

  def Has(self, name):
    return self._GetClassOrNone(name) is not None

  def Get(self, name):
    if name in self._instances:
      ret = self._instances[name]
    else:
      ret = self._instances[name] = (
          self._GetClassOrNone(name)(*self._init_params, **self._init_dict))
    return ret

