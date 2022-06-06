from os import path

from pytest import fixture


@fixture()
def examples_dir() -> str:
    return path.join(path.dirname(__file__), "..", "..", "examples")
