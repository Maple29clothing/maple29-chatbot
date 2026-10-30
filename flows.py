"""All customer-facing reply text — Burmese wording copied exactly from the
approved conversation-flows draft (v2, option-2 stock policy).

RULE: the bot never states stock levels. Prices/sizes/colors come from
Loyverse; availability is always confirmed by the human team.
"""
import catalog
from catalog import my_num, size_sort_key
from charts import CHARTS

# --- Flow 1: welcome ---------------------------------------------------------
WELCOME = "🍁 Maple29 မှ ကြိုဆိုပါတယ်! ဘာကူညီပေးရမလဲ?"
WELCOME_QUICK_REPLIES = [
    ("ဈေးနှုန်း / Size မေးချင်တယ်", "PRICE_SIZE"),
    ("Delivery အကြောင်း သိချင်တယ်", "DELIVERY"),
    ("Order မှာချင်တယ်", "ORDER"),
]

# --- Flow 2: delivery ---------------------------------------------------------
DELIVERY_INFO = (
    "Delivery ခက နေရာပေါ်မူတည်ပါတယ်။\n"
    "🚚 ရန်ကုန် — ၃-၅ ရက်\n"
    "🚚 တခြားမြို့ — ၁ ပတ်အတွင်း\n"
    "ArLuPost courier နဲ့ ပို့ပေးတာပါ။"
)
COD_INFO = (
    "ArLuPost ရောက်တဲ့နေရာဆို cash on delivery ရပါတယ်။ ✅\n"
    "မရောက်တဲ့နေရာဆိုရင်တော့ prepaid ကြိုပေးရပါမယ်။"
)

# --- Flow 3: preorder ----------------------------------------------------------
PREORDER_INFO = (
    "Preorder ပစ္စည်းဆို ၁၀-၂၀ ရက် စောင့်ရပါတယ်။ Half deposit ကြိုပေးရပါမယ်။\n"
    "📌 ဥပမာ: Zero Waste Pants ကတော့ instock ပဲရှိပါတယ် — preorder မရပါ။\n"
    "📌 Tulip Garden Blouse ကတော့ instock ရှိရင် instock ရောင်းပါတယ် — မရှိရင် preorder လက်ခံပါတယ်။"
)
TULIP_STOCK = (
    "Tulip Garden Blouse ကတော့ instock ရှိရင် instock ရောင်းပါတယ် — မရှိရင် preorder လက်ခံပါတယ် (၁၀-၂၀ ရက်၊ half deposit)။\n"
    "လက်ရှိရှိမရှိကို team က စစ်ပေးပါမယ် — နာမည် နဲ့ ဖုန်းလေး ချန်ထားပေးပါနော်။"
)

# --- Flow 4: exchange ----------------------------------------------------------
EXCHANGE_INFO = (
    "လဲပေးပါတယ် — ဒါပေမယ့် အခြေအနေနှစ်မျိုးရှိပါတယ်:\n"
    "✅ စက်ရုံအမှား (factory error) ဒါမှမဟုတ် အထည်အမှား (fabric error) ဆို delivery free နဲ့ လဲပေးပါတယ်\n"
    "❌ ကိုယ်တိုင်ရွေးမှားတဲ့ size ကတော့ လဲမပေးပါဘူး"
)

# --- Flow 5: how to order -------------------------------------------------------
HOW_TO_ORDER = (
    "မှာယူဖို့ လွယ်ပါတယ်:\n"
    "1️⃣ လိုချင်တဲ့ item ရဲ့ screenshot, link ဒါမှမဟုတ် photo ပို့ပေးပါ\n"
    "2️⃣ Size ပြောပေးပါ\n"
    "3️⃣ နာမည်၊ ဖုန်း၊ မြို့နယ်/လိပ်စာ ပေးပါ\n"
    "Team က အတည်ပြုပြီး ဆက်သွယ်ပါမယ်။"
)

# --- Flow 6: order flow ----------------------------------------------------------
ORDER_STEP1 = "ဘယ် item လိုချင်လဲ? Screenshot, link ဒါမှမဟုတ် photo ပို့ပေးပါနော်။"
ORDER_STEP3 = "နာမည်၊ ဖုန်းနံပါတ်၊ မြို့နယ်/လိပ်စာ ပြောပေးပါ။"
ORDER_DONE = "Order လက်ခံရရှိပါပြီ! 🎉 Team က stock စစ်ပြီး မကြာခင် ဆက်သွယ်ပါမယ်။"

# --- Flow 7: size help ------------------------------------------------------------
# Zero Waste Pants keeps the EXACT draft wording.
ZW_PANTS_SIZE_GUIDE = (
    "Zero Waste Pants size လမ်းညွှန် (လက်မနဲ့):\n"
    "📏 **Free Size** — ၄၁,၅၀၀ ကျပ်\n"
    "- ခါး: ၂၄-၃၈\n"
    "- တင်: ၃၄-၄၆\n"
    "- အရှည်: ၃၈-၃၉\n"
    "📏 **2XL** — ၄၄,၀၀၀ ကျပ်\n"
    "- ခါး: ၃၆-၄၄\n"
    "- တင်: ၄၆-၅၆\n"
    "Instock ပဲရှိပါတယ်။"
)
NO_CHART = (
    "အဲဒီ item ရဲ့ size chart မရှိသေးပါဘူး — team ကို မေးပေးပါမယ်။ "
    "နာမည် နဲ့ ဖုန်းလေး ချန်ထားပေးပါနော်။"
)

