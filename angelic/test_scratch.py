import scratch


def test__choose_int():
    """ ?int? == 4 """
    ast = ["?int"]
    _in = {}
    _out = 4

    specified = scratch.choose(ast, _in, _out)
    assert scratch.eval(specified, _in) == _out


def test__choose__add():
    """ 3 + ?int? == 5 """
    ast = ["+", ["value", 3], ["?int"]]
    _in = {}
    _out = 5

    specified = scratch.choose(ast, _in, _out)
    assert scratch.eval(specified, _in) == _out


def test__choose__deep_add():
    """ ((1 + 2) + (3 + 4)) + ((5 + ?int?) + (7 + 8)) == 0 """
    ast = [
        "+",
        ["+", ["+", ["value", 1], ["value", 2]], ["+", ["value", 3], ["value", 4]]],
        ["+", ["+", ["value", 5], ["?int"]], ["+", ["value", 7], ["value", 8]]],
    ]
    _in = {}
    _out = 0

    specified = scratch.choose(ast, _in, _out)
    assert scratch.eval(specified, _in) == _out


def test__choose__add_and_sub():
    """ 3 + (?int? - 4) == 5 """
    ast = ["+", ["value", 3], ["-", ["?int"], ["value", 4]]]
    _in = {}
    _out = 5

    specified = scratch.choose(ast, _in, _out)
    assert scratch.eval(specified, _in) == _out


def test__choose__inputs():
    """ aaa=2; aaa + ?int? == 3 """
    ast = ["+", ["variable", "aaa"], ["?int"]]
    _in = {"aaa": 2}
    _out = 3

    specified = scratch.choose(ast, _in, _out)
    assert scratch.eval(specified, _in) == _out
