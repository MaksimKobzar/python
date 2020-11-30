#!/usr/bin/env python3

from os import path, walk


def filter_extension(file, extns=None):
    if extns is None:
        return True
    else:
        for extn in extns:
            # If last chars in file name is 'extension_name'
            if file[-len(extn):] == str(extn):
                return True
        return False


def without(iterable, remove_indices):
    # Returns an iterable for a collection or iterable,
    # which returns all items except the specified indices.
    # TODO
    if not hasattr(remove_indices, '__iter__'):
        remove_indices = {remove_indices}
    else:
        remove_indices = set(remove_indices)
    for k, item in enumerate(iterable):
        if k in remove_indices:
            continue
        yield item


def smart_walk(settings, func, extns=None):
    if settings['dir_not_file']:  # Directory
        p = walk(settings['path'])
        for root, dirs, files in p:
            for file in files:
                if filter_extension(file, extns):
                    func(path.join(root, file), settings)
    else:  # File
        func(settings['path'], settings)
