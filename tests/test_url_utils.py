import collections

import url_utils

Case = collections.namedtuple("Case", ("argument", "expected"))


def test_extract_url():
    case_list = [
        Case(
            argument="https://www.example.com/",
            expected="https://www.example.com/",
        ),
        Case(
            argument="https://www.example.com/?a=1&b=2",
            expected="https://www.example.com/?a=1&b=2",
        ),
        Case(
            argument="https://www.example.com/?utm_medium=1",
            expected="https://www.example.com/",
        ),
        Case(
            argument="https://www.example.com/?a=1&b=2&utm_medium=1",
            expected="https://www.example.com/?a=1&b=2",
        ),
        Case(
            argument="https://www.example.com/?n_cid=1&b=2&utm_medium=1",
            expected="https://www.example.com/?b=2",
        ),
        Case(
            argument="https://www.example.com/?n_cid=1",
            expected="https://www.example.com/",
        ),
        Case(
            argument="https://www.example.com/?utm_medium=1&gclid=1dd",
            expected="https://www.example.com/",
        ),
        Case(
            argument="https://www.example.com/?utm_medium=1&gclid=1dd&a=1&a=2",
            expected="https://www.example.com/?a=1&a=2",
        ),
    ]

    for case in case_list:
        result = url_utils.remove_tracking_query(case.argument)
        print(result)
        assert result == case.expected
