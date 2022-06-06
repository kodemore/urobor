from typing import Type

from urobor.commands.command import Command
from urobor.commands.print_command import PrintCommand
from urobor.commands.set_command import SetCommand


class CommandCatalog:
    def __init__(self):
        self._catalog = {}

    def add(self, value: Type[Command]) -> None:
        self._catalog[value.id()] = value

    def get(self, key: str) -> Type[Command]:
        if key in self:
            return self._catalog[key]

        raise KeyError(f"Unknown command `{key}`.")

    def __contains__(self, name: str) -> bool:
        return name in self._catalog


DEFAULT_CATALOG = CommandCatalog()
DEFAULT_CATALOG.add(SetCommand)
DEFAULT_CATALOG.add(PrintCommand)

