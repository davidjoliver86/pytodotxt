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


def test_priority_identity():
    todo = Todo('(A) task with priority')
    assert repr(todo) == '(A) task with priority'


def test_priority_unset():
    todo = Todo('(A) task with priority')
    assert repr(todo)


def test_set_priority_from_none():
    todo = Todo('i need a priority')
    todo.priority = 'A'
    assert repr(todo) == '(A) i need a priority'


def test_replace_priority():
    todo = Todo('(A) im getting my priority replaced')
    todo.priority = 'B'
    assert repr(todo) == '(B) im getting my priority replaced'


def test_unset_priority():
    todo = Todo('(A) im losing my priority')
    todo.priority = None
    assert repr(todo) == 'im losing my priority'


def test_contexts():
    todo = Todo('do stuff @Home @Phone')
    assert set(todo.contexts) == set(('@Home', '@Phone'))


def test_projects():
    todo = Todo('do +thing about +stuff')
    assert set(todo.projects) == set(('+thing', '+stuff'))
