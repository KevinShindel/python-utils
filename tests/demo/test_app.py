import unittest
from src.demo.app import say_hello


class TestSayHello(unittest.TestCase):

    def test_say_hello(self):
        # this assertion is *supposed* to fail, so we wrap it with assertRaises
        with self.assertRaises(AssertionError):
            self.assertEqual(say_hello("Stefan"), "Hello Bob!")

    def test_say_hello_multi(self):
        assert say_hello('Stefan') == 'Hello Stefan!'

        bob, empty, none, integer, li, tup = names

        assert say_hello(bob) == 'Hello Bob!'
        assert say_hello(empty) == 'Hello !'
        assert say_hello(none) == 'Hello None!'
        assert say_hello(integer) == 'Hello 123!'
        assert say_hello(li) == 'Hello []!'
        assert say_hello(tup) == 'Hello ()!'
