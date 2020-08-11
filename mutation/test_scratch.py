import scratch


def test_mutate__simple():
    ast = ["value", 4]
    tests = [({}, 4)]

    assert scratch.mutate(ast, tests)


def test_mutate__simple_fails():
    ast = ["value", 3]
    tests = [({}, 4)]

    assert not scratch.mutate(ast, tests)


def test_mutate__simple_underconstrained():
    ast = ["+", ["value", 3], ["value", 0]]
    tests = [({}, 3)]

    assert not scratch.mutate(ast, tests)


def test_mutate__simple_arg():
    ast = ["variable", "aaa"]
    tests = [({"aaa": 4}, 4), ({"aaa": 7}, 7)]

    assert scratch.mutate(ast, tests)


def test_mutate__simple_arg_underconstrained():
    ast = ["+", ["variable", "aaa"], ["value", 0]]
    tests = [({"aaa": 4}, 4), ({"aaa": 7}, 7)]

    assert not scratch.mutate(ast, tests)
