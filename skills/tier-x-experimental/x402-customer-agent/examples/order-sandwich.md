# Example: Order a Sandwich via awal CLI

A complete walkthrough of ordering from Prospect Butcher Co using the `awal` CLI and FoodCourts.ai API.

---

## Step 1: Verify Wallet & Profile

```bash
# Check wallet is authenticated
npx awal@2.0.3 status --json
# → { "authenticated": true, "address": "0x1234...abcd" }

# Check balance
npx awal@2.0.3 balance --json
# → { "balance": "45.00", "currency": "USDC" }

# Read saved profile
cat ~/.agents/config/foodcourts-profile.json
# → { "name": "Alex", "phone": "2125551234", "email": "alex@example.com" }
```

## Step 2: Find Restaurant & Browse Menu

```bash
# Search for restaurants near Brooklyn
curl -s 'https://api.foodcourts.ai/api/restaurants?near=Prospect+Heights+Brooklyn' | python3 -m json.tool

# Browse menu (use chownow_id from search results)
curl -s 'https://api.foodcourts.ai/api/restaurants/35453/menu' | python3 -m json.tool
```

Pick an item using the numeric `id` field (e.g., `"id": "67890"` for PBC Roast Beef Sandwich).

## Step 3: Preview Order

```bash
curl -s -X POST 'https://api.foodcourts.ai/api/order/preview' \
  -H 'Content-Type: application/json' \
  -d '{
    "restaurant_id": "35453",
    "items": [{ "id": "67890", "quantity": 1 }],
    "fulfillment": "pickup"
  }'
```

Response includes subtotal, tax, and $1.99 convenience fee. **Show this to the user and get "yes" before continuing.**

## Step 4: Place Order

```bash
curl -s -D - -X POST 'https://api.foodcourts.ai/api/order' \
  -H 'Content-Type: application/json' \
  -d '{
    "restaurant_id": "35453",
    "items": [{ "id": "67890", "quantity": 1 }],
    "fulfillment": "pickup",
    "customer": { "name": "Alex", "phone": "2125551234", "email": "alex@example.com" }
  }'
```

Response: HTTP 402 with body `{ "payTo": "0xAbCd...1234", "amount": "18.32" }` and header `x-order-id: FC-MM29YISJ`.

## Step 5: Pay (Gasless)

```bash
npx awal@2.0.3 send 18.32 0xAbCd...1234
```

Confirms in ~2 seconds. No ETH needed.

## Step 6: Poll for Confirmation

```bash
curl -s 'https://api.foodcourts.ai/api/order/FC-MM29YISJ'
# Repeat every 3 seconds until status = "confirmed"
```

## Human-Facing Messages

**Before payment:**
> "Your order from Prospect Butcher Co: 1x PBC Roast Beef Sandwich — $15.00 + $1.33 tax + $1.99 fee = **$18.32 total**. Your wallet has $45.00. Want me to go ahead and pay?"

**After confirmation:**
> "Order confirmed! Your PBC Roast Beef Sandwich will be ready for pickup. Confirmation number: FC-MM29YISJ."

## If Spending Limit Is Too Low

```bash
npx awal@2.0.3 send 18.32 0xAbCd...1234
# → Transaction failed: Amount $18.32 exceeds per-request limit of $5.00. Adjust limits in the wallet app.

npx awal@2.0.3 show
# Tell user to increase per-transaction limit to at least $20
# After user adjusts, retry:
npx awal@2.0.3 send 18.32 0xAbCd...1234
```
