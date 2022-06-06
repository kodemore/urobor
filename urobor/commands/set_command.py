import re
from typing import Pattern

from .command import Command, Context, Result


class SetCommand(Command):
    """
    Example usage:
    ```
    set variable_name value
    ```
    """
    LINE_ARGUMENTS = re.compile(r"([_a-z][_a-z0-9\\.-]*)(?:\s+(.+)?(?<!\s))?\s*")

    def execute(self, context: Context) -> Result:
        if len(self.arguments) != 2:
            raise RuntimeError(f"Invalid number of arguments passed to `set` command. Expected `2`, got `{len(self.arguments)}`")
        context[self.arguments[0].parse(context)] = self.arguments[1].parse(context)

        return Result()

    @classmethod
    def id(cls) -> str:
        return "set"

    @classmethod
    def line_arguments(cls) -> Pattern:
        return cls.LINE_ARGUMENTS
