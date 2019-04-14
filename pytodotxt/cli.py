import os
import sys
import configparser
from typing import List, Callable

import click

from . import todotxt

CONFIG_FILE_LOCATION = os.path.expanduser('~/.config/pytodotxt.ini')

DEFAULT_CONFIG = """[pytodotxt]
TodoTxtFile=~/todo.txt
ContextFilter=
ShowCompleted=True
"""

# type signature and register for filter functions

FILTER_FUNC = Callable[[configparser.ConfigParser, List[todotxt.Todo]], List[todotxt.Todo]]
_FILTER_FUNCS: List[FILTER_FUNC] = []


def register_filter(func: FILTER_FUNC):
    _FILTER_FUNCS.append(func)
    return func


def parse_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    try:
        with open(CONFIG_FILE_LOCATION, 'r') as fp:
            config.read_file(fp)
        return config['pytodotxt']
    except FileNotFoundError:
        click.secho(f'Config file not found! Creating a default config at {CONFIG_FILE_LOCATION}.', fg='yellow')
        click.secho('Please ensure your TodoTxtFile is correct, then run PyTodoTxt again.', fg='green')
        with open(CONFIG_FILE_LOCATION, 'w') as fp:
            fp.write(DEFAULT_CONFIG)
        sys.exit(0)


@register_filter
def filter_context(config: configparser.ConfigParser, todos: List[todotxt.Todo]) -> List[todotxt.Todo]:
    if config['ContextFilter']:
        contexts = set([f'{todotxt.CONTEXT}{context}' for context in config['ContextFilter'].split(',')])
        todos = [todo for todo in todos if set(todo.contexts) & contexts]
    return todos


def print_todos(todos: List[todotxt.Todo]):
    for todo in todos:
        print(todo)


def main():
    config = parse_config()
    todos = todotxt.read_file(config['TodoTxtFile'])
    for func in _FILTER_FUNCS:
        todos = func(config, todos)
    print_todos(todos)
