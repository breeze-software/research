import itertools
import json
import operator
import random
import sys
import zlib
from copy import deepcopy
from pprint import pprint


def serialize(data):
    return json.dumps(data)


def count_nodes(data):
    if not isinstance(data, list):
        return 1
    out = 0
    for e in data:
        out += count_nodes(e)
    return out


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


def contains_nonconstant(ast):
    if not isinstance(ast, list):
        return False
    if ast[0] == "variable":
        return True
    out = False
    for e in ast:
        out = out or contains_nonconstant(e)
    return out


def add_to_set(programs, ast, inputs):
    ast = simplify_ast(ast)
    ast = normalize_ast(ast)

    if count_nodes(ast) > 20:
        return programs

    outputs = [eval(ast, i) for i in inputs]
    if min(outputs) < -20 or max(outputs) > 20:
        return programs

    s_outputs = serialize(outputs)
    s_ast = serialize(ast)

    if s_outputs not in programs["out_to_source"]:
        programs["out_to_source"][s_outputs] = set()
    programs["out_to_source"][s_outputs].add(s_ast)

    if s_ast not in programs["source_to_ast"]:
        programs["source_to_ast"][s_ast] = {}
    programs["source_to_ast"][s_ast] = ast

    return programs


def get_random_ast(programs):
    return random.choice(list(programs["source_to_ast"].values()))


def normalize_ast(ast):
    if not isinstance(ast, list):
        return ast

    if ast[0] in ["+", "*"] and serialize(ast[1]) > serialize(ast[2]):
        return [ast[0], ast[2], ast[1]]

    # convert '-1 + a' to 'a - 1'
    if (
        ast[0] == "+"
        and isinstance(ast[1], list)
        and ast[1][0] == "value"
        and ast[1][1] < 0
    ):
        return ["-", ast[2], ["value", -1 * ast[1][1]]]

    # convert 'a + -1' to 'a - 1'
    if (
        ast[0] == "+"
        and isinstance(ast[2], list)
        and ast[2][0] == "value"
        and ast[2][1] < 0
    ):
        return ["-", ast[1], ["value", -1 * ast[2][1]]]

    return [normalize_ast(e) for e in ast]


def simplify_ast(ast):
    if not isinstance(ast, list):
        return ast
    # TODO

    if not contains_nonconstant(ast):
        return ["value", eval(ast, {})]

    if ast[0] == "+" and ast[1] == ["value", 0]:
        return ast[2]
    if ast[0] == "+" and ast[2] == ["value", 0]:
        return ast[1]
    if ast[0] == "-" and ast[2] == ["value", 0]:
        return ast[1]
    if ast[0] == "*" and ast[1] == ["value", 1]:
        return ast[2]
    if ast[0] == "*" and ast[2] == ["value", 1]:
        return ast[1]

    return [simplify_ast(e) for e in ast]


def add_layer(corpus):
    out = deepcopy(corpus)
    for a, b in itertools.product(corpus, repeat=2):
        out.append(["+", a, b])
        out.append(["-", a, b])
        out.append(["*", a, b])
    return out


def deduplicate(corpus):
    out = {}
    for ast in corpus:
        ast = simplify_ast(ast)
        ast = normalize_ast(ast)
        out[serialize(ast)] = ast
    return list(out.values())


def get_winner(programs, _inputs, _outputs):
    winners = []
    for p in programs:
        if all(eval(p, i) == o for i, o in zip(_inputs, _outputs)):
            winners.append(p)

    if not winners:
        return "FAILED"

    winners = [(count_nodes(p), p) for p in winners]
    winners = sorted(winners, key=lambda e: e[0])
    return winners[0][1]


def create_seeds(_inputs):
    programs = []
    for val in [-1, 0, 1]:
        p = ["value", val]
        programs.append(p)
    for var in _inputs[0].keys():
        p = ["variable", var]
        programs.append(p)
    return programs


def pivot_io(tests):
    _inputs = []
    _outputs = []
    for i, o in tests:
        _inputs.append(i)
        _outputs.append(o)
    return _inputs, _outputs


def synth(tests):
    _inputs, _outputs = pivot_io(tests)

    programs = create_seeds(_inputs)

    for _ in range(2):
        programs = add_layer(programs)
        programs = deduplicate(programs)

    pprint(get_winner(programs, _inputs, _outputs))

    return None
