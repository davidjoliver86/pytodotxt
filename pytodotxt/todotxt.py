import re
from typing import List, AnyStr
import pathlib

PRIORITY_REGEX = r'\(([A-Z])\)'

CONTEXT = '@'
PROJECT = '+'


class Todo:

    __priority = None
    __completed = False

    contexts = []
    projects = []

    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, val: AnyStr):
        # find priority in raw
        found = re.search(PRIORITY_REGEX, self._raw)
        if found:
            old = found.group(1)
            if val:  # update raw to reflect priorty; if initializing, old will == val
                self._raw = self._raw.replace(f'({old}) ', f'({val}) ')
            else:  # remove existing priority
                self._raw = self._raw.replace(f'({old}) ', '')
        else:  # adding a priority from none
            self._raw = f'({val}) {self._raw}'
        self.__priority = val

    @property
    def completed(self):
        return self.__completed

    @completed.setter
    def completed(self, val: AnyStr):
        self.__completed = val
        if val:
            if not self._raw.startswith('x '):
                self._raw = 'x ' + self._raw
        else:
            if self._raw.startswith('x '):
                self._raw = self._raw[2:]

    @property
    def contexts(self):
        return [token for token in self._raw.split() if token.startswith(CONTEXT)]

    @property
    def projects(self):
        return [token for token in self._raw.split() if token.startswith(PROJECT)]

    def __repr__(self):
        return self._raw.strip()

    def __init__(self, _id, val):
        self._id = _id
        self._raw = val
        tokens: List[AnyStr] = val.split()
        if tokens[0] == 'x':
            self.completed = True
        found_priority = re.search(PRIORITY_REGEX, self._raw)
        if found_priority:
            self.priority = found_priority.group(1)


def read_file(filename) -> List[Todo]:
    with pathlib.Path(filename).expanduser().open('r') as fp:
        return [Todo(_id, line) for _id, line in enumerate(fp)]
