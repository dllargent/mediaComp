def add_numbers(a, b):
    return a + b

def test_add_two_numbers():
    assert add_numbers(2, 3) == 5

def test_add_negative_numbers():
    assert add_numbers(-1, -5) == -6

