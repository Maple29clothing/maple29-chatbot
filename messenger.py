"""Thin client for the Messenger Send API."""
import logging

import requests

import config

log = logging.getLogger(__name__)


def _post(payload):
    url = f"https://graph.facebook.com/{config.GRAPH_VERSION}/me/messages"
    try:
        r = requests.post(
            url,
            params={"access_token": config.PAGE_ACCESS_TOKEN},
            json=payload,
            timeout=15,
        )
        if r.status_code != 200:
            log.warning("Send API %s: %s", r.status_code, r.text[:300])
        return r.status_code == 200
    except Exception as e:  # noqa: BLE001 - must not crash the webhook
        log.warning("Send API error: %s", e)
        return False


def send_text(psid, text):
    """Send a plain text message."""
    return _post({"recipient": {"id": psid}, "message": {"text": text}})


def send_quick_replies(psid, text, replies):
    """Send text with quick-reply buttons. replies: list of (title, payload)."""
    qr = [
        {"content_type": "text", "title": title, "payload": payload}
        for title, payload in replies
    ]
    return _post(
        {"recipient": {"id": psid}, "message": {"text": text, "quick_replies": qr}}
    )
