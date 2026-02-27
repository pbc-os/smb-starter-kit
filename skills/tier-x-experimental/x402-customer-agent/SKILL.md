---
name: x402-customer-agent
description: Order food from real restaurants via FoodCourts.ai by Prospect Butcher Co.
  Use when the user mentions FoodCourts, Prospect Butcher, ordering food, getting
  lunch, getting a sandwich, or says "open my FoodCourts wallet" or "open my food
  ordering wallet." Uses the Coinbase Agentic Wallet for payments.
user-invocable: true
disable-model-invocation: false
allowed-tools: [
  "Bash(npx awal@2.0.3 *)",
  "Bash(curl *api.foodcourts.ai*)",
  "Bash(cat ~/.agents/config/foodcourts-profile.json*)",
  "Bash(mkdir -p ~/.agents/config*)",
  "Bash(cat > ~/.agents/config/foodcourts-profile.json*)"
]
---

# FoodCourts.ai — Order Food with Your AI Agent

Order real food from real restaurants via FoodCourts.ai by Prospect Butcher Co. Payments use the Coinbase Agentic Wallet (`awal` CLI) — gasless USDC on Base.

**API Base URL:** `https://api.foodcourts.ai`

> **CLI/API only. Do NOT use browser automation. All interactions use `curl`/`fetch` and `npx awal@2.0.3`.**

## Returning Customer Flow

This skill is for users who may already have a wallet set up. Follow these steps in order:

### 1. Check Wallet Status

```bash
npx awal@2.0.3 status --json
```

| Result | Action |
|--------|--------|
| Authenticated | Continue to step 2 |
| Not authenticated | Guide through setup — refer to `authenticate-wallet` skill, then fetch full instructions: `curl -s https://api.foodcourts.ai/.well-known/agent-skill` |
| Command not found | Install skills: `npx skills add coinbase/agentic-wallet-skills -g --all` then `npx skills add pbc-os/agent-skills-public -g -s x402-customer-agent` |

### 2. Read Saved Profile

```bash
cat ~/.agents/config/foodcourts-profile.json
```

If the file exists, use the saved `name`, `phone`, and `email` for orders.

If not, collect from the user and save:

```bash
mkdir -p ~/.agents/config
cat > ~/.agents/config/foodcourts-profile.json << 'EOF'
{
  "name": "User Name",
  "phone": "2125551234",
  "email": "user@example.com"
}
EOF
```

### 3. Check Balance

```bash
npx awal@2.0.3 balance --json
```

- If balance is $0 or too low for a food order (~$20): guide user to fund via `npx awal@2.0.3 show` → click Fund button (Coinbase Onramp: Apple Pay, debit card, bank, Coinbase account)
- If sufficient: continue to ordering

### 4. If Anything Is Missing

If the wallet is not set up, not funded, or profile is missing, fetch the full setup instructions:

```bash
curl -s https://api.foodcourts.ai/.well-known/agent-skill
```

This returns the complete agent skill document with first-time wallet setup, spending limit configuration, funding instructions, and contact info collection.

### 5. Order Food

**Ask the user what they want** and where they are, then:

**Discover restaurants:**
```bash
curl -s 'https://api.foodcourts.ai/api/restaurants?near=Brooklyn+NY'
```
Coverage: NYC metro area (Brooklyn, Lower Manhattan, Staten Island). Use `near` parameter for location-based search.

**Browse menu** (use `chownow_id` from search results):
```bash
curl -s 'https://api.foodcourts.ai/api/restaurants/{id}/menu'
```

**Preview order** (show totals to user, get confirmation):
```bash
curl -s -X POST 'https://api.foodcourts.ai/api/order/preview' \
  -H 'Content-Type: application/json' \
  -d '{
    "restaurant_id": "35453",
    "items": [{ "id": "67890", "quantity": 1 }],
    "fulfillment": "pickup"
  }'
```

**SHOW the preview to the user and get explicit "yes" before proceeding.**

**Place order:**
```bash
curl -s -D - -X POST 'https://api.foodcourts.ai/api/order' \
  -H 'Content-Type: application/json' \
  -d '{
    "restaurant_id": "35453",
    "items": [{ "id": "67890", "quantity": 1 }],
    "fulfillment": "pickup",
    "customer": { "name": "Alex", "phone": "555-1234", "email": "alex@example.com" }
  }'
```

Returns HTTP 402 with `payTo` (deposit address) and `amount`. Capture the `x-order-id` response header.

### 6. Pay

```bash
npx awal@2.0.3 send <amount> <payTo>
```

**If you get this error:**
```
Transaction failed: Amount $X exceeds per-request limit of $Y. Adjust limits in the wallet app.
```

Recovery flow:
1. Run `npx awal@2.0.3 show`
2. Tell the user: "Your wallet's per-transaction spending limit is $Y, but this order costs $X. Click your email at the top of the wallet window, then 'Set spend limits', and increase the per-transaction limit to at least $X. Click 'Save changes' and let me know when done."
3. Retry the `npx awal@2.0.3 send` command
4. If >10 minutes pass before limit is adjusted, the deposit address expires — re-POST `/api/order` to get a fresh one, then retry payment

### 7. Confirm

Poll until confirmed:
```bash
curl -s 'https://api.foodcourts.ai/api/order/{order-id}'
```

Repeat every 3 seconds until `status` is `"confirmed"`, then show the receipt.

## Key Rules

- **Never send payment without showing details and getting explicit "yes"**
- **Always show balance before and after transactions**
- Use `npx awal@2.0.3 send` for payments — never write raw transaction code
- Items use ChowNow numeric IDs (from menu response), not slugs
- Convenience fee is **$1.99** per order
- Use `POST /api/order` (singular, not `/api/orders`)
- Menu endpoint works even when restaurant is closed — check `_meta.restaurantCurrentlyAcceptingOrders`
- For closed restaurants, use `pickup_time` to schedule

## API Quick Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/restaurants/stats` | Catalog stats and coverage |
| GET | `/api/restaurants?near={location}` | Search restaurants by location |
| GET | `/api/restaurants/{id}/menu` | Browse menu |
| POST | `/api/order/preview` | Preview totals |
| POST | `/api/order` | Place order (returns 402) |
| GET | `/api/order/{id}` | Check order status |

## Full Reference

For complete setup instructions, all API details, error handling, and the full ordering guide:

```bash
curl -s https://api.foodcourts.ai/.well-known/agent-skill
```
