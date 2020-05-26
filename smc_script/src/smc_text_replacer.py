#!/usr/bin/env python3

# TODO:
# * chmod of files
# * think about absolute/relative paths
# * take old_text and new_text from files (not inline)
# * better alignments

import getopt
import sys
from sys import argv, exit
from os import path, walk, getcwd, chmod
import fileinput

SCRIPT_FILENAME = path.basename(__file__)
CALL_HELP_MSG = 'For more information call: ./%s -h' % SCRIPT_FILENAME

def receive_settings(args, settings):
  try:
    opts, args = getopt.getopt(args, 'hf:i:t:s')
  except getopt.GetoptError as err:
    print str(err)
    print CALL_HELP_MSG
    exit(1)
  # Go through the arguments
  for opt, arg in opts:
    print arg
    print repr(arg)
    if opt == '-h':
        print('Usage: ./%s -f <text_to_find> -i <text_to_insert> -t <target> [ -s ]') % SCRIPT_FILENAME
      print('-f : set text to find inline using quotes or set path to file with text')
      print('-i : set text to insert inline using quotes or set path to file with text')
      print('-t : set target as directory or file path')
      print('-s : to enable silent mode')
      print('To add tabs and new lines inline use Python Escape Sequences (\\t, \\n and other) inside quotes.')
      print("Example to replace all tabs by the 2 spaces: ./%s -f '\\t' -i '  ' -t dir_path/ -s") % SCRIPT_FILENAME
      print("Example 0: ./%s -f 'text_to_search' -i 'text_to_insert' -t file_path") % SCRIPT_FILENAME
      print("Example 1: ./%s -f file_path -i 'text_to_insert' -t dir_path/ -s") % SCRIPT_FILENAME
      print("Example 2: ./%s -f 'text_to_find' -i file_path -t dir_path/") % SCRIPT_FILENAME
      exit()
    elif opt == '-f':
      if arg[0] in ("'", '"'):
        settings['old_text'] = str(arg.decode('string_escape'))
      else:
        settings['old_text_path'] = arg
    elif opt == '-i':
      if arg[0] in ("'", '"'):
        settings['new_text'] = str(arg.decode('string_escape'))
      else:
        settings['new_text_path'] = arg
    elif opt == '-t':
      settings['path'] = arg
  # Return filled settings
  return settings


def check_settings(settings):
  do_exit = 0
  # Check OLD_TEXT setting
  if settings['old_text'] == '' and settings['old_text_path'] == '':
    print('Please, set what will be finding via -f option.')
    do_exit = 1
  elif settings['old_text'] == '':
    if path.exists(settings['old_text_path']) and path.isfile(settings['old_text_path']):
      with open(settings['old_text_path']) as f:
        settings['old_text'] = f.read()
    else:
      print('File path that was set as text to find is incorrect. Please, try another.')
      do_exit = 1
  # Check NEW_TEXT setting
  if settings['new_text'] == '' and settings['new_text_path'] == '':
    print('Please, set what will be inserting via -i option.')
    do_exit = 1
  elif settings['new_text'] == '':
    if path.exists(settings['new_text_path']) and path.isfile(settings['new_text_path']):
      with open(settings['new_text_path']) as f:
        settings['new_text'] = f.read()
    else:
      print('File path that was set as text to insert is incorrect. Please, try another.')
      do_exit = 1
  # Check PATH setting
  if settings['path'] == '':
    print('Please, set target directory or file path.')
    do_exit = 1
  else:
    if path.exists(settings['path']):
      if path.isdir(settings['path']):
        settings['dir'] = True
      else:
        settings['file'] = True
    else:
      print('Target path doesn`t exist. Please, try another.')
      do_exit = 1
  # Stop because of errors
  if do_exit == 1:
    print CALL_HELP_MSG
    exit(1)

def update_file(filename, old_text, new_text):
  # inplace argument is needed for backuping
  for line in fileinput.input(filename, inplace=1):
    sys.stdout.write(line.replace(old_text, new_text))

def work_with_file(file_path, old_text, new_text):
  # chmod
  update_file(file_path, old_text, new_text)

def work_with_dir(dir_path, old_text, new_text):
  p = walk(dir_path)
  for root, dirs, files in p:
    for file in files:
      # chmod
      update_file(file, old_text, new_text)

def run_main(argv):
  settings = dict()

  # Initial settings
  settings['dir']  = False
  settings['file'] = False
  settings['path'] = ''
  settings['old_text'] = ''
  settings['old_text_path'] = ''
  settings['new_text'] = ''
  settings['new_text_path'] = ''

  settings = receive_settings(argv, settings)
  print('Pre check_settings: %s') % (settings)
  check_settings(settings)
  print('Post check_settings: %s') % (settings)

  if settings['dir']:
    work_with_dir(settings['path'], settings['old_text'], settings['new_text'])
  if settings['file']:
    work_with_file(settings['path'], settings['old_text'], settings['new_text'])

def main(args):
  run_main(args)

if __name__ == '__main__':
  main(argv[1:])

