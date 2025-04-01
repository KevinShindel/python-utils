"""Some data for our tests."""

from pytest import fixture


@fixture
def names():
    return 'Bob', '', None, 123, [], ()
