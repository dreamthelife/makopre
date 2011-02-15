# Copyright 2011 Andrea Lattuada <utaaal@gmail.com>

import unittest

import makopre
import mox
import StringIO

PREPROCESS_BEFORE = """${"TEST"}"""
PREPROCESS_AFTER = """TEST"""

class TestProcessors(unittest.TestCase):
  def setUp(self):
    self.mox = mox.Mox()

  def test_proc_preprocess(self):
    input_file = StringIO.StringIO(PREPROCESS_BEFORE)
    makopre.proc_preprocess(input_file)

if __name__ == '__main__':
  unittest.main()
