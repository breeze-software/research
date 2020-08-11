import operator


def choose_add(ast, _in, _out):
    err_left, val_left = _eval(ast[1], _in)
    err_right, val_right = _eval(ast[2], _in)
    if (not err_left) and (not err_right):
        return False, ast
    if err_left and err_right:
        return True, None
    if err_left and (not err_right):
        # if left is underspecified and right is fully specified
        # we know value of left must equal output minus value of right
        err, chosen = _choose(ast[1], _in, _out - val_right)
        if err:
            return True, None
        return False, [ast[0], chosen, ast[2]]
    if (not err_left) and err_right:
        err, chosen = _choose(ast[2], _in, _out - val_left)
        if err:
            return True, None
        return False, [ast[0], ast[1], chosen]


def choose_sub(ast, _in, _out):
    err_left, val_left = _eval(ast[1], _in)
    err_right, val_right = _eval(ast[2], _in)
    if (not err_left) and (not err_right):
        return ast
    if err_left and err_right:
        return ["INVALID"]
    elif err_left:
        # if left is underspecified and right is fully specified
        # we know value of left must equal output plus value of right
        err, chosen = _choose(ast[1], _in, _out + val_right)
        if err:
            return True, None
        return False, [ast[0], chosen, ast[2]]
    if (not err_left) and err_right:
        # we know value of right must equal value of left minus output
        err, chosen = _choose(ast[2], _in, val_left - _out)
        if err:
            return True, None
        return False, [ast[0], ast[1], chosen]


def _choose(ast, _in, _out):
    if ast[0] == "?int":
        return False, ["value", _out]
    if ast[0] == "variable":
        return False, _eval(ast, _in)
    elif ast[0] in ["+", "-"]:
        f = {"+": choose_add, "-": choose_sub}[ast[0]]
        err, chosen = f(ast, _in, _out)
        if err:
            return True, None
        return False, chosen
    else:
        raise Exception(f"Cannot 'choose' AST of type '{ast[0]}'")


def choose(ast, _in, _out):
    err, result = _choose(ast, _in, _out)
    if err:
        raise TypeError()
    return result


def _eval(ast, _in):
    if ast[0].startswith("?"):
        return True, None
    if ast[0] == "value":
        return False, ast[1]
    if ast[0] == "variable":
        if ast[1] in _in:
            return False, _in[ast[1]]
        else:
            return True, None
    if ast[0] in ["+", "-", "*", "/"]:
        err_left, left = _eval(ast[1], _in)
        err_right, right = _eval(ast[2], _in)
        if err_left or err_right:
            return True, []
        f = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.imul,
            "/": operator.itruediv,
        }[ast[0]]
        return False, f(left, right)
    raise Exception(f"Cannot '_eval' AST of type '{ast[0]}'")


def eval(ast, _in):
    _, out = _eval(ast, _in)
    return out
