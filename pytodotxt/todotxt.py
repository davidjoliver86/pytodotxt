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
    def priority(self, val):
        self.__priority = val
        wrapped = f'({val})'
        self._raw = re.sub(PRIORITY_REGEX, wrapped, self._raw)

    @property
    def completed(self):
        return self.__completed

    @completed.setter
    def completed(self, val):
        self.__completed = val
        if val:
            if not self._raw.startswith('x '):
                self._raw = 'x ' + self._raw
        else:
            if self._raw.startswith('x '):
                self._raw = self._raw[2:]

    @property
    def contexts(self):
        return [token for token in self._tokens if token.startswith(CONTEXT)]

    @property
    def projects(self):
        return [token for token in self._tokens if token.startswith(PROJECT)]

    def __repr__(self):
        return self._raw

    def __init__(self, val):
        self._raw = val
        self._tokens: List[AnyStr] = val.split()
        priority_token_index = 0
        if self._tokens[0] == 'x':
            self.completed = True
            priority_token_index = 1
        match = re.match(PRIORITY_REGEX, self._tokens[priority_token_index])
        if match:
            self.priority = match.group(1)


def read_file(filename) -> List[Todo]:
    with pathlib.Path(filename).expanduser().open('r') as fp:
        return [Todo(line) for line in fp]
