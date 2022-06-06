from typing import List

from markdown_it import MarkdownIt
from markdown_it.token import Token

from urobor.commands.catalog import CommandCatalog, DEFAULT_CATALOG
from urobor.commands.command import BlockArgument, Command
from urobor.test_case import TestCase
from os import path


class Parser:
    _index = 0

    def __init__(self, filename: str, command_catalog: CommandCatalog = DEFAULT_CATALOG) -> None:
        parser = MarkdownIt()
        self.catalog = command_catalog

        with open(filename, "r") as md_file:
            self.filename = path.realpath(filename)
            contents = md_file.read()
            self._tokens = parser.parse(contents)
            self._test = self._process_tokens()

    def _process_tokens(self) -> TestCase:
        root_test = TestCase(name="__root__", level=0)
        current_test = root_test
        self._index = 0

        while self._index < len(self._tokens):
            token = self._tokens[self._index]
            if token.type == "heading_open":
                current_test = self._parse_header(current_test, token)
                continue

            if token.type == "blockquote_open":
                command = self._parse_command(token)
                current_test.commands.append(command)
                continue

            self._index += 1

        return root_test

    def _parse_command(self, token: Token) -> Command:
        tokens = self._seek("blockquote_close")
        self._index += 1
        current_command = self._tokens_to_string(tokens)
        space_pos = current_command.find(" ")
        command_name = current_command[:space_pos]
        command_args = current_command[space_pos + 1:]
        block_args = [token for token in self._seek("blockquote_open", "heading_open") if token.type == "fence"]
        if command_name not in self.catalog:
            raise RuntimeError(f"Unknown command `{command_name}`, in file `{self.filename}:{token.map[0] + 1}`")
        command_class = self.catalog.get(command_name)
        parsed_args = command_class.parse_line_arguments(command_args)
        if block_args:
            for block_arg in block_args:
                block_info = block_arg.info
                space_pos = block_info.find(" ")
                if space_pos < 0:
                    parsed_args.append(
                        BlockArgument(
                            self._tokens_to_string([block_arg]),
                            block_info,
                        )
                    )
                else:
                    parsed_args.append(
                        BlockArgument(
                            self._tokens_to_string([block_arg]),
                            block_info[: space_pos],
                            block_info[space_pos + 1:]
                        )
                    )
        return command_class(parsed_args)

    def _parse_header(self, current_test, token) -> TestCase:
        level = len(token.markup)
        tokens = self._seek("heading_close")
        name = self._tokens_to_string(tokens)
        if level > current_test.level:
            new_test = TestCase(name=name, level=level, parent=current_test)
            current_test.children.append(new_test)

            return new_test

        if level == current_test.level:
            new_test = TestCase(name=name, level=level, parent=current_test.parent)
            current_test.parent.children.append(new_test)

            return new_test

        offset = 0
        while current_test.level - offset >= level:
            current_test = current_test.parent
            offset += 1
        current_test = current_test.parent
        new_test = TestCase(name=name, level=level, parent=current_test)
        current_test.children.append(new_test)

        return new_test

    def _seek(self, *next_token: str) -> List[Token]:
        tokens = []
        while self._index < len(self._tokens):
            token = self._tokens[self._index]
            if token.type in next_token:
                break
            tokens.append(token)
            self._index += 1

        return tokens

    def _tokens_to_string(self, tokens: List[Token]) -> str:
        value = ""
        for token in tokens:
            if token.children:
                value += self._tokens_to_string(token.children)
            else:
                value += token.content

        return value

    @property
    def test(self) -> TestCase:
        return self._test
