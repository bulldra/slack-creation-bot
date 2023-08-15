"""
slack_link_utils.pyのテスト
"""
import collections

import slack_link_utils

Case = collections.namedtuple("Case", ("argument", "expected"))


def test_extract_url():
    """
    extract_urlのテスト
    """
    case_list = [
        Case(
            argument=None,
            expected=None,
        ),
        Case(
            argument="",
            expected=None,
        ),
        Case(
            argument="<https://www.example.com/?utm_medium=1&gclid=1dd&a=1&a=2|aa>",
            expected="https://www.example.com/?utm_medium=1&gclid=1dd&a=1&a=2",
        ),
        Case(
            argument="あいう<https://www.example.com/?a=1&a=2|aa>",
            expected="https://www.example.com/?a=1&a=2",
        ),
        Case(
            argument="あいう<https://www.example.com/?a=2>ああ",
            expected="https://www.example.com/?a=2",
        ),
        Case(
            argument="あいう<https://www.du-soleil.com/?abc=1>ああ",
            expected="https://www.du-soleil.com/?abc=1",
        ),
        Case(
            argument="ああhttps://www.example.com/?utm_medium=1&gclid=1dd&a=1&"
            "a=2#aaaあい",
            expected="https://www.example.com/?utm_medium=1&gclid=1dd&a=1&a=2#aaa",
        ),
        Case(
            argument="あhttps://slack.com/intl/ja-jp/help/articles/218688467-Slack-%E"
            "3%81%AB-RSS-%E3%83%95%E3%82%A3%E3%83%BC%E3%83%89%E3%82%92%E8%BF%BD%E5%8A"
            "%A0%E3%81%99%E3%82%8Bああ",
            expected="https://slack.com/intl/ja-jp/help/articles/218688467-Slack-%E3"
            "%81%AB-RSS-%E3%83%95%E3%82%A3%E3%83%BC%E3%83%89%E3%82%92%E8%BF%BD%E5%8A"
            "%A0%E3%81%99%E3%82%8B",
        ),
    ]
    for case in case_list:
        actual = slack_link_utils.extract_url(case.argument)
        print(
            f"""slack_link_utils.extract_url('{case.argument}')
assert '{actual}' == '{case.expected}'"""
        )

        assert actual == case.expected


def test_redirect_url():
    """
    redirect_urlのテスト
    """
    case_list = [
        Case(
            argument=None,
            expected=None,
        ),
        Case(
            argument="",
            expected=None,
        ),
        Case(
            argument="https://www.google.com/url?rct=j&sa=t&url=https://www.mapion.co"
            ".jp/news/release/000000056.000019803/&ct=ga&cd=CAIyHDMxZDQ1MjNhNDQ1ODNjZ"
            "jg6Y28uanA6amE6SlA&usg=AOvVaw0Hut30ozpDqyRMJ8wtezpt",
            expected="https://www.mapion.co.jp/news/release/000000056.000019803/",
        ),
        Case(
            argument="https://www.example.com/?a=1&b=2",
            expected="https://www.example.com/?a=1&b=2",
        ),
        Case(
            argument="https://www.google.com/url?rct=j",
            expected="https://www.google.com/url?rct=j",
        ),
    ]

    for case in case_list:
        actual = slack_link_utils.redirect_url(case.argument)
        print(
            f"""slack_link_utils.redirect_url('{case.argument}')
assert '{actual}' == '{case.expected}'"""
        )

        assert actual == case.expected


def test_canonicalize_url():
    """
    canonicalize_urlのテスト
    """
    case_list = [
        Case(
            argument=None,
            expected=None,
        ),
        Case(
            argument="",
            expected=None,
        ),
        Case(
            argument="https://t.co/9nalLlGkkj?amp=1",
            expected="https://www.du-soleil.com/entry/slack-url-share",
        ),
    ]
    for case in case_list:
        actual = slack_link_utils.canonicalize_url(case.argument)
        print(
            f"""slack_link_utils.canonicalize_url('{case.argument}')
assert '{actual}' == '{case.expected}'"""
        )

        assert actual == case.expected


def test_remove_tracking_url():
    """
    test_remove_tracking_urlのテスト
    """

    case_list = [
        Case(
            argument=None,
            expected=None,
        ),
        Case(
            argument="",
            expected=None,
        ),
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
        Case(
            argument="https://www.example.com/?utm_medium=1&gclid=1dd&a=1&a=2#aaa",
            expected="https://www.example.com/?a=1&a=2",
        ),
    ]

    for case in case_list:
        actual = slack_link_utils.remove_tracking_query(case.argument)
        print(
            f"""url_utils.remove_tracking_query('{case.argument}')
assert '{actual}' == '{case.expected}'"""
        )
        assert actual == case.expected
