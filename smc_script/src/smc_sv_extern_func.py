#!/usr/bin/env python3

"""

ALGORITHM for internal -> external:
    1 Read file to old_lines
    2 Copy old_lines -> new_lines
    3 Add 'extern' keyword for every method in new_lines
    4 Collect all line indices to remove in new_lines
    5 Remove all excess lines from new_lines
    6 Add after each class corresponding methods from old_lines to new_lines:
        * after class_1 copy all methods' implementation from old_lines
        * after class_2 copy all methods' implementation from old_lines
    7 Write new_lines to file

TESTS:
    * example_int_simple +
    * example_int_complex
    * example_int_multi_class
    * example_int_mixed
    * example_ext_base
    * example_int_ext_mix

"""

# TODO:

import getopt
from sys import argv, exit
from os import path, walk, getcwd, remove, chmod
from smc_func import filter_extension as fe
from smc_func import smart_walk
from smc_func import without
from smc_func import without_s


def get_settings(args, settings):
    pass


def inject_class_scope(s, class_name):
    if '(' not in s:
        print('[Error] Method definition doesn\'t contain symbol \'(\': %s ', s)
    if 'extern ' in s:
        s = without_s(s, 'extern ')
    split = s.split('(')
    split[0] = split[0].strip()
    idx = split[0].rfind(' ')
    return split[0][:idx] + ' ' + class_name + '::' + split[0][idx + 1:] + '(' + split[1]


def check_settings(settings):
    pass


def parse_sv_file(file):
    # sv_info = get_sv_info(file.read())
    '''
    sv_info = [  # example_int_simple
        {
            'name': 'hsr_eth_dm_seq',
            'st_line': 10,
            'fn_line': 30,
            'methods': [
                {
                    'type': 'function',
                    'extern': False,
                    'def_st_line': 16,
                    'def_fn_line': 16,
                    'imp_st_line': 17,
                    'imp_fn_line': 19
                },
                {
                    'type': 'task',
                    'extern': False,
                    'def_st_line': 20,
                    'def_fn_line': 23,
                    'imp_st_line': 24,
                    'imp_fn_line': 29
                }
            ]
        }
    ]
    '''
    sv_info = [  # example_int_complex
        {
            'name': 'hsr_eth_dm_seq',
            'st_line': 10,
            'fn_line': 52,
            'methods': [
                {
                    'type': 'function',
                    'extern': False,
                    'def_st_line': 17,
                    'def_fn_line': 17,
                    'imp_st_line': 18,
                    'imp_fn_line': 20
                },
                {
                    'type': 'task',
                    'extern': False,
                    'def_st_line': 22,
                    'def_fn_line': 25,
                    'imp_st_line': 26,
                    'imp_fn_line': 31
                },
                {
                    'type': 'function',
                    'extern': False,
                    'def_st_line': 33,
                    'def_fn_line': 33,
                    'imp_st_line': 34,
                    'imp_fn_line': 34
                },
                {
                    'type': 'task',
                    'extern': False,
                    'def_st_line': 35,
                    'def_fn_line': 35,
                    'imp_st_line': 36,
                    'imp_fn_line': 37
                },
                {
                    'type': 'function',
                    'extern': False,
                    'def_st_line': 39,
                    'def_fn_line': 49,
                    'imp_st_line': 41,
                    'imp_fn_line': 51
                }
            ]
        }
    ]
    '''
    sv_info = [ # example_ext_base
        {
            'name': 'hsr_eth_dm_seq',
            'st_line': 9,
            'fn_line': 24,
            'methods': [
                {
                    'type': 'function',
                    'extern': True,
                    'def_st_line': 16,
                    'def_fn_line': 18,
                    'imp_st_line': 28,
                    'imp_fn_line': 31
                },
                {
                    'type': 'task',
                    'extern': True,
                    'def_st_line': 19,
                    'def_fn_line': 19,
                    'imp_st_line': 33,
                    'imp_fn_line': 38
                },
                {
                    'type': 'function',
                    'extern': True,
                    'def_st_line': 22,
                    'def_fn_line': 24,
                    'imp_st_line': 40,
                    'imp_fn_line': 53
                }
            ]
        }
    ]
    '''
    return sv_info


def inject_extern(s):
    first_char_idx = len(s) - len(s.lstrip())
    return s[:first_char_idx] + 'extern ' + s.rstrip()[first_char_idx:] + '\n'


def fill_indices_to_remove(settings, lines, st_idx, fn_idx, remove_indices):
    # Clean class body from methods' implementation
    opt = 1 if settings['delete_spaces_between_externals'] and lines[fn_idx].isspace() else 0
    # Form list of removed indexes
    remove_indices += range(st_idx, fn_idx + opt)
    print('DBG: fill_indices_to_remove {%s}' % remove_indices)

def process_file(filepath, settings):
    with open(filepath, 'r+') as f:
        # 1. get necessary info
        old_lines = f.readlines()
        f.seek(0)  # go to the start of the file
        sv_info = parse_sv_file(f)
        # 2. copy old_lines -> new_lines
        new_lines = old_lines[:]
        remove_indices = []

        # cls is class, class is keyword
        for cls in sv_info:
            methods = cls['methods']
            for method in methods:
                if not method['extern'] and settings['external_or_internal']:
                    # 3. Add 'extern' keyword for all internal methods
                    new_lines[method['def_st_line']] = inject_extern(old_lines[method['def_st_line']])
                    # 4. Form list of indices to remove
                    fill_indices_to_remove(settings, old_lines, method['imp_st_line'], method['imp_fn_line'] + 1, remove_indices)
                # elif method['extern'] and not settings['external_or_internal']:
            cls['fn_line'] -= len(remove_indices)

        # 5. Remove lines with corresponding indexes
        # print('DBG: print remove_indices before without() call - {%s}' % remove_indices)
        new_lines = list(without(new_lines, remove_indices=remove_indices))

        # cls is class, class is keyword
        for cls in sv_info:
            methods_imp_st_line = cls['fn_line'] + 1
            methods = cls['methods']
            for method in methods:
                if not method['extern'] and settings['external_or_internal']:
                    # 6. Copy methods' implementation from old_lines to new_lines after each class
                    method_line_num = method['imp_fn_line'] + 1 + 1 - method['def_st_line']
                    for i in range(method_line_num):
                        if i == 0:
                            new_line = '\n'
                        else:
                            s = old_lines[method['def_st_line'] + i - 1]
                            if i == 1:  # method definition start line
                                new_line = inject_class_scope(s, cls['name'])
                            else:
                                # if s[:settings['spaces']] == (settings['spaces'] * ' '):
                                if i == (method_line_num - 1):  # not last
                                    s = s.lstrip()
                                    # print('DBG: truncate space in the start of the line: %s -> %s' % (s, s[settings['spaces']:]))
                                    # s = s[settings['spaces']:]
                                new_line = s
                        new_lines.insert(methods_imp_st_line, new_line)
                        methods_imp_st_line += 1
                # elif method['extern'] and not settings['external_or_internal']:

        # 7. Write all new_lines to file
        f.writelines(new_lines)
        f.truncate()


def run_main(args):
    settings = dict()

    # Initial settings
    settings['path'] = 'D:\\projects\\py\\git_python\\smc_script\\test\\test_sv_extern_func\\example_int_complex.sv'
    settings['dir_not_file'] = False  # True - work with directory, False - work with file
    settings['silent'] = False
    settings['external_or_internal'] = True  # True - make external, False - make internal
    settings['spaces'] = 2
    settings['delete_spaces_between_externals'] = True

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
