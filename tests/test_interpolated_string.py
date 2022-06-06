import pytest

from urobor.interpolation.interpolated_string import InterpolatedString
from urobor.interpolation.modifiers import string_to_snake_case, string_strip, string_to_upper


def test_interpolate_string() -> None:
    # given
    test_string = "Test {{ variable_1 }} {{ variable_2 }}"
    template = InterpolatedString(test_string)

    # when
    substituted_string = template + {
        "variable_1": "tasty",
        "variable_2": "flavour",
    }

    # then
    assert substituted_string == "Test tasty flavour"


def test_fail_interpolate_string_with_missing_keys() -> None:
    # given
    test_string = "Some text with a {{ variable_1 }} {{ variable_2 }}"
    template = InterpolatedString(test_string)

    # then
    assert template.interpolate({"variable_1": "present"}) == "Some text with a present "


def test_interpolate_string_with_nested_values() -> None:
    # given
    test_string = "{{ foo.bar.baz }} {{ bar }} {{ foo.barbar }}"
    template = InterpolatedString(test_string)
    values = {
        "foo": {
            "bar": {
                "baz": "foobarbaz",
            },
            "barbar": "foobarbar",
        },
        "bar": "baz"
    }

    # when
    result = template + values

    # then
    assert result == "foobarbaz baz foobarbar"


def test_fail_interpolation_with_invalid_placeholder() -> None:
    # given
    test_string = "Some text with a {{ invalid placeholder }}"
    template = InterpolatedString(test_string)

    # then
    with pytest.raises(ValueError):
        template + {"invalid": 123}


@pytest.mark.parametrize(
    "given, expected",
    [
        ["Project Name", "project_name"],
        ["project   Name", "project_name"],
        ["project_ _ Name", "project_name"],
        ["project.name", "project_name"],
        ["Project. . Name", "project_name"],
        ["Project' Name", "project_name"],
    ],
)
def test_interpolation_with_a_filter(given: str, expected: str) -> None:
    # given
    InterpolatedString.register_filter("snake-case", string_to_snake_case)
    test_string = InterpolatedString("{{ project_name | snake-case }}")

    # then
    assert test_string + {"project_name": given} == expected

    # tear-down
    InterpolatedString.unregister_filter("snake-case")


def test_can_escape_interpolation() -> None:
    # given
    test_string = InterpolatedString("`{{` string|hyphened `}}`")

    # then
    assert test_string + {"project_name": "test"} == "{{ string|hyphened }}"


def test_can_chain_filters() -> None:
    # given
    InterpolatedString.register_filter("strip", string_strip)
    InterpolatedString.register_filter("upper-case", string_to_upper)
    InterpolatedString.register_filter("snake-case", string_to_snake_case)

    test_string = "{{ string | strip | snake-case | upper-case }}"
    template = InterpolatedString(test_string)

    # when
    substituted_string = template + {
        "string": "  tasty flavour  ",
    }

    # then
    assert substituted_string == "TASTY_FLAVOUR"

    InterpolatedString.unregister_filter("strip")
    InterpolatedString.unregister_filter("upper-case")
    InterpolatedString.unregister_filter("snake-case")


def test_can_use_filter_with_extra_parameters() -> None:
    # given
    def string_replace(value: str, extra: str = "") -> str:
        params = [item.strip() for item in extra.split(">")]
        return value.replace(params[0], params[1])

    InterpolatedString.register_filter("replace", string_replace)
    test_string = "{{ string | replace a > e }}"
    template = InterpolatedString(test_string)

    # when
    substituted_string = template + {
        "string": "  tasty flavour  ",
    }

    # then
    assert substituted_string == "  testy flevour  "

    InterpolatedString.unregister_filter("replace")


def test_can_call_a_user_defined_function() -> None:
    # given
    test_string = "Hello, {{ name () }}!"
    template = InterpolatedString(test_string)

    # when
    InterpolatedString.register_function("name", lambda: "Bob")

    # then
    assert template + {} == "Hello, Bob!"


def test_can_call_a_user_defined_function_with_extra() -> None:
    # given
    test_string = "Hello, {{ name ( Bob, Paul, Rob ) }}!"
    template = InterpolatedString(test_string)

    # when
    InterpolatedString.register_function("name", lambda extra="": [name.strip() for name in extra.split(",")][2])
    substituted_string = template + {}

    # then
    assert substituted_string == "Hello, Rob!"

