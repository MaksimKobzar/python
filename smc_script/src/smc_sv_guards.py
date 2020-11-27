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
        print('For more information call: ./%s -h' % SCRIPT_FILENAME)
        exit(1)
    # Go through the arguments
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: ./%s -t <path> [-n -s]' % SCRIPT_FILENAME)
            print('-t : set target as directory or file path')
            print('-n : to enable "no change" mode, so missed guards will be reported but will not be injected')
            print('-s : to enable "silent" mode, this argument is ignored in case of "no change" mode')
            print("Example: ./%s -t path -n" % SCRIPT_FILENAME)
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
        print('For more information call: ./%s -h' % SCRIPT_FILENAME)
        exit(1)


def valid_line(commented, idx, line):
    line = line.strip()
    # Not empty and not commented
    if idx not in commented and line != '' and line != '\n':
        print('DBG: line %0s is valid' % line)
        return True
    return False


def line_has_text(line, text):
    if text in line:
        return True
    else:
        return False


def last_valid_line_has_text(commented, lines, text):
    # for line in reversed(lines):
    print('last_valid_line_has_text')
    for idx in range(len(lines)-1, 0, -1):
        if valid_line(commented, idx, lines[idx]):
            if line_has_text(lines[idx], text):
                return True
            break
    return False


def insert_guards(file, lines, line_idx, settings):
    guards = 'INC_' + path.basename(file.name).upper().replace('.', '_')
    lines.insert(line_idx, '\n' + '`ifndef ' + guards + '\n' + '`define ' + guards + '\n' + '\n')
    lines.append('\n' + '`endif // !' + guards + '\n')
    file.seek(0)  # go to the start of the file
    file.writelines(lines)


def get_tag_from_line(line, before_tag):
    line_splits = line.strip().split()
    print('DBG: before_tag %s, line_splits %s' % (before_tag, line_splits))
    if before_tag in line_splits[0]:
        return line_splits[1]
    print('return -1')
    return -1
    # st_idx = line.find(before_tag)
    # line = line[st_idx:]


def has_sv_guards(commented, lines, idx1, idx2):
    return (
            # line_has_text(lines[idx1], '`ifndef ') and
            # line_has_text(lines[idx2], '`define ') and
            last_valid_line_has_text(commented, lines, '`endif') and
            get_tag_from_line(lines[idx1], '`ifndef ') != -1 and
            get_tag_from_line(lines[idx1], '`ifndef ') == get_tag_from_line(lines[idx2], '`define ')

    )


def get_commented_lines(lines):
    in_commented_zone = 0
    commented = list()
    for idx in range(len(lines)):
        t = lines[idx].strip()
        if in_commented_zone:
            commented.append(idx)
            if t[-2:] == '*/':
                in_commented_zone = 0
        elif t[:2] == '//':
            commented.append(idx)
        elif t[:2] == '/*':
            commented.append(idx)
            in_commented_zone = 1
    print('commented_lines', commented)
    return commented


def process_file(filepath, settings):
    open_mod = 'r' if settings['no_change'] else 'r+'
    # print('DBG: open_mod:', open_mod)
    with open(filepath, open_mod) as f:
        lines = f.readlines()

        commented = get_commented_lines(lines)

        first_valid_line_found = 0
        first_valid_line_idx = 0
        for idx in range(len(lines)):
            if valid_line(commented, idx, lines[idx]):
                if first_valid_line_found == 0:
                    first_valid_line_found = 1
                    first_valid_line_idx = idx
                else:
                    print('idx1 %0d idx2 %0d' % (first_valid_line_idx, idx))
                    if has_sv_guards(commented, lines, first_valid_line_idx, idx):  # Has SV_GUARD
                        if not settings['silent']:
                            print('SV_GUARDS are already in the file: %s' % filepath)
                    else:  # No SV_GUARD
                        if not settings['silent'] or settings['no_change']:
                            print('There is no SV_GUARDS for file: %s' % filepath)
                        if not settings['no_change']:
                            insert_guards(f, lines, idx, settings)
                            print('SV_GUARDS have been added for file: %s' % filepath)
                    # stop iterations after the 2nd valid line
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
    print('setting:', settings)

    # Analyze files
    if settings['dir_not_file']:  # Directory
        p = walk(settings['path'])
        for root, dirs, files in p:
            for file in files:
                print('file:', file)
                if fe(file, ['v', 'sv', 'svh']):
                    print('DBG: find .v/.sv/.svh')
                    process_file(path.join(root, file), settings)
    else:  # File
        process_file(settings['path'], settings)


def main(args):
    run_main(args)


if __name__ == '__main__':
    main(argv[1:])
