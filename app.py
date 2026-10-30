"""Maple29 Messenger chatbot webhook.

GET  /webhook  - Meta verification (hub.verify_token / hub.challenge)
POST /webhook  - incoming message/postback events
GET  /         - health check

Conversation state is kept in memory per sender (PSID). Order handoffs are
appended to a JSONL log for the human team.
"""
import logging
import re

from flask import Flask, request

import catalog
import config
import flows
import handoff
import intents
import messenger
from charts import CHARTS

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = Flask(__name__)

# psid -> {"step": str, "product": dict, "chart_name": str|None,
#          "size": str|None, "color": str|None}
sessions = {}

PHONE_RE = re.compile(r"0\d[\d\s\-]{7,}")


def _warn_missing_env():
    for name in ("VERIFY_TOKEN", "PAGE_ACCESS_TOKEN", "LOYVERSE_TOKEN"):
        if not getattr(config, name):
            log.warning("%s is not set", name)


_warn_missing_env()


# --------------------------------------------------------------------------- #
# webhook endpoints
# --------------------------------------------------------------------------- #
@app.get("/")
def index():
    return "maple29-bot ok", 200


@app.get("/webhook")
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token and token == config.VERIFY_TOKEN:
        return challenge or "", 200
    return "Forbidden", 403


@app.post("/webhook")
def webhook():
    data = request.get_json(force=True, silent=True) or {}
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                try:
                    handle_event(event)
                except Exception:  # noqa: BLE001 - one bad event must not 500
                    log.exception("failed handling event")
    return "OK", 200


# --------------------------------------------------------------------------- #
# event routing
# --------------------------------------------------------------------------- #
def handle_event(event):
    sender = event.get("sender", {})
    psid = sender.get("id")
    if not psid:
        return
    if event.get("message", {}).get("is_echo"):
        return  # our own sent messages

    if "postback" in event:
        handle_payload(psid, event["postback"].get("payload", ""))
        return

    msg = event.get("message", {})
    if "quick_reply" in msg:
        handle_payload(psid, msg["quick_reply"].get("payload", ""))
        return
    if msg.get("text"):
        handle_text(psid, msg["text"])
        return
    if msg.get("attachments"):
        handle_attachment(psid, msg["attachments"])
        return


def handle_payload(psid, payload):
    if payload == "DELIVERY":
        messenger.send_text(psid, flows.DELIVERY_INFO)
    elif payload == "ORDER":
        start_order(psid)
    elif payload == "PRICE_SIZE":
        messenger.send_text(psid, flows.ASK_ITEM_NAME)
    elif payload in ("GET_STARTED", "START"):
        send_welcome(psid)
    else:
        handle_text(psid, payload)


def handle_attachment(psid, attachments):
    session = sessions.get(psid)
    has_image = any(a.get("type") == "image" for a in attachments)
    if session and session["step"] == "awaiting_item" and has_image:
        messenger.send_text(psid, flows.PHOTO_RECEIVED)
        return
    # Photo-first customers: begin the order flow at the item step.
    if has_image and not session:
        sessions[psid] = {"step": "awaiting_item"}
        messenger.send_text(psid, flows.PHOTO_RECEIVED)
        return
    messenger.send_text(psid, flows.FALLBACK)
    handoff.log_handoff(psid, "fallback", {"reason": "unhandled_attachment"})


# --------------------------------------------------------------------------- #
# text handling
# --------------------------------------------------------------------------- #
def send_welcome(psid):
    messenger.send_quick_replies(psid, flows.WELCOME, flows.WELCOME_QUICK_REPLIES)


def handle_text(psid, text):
    session = sessions.get(psid)
    if session:
        handle_order_step(psid, text, session)
        return

    intent = intents.detect(text)

    if intent == "greeting":
        send_welcome(psid)
        return

    product = catalog.find_product(text)
    if product:
        handle_product(psid, product, intent, text)
        return

    if intent == "tulip":
        messenger.send_text(psid, flows.TULIP_STOCK)
        handoff.log_handoff(psid, "tulip_stock", {"text": text})
    elif intent == "cod":
        messenger.send_text(psid, flows.COD_INFO)
    elif intent == "delivery":
        messenger.send_text(psid, flows.DELIVERY_INFO)
    elif intent == "preorder":
        messenger.send_text(psid, flows.PREORDER_INFO)
    elif intent == "exchange":
        messenger.send_text(psid, flows.EXCHANGE_INFO)
    elif intent == "how_to_order":
        messenger.send_text(psid, flows.HOW_TO_ORDER)
    elif intent == "order":
        start_order(psid)
    elif intent in ("price", "size", "color", "stock"):
        # keyword but no product identified -> ask which item
        messenger.send_text(psid, flows.ASK_ITEM_NAME)
    else:
        messenger.send_text(psid, flows.FALLBACK)
        handoff.log_handoff(psid, "fallback", {"text": text})


