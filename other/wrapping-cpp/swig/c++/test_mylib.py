import os
import mylib
os.system('make all')


def test_squared():
    assert 16. == mylib.squared(4) 


def test_myfunction():
    assert 16. == mylib.myfunction(mylib.squared, 4) 


os.system('make clean')
