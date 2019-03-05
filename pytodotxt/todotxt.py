import re
from typing import List, AnyStr
import pathlib

from . import constants


class Todo(str):

    complete = False
    priority = None
    contexts = []
    projects = []

    def __repr__(self):
        return self._raw

    def __init__(self, val):
        self._raw = val.strip()
        tokens: List[AnyStr] = val.split()
        if tokens[0] == 'x':
            self.complete = True
            tokens = tokens[1:]
        if re.match(constants.PRIORITY_REGEX, tokens[0]):
            self.priority = tokens[0][1]
            tokens = tokens[1:]
        self.contexts = [token for token in tokens if token.startswith(constants.CONTEXT)]
        self.projects = [token for token in tokens if token.startswith(constants.PROJECT)]


def read_file(filename) -> List[Todo]:
    """
    """
    with pathlib.Path(filename).expanduser().open('r') as fp:
        return [Todo(line) for line in fp]
