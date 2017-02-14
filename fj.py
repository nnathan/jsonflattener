#!/usr/bin/env python

import json
import sys

# stupid python 2/3 compatibility crap, grrr...

try:
    dict.iteritems
except AttributeError:
    # Python 3
    def itervalues(d):
        return iter(d.values())

    def iteritems(d):
        return iter(d.items())
else:
    # Python 2
    def itervalues(d):
        return d.itervalues()

    def iteritems(d):
        return d.iteritems()


# tests should definitely be run using pytest


def test_empty_object():
    in_ = '{}'
    expected = ''
    actual = '\n'.join(flatten_json(in_))
    assert actual == expected


def test_simple_object():
    in_ = '{"1": 2}'
    expected = '1: 2'
    actual = '\n'.join(flatten_json(in_))
    assert actual == expected


def test_nested_object():
    in_ = '{"1": {"2": 3}}'
    expected = '1.2: 3'
    actual = '\n'.join(flatten_json(in_))
    assert actual == expected


def test_mixed_object():
    in_ = '''
    {
        "1": {"2": 3},
        "4": 5
    }
    '''
    expected = {'1.2: 3', '4: 5'}
    actual = set(flatten_json(in_))
    assert actual == expected


def test_omit_null_value():
    in_ = '{"1": null}'
    expected = '1:'
    actual = '\n'.join(flatten_json(in_, omit_null_value=True))
    assert actual == expected


def test_dont_omit_null_value():
    in_ = '{"1": null}'
    expected = '1: null'
    actual = '\n'.join(flatten_json(in_, omit_null_value=False))
    assert actual == expected


def test_path_separator():
    in_ = '{"1": {"2": 3}}'
    expected = '1>2: 3'
    actual = '\n'.join(flatten_json(in_, path_separator='>'))
    assert actual == expected


def test_value_separator():
    in_ = '{"1": 2}'
    expected = '1> 2'
    actual = '\n'.join(flatten_json(in_, value_separator='>'))
    assert actual == expected


def test_empty_array():
    in_ = '[]'
    expected = ''
    actual = '\n'.join(flatten_json(in_))
    assert actual == expected


def test_array():
    in_ = '["a", 1, {"2": 3}]'
    expected = '[0]: a\n[1]: 1\n[2].2: 3'
    actual = '\n'.join(flatten_json(in_))
    assert actual == expected


def test_nested_array():
    in_ = '[[1,2,3]]'
    expected = '[0].[0]: 1\n[0].[1]: 2\n[0].[2]: 3'
    actual = '\n'.join(flatten_json(in_))
    assert actual == expected


def test_mixed():
    in_ = '''
    {
        "1": [
            {"a": 1},
            null
        ],
        "4": 5
    }
    '''
    expected = {'1.[0].a: 1', '1.[1]: null', '4: 5'}
    actual = set(flatten_json(in_))
    assert actual == expected


def flatten(d):
    '''
       Generator function that takes in dict d and iterates over the structure (recursively) yielding
       ((k1,k2,...,kn), value) where k1, k2, ..., kn are the path of keys to each terminal value.
    '''

    if isinstance(d, (list, dict)) is False:
        raise ValueError('flatten can only be called with list or dict type')

    # maintain a stack as we descend dict/lists maintaining components (which derives to the path of keys)
    # to get to the values
    stack = [([], d)]

    while len(stack) > 0:
        components, seq = stack.pop()

        if isinstance(seq, list):
            seq = enumerate(seq)
        else:
            seq = iteritems(seq)

        for k, val in seq:
            path = components + [k]

            if isinstance(val, (list, dict)):
                stack.append((path, val))
                continue

            yield (path, val)


def flatten_json(j, path_separator='.', value_separator=':', omit_null_value=False):
    '''
       Generator function that decomposes a JSON string into a path, value pairs where the rendering of the line
       is controlled by path_separator, value_separator, and omit_null_value.

       E.g. JSON in the form:
           {
               "a": {
                   "b": 5,
                   "c": [
                       {"1": 2},
                       null
                   ]
               },
               "b": null
           }

       generates the following lines (in no particular order):
           b: null
           a.c.[0]: 2
           a.c.[1]: null
           a.b: 5
    '''

    def fixup(p):
        if isinstance(p, int):
            return '[{0}]'.format(p)
        return p

    d = json.loads(j)

    for path_components, value in flatten(d):
        path = path_separator.join(fixup(p) for p in path_components)

        out = '{0}{1} {2}'.format(path, value_separator, value)

        if value is None:
            if omit_null_value:
                out = path + value_separator
            else:
                out = path + value_separator + " null"

        yield out

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='JSON hierarchy flattener')
    ap.add_argument('-p', '--path-separator', help="specify path separator (default is '.')", default='.')  # noqa
    ap.add_argument('-v', '--value-separator', help="specify value separator (default is ':')", default=':')  # noqa
    ap.add_argument('-n', '--omit-null-value', help='elide JSON null value in output (no output after value separator)', action='store_true')  # noqa
    ap.add_argument('args', nargs=argparse.REMAINDER, help='specify JSON pathnames to flatten')

    # this namespace shit that argparse does is the most braindead shit i've seen in stdlib for awhile
    kwargs = vars(ap.parse_args(sys.argv[1:]))
    files = kwargs['args']
    del kwargs['args']

    # paying homage to djb
    def doit(f):
        for l in flatten_json(f.read(), **kwargs):
            print(l)

    if not sys.stdin.isatty():
        doit(sys.stdin)

    for fn in files:
        with open(fn) as f:
            doit(f)