# Copyright 2011 Andrea Lattuada <utaaal@gmail.com>

import unittest

import filecmp
import logging
import subprocess
import os.path
import shutil
import sys
import tempfile

TMP_DIR = os.path.join(tempfile.gettempdir(), 'makopreout')
TEST_FILE_SIMPLE = 'template.txt'

ARGS = ['../../makopre.py', '--debug', '--output', TMP_DIR]

def setUp():
  logging.info('Output path: %s', TMP_DIR)

class TestBinary(unittest.TestCase):
  def setUp(self):
    logging.debug(os.getcwd())
    self.restored_dir = os.getcwd()
    if os.path.isdir(TMP_DIR):
      shutil.rmtree(TMP_DIR)
    os.mkdir(TMP_DIR)

  def tearDown(self):
    os.chdir(self.restored_dir)

  def CallMakopre(self):
    p = subprocess.Popen(ARGS, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    ret = p.wait()
    logging.debug(p.stdout.read())
    return ret

  def test_simple_invocation(self):
    os.chdir('testdata/simple')
    self.assertEqual(0, self.CallMakopre())
    with open(os.path.join(TMP_DIR, TEST_FILE_SIMPLE)) as output_file:
      self.assertEqual('Hello, world!\n', output_file.read())

  def test_dirtree_invocation(self):
    os.chdir('testdata/dirtree')
    self.assertEqual(0, self.CallMakopre())
    self.assert_(os.path.isfile(os.path.join(TMP_DIR, 'root.txt')))
    self.assert_(os.path.isfile(os.path.join(TMP_DIR, 'dir/leaf.txt')))

if __name__ == '__main__':
  unittest.main()
