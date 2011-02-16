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
  arg('paths', nargs='*')
  global ARGS
  ARGS = parser.parse_args()

import logging
import mako.template
import os
import os.path
import shutil
import subprocess
import sys

def tree_mode():
  logging.info("Walking directory tree")
  processes = []
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
      args = [sys.argv[0], '--output', ARGS.output, rel_file_path]
      if ARGS.debug:
        args[1:1] = ['--debug']
      logging.debug('Starting subprocess with args: %s', args)
      proc = subprocess.Popen(args,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
      processes.append(proc)
  for proc in processes:
    if proc.wait() != 0:
      logging.error('Failure:\n' + proc.stdout.read())
    else:
      logging.debug('Subprocess returned success:\n' + proc.stdout.read())

def file_mode():
  for input_file_path in ARGS.paths: 
    try:
      with open(input_file_path, 'r') as input_file:
        line1 = input_file.readline()
        if line1.strip() != '## makopre':
          logging.debug("Skipping file %s", input_file_path)
          continue
        input_text = input_file.read()
    except IOError:
      logging.error('Cannot open file %s', input_file_path)
      continue
    logging.info("Processing file %s", input_file_path)
    template = mako.template.Template(input_text)
    rendered = template.render()
    try:
      out_path = os.path.join(ARGS.output, input_file_path)
      with open(out_path, 'w') as output_file:
        output_file.write(rendered)
    except IOError:
      logging.error('Cannot open output file %s for writing.', out_path)

def main():
  ParseArgs()
  if ARGS.debug:
    logging.basicConfig(level=logging.DEBUG)
  if len(ARGS.paths) == 0:
    tree_mode()
  else:
    file_mode()

if __name__ == "__main__":
  main()
