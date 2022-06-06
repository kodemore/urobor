from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class TokenType(Enum):
    SECTION_START = 'section_start'
    SECTION_NAME = 'section_name'
    SECTION_DESCRIPTION = 'section_description'
    SECTION_END = 'section_end'
    COMMAND_START = 'command_start'
    COMMAND_NAME = 'command_name'
    COMMAND_EXTRA = 'command_extra'
    COMMAND_ATTRIBUTE_START = 'command_attribute_start'
    COMMAND_ATTRIBUTE_TYPE = 'command_attribute_type'
    COMMAND_ATTRIBUTE_EXTRA = 'command_attribute_extra'
    COMMAND_ATTRIBUTE_VALUE = 'command_attribute_value'
    COMMAND_ATTRIBUTE_END = 'command_attribute_end'


@dataclass
class Token:
    map: Tuple[int, int]
    type: TokenType
    value: str
    section: str = "__root__"
