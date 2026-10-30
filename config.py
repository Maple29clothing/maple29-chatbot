"""Environment-based configuration. No secrets in code."""
import os

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "")
LOYVERSE_TOKEN = os.environ.get("LOYVERSE_TOKEN", "")
PORT = int(os.environ.get("PORT", "8080"))
HANDOFF_LOG = os.environ.get("HANDOFF_LOG", "handoffs.jsonl")
CATALOG_TTL_SECONDS = int(os.environ.get("CATALOG_TTL_SECONDS", "900"))  # 15 min
GRAPH_VERSION = "v19.0"
LOYVERSE_BASE = "https://api.loyverse.com"