def chart_name_for(product):
    """User-facing chart name for this catalog product, if charted."""
    for user_name, chart in CHARTS.items():
        if catalog.normalize(chart["catalog"]) == catalog.normalize(product["name"]):
            return user_name
    # Zero Waste Pants has its chart in the draft, keyed by user name
    if catalog.normalize(product["name"]) == "zero waste pants":
        return "Zero Waste Pants"
    return None


def handle_product(psid, product, intent, text):
    chart_name = chart_name_for(product)

    if intent == "order":
        order_step2(psid, product, chart_name)
        return

    if intent == "size":
        if chart_name:
            messenger.send_text(psid, flows.chart_message(chart_name))
        else:
            messenger.send_text(psid, flows.NO_CHART)
            handoff.log_handoff(psid, "size_no_chart",
                                {"item": product["name"], "text": text})
        return

    if intent == "color":
        msg = flows.color_message(product)
        if msg:
            messenger.send_text(psid, msg)
        else:
            messenger.send_text(psid, flows.PRICE_UNKNOWN)
            handoff.log_handoff(psid, "color_check",
                                {"item": product["name"], "text": text})
        return

    if intent == "stock":
        messenger.send_text(psid, flows.STOCK_HANDOFF)
        handoff.log_handoff(psid, "stock_check",
                            {"item": product["name"], "text": text})
        return

    # price / general product mention
    msg = flows.price_message(product)
    if msg:
        messenger.send_text(psid, msg + "\n" + flows.PRODUCT_HINT)
    else:
        messenger.send_text(psid, flows.PRICE_UNKNOWN)
        handoff.log_handoff(psid, "price_unknown",
                            {"item": product["name"], "text": text})


# --------------------------------------------------------------------------- #
# order flow state machine (Flow 6)
# --------------------------------------------------------------------------- #
def start_order(psid):
    sessions[psid] = {"step": "awaiting_item"}
    messenger.send_text(psid, flows.ORDER_STEP1)


def order_step2(psid, product, chart_name):
    sessions[psid] = {"step": "awaiting_size", "product": product,
                      "chart_name": chart_name}
    messenger.send_text(psid, flows.order_step2_text(product))
    if chart_name:
        messenger.send_text(psid, flows.chart_message(chart_name))


def handle_order_step(psid, text, session):
    step = session["step"]
    product = session.get("product")

    if step == "awaiting_item":
        found = catalog.find_product(text)
        if not found:
            messenger.send_text(psid, flows.PRICE_UNKNOWN)
            handoff.log_handoff(psid, "price_unknown", {"text": text})
            sessions.pop(psid, None)
            return
        order_step2(psid, found, chart_name_for(found))
        return

    if step == "awaiting_size":
        size = catalog.match_size(product, text)
        if not size:
            sizes = ", ".join(sorted(product["sizes"], key=catalog.size_sort_key))
            messenger.send_text(
                psid, f"Size ကို သေချာမတွေ့ဘူး — {sizes} ထဲက ရွေးပေးပါနော်။")
            return
        session["size"] = size
        session["step"] = "awaiting_color"
        colors = sorted(product["sizes"][size]["colors"])
        if colors:
            messenger.send_text(psid, f"{flows.ASK_COLOR} ({', '.join(colors)})")
        else:
            messenger.send_text(psid, flows.ASK_COLOR)
        return

    if step == "awaiting_color":
        session["color"] = text.strip()
        session["step"] = "awaiting_details"
        messenger.send_text(psid, flows.ORDER_STEP3)
        return

    if step == "awaiting_details":
        details = build_order_details(session, text)
        messenger.send_text(psid, flows.order_summary(details))
        messenger.send_text(psid, flows.ORDER_DONE)
        handoff.log_handoff(psid, "order", details)
        sessions.pop(psid, None)
        return


def build_order_details(session, text):
    product = session["product"]
    size = session.get("size", "")
    info = product["sizes"].get(size, {})
    prices = sorted(info.get("prices", []))
    price = catalog.my_num(f"{prices[0]:,}") if prices else "—"

    phone = ""
    m = PHONE_RE.search(text or "")
    if m:
        phone = m.group(0)

    t = (text or "").lower()
    if "ရန်ကုန်" in t or "yangon" in t:
        delivery_time = "၃-၅ ရက်"
    else:
        delivery_time = "၁ ပတ်"

    return {
        "item": product["name"],
        "size": size,
        "color": session.get("color", ""),
        "price": price,
        "customer_text": text,
        "phone": phone,
        "township": text,
        "delivery_time": delivery_time,
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT)
