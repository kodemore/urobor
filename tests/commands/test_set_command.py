from urobor.commands import SetCommand, Command, Argument
from urobor import TestCase
import pytest

from urobor.commands.command import Context, BlockArgument


def test_can_instantiate() -> None:
    # given
    command = SetCommand([Argument("name")])

    # then
    assert isinstance(command, SetCommand)
    assert isinstance(command, Command)


@pytest.mark.parametrize("line_args", [
    "variable {{ value }}",
    "variable   {{ value }}   ",
    "variable {{ value }}\n"
])
def test_can_parse_full_line_arguments(line_args: str) -> None:

    # when
    args = SetCommand.parse_line_arguments(line_args)

    # then
    assert len(args) == 2
    assert args[0].value == "variable"
    assert args[1].value == "{{ value }}"


@pytest.mark.parametrize("line_args", [
    "variable ",
    "variable   ",
    "variable   \n"
])
def test_can_parse_one_line_arguments(line_args) -> None:
    # when
    args = SetCommand.parse_line_arguments(line_args)

    # then
    assert len(args) == 1
    assert args[0].value == "variable"


def test_can_execute_from_test() -> None:
    # given
    test_case = TestCase("Example test")
    command = SetCommand([Argument("variable"), Argument("{{ other }}")])
    context = Context({
        "other": "value"
    })

    # when
    test_case.commands.append(command)
    test_case.run(context)

    # then
    assert context["variable"] == "value"


def test_can_execute_multiple_sets() -> None:
    # given
    test_case = TestCase("Example test")
    command_0 = SetCommand([Argument("variable_0"), Argument("10")])
    command_1 = SetCommand([Argument("variable_1"), Argument("is {{ variable_0 }}")])
    command_2 = SetCommand([Argument("variable_2"), Argument("this {{ variable_1 }}")])
    context = Context({})

    # when
    test_case.commands.append(command_0)
    test_case.commands.append(command_1)
    test_case.commands.append(command_2)
    test_case.run(context)

    # then
    assert context["variable_0"] == 10
    assert context["variable_1"] == "is 10"
    assert context["variable_2"] == "this is 10"


def test_can_set_variables_from_yaml() -> None:
    # given
    test_case = TestCase("Example test")
    command = SetCommand([Argument("variable_0"), BlockArgument("variable:10\nother_variable: other_value", "yaml")])
    context = Context({})

    # when
    test_case.commands.append(command)
    test_case.run(context)

    # then
    assert context["variable_0"] == 10
    assert context["variable_1"] == "is 10"
    assert context["variable_2"] == "this is 10"
