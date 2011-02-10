#! env python

import unittest

import filecmp
import subprocess
import os.path

TMP_DIR = '/tmp/'
TEST_FILE_SIMPLE = 'simple_template.txt'

class TestBinary(unittest.TestCase):
  def test_simple_invocation(self):
    subprocess.call('pwd')
    args = ['../src/makopre.py', '--output', TMP_DIR, TEST_FILE_SIMPLE]
    self.assertEqual(0, subprocess.call(args))
    self.assert_(filecmp.cmp(os.path.join(TMP_DIR, TEST_FILE_SIMPLE),
                             TEST_FILE_SIMPLE))

if __name__ == '__main__':
  unittest.main()
