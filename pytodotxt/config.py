import click
import sys
import configparser
from pathlib import Path

DEFAULT_CONFIG_LOCATION = '~/.config/pytodotxt.ini'
DEFAULT_CONFIG = """[pytodotxt]
todo_file = ~/todo.txt
"""

def load_from_file(config_path: str) -> None:
    if config_path:
        config_path = Path(config_path).expanduser()
    else:
        config_path = Path(DEFAULT_CONFIG_LOCATION).expanduser()
    if not config_path.exists():
        config_path.write_text(DEFAULT_CONFIG)
        click.secho(f'Created a config file: {config_path}; edit the todo_file and rerun PyTodoTxt.', fg='yellow')
        sys.exit(0)
    parser = configparser.ConfigParser()
    parser.read([config_path])
    for section in parser.sections():
        for key in parser[section]:
            globals()[key.upper()] = parser[section][key]

# Configs

TODO_FILE = ''
