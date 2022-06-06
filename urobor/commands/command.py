from __future__ import annotations

from abc import abstractmethod, ABC
from typing import Any, List, Pattern, Dict
from copy import deepcopy

from urobor.interpolation.interpolated_string import InterpolatedString


class Error:
    def __init__(self, exception: Exception):
        self.exception = exception


class Argument:
    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def parse(self, context: Context) -> Any:
        if self.value == "true":
            return True

        if self.value == "false":
            return False

        if len(self.value) > 1 and self.value[0] == "0" and self.value[1] != ".":
            return self._interpolate_value(context)

        try:
            return int(self.value)
        except ValueError:
            pass

        try:
            return float(self.value)
        except ValueError:
            pass

        return self._interpolate_value(context)

    def _interpolate_value(self, context: Context) -> str:
        value = InterpolatedString(self.value)

        return value + context.variables

    def __repr__(self) -> str:
        return f"{self.value}"


class BlockArgument(Argument):
    def __init__(self, value: str, content_type: str, extra: str = ""):
        self.content_type = content_type
        self.extra = extra

        super().__init__(value)

    def __repr__(self) -> str:
        return f"code@{self.content_type}"


class Result:
    error: Error = None
    output: str

    def __init__(self):
        ...

    def __bool__(self) -> bool:
        return self.error is not None


class Context:
    variables: Dict[str, Any]

    def __init__(self, variables: Dict[str, Any]):
        self.variables = variables

    def __getitem__(self, key: str) -> Any:
        return self.variables[key]

    def copy(self) -> Context:
        return Context(deepcopy(self.variables))

    def __setitem__(self, key: str, value: Any) -> None:
        self.variables[key] = value


class Command(ABC):
    result: Result

    def __init__(self, args: List[Argument] = None):
        self.arguments = args or []

    @abstractmethod
    def execute(self, context: Context) -> Result:
        ...

    @classmethod
    @abstractmethod
    def id(cls) -> str:
        ...

    @classmethod
    @abstractmethod
    def line_arguments(cls) -> Pattern:
        ...

    @classmethod
    def parse_line_arguments(cls, line: str) -> List[Argument]:
        regex = cls.line_arguments()
        match = regex.match(line)
        args = []
        for index in range(0, len(match.groups())):
            value = match.group(index + 1)
            if value is None:
                break
            args.append(Argument(value))

        return args

    def __repr__(self) -> str:
        return f"{self.id()} {' '.join([str(arg) for arg in self.arguments])}"
