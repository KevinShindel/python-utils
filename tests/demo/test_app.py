from src.demo.app import say_hello


def test_say_hello():
    assert say_hello('Bob') == 'Hello Stefan!'


def test_say_hello_multi(names):
    assert say_hello('Stefan') == 'Hello Stefan!'

    bob, empty, none, integer, li, tup = names

    assert say_hello(bob) == 'Hello Bob!'
    assert say_hello(empty) == 'Hello !'
    assert say_hello(none) == 'Hello None!'
    assert say_hello(integer) == 'Hello 123!'
    assert say_hello(li) == 'Hello []!'
    assert say_hello(tup) == 'Hello ()!'
