import scratch


def test__synth():
    f = lambda a, b, c: a + b * c
    tests = [
        ({"aaa": 2, "bbb": 3, "ccc": 5}, f(2, 3, 5)),
        ({"aaa": 1, "bbb": 2, "ccc": 3}, f(1, 2, 3)),
        ({"aaa": 4, "bbb": 2, "ccc": 1}, f(4, 2, 1)),
    ]
    print(scratch.synth(tests))
