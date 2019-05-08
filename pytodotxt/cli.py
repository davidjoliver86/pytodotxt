import click

from . import config
from . import todotxt


@click.group()
def cli():
    pass


@cli.command()
def list():
    todos = todotxt.read_file(config.TODOTXT_FILE)
    for todo in todos:
        print(f'{todo.id:>5d} {todo.text}')
