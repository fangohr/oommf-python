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
