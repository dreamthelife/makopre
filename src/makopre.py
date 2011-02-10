#! /usr/bin/python

import argparse

ARGS = None

def ParseArgs():
  parser = argparse.ArgumentParser()
  def arg(*v, **vv):
    parser.add_argument(*v, **vv)
  arg('files', nargs='+')
  arg('--output', required=True)
  global ARGS
  ARGS = parser.parse_args()

import logging
import mako.template
import os.path
import sys

def main():
  ParseArgs()
  for filename in ARGS.files:
    try:
      template = mako.template.Template(filename=filename)
    except IOError:
      logging.error('Cannot open file %s.', filename)
      continue
    rendered = template.render()
    try:
      out_path = os.path.join(ARGS.output, filename)
      with open(out_path, 'w') as output_file:
        output_file.write(rendered)
    except IOError:
      logging.error('Cannot open output file %s for writing.', out_path)

main()
