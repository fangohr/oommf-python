import os

import pytest

@pytest.fixture
def setup(request):
    def teardown():
        print("Running make clean")
        os.system('make clean')
        print("Completed finaliser")
    request.addfinalizer(teardown)
    os.system('make clean')
    os.system('make all')


def test_squared(setup):
    import mylib
    assert 16. == mylib.squared(4) 


def test_myfunction(setup):
    import mylib
    assert 16. == mylib.myfunction(mylib.squared, 4) 

