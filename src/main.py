import json
import logging
import os

import flask
import functions_framework
import google.cloud.logging
import slack_bolt
from slack_bolt.adapter.google_cloud_functions import SlackRequestHandler

import url_utils

logging_client: google.cloud.logging.Client = google.cloud.logging.Client()
logging_client.setup_logging()
logger: logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

SECRETS: dict = json.loads(os.getenv("SECRETS"))
app: slack_bolt.App = slack_bolt.App(
    token=SECRETS.get("SLACK_BOT_TOKEN"),
    signing_secret=SECRETS.get("SLACK_SIGNING_SECRET"),
    request_verification_enabled=True,
)


@app.event("reaction_added")
def handle_reaction_added(event: dict):
    if event["reaction"] == SECRETS.get("REACTION_EMOJI"):
        channel_id: str = event["item"]["channel"]
        ts: str = event["item"]["ts"]
        result: dict = app.client.conversations_history(
            channel=channel_id, inclusive=True, latest=ts, limit=1
        )
        logger.debug(f"reaction at: {result}")

        text: str = result["messages"][0]["text"]
        link: str = url_utils.extract_url(text)
        link = url_utils.remove_tracking_query(link)

        if link is not None:
            app.client.chat_postMessage(
                channel=SECRETS.get("SHARE_CHANNEL_ID"), text=link, unfurl_links=True
            )


@functions_framework.http
def main(request: flask.Request):
    if request.method != "POST":
        return ("Only POST requests are accepted", 405)
    if request.headers.get("x-slack-retry-num"):
        return ("No need to resend", 200)

    content_type: str = request.headers.get("Content-Type")
    if content_type == "application/json":
        body: dict = request.get_json()
        if body.get("type") == "url_verification":
            headers: dict = {"Content-Type": "application/json"}
            res: str = json.dumps({"challenge": body.get("challenge")})
            return (res, 200, headers)
        else:
            return SlackRequestHandler(app).handle(request)
    elif content_type == "application/x-www-form-urlencoded":
        return SlackRequestHandler(app).handle(request)
    else:
        return ("Bad Request", 400)
