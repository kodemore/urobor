import re
from functools import cached_property
from typing import Any, Dict, List, Mapping

_NAME_PATTERN = r"[_a-z][_a-z0-9-]*"
_FUNCTION_PATTERN = _NAME_PATTERN + r"\s{0,1}\([^\)]*\)\s*"
_VARIABLE_PATTERN = r"[_a-z][_a-z0-9\.-]*"
_ID_PATTERN = f"({_FUNCTION_PATTERN}|{_VARIABLE_PATTERN})"
_FILTER_PATTERN = f"{_NAME_PATTERN}(?:\\s*[^|]*)?"
_PLACEHOLDER_PATTERN = (
    r"\s*"
    f"(?:(?P<name>{_ID_PATTERN})\\s*)"
    f"(?P<filters>(\\|\\s*({_FILTER_PATTERN})\\s*)*)?"
    r"(?P<invalid>.*?)"
    r"\s*"
)
_CHARACTERS_TO_ESCAPE = ("[", "]", "{", "}", "*", "+", "?", "|", "^", "$", ".", "\\")


def escape_sequence(sequence: str) -> str:
    escaped = ""
    for c in sequence:
        if c in _CHARACTERS_TO_ESCAPE:
            escaped += "\\" + c
            continue
        escaped += c

    return escaped


class InterpolatedString:
    """
    Simple template string class to replace {{ key }} occurrences with corresponding values in passed dict[key] value
    """

    FILTERS = {}
    FUNCTIONS = {}

    OPEN_SEQUENCE = "{{"
    CLOSE_SEQUENCE = "}}"

    def __init__(self, template: str):
        self.template = template

    @cached_property
    def pattern(self) -> Any:
        return re.compile(
            escape_sequence(InterpolatedString.OPEN_SEQUENCE)
            + _PLACEHOLDER_PATTERN
            + escape_sequence(InterpolatedString.CLOSE_SEQUENCE)
        )

    @cached_property
    def escaped_template(self) -> str:
        return self._escape_template(self.template)

    def interpolate(self, mapping: Mapping) -> str:
        template = self.escaped_template

        def convert(match: re.Match) -> str:
            if match.group("invalid"):
                i = match.start("invalid")
                lines = self.template[:i].splitlines(keepends=True)
                if not lines:
                    column_no = 1
                    line_no = 1
                else:
                    column_no = i - len("".join(lines[:-1]))
                    line_no = len(lines)
                raise ValueError(
                    f"Invalid placeholder `{match.group('invalid')}` on line `{line_no}`, at column `{column_no}`"
                )

            name = match.group("name").strip()
            filters = [item.strip() for item in match.group("filters").split("|")[1:]]

            if "." in name:
                value = self._resolve_value(name.split("."), mapping)
            elif name in mapping:
                value = mapping[name]
            elif name.endswith(")"):
                extra_pos = name.find("(")
                func_name = name[:extra_pos].strip()
                func_extra = name[extra_pos + 1: -1].strip()
                if func_name not in self.FUNCTIONS:
                    raise RuntimeError(
                        f"Call to unknown function `{func_name}`, "
                        f"use`InterpolatedString.register_function` to register your function."
                    )
                if func_extra:
                    value = self.FUNCTIONS[func_name](func_extra)
                else:
                    value = self.FUNCTIONS[func_name]()
            else:
                return ""

            if not filters:
                return str(value)

            return self._apply_filters(value, filters)

        return self._unescape_template(self.pattern.sub(convert, template))

    @staticmethod
    def _apply_filters(value: str, filters: List[str]) -> str:
        for item in filters:
            extra_position = item.find(" ")
            if extra_position < 0:
                filter_name = item
                filter_extra = ""
            else:
                filter_name = item[:extra_position]
                filter_extra = item[extra_position + 1:].strip()

            if filter_name not in InterpolatedString.FILTERS:
                raise KeyError(f"Filter `{filter_name}` not found.")

            if filter_extra:
                value = InterpolatedString.FILTERS[filter_name](value, filter_extra)
            else:
                value = InterpolatedString.FILTERS[filter_name](value)

        return value

    @staticmethod
    def _escape_template(template: str) -> str:
        template = template.replace(
            f"`{InterpolatedString.OPEN_SEQUENCE}`", "&escape_open_sequence;"
        )
        template = template.replace(
            f"`{InterpolatedString.CLOSE_SEQUENCE}`", "&escape_close_sequence;"
        )
        return template

    @staticmethod
    def _unescape_template(template: str) -> str:
        template = template.replace("&escape_open_sequence;", InterpolatedString.OPEN_SEQUENCE)
        template = template.replace("&escape_close_sequence;", InterpolatedString.CLOSE_SEQUENCE)
        return template

    @staticmethod
    def _resolve_value(path: List[str], mapping: Mapping) -> Any:
        value = mapping
        for item in path:
            if item in value:
                value = value[item]
            else:
                return ""

        return value

    @classmethod
    def register_function(cls, name: str, function: callable) -> None:
        cls.FUNCTIONS[name] = function

    @classmethod
    def register_filter(cls, name: str, function: callable) -> None:
        cls.FILTERS[name] = function

    @classmethod
    def unregister_function(cls, name: str) -> None:
        del cls.FUNCTIONS[name]

    @classmethod
    def unregister_filter(cls, name: str) -> None:
        del cls.FILTERS[name]

    def __str__(self) -> str:
        return self.template

    def __add__(self, other: Dict[str, Any]) -> str:
        return self.interpolate(other)
