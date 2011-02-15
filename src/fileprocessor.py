import logging
import mako.template
import os
import os.path
import shutil
import sys

class FileManager(object):
  def __init__(self, base_path_left, base_path_right):
    self.base_path_left, self.base_path_right = base_path_left, base_path_right
    self._os = os
    self._shutil = shutil
    self._open = open

  def RightExist(self, rel_path):
    return self._os.path.isfile(self._os.path.join(
        self.base_path_right, rel_path))

  def LeftIsNewer(self, rel_path):
    lmtime, rmtime = map(
        lambda bp: self._os.stat(self._os.path.join(bp, rel_path)).st_mtime,
        (self.base_path_left, self.base_path_right))
    return lmtime > rmtime

  def CopyLeftToRight(self, rel_path):
    paths = map(lambda bp: self._os.path.join(bp, rel_path),
        (self.base_path_left, self.base_path_right))
    self._shutil.copy(*paths)

  def WriteRight(self, rel_path, buf):
    with self._open(rel_path, 'w') as fd:
      fd.write(buf)

_PROCESSORS = {}

def GetProcessor(name, file_manager):
  return _PROCESSORS[name](file_manager)

class Processor(object):
  def __init__(self, file_manager):
    self._file_manager = file_manager

class MakoProcessor(Processor):
  def Process(self, rel_path, file_desc):
    template = mako.template.Template(file_desc.read())
    rendered = template.render()
    self._file_manager.WriteRight(rel_path, rendered)

_PROCESSORS['mako'] = MakoProcessor

class CopyProcessor(Processor):
  def Process(self, rel_path, file_desc):
    file_desc.read()
    self._file_manager.CopyLeftToRight(rel_path)

_PROCESSORS['copy'] = CopyProcessor

_UPDATE_POLICIES = {}

def GetUpdatePolicy(name, file_manager):
  return _UPDATE_POLICIES[name](file_manager)

class UpdatePolicy(object):
  def __init__(self, file_manager):
    self._file_manager = file_manager

class AlwaysUpdatePolicy(UpdatePolicy):
  def NeedsUpdate(self, rel_path):
    return True

_UPDATE_POLICIES['always'] = AlwaysUpdatePolicy

