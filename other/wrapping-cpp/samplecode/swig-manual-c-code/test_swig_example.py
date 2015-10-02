def test_import():
    import example

def test_fact():
    import example
    assert example.fact(1) == 1
    assert example.fact(3) == 6
    assert example.fact(4) == 24

def test_mod():
    import example
    assert example.my_mod(10, 8) == 2
    assert example.my_mod(10, 7) == 3
    assert example.my_mod(11, 7) == 4
    assert example.my_mod(11, 11) == 0
    assert example.my_mod(2, 1) == 0

def test_get_time():
    import example
    time_string = example.get_time()
    assert type(time_string) == str
    assert len(time_string) == 25
    assert time_string.endswith('\n')
