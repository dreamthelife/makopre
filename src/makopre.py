#! /usr/bin/python

# Makopre - a small binary to preprocess text using mako
#
# Copyright 2011 Andrea Lattuada <utaaal@gmail.com>

import argparse

ARGS = None

def ParseArgs():
  parser = argparse.ArgumentParser()
  def arg(*v, **vv):
    parser.add_argument(*v, **vv)
  arg('--output', default='out/',
      help='Path to the directory the preprocessed files are stored into.')
  arg('--debug', default=False, action='store_const', const=True,
      help='Enable debug level logging.')
  global ARGS
  ARGS = parser.parse_args()

import logging
import mako.template
import os
import os.path
import shutil
import sys

class FileManager:
  def __init__(self, base_path_left, base_path_right):
    self.base_path_left, self.base_path_right = base_path_left, base_path_right
    self.os = os
    self.shutil = shutil

  def LeftIsNewer(self, rel_path):
    lmtime, rmtime = map(
        lambda bp: self.os.stat(self.os.path.join(bp, rel_path)).st_mtime,
        (self.base_path_left, self.base_path_right))
    return lmtime > rmtime

  def CopyLeftToRight(self, path):
    paths = map(lambda bp: self.os.path.join(bp, path),
        (self.base_path_left, self.base_path_right))
    self.shutil.copy(*paths)

FILE_PROCESSORS = {}

def proc_preprocess(open_file):
  input_text = open_file.read()

def main():
  ParseArgs()
  if ARGS.debug:
    logging.basicConfig(level=logging.DEBUG)
  logging.info("Walking directory tree")
  for dirpath, dirnames, filenames in os.walk(os.curdir):
    logging.info("Entering directory %s", dirpath)
    output_dir_path = ARGS.output
    if dirpath != '.':
      output_dir_path = os.path.join(ARGS.output, dirpath)
    if not os.path.isdir(output_dir_path):
      logging.info("Creating output directory %s", output_dir_path)
      os.mkdir(output_dir_path)
    for filename in filenames:
      rel_file_path = os.path.join(dirpath, filename)
      try:
        with open(rel_file_path, 'r') as input_file:
          line1 = input_file.readline()
          if line1.strip() != '## makopre':
            logging.debug("Skipping file %s", rel_file_path)
            continue
          input_text = input_file.read()
      except IOError:
        logging.error('Cannot open file %s', rel_file_path)
        continue
      logging.info("Processing file %s", filename)
      template = mako.template.Template(input_text)
      rendered = template.render()
      try:
        out_path = os.path.join(ARGS.output, rel_file_path)
        with open(out_path, 'w') as output_file:
          output_file.write(rendered)
      except IOError:
        logging.error('Cannot open output file %s for writing.', out_path)

if __name__ == "__main__":
  main()
