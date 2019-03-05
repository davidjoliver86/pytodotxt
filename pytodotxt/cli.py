import os
import sys
import configparser

from clint.textui import puts
from clint.textui.colored import green, yellow

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
        puts(yellow(f'Config file not found! Creating a default config at {CONFIG_FILE_LOCATION}.'))
        puts(green('Please ensure your TodoTxtFile is correct, then run PyTodoTxt again.'))
        with open(CONFIG_FILE_LOCATION, 'w') as fp:
            fp.write(DEFAULT_CONFIG)
        sys.exit(0)


def main():
    config = parse_config()
    todos = todotxt.read_file(config['TodoTxtFile'])
    if config['ContextFilter']:
        import ipdb; ipdb.set_trace()
    print(todos)
