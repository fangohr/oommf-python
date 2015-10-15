import os
import mylib
os.system('make all')
def test_squared():
    assert mylib.squared(4) - 16.0 <= 10**-8

def test_myfunction():
    assert mylib.myfunction(mylib.squared, 4) - 16.0 <= 10**-8


os.system('make clean')
