"""
slack_link_utils.pyのテスト
"""
import collections

import common.scraping_utils as scraping_utils

Case = collections.namedtuple("Case", ("argument", "expected"))


def test_is_not_scraping_url():
    """.env"""
    case_list = [
        Case(argument=None, expected=False),
        Case(argument="", expected=False),
        Case(argument="https://www.example.com/", expected=True),
        Case(argument="https://twitter.com/", expected=False),
        Case(
            argument="https://twitter.com/fladdict/status/168\
7823985223049216?s=12&t=IvjulIA2mH3OtCURIsDoVw",
            expected=False,
        ),
    ]

    for case in case_list:
        actual = scraping_utils.is_allow_scraping(case.argument)
        print(
            f"""scraping_utils.is_allow_scraping('{case.argument}')
assert '{actual}' == '{case.expected}'"""
        )
        assert actual == case.expected


def test_scraping():
    """test scraping"""
    site = scraping_utils.scraping("https://note.com/shi3zblog/n/nca77cd7fe0c1")
    print(site)
