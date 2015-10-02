import rect

def test_area():
    assert rect.PyRectangle(0, 0,10,20).getArea() == 200
    assert rect.PyRectangle(0, 10, 30, 50).getArea() == 1200

