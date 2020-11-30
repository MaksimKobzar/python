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

import getopt
from sys import argv, exit
from os import path, walk, getcwd, remove, chmod
from smc_func import filter_extension as fe
from smc_func import smart_walk

# Constants
SCRIPT_FILENAME = path.basename(__file__)
ST_COMMENTED = '/*'
FN_COMMENTED = '*/'
COMMENTED_LINE = '//'


def take_from_n_to_fn(small, big):
    if small in big:
        return big[big.index(small) + len(small):]
    return big


def take_from_n_to_st(small, big):
    if small in big:
        return big[:big.index(small)]
    return big


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
        print('[Error] Target path should be set.')
        do_exit = 1
    elif path.exists(settings['path']):
        if path.isdir(settings['path']):
            settings['dir_not_file'] = True
    else:
        print('[Error] Target path is not valid.')
        do_exit = 1
    if do_exit == 1:
        print('For more information call: ./%s -h' % SCRIPT_FILENAME)
        exit(1)


def valid_line(line):
    line = line.strip()
    # Not empty and not commented
    if line != '' and line != '\n':
        # print('DBG: line \'%s\' is valid' % line)
        return True
    return False


def line_has_text(line, text):
    if text in line:
        return True
    else:
        return False


def last_valid_line_has_text(lines, text):
    in_commented_zone = 0
    # print('DBG: last_valid_line_has_text() is started')
    # go through lines in reversed order:
    for idx in range(len(lines) - 1, 0, -1):
        t = lines[idx].strip()
        if in_commented_zone:
            if ST_COMMENTED in t:
                # print('DBG: Extract NOT commented part %s -> %s' % (t, take_from_n_to_st(ST_COMMENTED, t)))
                t = take_from_n_to_st(ST_COMMENTED, t)
                in_commented_zone = 0
            else:
                t = ''
        else:
            if FN_COMMENTED in t:
                # print('DBG: Extract NOT commented part %s -> %s' % (t, take_from_n_to_fn(FN_COMMENTED, t)))
                t = take_from_n_to_fn(FN_COMMENTED, t)
                in_commented_zone = 1
            if COMMENTED_LINE in t:
                # print('DBG: Extract NOT commented part %s -> %s' % (t, take_from_n_to_st(COMMENTED_LINE, t)))
                t = take_from_n_to_st(COMMENTED_LINE, t)
        if valid_line(t) and text in t:
            return True
    return False


def insert_guards(file, lines, line_idx, settings):
    guards = 'INC_' + path.basename(file.name).upper().replace('.', '_')
    lines.insert(line_idx, '\n' + '`ifndef ' + guards + '\n' + '`define ' + guards + '\n' + '\n')
    lines.append('\n' + '`endif // !' + guards + '\n')
    file.seek(0)  # go to the start of the file
    file.writelines(lines)


def get_tag_from_line(line, before_tag):
    frm_line = take_from_n_to_st(COMMENTED_LINE, line)
    frm_line = take_from_n_to_st(ST_COMMENTED, frm_line)
    frm_line = take_from_n_to_fn(FN_COMMENTED, frm_line)
    frm_line = frm_line.strip().split()
    # print('DBG: before_tag %s, line_splits %s' % (before_tag, frm_line))
    if before_tag == frm_line[0]:
        return frm_line[1]
    # print('DBG: get_tag_from_line -1')
    return -1


def has_sv_guards(lines, idx1, idx2):
    return (
            last_valid_line_has_text(lines, '`endif') and
            get_tag_from_line(lines[idx1], '`ifndef') != -1 and
            get_tag_from_line(lines[idx1], '`ifndef') == get_tag_from_line(lines[idx2], '`define')

    )


def count_guard_keywords(lines):
    ifdef_n = 0
    ifndef_n = 0
    endf_n = 0
    in_commented_zone = 0
    for idx in range(len(lines)):
        t = lines[idx].strip()
        if in_commented_zone:
            if FN_COMMENTED in t:
                t = take_from_n_to_fn(FN_COMMENTED, t)
                in_commented_zone = 0
            else:
                t = ''
        else:
            if COMMENTED_LINE in t:
                t = take_from_n_to_st(COMMENTED_LINE, t)
            if ST_COMMENTED in t:
                t = take_from_n_to_st(ST_COMMENTED, t)
                in_commented_zone = 1
        if valid_line(t):
            if '`ifdef' in t: ifdef_n += 1
            if '`ifndef' in t: ifndef_n += 1
            if '`endif' in t: endf_n += 1
    return ifdef_n, ifndef_n, endf_n


def process_file(filepath, settings):
    open_mod = 'r' if settings['no_change'] else 'r+'
    # print('DBG: open_mod:', open_mod)
    with open(filepath, open_mod) as f:
        lines = f.readlines()

        first_valid_line_found = 0
        first_valid_line_idx = 0
        in_commented_zone = 0

        for idx in range(len(lines)):
            t = lines[idx].strip()
            if in_commented_zone:
                if FN_COMMENTED in t:
                    # print('DBG: Extract NOT commented part %s -> %s' % (t, take_from_n_to_fn(FN_COMMENTED, t)))
                    t = take_from_n_to_fn(FN_COMMENTED, t)
                    in_commented_zone = 0
                else:
                    t = ''
            else:
                if COMMENTED_LINE in t:
                    # print('DBG: Extract NOT commented part %s -> %s' % (t, take_from_n_to_st(COMMENTED_LINE, t)))
                    t = take_from_n_to_st(COMMENTED_LINE, t)
                if ST_COMMENTED in t:
                    # print('DBG: Extract NOT commented part %s -> %s' % (t, take_from_n_to_st(ST_COMMENTED, t)))
                    t = take_from_n_to_st(ST_COMMENTED, t)
                    in_commented_zone = 1
            if valid_line(t):
                if first_valid_line_found == 0:
                    first_valid_line_found = 1
                    first_valid_line_idx = idx
                else:
                    # print('DBG: idx1 %0d, idx2 %0d' % (first_valid_line_idx, idx))
                    if has_sv_guards(lines, first_valid_line_idx, idx):  # Has SV_GUARD
                        if not settings['silent']:
                            print('SV_GUARDs are already in the file: %s' % filepath)
                    else:  # No SV_GUARD
                        if not settings['silent'] or settings['no_change']:
                            print('SV_GUARDs are missing for file: %s' % filepath)
                            ifdef_n, ifndef_n, endf_n = count_guard_keywords(lines)
                            if (ifdef_n + ifndef_n) != endf_n:
                                print('This file needs more attention: `ifdef - %d, `ifndef - %d, `endif - %d' %
                                      (ifdef_n, ifndef_n, endf_n))
                        if not settings['no_change']:
                            insert_guards(f, lines, first_valid_line_idx, settings)
                            print('SV_GUARDs have been added for file: %s' % filepath)
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
    # print('DBG: setting', settings)

    # Analyze files
    smart_walk(settings, process_file, ['v', 'sv', 'svh'])


def main(args):
    run_main(args)


if __name__ == '__main__':
    main(argv[1:])
