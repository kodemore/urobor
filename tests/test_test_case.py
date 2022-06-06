from urobor import TestCase
from urobor.test_case import Status


def test_can_instantiate() -> None:
    # given
    test_case = TestCase("Example test")

    # then
    assert isinstance(test_case, TestCase)


def test_can_run() -> None:
    # given
    test_case = TestCase("Example test")

    # when
    test_case.run()

    # then
    assert test_case
    assert test_case.status == Status.PASSED
