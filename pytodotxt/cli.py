import os
import sys
import configparser
from typing import List

import click

from . import todotxt

CONFIG_FILE_LOCATION = os.path.expanduser('~/.config/pytodotxt.ini')

DEFAULT_CONFIG = """[pytodotxt]
TodoTxtFile=~/todo.txt
ContextFilter=
"""


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


def print_todos(config: configparser.ConfigParser, todos: List[todotxt.Todo]):
    if config['ContextFilter']:
        contexts = set([f'@{context}' for context in config['ContextFilter'].split(',')])
        todos = [todo for todo in todos if set(todo.contexts) & contexts]
    for todo in todos:
        print(todo)


def main():
    config = parse_config()
    todos = todotxt.read_file(config['TodoTxtFile'])
    print_todos(config, todos)
