from __future__ import annotations

from enum import IntEnum
from typing import List

from .commands.command import Context


class Reporter:
    ...


class Status(IntEnum):
    OTHER = - 3
    SKIPPED = -2
    NOT_STARTED = -1
    FAILED = 0
    PASSED = 1


class TestCase:
    __slots__ = ["name", "status", "commands", "children", "parent", "level"]

    def __init__(self, name: str, level: int = 1, parent: TestCase = None):
        self.name = name
        self.status = Status.NOT_STARTED
        self.commands = []
        self.children: List[TestCase] = []
        self.parent = parent
        self.level = level

    def run(self, context: Context = None) -> None:
        context = context or Context({})

        for command in self.commands:
            result = command.execute(context)
            if not result:
                self.status = Status.FAILED
                continue

        for test in self.children:
            test.run(context.copy())

            if test.status == Status.FAILED:
                self.status = test.status

        if self.status is Status.NOT_STARTED:
            self.status = Status.PASSED

    def __repr__(self) -> str:
        return f"{self.name} ({len([child for child in self.children if child.status == Status.PASSED])}/{len(self.children)})"

    def __bool__(self) -> bool:
        return self.status == Status.PASSED
