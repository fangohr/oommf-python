
import os

os.system('make all')
import example1
def test_f():
    assert example1.f(1) - 1 <= 10 ** -7


def test_myfun():
    assert example1.myfun(example1.f, 2.0) - 4.0 <= 10 ** -7

os.system('make alternate')

import example2


def test2_f():
    assert example2.f(1) - 1 <= 10 ** -7


def test2_myfun():
    assert example2.myfun(example2.f, 2.0) - 4.0 <= 10 ** -7

os.system('make clean')
