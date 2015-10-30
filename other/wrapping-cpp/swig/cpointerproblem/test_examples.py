"""
The code this example is all based on is from http://tinyurl.com/pmmnbxv
Some notes on this in the oommf-devnotes repo
"""

import os

import pytest

#print("pwd:")
#os.system('pwd')
#import subprocess
#subprocess.check_output('pwd')


os.system('make all')
import example1


def test_f():
    assert example1.f(1) - 1 <= 10 ** -7


def test_myfun():
    """Demonstrate that calling code with wrong object type results
    in TypeError exception."""
    with pytest.raises(TypeError):
        assert example1.myfun(example1.f, 2.0) - 4.0 <= 10 ** -7

os.system('make alternate')

import example2


def test2_f():
    assert example2.f(1) - 1 <= 10 ** -7


def test2_myfun():
    assert example2.myfun(example2.f, 2.0) - 4.0 <= 10 ** -7

os.system('make clean')
