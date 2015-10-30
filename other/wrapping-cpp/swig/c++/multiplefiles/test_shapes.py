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

def setup(request):
    def teardown():
        print("Running make clean")
        call_make('clean')
        print("Completed finaliser")
    request.addfinalizer(teardown)
    call_make('clean')
    call_make('all')


def test_square(setup):
    import shapes
    assert shapes.square(10).area() == 100
    assert shapes.square(100).area() == 10000
    assert shapes.square(5).area() == 25


def test_rectangle(setup):
    import shapes
    assert shapes.rectangle(10, 10).area() == 100
    assert shapes.rectangle(100, 10).area() == 1000
    assert shapes.rectangle(1, 2).area() == 2
