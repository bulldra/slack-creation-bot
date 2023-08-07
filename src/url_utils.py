import re
import urllib

import requests


def extract_url(text: str) -> str:
    links: [str] = re.findall(
        r"https?://[a-zA-Z0-9_/:%#\$&\?\(\)~\.=\+\-]+", text or ""
    )
    if len(links) == 0:
        return None
    else:
        canonical_url: str = links[0]
        try:
            with requests.get(canonical_url, stream=True) as res:
                if res.status_code != 200:
                    raise requests.exceptions.RequestException
                else:
                    canonical_url = res.url
        except requests.exceptions.RequestException:
            pass
        return canonical_url


def remove_tracking_query(url: str) -> str:
    tracking_param: [str] = [
        "utm_medium",
        "utm_source",
        "utm_campaign",
        "n_cid",
        "gclid",
        "fbclid",
        "yclid",
        "msclkid",
    ]
    url_obj: urllib.parse.ParseResult = urllib.parse.urlparse(url)
    if url_obj.netloc == b"" or url_obj.netloc == "":
        return None
    query_dict: dict = urllib.parse.parse_qs(url_obj.query)
    new_query: dict = {k: v for k, v in query_dict.items() if k not in tracking_param}
    url_obj = url_obj._replace(
        query=urllib.parse.urlencode(new_query, doseq=True),
        fragment="",
    )
    return urllib.parse.urlunparse(url_obj)
