# Copyright 2011 Andrea Lattuada <utaaal@gmail.com>

import unittest

import instancecache

CLASSES = {
  'int': int,
  'string': str
}
  

class InstanceCacheTest(unittest.TestCase):
  def test(self):
    class DummyCache(instancecache.InstanceCache):
      _dict = CLASSES
      pass

    cache = DummyCache("3")

    self.assertTrue(DummyCache.Has('int'))
    self.assertFalse(DummyCache.Has('ddd'))

    self.assertEqual(3, cache.Get('int'))
