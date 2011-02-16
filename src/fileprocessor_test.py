# Copyright 2011 Andrea Lattuada <utaaal@gmail.com>

import unittest

import fileprocessor
import mox
import os
import shutil
import StringIO

BASE_PATH_LEFT = 'base/'
BASE_PATH_RIGHT = 'base/right/'
FILENAME = 'test.html'
MTIME_OLD = 456
MTIME_NEW = 678
CONTENT = 'abcd'

class FakeStat(object):
  def __init__(self, mtime):
    self.st_mtime = mtime

class _FileLike(object):
  def write(self, text):
    pass
  def close(self):
    pass
  def __enter__(self):
    return self
  def __exit__(self, exc_type, exc_value, traceback):
    self.close()

class FileManagerTest(unittest.TestCase):
  def setUp(self):
    self.mox = mox.Mox()
    self.mgr = fileprocessor.FileManager(BASE_PATH_LEFT, BASE_PATH_RIGHT)

  def tearDown(self):
    self.mox.ResetAll()

  def testRightExists(self):
    mock_os = self.mox.CreateMock(os)
    mock_os.path = self.mox.CreateMock(os.path)
    mock_os.path.join = os.path.join
    mock_os.path.isfile(BASE_PATH_RIGHT + FILENAME).AndReturn(True)
    self.mox.ReplayAll()
    self.mgr._os= mock_os
    self.assertTrue(self.mgr.RightExists(FILENAME))
    self.mox.VerifyAll()

  def testLeftIsNewer(self):
    mock_os = self.mox.CreateMock(os)
    self.mox.StubOutWithMock(self.mgr, 'RightExists')
    self.mgr.RightExists(FILENAME).AndReturn(True)
    mock_os.stat(BASE_PATH_LEFT + FILENAME).InAnyOrder().AndReturn(
        FakeStat(MTIME_NEW))
    mock_os.stat(BASE_PATH_RIGHT + FILENAME).InAnyOrder().AndReturn(
        FakeStat(MTIME_OLD))
    self.mox.ReplayAll()
    self.mgr._os = mock_os
    self.assertTrue(self.mgr.LeftIsNewer(FILENAME))
    self.mox.VerifyAll()

  def testLeftIsNewerRaisesOnMissingRightFile(self):
    self.mox.StubOutWithMock(self.mgr, 'RightExists')
    self.mgr.RightExists(FILENAME).AndReturn(False)
    self.mox.ReplayAll()
    self.assertRaises(AssertionError, self.mgr.LeftIsNewer, FILENAME)

  def testCopyLeftToRight(self):
    mock_shutil = self.mox.CreateMock(shutil)
    mock_shutil.copy(BASE_PATH_LEFT + FILENAME, BASE_PATH_RIGHT + FILENAME)
    self.mox.ReplayAll()
    self.mgr._shutil = mock_shutil
    self.mgr.CopyLeftToRight(FILENAME)
    self.mox.VerifyAll()

  def testWriteRight(self):
    mock_open = self.mox.CreateMock(open)
    mock_file = _FileLike()
    self.mox.StubOutWithMock(mock_file, 'write')
    self.mox.StubOutWithMock(mock_file, 'close')
    mock_open(FILENAME, 'w').AndReturn(mock_file)
    mock_file.write(CONTENT)
    mock_file.close()
    self.mox.ReplayAll()
    self.mgr._open = mock_open
    self.mgr.WriteRight(FILENAME, CONTENT)
    self.mox.VerifyAll()

FILENAME_2 = 'two.html'
FILENAME_3 = 'three.html'

class FileManagerMock(object):
  class _FileDesc(object):
    def __init__(self, right_exist=False, left_is_newer=False):
      self.right_exist = right_exist
      self.left_is_newer = left_is_newer

  _FILES = {
      FILENAME: _FileDesc(False),
      FILENAME_2: _FileDesc(True),
      FILENAME_3: _FileDesc(True, True)
      }
      

  def __init__(self):
    self._copy_left_to_right_counter = {}
    self._write_right_buffers = {}

  def RightExists(self, rel_path):
    return FileManagerMock._FILES[rel_path].right_exist

  def LeftIsNewer(self, rel_path):
    return FileManagerMock._FILES[rel_path].left_is_newer

  def CopyLeftToRight(self, rel_path):
    counter = self._copy_left_to_right_counter
    counter[rel_path] = counter[rel_path] if rel_path in counter else 1

  def WriteRight(self, rel_path, buf):
    self._write_right_buffers[rel_path] = buf

MAKO_TEMPLATE = '${"hello"}\n'
MAKO_OUTPUT = 'hello\n'

class FileManagerBasedTestBase(unittest.TestCase):
  def setUp(self):
    self.mox = mox.Mox()
    self.mock_file_manager = FileManagerMock()

  def tearDown(self):
    self.mox.ResetAll()

class MakoProcessorTest(FileManagerBasedTestBase):
  def testGet(self):
    proc_cache = fileprocessor.ProcessorCache(self.mock_file_manager)
    proc = proc_cache.Get('mako')
    self.assert_(isinstance(proc, fileprocessor.MakoProcessor))

  def testProcess(self):
    proc = fileprocessor.MakoProcessor(self.mock_file_manager)
    proc.Process(FILENAME, StringIO.StringIO(MAKO_TEMPLATE))
    self.assertEqual(MAKO_OUTPUT,
                     self.mock_file_manager._write_right_buffers[FILENAME])

class CopyProcessorTest(FileManagerBasedTestBase):
  def testProcess(self):
    proc = fileprocessor.CopyProcessor(self.mock_file_manager)
    proc.Process(FILENAME, StringIO.StringIO(CONTENT))
    self.assertEqual(
        1, self.mock_file_manager._copy_left_to_right_counter[FILENAME])

class AlwaysUpdatePolicy(FileManagerBasedTestBase):
  def testGet(self):
    pol_cache = fileprocessor.UpdatePolicyCache(self.mock_file_manager)
    pol = pol_cache.Get('always')
    self.assert_(isinstance(pol, fileprocessor.AlwaysUpdatePolicy))

  def testNeedsUpdate(self):
    pol = fileprocessor.AlwaysUpdatePolicy(self.mock_file_manager)
    self.assertTrue(pol.NeedsUpdate(FILENAME))
    self.assertTrue(pol.NeedsUpdate(FILENAME_2))
    self.assertTrue(pol.NeedsUpdate(FILENAME_3))

class NewerUpdatePolicy(FileManagerBasedTestBase):
  def testNeedsUpdate(self):
    pol = fileprocessor.NewerUpdatePolicy(self.mock_file_manager)
    self.assertTrue(pol.NeedsUpdate(FILENAME))
    self.assertFalse(pol.NeedsUpdate(FILENAME_2))
    self.assertTrue(pol.NeedsUpdate(FILENAME_3))

class UpdatePolicyCacheTest(unittest.TestCase):
  def testHasDefaultUpdatePolicy(self):
    self.assertTrue(fileprocessor.UpdatePolicyCache.Has(
        fileprocessor.DEFAULT_UPDATE_POLICY))

if __name__ == '__main__':
  unittest.main()
