"""Append-only JSONL log of everything handed to the human team.

Each line: {"ts": ..., "psid": ..., "kind": ..., ...details}
kinds: order, stock_check, price_unknown, size_no_chart, color_check,
       tulip_stock, fallback
"""
import json
import logging
from datetime import datetime, timezone

import config

log = logging.getLogger(__name__)


def log_handoff(psid, kind, details=None):
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "psid": psid,
        "kind": kind,
    }
    if details:
        entry.update(details)
    try:
        with open(config.HANDOFF_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:  # noqa: BLE001 - logging must never crash the bot
        log.warning("handoff log failed: %s", e)
