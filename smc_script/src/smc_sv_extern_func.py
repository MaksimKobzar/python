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

import getopt
from sys import argv, exit
from os import path, walk, getcwd, remove, chmod
from smc_func import filter_extension as fe
from smc_func import smart_walk


from smc_func import without


def get_settings(args, settings):
    pass


def check_settings(settings):
    pass


def parse_sv_file(file):
    # text = file.read()
    sv_info = [
        {
            'class_name': 'smc_llc_env_cfg',
            'class_start': 2,
            'class_end': 29,
            'methods': [
                {
                    'method_name': 'new',
                    'method_type': 'function',
                    'method_extern': False,
                    'method_def_line': 19,
                    'method_imp_start_line': 19,
                    'method_imp_end_line': 21,
                    'method_keywords': []
                },
                {
                    'method_name': 'build',
                    'method_type': 'function',
                    'method_extern': False,
                    'method_def_line': 23,
                    'method_imp_start_line': 23,
                    'method_imp_end_line': 27,
                    'method_keywords': ['virtual']
                }
            ]
        }
    ]
    return sv_info


def inject_extern(s):
    non_space_char_idx = len(s) - len(s.lstrip()) - 1
    print('DBG: inject_extern before - {%s} after - {%s}' % (s, s[:non_space_char_idx] + 'extern ' + s.rstrip()[non_space_char_idx:]))
    return s[:non_space_char_idx] + 'extern ' + s.rstrip()[non_space_char_idx+1:] + '\n'


def process_file(filepath, settings):
    with open(filepath, 'r+') as f:
        correction = 0
        remove_indices = []

        sv_info = parse_sv_file(f)
        lines = f.readlines()
        methods = sv_info[0]['methods']
        print('DBG: methods %s' % methods)
        print('DBG: lines was %s' % lines)
        for method in methods:
            if not method['method_extern']:
                line_with_def = method['method_imp_start_line'] - 1  # DONT NEED?! - correction
                lines[line_with_def] = inject_extern(lines[line_with_def])
                lines_in_method_imp = method['method_imp_end_line'] - method['method_imp_start_line']
                remove_indices += range(line_with_def + 1, line_with_def + 1 + lines_in_method_imp)
                correction += lines_in_method_imp
            print('DBG: print vars after iter - {remove_indices %s, correction %s}' % (remove_indices, correction))
        print('DBG: print remove_indices before without call - {%s}' % remove_indices)
        lines = list(without(lines, remove_indices=remove_indices))
        print('DBG: lines became %s' % lines)
        f.seek(0)  # go to the start of the file
        f.writelines(lines)

def run_main(args):
    settings = dict()

    # Initial settings
    settings['path'] = 'test/class.sv'  # path
    settings['dir_not_file'] = False  # True - work with directory, False - work with file
    settings['silent'] = False
    settings['external_or_internal'] = True  # True - external, False - internal

    get_settings(args, settings)
    check_settings(settings)

    smart_walk(settings, process_file, ['v', 'sv', 'svh'])
    # # Analyze files
    # if settings['dir_not_file']:  # Directory
    #     p = walk(settings['path'])
    #     for root, dirs, files in p:
    #         for file in files:
    #             if fe(file, ['v', 'sv', 'svh']):
    #                 process_file(path.join(root, file), settings)
    # else:  # File
    #     process_file(settings['path'], settings)


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
