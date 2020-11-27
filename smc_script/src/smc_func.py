#!/usr/bin/env python3


def filter_extension(file, extns=None):
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
