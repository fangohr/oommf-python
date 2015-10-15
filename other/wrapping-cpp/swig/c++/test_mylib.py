import os
import mylib
os.system('make all')


def test_squared():
    assert mylib.squared(4) == 16.0 


def test_myfunction():
    assert mylib.myfunction(mylib.squared, 4) == 16.0 


os.system('make clean')
