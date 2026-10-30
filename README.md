# Maple29 Messenger chatbot — webhook server

Flask webhook implementing the 10 approved conversation flows
(`../conversation-flows-draft.md`, v2, option-2 stock policy: prices, sizes
and colors from Loyverse; the bot never states stock levels — the human team
confirms availability).

## Layout

| File | What it does |
|---|---|
| `app.py` | Webhook verification, event routing, order-flow state machine |
| `config.py` | Env vars (`VERIFY_TOKEN`, `PAGE_ACCESS_TOKEN`, `LOYVERSE_TOKEN`, `PORT`, …) |
| `messenger.py` | Send API client (text + quick replies) |
| `catalog.py` | Loyverse `/v1.0/items` fetch, 15-min TTL cache, product index, name matching, Myanmar-numeral prices |
| `charts.py` | The 16 user-confirmed size charts (measurements + prices) |
| `intents.py` | Keyword/regex intent detection (Burmese + English) |
| `flows.py` | Every reply string, copied exactly from the approved draft |
| `handoff.py` | JSONL log of everything handed to the team |

## Run locally

```bash
cd ~/workspace/maple29-chatbot/bot
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in real tokens
python app.py
```

Expose it for Meta with e.g. `ngrok http 8080`, then set the webhook callback
to `https://<ngrok-url>/webhook`.

## Deploy

See [DEPLOY.md](DEPLOY.md). Any host that serves the Dockerfile over https
works (Render / Railway / Fly.io).

## Notes / assumptions

- Zero Waste Pants prices/sizes come from the merchant-confirmed facts
  (Free 41,500 / 2XL 44,000) because the live catalog has no usable 2XL entry.
- Variable-price variants are never quoted; the bot hands those to the team.
- If Loyverse is unreachable, the last cached catalog is served; with no
  cache at all, product questions hand off to the team instead of guessing.
- Sessions live in memory (fine for one or two workers; use sticky sessions
  or an external store if you scale past that).
