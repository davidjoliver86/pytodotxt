import sys
import click

from . import todotxt
from . import config


def error(msg):
    click.secho(msg, fg='red')
    sys.exit(1)


@click.group()
@click.option('--config-file')
@click.pass_context
def cli(ctx, config_file):
    config.load_from_file(config_file)


@cli.command(name='list')
@click.option('--sort-order')
@click.option('--show-done', is_flag=True, default=False)
@click.pass_context
def _list(ctx, show_done, sort_order):
    if not sort_order:
        sort_order = config.SORT_ORDER
    todos = todotxt.read_file(config.TODO_FILE)
    sorted_todos = _sort(todos, sort_order)
    for todo in sorted_todos:
        if not show_done and todo.completed:
            continue
        print(f'{todo.text}')


def _sort(todos, sort_order):
    """
    Builds a list alongside each Todo that acts as the sort key.

    Options for sort_order:
    - none: Do not sort; preserve order of the todo.txt file.
    - priority: Sort by priority only.
    - context: Sort by context(s) only.
    - priority,context: Sort by priority, then subsort by context(s).
    - context,priority: Sort by context(s), then subsort by priority.
    """
    if sort_order == 'none':
        return todos
    sorting = sort_order.split(',')
    todos_with_key = list(zip(todos, [list() for i in range(len(todos))]))
    for sort_type in sorting:
        if sort_type == 'priority':
            for todo, key in todos_with_key:
                key.append(todo.priority or '')  # because priority can be None
        elif sort_type == 'context':
            for todo, key in todos_with_key:
                key.append(todo.contexts)
        else:
            error(f'Unsupported sort type: {sort_type}')
    return [x[0] for x in sorted(todos_with_key, key=lambda todo: todo[1])]
