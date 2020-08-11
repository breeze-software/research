import operator
import random
from copy import deepcopy


def eval(ast, _in):
    if ast[0] == "value":
        return ast[1]
    if ast[0] == "variable":
        return _in[ast[1]]
    if ast[0] in ["+", "-", "*", "/"]:
        f = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.imul,
            "/": operator.itruediv,
        }[ast[0]]
        return f(eval(ast[1], _in), eval(ast[2], _in))
    raise Exception(f"Cannot 'eval' AST of type '{ast[0]}'")


def _walk(ast):
    if not isinstance(ast, list):
        yield []
        return

    # if ast[0] in ["value"]:
    #    yield [0] + [ast]
    #    return

    for i, e in enumerate(ast):
        for elem in _walk(e):
            yield [i] + elem


def walk(ast):
    return [[]] + list(_walk(ast))


def validate(ast, tests):
    for i, o in tests:
        if not eval(ast, i) == o:
            return False
    return True


def vary(path, ast):
    if path:
        for e in vary(path[1:], ast[path[0]]):
            new_ast = deepcopy(ast)
            new_ast[path[0]] = e
            yield new_ast
        return

    if isinstance(ast, int):
        yield ast - 1
        yield ast + 1
        for _ in range(100):
            n = random.randint(-10, 10)
            if n == 0:
                continue
            yield ast + n
        return
    if isinstance(ast, list) and len(ast) == 3 and ast[0] == "+":
        yield ["-"] + ast[1:]
        yield ast[1]
        yield ast[2]
        return


def mutate(ast, tests):
    # program should pass tests initially
    if not validate(ast, tests):
        return False

    # no mutation should still pass
    for path in walk(ast):
        for a in vary(path, ast):
            if validate(a, tests):
                return False

    return True
