from pytodotxt.todotxt import Todo


def test_todo_identity():
    todo = Todo('i am a todo')
    assert repr(todo) == 'i am a todo'


def test_completed():
    todo = Todo('x completed task')
    assert todo.completed


def test_mark_complete():
    todo = Todo('task that will be completed')
    todo.completed = True
    assert repr(todo) == 'x task that will be completed'


def test_priority():
    todo = Todo('(A) task with priority')
    assert todo.priority == 'A'


def test_contexts():
    todo = Todo('do stuff @Home @Phone')
    assert set(todo.contexts) == set(('@Home', '@Phone'))


def test_projects():
    todo = Todo('do +thing about +stuff')
    assert set(todo.projects) == set(('+thing', '+stuff'))
