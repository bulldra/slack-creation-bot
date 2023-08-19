"""
main test
"""
import json
import os

with open("secrets.json", "r", encoding="utf-8") as secret_file:
    secrets = json.load(secret_file)
    os.environ["SECRETS"] = json.dumps(secrets)
    import main


def test_auth():
    """.env"""
    print(main.SECRETS.get("SLACK_SIGNING_SECRET"))
    print(main.SECRETS.get("SLACK_BOT_TOKEN"))
    print(main.SECRETS.get("SHARE_CHANNEL_ID"))
