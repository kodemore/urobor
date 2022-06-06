from glob import glob
from os import path


current_dir = path.dirname(__file__)


def convert_filename_to_pymodule(string: str) -> str:
    return string.replace(current_dir, "tests").replace(path.sep, ".").replace(".py", "")


pytest_plugins = [
    convert_filename_to_pymodule(fixture) for fixture in glob(path.join(current_dir, "fixtures/*.py")) if "__" not in fixture
]
