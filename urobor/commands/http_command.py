from .command import Command


class HttpCommand(Command):
    method: str
    url: str
    headers: dict
    body: bytes


class PostCommand(Command):
    method = "post"
