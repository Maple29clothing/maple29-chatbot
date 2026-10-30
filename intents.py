"""Keyword/regex intent detection (Burmese + English). No ML.

detect(text) -> one of:
  greeting, tulip, cod, delivery, preorder, exchange, how_to_order,
  price, size, color, stock, order, none
"""
import re

_GREETING = re.compile(
    r"^(မင်္ဂလာပါ|မဂ်လာပါ|hello|hi|hey|ဟယ်လို|ဟိုင်း)[!！\s?.…]*$", re.IGNORECASE
)

# (intent, [patterns]) in priority order
_PATTERNS = [
    ("tulip", [r"tulip"]),
    ("cod", [r"\bcod\b", r"cash on delivery", r"ငွေချေ", r"အိမ်ရောက်ငွေချေ"]),
    ("preorder", [r"pre[\s\-]?order", r"ပရီ", r"ကြိုတင်", r"ကြိုမှ"]),
    ("exchange", [r"exchange", r"လဲလို့", r"\bလဲ\b", r"\breturn\b", r"refund", r"အလဲအထပ်"]),
    ("how_to_order", [r"ဘယ်လိုမှာ", r"how to order", r"မှာနည်း", r"ဘယ်လိုဝယ်"]),
    ("delivery", [
        r"delivery", r"ပို့ခ", r"ပို့ဆောင်", r"ပို့ပေး", r"ဘယ်နှရက်",
        r"ဘယ်နှစ်ရက်", r"ကြာချိန်", r"shipping", r"ပို့စ်တင်",
    ]),
    ("size", [r"\bsize\b", r"ဆိုဒ်", r"လမ်းညွှန်", r"size chart", r"ပေကြိုး"]),
    ("color", [r"အရောင်", r"\bcolors?\b", r"\bcolours?\b", r"ကာလာ"]),
    ("price", [r"ဈေး", r"\bprice\b", r"ဘယ်လောက်", r"ဈေးနှုန်း", r"\bcost\b", r"တန်ဖိုး"]),
    ("stock", [r"ရှိသေးလား", r"ရှိလား", r"\binstock\b", r"in stock", r"ကုန်နေ",
               r"ပစ္စည်းရှိ", r"ရသေးလား"]),
    ("order", [r"\border\b", r"မှာချင်", r"ဝယ်ချင်", r"မှာမယ်", r"\bယူမယ်\b",
               r"လိုချင်", r"ဝယ်မယ်"]),
]

_COMPILED = [(intent, [re.compile(p, re.IGNORECASE) for p in pats])
             for intent, pats in _PATTERNS]


def detect(text):
    t = (text or "").strip()
    if not t:
        return "none"
    if _GREETING.match(t):
        return "greeting"
    for intent, regexes in _COMPILED:
        for rx in regexes:
            if rx.search(t):
                return intent
    return "none"
