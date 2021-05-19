import scratch


def test_trace_simple():
    _in = {"aaa": 4}
    ast = [
        "+",
        ["+", ["+", ["variable", "aaa"], ["value", 1]], ["value", 2]],
        ["value", 3],
    ]
    trace = scratch.trace(ast, _in)
    expected = [
        4,
        ["+", "_", ["value", 1]],
        5,
        ["+", "_", ["value", 2]],
        7,
        ["+", "_", ["value", 3]],
        10,
    ]

    assert trace == expected


def test_trace_multi():
    _in = {"aaa": 4, "bbb": 7}
    ast = ["+", ["+", ["variable", "aaa"], ["value", 1]], ["variable", "bbb"]]
    trace = scratch.trace(ast, _in)
    expected = [([4], ["+", "_", ["value", 1]], 5), ([4, 7], ["+", "_", "_"], 11)]

    assert trace == expected
