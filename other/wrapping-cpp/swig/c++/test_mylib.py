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


def test_squared(setup):
    import mylib
    assert 16. == mylib.squared(4) 


def test_myfunction(setup):
    import mylib
    assert 16. == mylib.myfunction(mylib.squared, 4) 

