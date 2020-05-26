#!/usr/bin/env python3


import getopt
from sys import argv, exit
from os import path, walk, getcwd, makedirs

# Constants
SCRIPT_FILENAME = path.basename(__file__)
SCRIPT_FILEPATH = path.dirname(__file__)
SCRIPT_FULLPATH = SCRIPT_FILEPATH + '/' + SCRIPT_FILENAME

def receive_settings(args, settings_abc):
  global opts
  try:
    opts, args = getopt.getopt(args, "ht:n:s")
  except getopt.GetoptError as err:
    print str(err)
    print('For more information call: ./%s -h') % SCRIPT_FILENAME
    exit(1)

  # go throw the arguments one by one
  for opt_key, arg in opts:
    if opt_key == '-h':
        print('Usage: %s [-t <path> -n <name> -s]') % SCRIPT_FILENAME
        print('-t : set target as directory path, as default where script is run from')
        print('-n : to set name of the table')
        print('-s : to enable "silent" mode')
        print('Example: %s -t path') % SCRIPT_FULLPATH
      exit()
    elif opt_key == '-t':
      settings_abc['path'] = arg if path.isabs(arg) else path.abspath(arg)
    elif opt_key == '-n':
      settings_abc['name'] = arg
    elif opt == '-s':
      settings_abc['silent'] = True

def check_settings(settings):
  do_exit = 0
  # check that path which is typed throw the terminal is existed
  # if not, script can create it or ask to type new path
  if not path.exists(settings['path']):
    ans = ""
    print("Path doesn`t exist: %s\nCreate: y/n?") % (settings['path'])
    while True:
      ans = raw_input()
      if ans in ["y", "n"]: break;
      print("Please, type correct answer.")
    if ans == "y":
      makedirs(settings['path'])
      if settings['silent'] == False:
        print("Path is created: %s") % (settings['path'])
    else:
      print("Please, change target path to run successfully!")
      do_exit = 1
  if do_exit == 1:
    print('For more information call: %s -h') %(SCRIPT_FULLPATH)
    exit(1)

def create_table(settings):
  # Create and fill the table
  temp = path.normpath(settings['path'] + '/' + settings['name'])
  with open(temp , 'w+') as table:
    table.write('----------------------------------------------------------------------------------------------------------------------------------------------------------|\n')
    table.write('- ARG NAME                | YOUR CHOICE                          | POSSIBLE VALUES, EXAMPLES           | COMMENTS                                         |\n')
    table.write('----------------------------------------------------------------------------------------------------------------------------------------------------------|\n')
    table.write('| author_name             | Maksim Kobzar (maksim.kobzar@sk.com) | -                                   | It affect some Makefile configurations           |\n')
    table.write('| uvm_version             | uvm1.2                               | uvm1.2, uvm1.1d                     |                                                  |\n')
    table.write('| tb_tag                  | smc_llc                              | smc_rm                              |                                                  |\n')
    table.write('| script_project_dir_path | $(CDVE_PATH)/script/project/Atomos   | $(CDVE_PATH)/script/project/AtomosC |                                                  |\n')
    table.write('| ip_dir_path             | $(PROJ)/design/llc                   | $(PROJ)/design/rm                   |                                                  |\n')
    table.write('| dut_filelist_name       | llc_wrapper_dut                      | rm_dut                              |                                                  |\n')
    table.write('| dut_toplevel_name       | llc_wrapper.f                        | rm_top.f                            |                                                  |\n')
    table.write('| has_reg_model           | y                                    | y, n                                |                                                  |\n')
    table.write('| reg_model_class_name    | csr_block_llc                        | csr_rm_block_reg                    | If has reg_model                                 |\n')
    table.write('| uvm_reg_addr_width      | 32                                   | 1-128                               | If has reg_model                                 |\n')
    table.write('| uvm_reg_data_width      | 32                                   | 1-8196                              | If has reg_model                                 |\n')
    table.write('| submit_run_dir          | y                                    | y, n                                |                                                  |\n')
    table.write('| mini_run_dir            | y                                    | y, n                                |                                                  |\n')
    table.write('| nightly_run_dir         | y                                    | y, n                                |                                                  |\n')
    table.write('| cdve_comps              | n                                    | y, n                                | If "y" is set it will be left some special marks |\n')
    table.write('----------------------------------------------------------------------------------------------------------------------------------------------------------|\n')
  # Script has finished successfully
  if not settings['silent']:
    print("Table %s is created in directory %s") % (settings['name'], settings['path'])

def run_main(args):
  settings = dict()

  # Initial settings
  settings['path'] = getcwd()
  settings['name'] = 'smc_gen_tb_table.dat'
  settings['silent'] = False

  receive_settings(args, settings)
  check_settings(settings)
  create_table(settings)

def main(args):
  run_main(args)


if __name__ == "__main__":
  main(argv[1:])