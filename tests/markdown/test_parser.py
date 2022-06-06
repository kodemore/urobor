from os import path

from urobor import TestCase
from urobor.markdown import Parser


def test_can_instantiate(examples_dir: str) -> None:
    # given
    instance = Parser(path.join(examples_dir, "variables.md"))

    # then
    assert isinstance(instance, Parser)


def test_can_parse_headers(examples_dir: str) -> None:
    # given
    instance = Parser(path.join(examples_dir, "variables.md"))

    # when
    test = instance.test

    # then
    assert isinstance(test, TestCase)
    assert len(test.children) == 3
    assert test.children[0].name == "Variables usage"
    assert test.children[1].name == "Using modifiers/filters"
    assert test.children[2].name == "Built-in functions"
    assert len(test.children[0].children) == 4
    assert test.children[0].children[0].name == "Declaring a variable"
    assert test.children[0].children[1].name == "Reusing a variable"
    assert len(test.children[1].children) == 4
    assert len(test.children[2].children) == 5


def test_can_parse_commands(examples_dir: str) -> None:
    # given
    instance = Parser(path.join(examples_dir, "variables.md"))

    # when
    test = instance.test

    # then
    a = 1
