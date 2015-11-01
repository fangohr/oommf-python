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


@pytest.fixture
def setup_all(request):
    call_make('all')

    def fin():
        print("teardown smtp")
        call_make('clean')
    request.addfinalizer(fin)


def test_f(setup_all):
    import example1
    assert example1.f(1) - 1 <= 10 ** -7


def test_myfun(setup_all):
    """Demonstrate that calling code with wrong object type results
    in TypeError exception."""
    import example1
    with pytest.raises(TypeError):
        assert example1.myfun(example1.f, 2.0) - 4.0 <= 10 ** -7


@pytest.fixture
def setup_alternate(request):
    call_make('alternate')

    def fin():
        print("teardown smtp")
        call_make('clean')
    request.addfinalizer(fin)


def test2_f(setup_alternate):
    import example2
    assert example2.f(1) - 1 <= 10 ** -7


def test2_myfun(setup_alternate):
    import example2
    assert example2.myfun(example2.f, 2.0) - 4.0 <= 10 ** -7
