"""
The code this example is all based on is from http://tinyurl.com/pmmnbxv
Some notes on this in the oommf-devnotes repo
"""

import os

import pytest


# Need to call Makefile in directory where this test file is
def call_make(target):
    # where is this file
    this_file = os.path.realpath(__file__)
    this_dir = os.path.split(this_file)[0]
    cd_command = "cd {}".format(this_dir)
    make_command = "make {}".format(target)
    command = '{}; {}'.format(cd_command, make_command)
    print("About to execute: '{}'".format(command))
    os.system(command)


call_make('all')
import example1


def test_f():
    assert example1.f(1) - 1 <= 10 ** -7


def test_myfun():
    """Demonstrate that calling code with wrong object type results
    in TypeError exception."""
    with pytest.raises(TypeError):
        assert example1.myfun(example1.f, 2.0) - 4.0 <= 10 ** -7

call_make('alternate')

import example2


def test2_f():
    assert example2.f(1) - 1 <= 10 ** -7


def test2_myfun():
    assert example2.myfun(example2.f, 2.0) - 4.0 <= 10 ** -7

call_make('clean')
