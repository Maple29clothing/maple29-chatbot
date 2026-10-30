# Maple29 Messenger Chatbot — deploy guide

The bot is a small Flask webhook. Meta sends it every Page message; it replies
in Burmese using the approved conversation flows, with prices/sizes/colors
from your Loyverse catalog. It never states stock levels — the team confirms
availability (option-2 policy).

## 1. Tokens you need

| Env var | Where to get it |
|---|---|
| `VERIFY_TOKEN` | You invent it: any long random string. You will type the same string into the Meta app dashboard. |
| `PAGE_ACCESS_TOKEN` | Meta app dashboard → your app → Messenger → Access tokens → generate for the Maple-29 Page. |
| `LOYVERSE_TOKEN` | Loyverse Back Office → Integrations → +Add Access Token. Personal access token, read-only use. |

No token goes in code or git — only in environment variables.

## 2. Deploy (pick one)

**Render** (simplest):
1. Push this `bot/` folder to a GitHub repo.
2. Render → New → Web Service → connect the repo. Render detects the Dockerfile.
3. Add the three env vars above (Environment tab). Leave `PORT` unset — Render provides it.
4. Deploy. Note your service URL, e.g. `https://maple29-bot.onrender.com`.

**Railway:** New Project → Deploy from GitHub → add env vars → deploy. Same Dockerfile works.

**Fly.io:** `fly launch` in this folder (accept the Dockerfile), then `fly secrets set VERIFY_TOKEN=… PAGE_ACCESS_TOKEN=… LOYVERSE_TOKEN=…`, then `fly deploy`.

Any host works as long as the webhook URL is **https**.

## 3. Connect the Meta app

You need a Meta developer app with the Messenger product (this is the
step-by-step part we do together):

1. [developers.facebook.com](https://developers.facebook.com) → create an app (type: Business) → add the **Messenger** product.
2. Messenger → Settings → **Webhooks** → Add Callback URL:
   - Callback URL: `https://<your-host>/webhook`
   - Verify Token: the same `VERIFY_TOKEN` string from step 1.
   - Click Verify and Save.
3. On the same page, **Subscribe** the webhook to these fields: `messages`, `messaging_postbacks`.
4. Still under Messenger → generate a **Page access token** for the Maple-29 Page and put it in `PAGE_ACCESS_TOKEN`.
5. Subscribe the app to the Page (Messenger → Settings → Add/Subscribe Page), or the Page won't deliver events.
6. While testing, keep the app in Development mode and add testers; switch to Live when ready.

## 4. Test

1. Open the Maple-29 Page in Messenger and send `hello` → you should get the Burmese welcome with quick replies.
2. Try: `Zero Waste Pants ဈေးဘယ်လောက်`, `delivery ဘယ်နှစ်ရက်`, `order မှာချင်တယ်`.
3. Check the host's logs, and `handoffs.jsonl` — every team handoff (orders, stock checks, fallbacks) is appended there as JSON, one line per event.

## 5. Day-to-day

- **Prices/sizes/colors** come from Loyverse, cached 15 minutes. Update them in Loyverse Back Office; the bot picks them up automatically.
- **Stock:** the bot never quotes stock. Keep fixing the Loyverse inventory counts; when they're trustworthy we flip the bot to live stock answers.
- **Handoffs:** read `handoffs.jsonl` (or ship it to wherever the team works) — it has every order with item/size/color/price/phone/township.

## Troubleshooting

- Webhook verify fails → `VERIFY_TOKEN` env var and dashboard string must match exactly.
- Bot doesn't reply → check the app is subscribed to the Page, the Page token is valid, and the app has the `messages` field subscribed.
- "ဈေးလေးကို team က စစ်ပြီး…" for everything → `LOYVERSE_TOKEN` missing/invalid; check host logs for `Loyverse refresh failed`.
