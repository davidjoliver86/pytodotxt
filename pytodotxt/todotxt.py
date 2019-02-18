from typing import List
import pathlib


class Todo:
    pass


def read_file(filename) -> List[Todo]:
    """
    """
    with pathlib.Path(filename).expanduser().open('r') as fp:
        return [line for line in fp]
