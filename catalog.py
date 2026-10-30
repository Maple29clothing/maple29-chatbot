"""Loyverse catalog access with in-memory TTL cache.

Auth: LOYVERSE_TOKEN env var, sent as a Bearer header (personal access token
created in Loyverse Back Office -> Integrations). No redirects on requests.

Builds an index: normalized product name -> {
    "name": catalog item_name,
    "sizes": { size_value: {"prices": set[int], "colors": set[str],
                            "variable": bool} },
}

IMPORTANT (option-2 stock policy): stock/inventory is fetched nowhere here on
purpose. The bot must NEVER state stock levels to customers until the
merchant's Loyverse inventory is stable. Price/size/color info only.
"""
import logging
import threading
import time

import requests

import config

log = logging.getLogger(__name__)

MY_DIGITS = str.maketrans("0123456789", "၀၁၂၃၄၅၆၇၈၉")


def my_num(value):
    """Render digits in Myanmar numerals for customer-facing text."""
    return str(value).translate(MY_DIGITS)


def fmt_price(amount):
    """12345 -> '12,345' then Myanmar numerals at render time."""
    return f"{int(amount):,}"


SIZE_ORDER = ["XS", "S", "M", "L", "XL", "2XL", "3XL", "4XL", "5XL", "6XL",
              "7XL", "Free", "F", "C"]


def size_sort_key(size):
    low = str(size).lower()
    if low.startswith("free"):
        return (SIZE_ORDER.index("Free"), str(size))
    return (SIZE_ORDER.index(size) if size in SIZE_ORDER else 99, str(size))


def normalize(name):
    return " ".join((name or "").lower().split())


def _fetch_items():
    """Page through /v1.0/items. Raises on failure."""
    headers = {"Authorization": f"Bearer {config.LOYVERSE_TOKEN}"}
    items, cursor = [], None
    while True:
        url = f"{config.LOYVERSE_BASE}/v1.0/items?limit=250"
        if cursor:
            url += f"&cursor={cursor}"
        # redirects stay disabled on authenticated requests
        r = requests.get(url, headers=headers, timeout=30, allow_redirects=False)
        r.raise_for_status()
        data = r.json()
        items.extend(data.get("items", []))
        cursor = data.get("cursor")
        if not cursor:
            break
    return items


def _build_index(items):
    products = {}
    for it in items:
        name = it.get("item_name") or ""
        if not name:
            continue
        size_idx = color_idx = None
        for i in (1, 2, 3):
            opt_name = (it.get(f"option{i}_name") or "").lower()
            if "size" in opt_name:
                size_idx = i
            elif "color" in opt_name or "colour" in opt_name:
                color_idx = i
        sizes = {}
        for v in it.get("variants") or []:
            if v.get("deleted_at"):
                continue
            if size_idx:
                size = v.get(f"option{size_idx}_value") or "one size"
            else:
                size = v.get("option1_value") or "one size"
            color = v.get(f"option{color_idx}_value") if color_idx else None
            stores = v.get("stores") or []
            if stores:
                price = stores[0].get("price")
                ptype = stores[0].get("pricing_type")
            else:
                price = v.get("default_price")
                ptype = v.get("default_pricing_type")
            entry = sizes.setdefault(
                size, {"prices": set(), "colors": set(), "variable": False}
            )
            if ptype == "VARIABLE" or price is None:
                entry["variable"] = True
            else:
                try:
                    entry["prices"].add(int(float(price)))
                except (TypeError, ValueError):
                    entry["variable"] = True
            if color:
                entry["colors"].add(color)
        products[normalize(name)] = {"name": name, "sizes": sizes}

    # User-verified facts override: the live catalog has no usable 2XL entry
    # for Zero Waste Pants, but the merchant confirmed Free 41,500 / 2XL 44,000.
    zwp = products.get("zero waste pants")
    if zwp:
        zwp["sizes"] = {
            "Free Size": {
                "prices": {41500},
                "colors": zwp["sizes"].get("Free", {}).get("colors", set()),
                "variable": False,
            },
            "2XL": {"prices": {44000}, "colors": set(), "variable": False},
        }
    return products


_cache = {"at": 0.0, "products": None}
_lock = threading.Lock()
_warned_no_token = False


def get_products():
    """Return the cached product index, refreshing after the TTL.

    Returns None when Loyverse is unreachable (callers must hand off to the
    team instead of guessing). Serves stale cache on transient failures.
    """
    global _warned_no_token
    if not config.LOYVERSE_TOKEN:
        if not _warned_no_token:
            log.warning("LOYVERSE_TOKEN not set - product lookups disabled")
            _warned_no_token = True
        return None
    now = time.time()
    with _lock:
        if _cache["products"] is not None and now - _cache["at"] < config.CATALOG_TTL_SECONDS:
            return _cache["products"]
        try:
            products = _build_index(_fetch_items())
        except Exception as e:  # noqa: BLE001 - serve stale rather than fail
            log.warning("Loyverse refresh failed: %s", e)
            return _cache["products"]
        _cache["products"] = products
        _cache["at"] = now
        log.info("Loyverse catalog refreshed: %d products", len(products))
        return products


# --- product name matching -------------------------------------------------
# user-facing name -> normalized catalog name (for names that differ)
ALIASES = {
    "vietnamese blouse": "vietnam blouse",
    "bowtie vietnam blouse": "bow tie vietnam blouse",
    "summer escape mermaid top": "summer escape midmaid blouse",
    "plus size short sleeve shirt": "over size short sleeve shirt",
    "zero waste crop top": "zero waste top short sleeves",
    "zero waste short sleeve": "zero waste top short sleeves",
    "plus size zero waste pants": "zero waste plus size pants tissue",
    "plus size stripe pants": "zero waste stripe pant",
    "vest": "cheik vest",
}


def find_product(text, products=None):
    """Return the product dict whose name/alias appears in text, or None.

    Longest match wins so 'zero waste plus size pants' beats 'zero waste pants'.
    """
    if products is None:
        products = get_products()
    if not products:
        return None
    t = normalize(text)
    candidates = []
    for alias, canonical in ALIASES.items():
        if alias in t and canonical in products:
            candidates.append((len(alias), products[canonical]))
    for name in products:
        if len(name) >= 4 and name in t:
            candidates.append((len(name), products[name]))
    if not candidates:
        return None
    candidates.sort(key=lambda c: c[0], reverse=True)
    return candidates[0][1]


def match_size(product, text):
    """Fuzzy-match a size string against the product's sizes."""
    t = normalize(text)
    for size in product["sizes"]:
        if normalize(size) == t:
            return size
    for size in product["sizes"]:
        if normalize(size) in t or t in normalize(size):
            return size
    return None


def all_colors(product):
    colors = set()
    for info in product["sizes"].values():
        colors |= info["colors"]
    return sorted(colors)


def price_lines(product):
    """Return [(size, 'p1, p2' or None)] with fixed prices; None = variable."""
    out = []
    for size in sorted(product["sizes"], key=size_sort_key):
        info = product["sizes"][size]
        if info["prices"]:
            out.append((size, ", ".join(fmt_price(p) for p in sorted(info["prices"]))))
        else:
            out.append((size, None))
    return out
