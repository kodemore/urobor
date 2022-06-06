import re
from typing import Pattern

from .command import Command, Context, Result


class PrintCommand(Command):
    """
    Example usage:
    ```
    print value
    print value > filename.txt
    ```
    """
    LINE_ARGUMENTS = re.compile(r"([^>]+)(?<!\s)\s*(?:>\s*(.+)?(?<!\s)\s*)?")

    def execute(self, context: Context) -> Result:
        if len(self.arguments) != 2:
            raise RuntimeError(f"Invalid number of arguments passed to `{self.id()}` command. Expected `2`, got `{len(self.arguments)}`")

        return Result()

    @classmethod
    def id(cls) -> str:
        return "print"

    @classmethod
    def line_arguments(cls) -> Pattern:
        return cls.LINE_ARGUMENTS
