# Copyright 2011 Andrea Lattuada <utaaal@gmail.com>

import unittest

import fileprocessor
import inputparser

DEFAULT_UPDATE_POLICY = 'default'
UPDATE_POLICY = 'policy'
PROCESSOR = 'processor'

class UpdatePolicyCacheMock(object):
  @classmethod
  def Has(cls, name):
    return name == UPDATE_POLICY or name == DEFAULT_UPDATE_POLICY

class ProcessorCacheMock(object):
  @classmethod
  def Has(cls, name):
    return name == PROCESSOR

class DirectiveParserTest(unittest.TestCase):
  def setUp(self):
    self.parser = inputparser.DirectiveParser()
    self.parser._update_policy_cache = UpdatePolicyCacheMock()
    self.parser._processor_cache = ProcessorCacheMock()

  def testRaiseOnInvalidInit(self):
    self.assertRaises(
        inputparser.InvalidUpdatePolicyError, self.parser.Init, 'dummy')

  def testRaiseOnParseBeforeInit(self):
    self.assertRaises(AssertionError, self.parser.Parse, '123456')

  def testParse(self):
    self.parser.Init(DEFAULT_UPDATE_POLICY)
    
    ret = self.parser.Parse('# makopre processor policy')
    self.assertEqual(PROCESSOR, ret.processor)
    self.assertEqual(UPDATE_POLICY, ret.update_policy)

    ret = self.parser.Parse('# makopre processor')
    self.assertEqual(PROCESSOR, ret.processor)
    self.assertEqual(DEFAULT_UPDATE_POLICY, ret.update_policy)

    self.assertEqual(None, self.parser.Parse('# kl; sfs fsdfs dfsd'))
    self.assertEqual(None, self.parser.Parse('makopre sfs fsdfs dfsd'))

    self.assertRaises(inputparser.InvalidProcessorError,
                      self.parser.Parse, '# makopre dummy')
    self.assertRaises(inputparser.InvalidUpdatePolicyError,
                      self.parser.Parse, '# makopre processor dummy')
