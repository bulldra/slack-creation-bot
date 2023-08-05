import json
import os


def test_auth():
    with open("secrets.json", "r") as f:
        secrets = json.load(f)
        os.environ["SECRETS"] = json.dumps(secrets)
        import main

        print(main.SECRETS.get("SLACK_SIGNING_SECRET"))
        print(main.SECRETS.get("SLACK_BOT_TOKEN"))
        print(main.SECRETS.get("SHARE_CHANNEL_ID"))
