#!/usr/bin/env python3

"""

ALGORITHM:
    * open file
    * go through lines one by one
    * find VALID lines (VALID lines that are not empty and that are not commented)
    * IF
        the 1st  VALID line starts with `ifndef
        the 2nd  VALID line starts with `define
        the last VALID line starts with `endif
       => it`s OKAY
    * ELSE
       => file doesn't have GUARDS, they can be injected

"""

# TODO:
# * chmod of files
# * filter lines from this /* comments */

import getopt
from sys import argv, exit
from os import path, walk, getcwd, remove, chmod
from smc_func import filter_extension as fe

# Constants
SCRIPT_FILENAME = path.basename(__file__)


def receive_settings(args, settings):
    try:
        opts, args = getopt.getopt(args, 'ht:ns')
    except getopt.GetoptError as err:
        print(str(err))
        print('For more information call: ./%s -h') % SCRIPT_FILENAME
        exit(1)
    # Go through the arguments
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: ./%s -t <path> [-n -s]') % SCRIPT_FILENAME
            print('-t : set target as directory or file path')
            print('-n : to enable "no change" mode, so missed guards will be reported but will not be injected')
            print('-s : to enable "silent" mode, this argument is ignored in case of "no change" mode')
            print("Example: ./%s -t path -n") % SCRIPT_FILENAME
            exit()
        elif opt == '-t':
            settings['path'] = arg
        elif opt == '-n':
            settings['no_change'] = True
        elif opt == '-s':
            settings['silent'] = True
    # Return filled settings
    return settings


def check_settings(settings):
    do_exit = 0
    if settings['path'] == '':
        print('Target path should be set.')
        do_exit = 1
    elif path.exists(settings['path']):
        if path.isdir(settings['path']):
            settings['dir_not_file'] = True
    else:
        print('Target path is not valid.')
        do_exit = 1
    if do_exit == 1:
        print('For more information call: ./%s -h' % (SCRIPT_FILENAME))
        exit(1)


def valid_line(line):
    line = line.strip()
    # Not empty and not commented
    if line != '' and line != '\n' and line[:2] != '//':
        return True
    return False


def line_has_text(line, text):
    if text in line:
        return True
    else:
        return False


def last_valid_line_has_text(lines, text):
    for line in reversed(lines):
        if valid_line(line):
            if line_has_text(line, text):
                return True
            break
    return False


def insert_guards(file, lines, line_idx, settings):
    guards = 'INC_' + path.basename(file.name).upper().replace('.', '_')
    lines.insert(line_idx, '\n' + '`ifndef ' + guards + '\n' + '`define ' + guards + '\n' + '\n')
    lines.append('\n' + '`endif // !' + guards + '\n')
    file.seek(0)  # go to the start of the file
    file.writelines(lines)


def process_file(filepath, settings):
    open_mod = 'r' if settings['no_change'] else 'r+'
    with open(filepath, open_mod) as f:
        lines = f.readlines()
        for idx in range(len(lines)):
            if valid_line(lines[idx]):
                if (
                        valid_line(lines[idx + 1]) and
                        line_has_text(lines[idx], '`ifndef ') and
                        line_has_text(lines[idx + 1], '`define ') and
                        last_valid_line_has_text(lines, '`endif')
                ):  # Has SV_GUARD
                    if not settings['silent']:
                        print('SV_GUARDS are already in the file: %s') % filepath
                else:  # No SV_GUARD
                    if not settings['silent'] or settings['no_change']:
                        print('There is no SV_GUARDS for file: %s') % filepath
                    if not settings['no_change']:
                        insert_guards(f, lines, idx, settings)
                        print('SV_GUARDS have been added for file: %s') % filepath
                # stop iterations after the 1st valid line
                break


def run_main(args):
    settings = dict()

    # Initial settings
    settings['path'] = ''  # path
    settings['dir_not_file'] = False  # True - work with directory, False - work with file
    settings['no_change'] = False  # no file changing
    settings['silent'] = False  # no prints

    # Setting are received and checked
    settings = receive_settings(args, settings)
    check_settings(settings)

    # Analyze files
    if settings['dir_not_file']:  # Directory
        p = walk(settings['path'])
        for root, dirs, files in p:
            for file in files:
                if fe(file, ['v', 'sv', 'svh']):
                    process_file(path.join(root, file), settings)
    else:  # File
        process_file(settings['path'], settings)


def main(args):
    run_main(args)


if __name__ == '__main__':
    main(argv[1:])

