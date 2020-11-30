#!/usr/bin/env python3

"""

ALGORITHM:
    *

"""

# TODO:

import getopt
from sys import argv, exit
from os import path, walk, getcwd, remove, chmod
from smc_func import filter_extension as fe
from smc_func import smart_walk
from smc_func import without


from smc_func import without


def get_settings(args, settings):
    pass


def check_settings(settings):
    pass


def parse_sv_file(file):
    # text = file.read()
    sv_info = [
        {
            'class_name': 'hsr_eth_dm_seq',
            'class_start': 9,
            'class_end': 41,
            'methods': [
                {
                    'method_name': 'new',
                    'method_type': 'function',
                    'method_extern': False,
                    'method_def_line': 16,
                    'method_imp_st_line': 16,
                    'method_imp_fn_line': 19,
                    'method_keywords': []
                },
                {
                    'method_name': 'pre_body',
                    'method_type': 'task',
                    'method_extern': False,
                    'method_def_line': 21,
                    'method_imp_st_line': 21,
                    'method_imp_fn_line': 26,
                    'method_keywords': []
                },
                {
                    'method_name': 'body',
                    'method_type': 'task',
                    'method_extern': False,
                    'method_def_line': 28,
                    'method_imp_st_line': 28,
                    'method_imp_fn_line': 39,
                    'method_keywords': ['virtual']
                }
            ]
        }
    ]
    return sv_info


def inject_extern(s):
    first_char_idx = len(s) - len(s.lstrip())
    return s[:first_char_idx] + 'extern ' + s.rstrip()[first_char_idx:] + '\n'

def inject_class_scope(method, class_name, func_args):
    start = ''
    if method['method_keywords']:
        start = ''.join(method['method_keywords']) + ' '
    return start +\
           ''.join(method['method_type']) + ' ' + class_name + '::' +\
           ''.join(method['method_name']) + '(' + func_args + ');\n'

def process_file(filepath, settings):
    with open(filepath, 'r+') as f:
        correction = 0
        remove_indices = []

        # Get necessary info
        lines = f.readlines()
        sv_info = parse_sv_file(f)
        methods = sv_info[0]['methods']

        for method in methods:
            if not method['method_extern']:
                # Add 'extern' keyword for all internal methods
                lines[method['method_def_line']] = inject_extern(lines[method['method_def_line']])
                # Clean class body
                remove_indices += range(method['method_imp_st_line'] + 1, method['method_imp_fn_line'] + 2)
        print('DBG: print remove_indices before without call - {%s}' % remove_indices)
        new_lines = list(without(lines, remove_indices=remove_indices))

        sv_info[0]['class_end'] -= len(remove_indices)
        line_idx_to_inject = sv_info[0]['class_end'] + 1
        # Inject method's bodies in the end
        for method in methods:
            if not method['method_extern']:
                method_line_num = method['method_imp_fn_line'] - method['method_imp_st_line'] + 1 + 1
                for i in range(method_line_num):
                    if i == 0:
                        new_line = '\n'
                    elif i == 1:
                        s = lines[method['method_imp_st_line'] + i - 1]
                        new_line = inject_class_scope(
                            method,
                            sv_info[0]['class_name'],
                            s[s.find('(') + len('('):s.rfind(')')]
                        )
                    else:
                        new_line = lines[method['method_imp_st_line'] + i - 1]
                    new_lines.insert(line_idx_to_inject + i, new_line)
                line_idx_to_inject += method_line_num

        print('DBG: lines \n{%s}\nnew_lines \n{%s}' % (lines, new_lines))
        f.seek(0)  # go to the start of the file
        f.writelines(new_lines)
        f.truncate()

def run_main(args):
    settings = dict()

    # Initial settings
    settings['path'] = 'D:\git\python\smc_script\\test\\test_sv_extern_func\example.sv'  # path
    settings['dir_not_file'] = False  # True - work with directory, False - work with file
    settings['silent'] = False
    settings['external_or_internal'] = True  # True - external, False - internal

    get_settings(args, settings)
    check_settings(settings)

    # Analyze files
    smart_walk(settings, process_file, ['v', 'sv', 'svh'])


def main(args):
    run_main(args)


if __name__ == "__main__":
    main(argv[1:])

"""

    sv_info = [
        {
            'class_name' : 'smc_env_cfg',
            'class_start' : 5,
            'class_end'   : 50,
            'methods' : [
                {
                    'method_name' : 'build_phase',
                    'method_type' : 'function',
                    'method_extern' : False,
                    'method_definition_line' : 27,
                    'method_implementation_start_line' : 27,
                    'method_implementation_end_line' : 43,
                    'method_keywords' : ['protected', 'virtual']
                },
                {
                    'method_name' : 'run_phase',
                    'method_type' : 'task',
                    'method_extern' : True,
                    'method_definition_line' : 55,
                    'method_implementation_start_line' : 129,
                    'method_implementation_end_line' : 178,
                    'method_keywords' : ['protected']
                }
            ]
        },
        {
            'class_name' : 'smc_env',
            ........................
        }
    ]

"""
