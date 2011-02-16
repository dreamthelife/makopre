# Copyright 2011 Andrea Lattuada <utaaal@gmail.com>

import fileprocessor

class FilePipeline(object):
  def __init__(self, update_policy, processor):
    self.update_policy = update_policy
    self.processor = processor

class InvalidProcessorError(Exception):
  def __init__(self, requested_processor):
    self.requested_processor = requested_processor

class InvalidUpdatePolicyError(Exception):
  def __init__(self, requested_policy):
    self.requested_policy = requested_policy

DIRECTIVE_LINE_START = ('#', 'makopre')

class DirectiveParser(object):
  def __init__(self):
    self._update_policy = None
    self._update_policy_cache = fileprocessor.UpdatePolicyCache
    self._processor_cache = fileprocessor.ProcessorCache
  
  def Init(self, default_update_policy=fileprocessor.DEFAULT_UPDATE_POLICY):
    if not self._update_policy_cache.Has(default_update_policy):
      raise InvalidUpdatePolicyError(default_update_policy)
    self._update_policy = default_update_policy

  def Parse(self, line):
    assert self._update_policy is not None

    line = line.split(' ')
    if len(line) < 2 or tuple(line[:2]) != DIRECTIVE_LINE_START:
      return None
    if len(line) < 3 or not self._processor_cache.Has(line[2]):
      raise InvalidProcessorError(line[2])
    pipeline = FilePipeline(self._update_policy, line[2])

    if len(line) >= 4:
      if not self._update_policy_cache.Has(line[3]):
        raise InvalidUpdatePolicyError(line[3])
      pipeline.update_policy = line[3]

    return pipeline

