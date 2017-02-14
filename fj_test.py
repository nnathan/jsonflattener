#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this software is public domain

from fj import flatten_json


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
