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
from smc_func import without_s


def get_settings(args, settings):
    pass


def inject_class_scope(s, class_name):
    if '(' not in s:
        print('[Error] Method definition doesn\'t contain symbol \'(\': %s ', s)
    s = without_s(s, 'extern ')
    split = s.split('(')
    split[0] = split[0].strip()
    idx = split[0].rfind(' ')
    return split[0][:idx] + ' ' + class_name + '::' + split[0][idx+1:] + '(' + split[1]


def check_settings(settings):
    pass


def parse_sv_file(file):
    # text = file.read()

    # External
    '''
    sv_info = [
        {
            'name': 'hsr_eth_dm_seq',
            'st_line': 9,
            'fn_line': 44,
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
                    'def_st_line': 21,
                    'def_fn_line': 24,
                    'imp_st_line': 25,
                    'imp_fn_line': 29
                },
                {
                    'type': 'function',
                    'extern': False,
                    'def_st_line': 31,
                    'def_fn_line': 32,
                    'imp_st_line': 33,
                    'imp_fn_line': 43
                }
            ]
        }
    ]
    '''
    sv_info = [
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
    return sv_info


def inject_extern(s):
    first_char_idx = len(s) - len(s.lstrip())
    return s[:first_char_idx] + 'extern ' + s.rstrip()[first_char_idx:] + '\n'


def process_file(filepath, settings):
    with open(filepath, 'r+') as f:
        correction = 0
        where_was_stop = 0

        # Get necessary info
        lines = f.readlines()
        f.seek(0)  # go to the start of the file
        sv_info = parse_sv_file(f)

        # cls is class, class is keyword
        for cls in sv_info:
            remove_indices = []
            methods = cls['methods']
            for method in methods:
                if not method['extern'] and settings['external_or_internal']:
                    # Add 'extern' keyword for all internal methods
                    lines[method['def_st_line']] = inject_extern(lines[method['def_st_line']])
                    # Clean class body
                    opt = 1 if settings['delete_spaces_between_externals'] is True and lines[method['imp_fn_line'] + 1] == '\n' else 0
                    remove_indices += range(
                        method['imp_st_line'],
                        method['imp_fn_line'] + 1 + opt
                    )
                    correction = len(remove_indices)
                elif method['extern'] and not settings['external_or_internal']:
                    # Sub 'extern' keyword for all internal methods
                    lines[method['def_st_line']] = without_s(lines[method['def_st_line']], 'extern ')
                    # Clean method definition beside 1st line
                    method['def_st_line'] -= correction
                    method['def_fn_line'] -= correction
                    remove_indices += range(
                        method['def_st_line'] + 1,
                        method['def_fn_line'] + 1
                    )
                    correction += method['def_fn_line'] - method['def_st_line']
                    # Clean method implementations
                    opt = 1 if settings['delete_spaces_between_externals'] is True and lines[method['imp_fn_line'] + 1] == '\n' else 0
                    remove_indices += range(
                        method['imp_st_line'],
                        method['imp_fn_line'] + 1 + opt
                    )
            print('DBG: print remove_indices before without call - {%s}' % remove_indices)
            new_lines = list(without(lines[where_was_stop:cls['fn_line']+1], remove_indices=remove_indices))
            where_was_stop = cls['fn_line']
            cls['fn_line'] -= correction

            new_lines.insert(cls['fn_line']+1, '\n')
            methods_imp_st_line = cls['fn_line'] + 2
            print('methods_imp_st_line', methods_imp_st_line)
            print('----------------------------------------------------------------------')
            print('DBG: sv_info', sv_info)
            print('----------------------------------------------------------------------')

            # Inject method's bodies in the end
            for method in methods:
                if not method['extern'] and settings['external_or_internal']:
                    method_line_num = method['imp_fn_line'] + 1 + 1 - method['def_st_line']
                    for i in range(method_line_num):
                        print('DBG: new_lines[%0s] = lines[%0s] = %s' % (
                            methods_imp_st_line + i,
                            method['def_st_line'] + i - 1,
                            lines[method['def_st_line'] + i - 1]
                        ))
                        if i == 0:
                            new_line = '\n'
                        else:
                            s = lines[method['def_st_line'] + i - 1]
                            if i == 1:  # method definition start line
                                new_line = inject_class_scope(s, cls['name'])
                            else:
                                if s[:settings['spaces']] == (settings['spaces'] * ' '):
                                    print('DBG: truncate space in the start of the line: %s -> %s' % (s, s[settings['spaces']:]))
                                    s = s[settings['spaces']:]
                                new_line = s
                        new_lines.insert(methods_imp_st_line + i, new_line)
                    methods_imp_st_line += method_line_num
                elif method['extern'] and not settings['external_or_internal']:
                    method_line_num = method['imp_fn_line'] - method['def_st_line']
                    methods_imp_st_line = method['def_st_line'] + 1
                    for i in range(method_line_num):
                        new_line = (settings['spaces'] * ' ') + lines[method['def_st_line'] + 1 + i]
                        print('DBG: new_lines[%0s] = lines[%0s] = %s' % (
                            methods_imp_st_line + i,
                            method['def_st_line'] + 1 + i,
                            new_line
                        ))
                        new_lines.insert(methods_imp_st_line + i, new_line)

            # Write new_lines to file
            print('DBG: class \'%s\'\nlines \n{%s}\nnew_lines \n{%s}' % (cls['name'], lines, new_lines))
            f.writelines(new_lines)
        f.writelines(lines[where_was_stop+1:])
        f.truncate()


def run_main(args):
    settings = dict()

    # Initial settings
    settings['path'] = 'D:\\projects\\py\\git_python\\smc_script\\test\\test_sv_extern_func\\example_ext.sv'  # path
    settings['dir_not_file'] = False  # True - work with directory, False - work with file
    settings['silent'] = False
    settings['external_or_internal'] = False  # True - external, False - internal
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