# --- Flow 8: price ---------------------------------------------------------------
STOCK_HANDOFF = (
    "လက်ရှိရှိမရှိကို team က စစ်ပေးပါမယ် — နာမည် နဲ့ ဖုန်းလေး ချန်ထားပေးပါနော်။"
)
PRICE_UNKNOWN = (
    "ဈေးလေးကို team က စစ်ပြီး ဖြေပေးပါမယ် — နာမည် နဲ့ ဖုန်းလေး ချန်ထားပေးပါနော်။"
)

# --- Flow 10: fallback ------------------------------------------------------------
FALLBACK = (
    "သေချာနားမလည်လိုက်ဘူး 😅 Team ကို လွှဲပေးပါမယ် — ခဏစောင့်ပေးပါနော်။"
)

# --- helper prompts (same voice, not in the draft but needed for the flow) ------
ASK_ITEM_NAME = "ဘယ် item ရဲ့ ဈေး/size သိချင်လဲ? နာမည်လေး ရိုက်ပေးပါနော်။"
ASK_COLOR = "အရောင် ဘယ်ဟာယူမလဲ?"
PHOTO_RECEIVED = "Photo လက်ခံရရှိပါတယ်! Item နာမည်လေး ရိုက်ပေးပါနော်။"
PRODUCT_HINT = "Size လမ်းညွှန်လိုချင်ရင် 'size' လို့ ရိုက်ပါ။ အရောင်သိချင်ရင် 'အရောင်' လို့ ရိုက်ပါ။"


def chart_message(user_product_name):
    """Flow 7: inch measurements + price per size for a charted product."""
    if user_product_name == "Zero Waste Pants":
        return ZW_PANTS_SIZE_GUIDE
    chart = CHARTS.get(user_product_name)
    if not chart:
        return None
    lines = [f"{user_product_name} size လမ်းညွှန် (လက်မနဲ့):"]
    for e in chart["entries"]:
        if e["price"]:
            lines.append(f"📏 {e['size']} — {my_num(e['price'])} ကျပ်")
        else:
            lines.append(f"📏 {e['size']} — ဈေးကို team က ပြောပေးပါမယ်")
        if e.get("measure"):
            lines.append(f"- {e['measure']}")
    if chart.get("note"):
        lines.append(chart["note"])
    return "\n".join(lines)


def price_message(product):
    """Flow 8: '[item] — [size]: [price] ကျပ်' lines. None if no fixed price."""
    lines = catalog.price_lines(product)
    fixed = [(s, p) for s, p in lines if p]
    if not fixed:
        return None
    out = [product["name"]]
    for size, price in fixed:
        out.append(f"- {size}: {my_num(price)} ကျပ်")
    return "\n".join(out)


def order_step2_text(product):
    """Flow 6 Step 2: '[Item] — [price] ကျပ်။ Size ဘယ်လောက်ယူမလဲ? ([sizes])'"""
    lines = catalog.price_lines(product)
    fixed_prices = sorted({p for _, p in lines if p},
                          key=lambda p: int(p.replace(",", "")))
    if len(fixed_prices) == 1:
        price_txt = my_num(fixed_prices[0])
    elif fixed_prices:
        price_txt = f"{my_num(fixed_prices[0])}–{my_num(fixed_prices[-1])}"
    else:
        price_txt = None
    sizes = ", ".join(s for s, _ in lines)
    if price_txt:
        return f"{product['name']} — {price_txt} ကျပ်။ Size ဘယ်လောက်ယူမလဲ? ({sizes})"
    return f"{product['name']}။ Size ဘယ်လောက်ယူမလဲ? ({sizes})"


def color_message(product, size=None):
    """Flow 9: '[item] — [size] ဆို [colors]… ဆိုပြီး ထွက်ပါတယ်'."""
    if size and size in product["sizes"]:
        colors = sorted(product["sizes"][size]["colors"])
        size_txt = size
    else:
        colors = catalog.all_colors(product)
        size_txt = ", ".join(sorted(product["sizes"], key=size_sort_key))
    if not colors:
        return None
    shown = ", ".join(colors[:12])
    if len(colors) > 12:
        shown += "…"
    return f"{product['name']} — {size_txt} ဆို {shown} ဆိုပြီး ထွက်ပါတယ်"


def order_summary(details):
    """Flow 6 Step 4: order summary for the team check."""
    return (
        "Order အကျဉ်း:\n"
        f"- Item: {details.get('item', '—')}\n"
        f"- Size: {details.get('size', '—')}\n"
        f"- အရောင်: {details.get('color', '—')}\n"
        f"- ဈေး: {details.get('price', '—')} ကျပ် (Loyverse live price)\n"
        f"- Delivery: {details.get('township', '—')} — {details.get('delivery_time', '၁ ပတ်')}\n"
        "- ငွေပေး: COD / prepaid (team က အတည်ပြုပေးပါမယ်)\n"
        "\n"
        "Team က stock ရှိမရှိ စစ်ပြီး အတည်ပြုပေးပါမယ် ✅"
    )
