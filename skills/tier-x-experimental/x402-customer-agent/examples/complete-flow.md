# Complete Flow Examples

## Scenario 1: New User — First Order

```
USER: I'm hungry, can you order me lunch?

AGENT: I can order from real restaurants near you! Let me check if you have
a payment wallet set up.

> npx awal@2.0.3 status --json
→ Not authenticated

AGENT: To order food, I need to set up a digital wallet for you. Think of it
like a digital debit card on your computer — it holds digital dollars (called
USDC) that are always worth $1. Your money is secured by Coinbase.

I'll need your email address to get started. Coinbase will send you a
verification code, like when you log in to a new app.

USER: Sure, use alex@example.com

> npx awal@2.0.3 auth login alex@example.com
→ ✓ Verification code sent! Flow ID: abc123...

AGENT: I've sent a 6-digit code to your email. Share it with me when you get it.

USER: It's 482901

> npx awal@2.0.3 auth verify abc123 482901
→ ✔ Authentication successful!

> npx awal@2.0.3 address --json
→ { "address": "0x1234...abcd" }

AGENT: Your digital wallet is set up! Next, we need to adjust the spending
limits — they default to $5 which is too low for food orders.

> npx awal@2.0.3 show

AGENT: I've opened your wallet app. Please:
1. Click your email at the top
2. Click "Set spend limits"
3. Set per-transaction to $30, session to $50
4. Click "Save changes"
Let me know when done!

USER: Done

AGENT: Great! Now let's add some funds. In the same wallet window, click the
Fund button. I'd suggest adding $25-50. It accepts Apple Pay, debit cards,
or bank transfers.

USER: OK, I added $50

> npx awal@2.0.3 balance --json
→ { "balance": "50.00" }

AGENT: I see $50 in your wallet. Before we order, I'll save your contact info
so restaurants can reach you. What's your name and phone number?

USER: Alex Johnson, 212-555-1234

> mkdir -p ~/.agents/config
> cat > ~/.agents/config/foodcourts-profile.json << 'EOF'
{ "name": "Alex Johnson", "phone": "2125551234", "email": "alex@example.com" }
EOF

AGENT: Saved! Now, where are you located? I'll find restaurants near you.

USER: Prospect Heights, Brooklyn

> curl -s 'https://api.foodcourts.ai/api/restaurants?near=Prospect+Heights+Brooklyn'
→ [{ "chownow_id": "35453", "name": "Prospect Butcher Co", ... }]

AGENT: I found Prospect Butcher Co nearby! Let me pull up their menu.

> curl -s 'https://api.foodcourts.ai/api/restaurants/35453/menu'
→ (menu with categories and items)

AGENT: Here's what they have:
- PBC Roast Beef Sandwich — $15.00
- Italian Hero — $14.00
- Turkey Club — $13.50
What sounds good?

USER: Roast beef sandwich please

> curl -s -X POST 'https://api.foodcourts.ai/api/order/preview' ...
→ { "subtotal": 15.00, "tax": 1.33, "fee": 1.99, "total": 18.32 }

AGENT: Here's your order:
- 1x PBC Roast Beef Sandwich: $15.00
- Tax: $1.33
- Convenience fee: $1.99
- **Total: $18.32**
Your wallet has $50.00. Want me to place this order?

USER: Yes

> curl -s -D - -X POST 'https://api.foodcourts.ai/api/order' ...
→ 402 { "payTo": "0xAbCd...1234", "amount": "18.32" }
→ x-order-id: FC-MM29YISJ

> npx awal@2.0.3 send 18.32 0xAbCd...1234
→ Transaction sent! Hash: 0x9876...

> curl -s 'https://api.foodcourts.ai/api/order/FC-MM29YISJ'
→ { "status": "confirmed", "confirmationNumber": "FC-MM29YISJ" }

AGENT: Order confirmed! Your PBC Roast Beef Sandwich is being prepared.
Remaining wallet balance: $31.68.
```

## Scenario 2: Returning User — Quick Order

```
USER: Can you order me lunch from Prospect Butcher?

> npx awal@2.0.3 status --json
→ { "authenticated": true, "address": "0x1234...abcd" }

> cat ~/.agents/config/foodcourts-profile.json
→ { "name": "Alex Johnson", "phone": "2125551234", "email": "alex@example.com" }

> npx awal@2.0.3 balance --json
→ { "balance": "31.68" }

AGENT: Welcome back, Alex! You have $31.68 in your wallet. Let me pull up
the Prospect Butcher menu.

> curl -s 'https://api.foodcourts.ai/api/restaurants/35453/menu'
→ (menu)

AGENT: Here's what's available today:
- PBC Roast Beef Sandwich — $15.00
- Italian Hero — $14.00
What would you like?

USER: Italian hero this time

(... preview, confirm, pay, poll — same as above ...)
```

## Scenario 3: Restaurant Closed

```
USER: Order me a sandwich from Prospect Butcher

> npx awal@2.0.3 status --json
→ authenticated

> curl -s 'https://api.foodcourts.ai/api/restaurants/35453/menu'
→ { "_meta": { "restaurantCurrentlyAcceptingOrders": false },
    "_agentInstructions": { "note": "The store is currently closed and opens at 11:30am" },
    "categories": [...] }

AGENT: Prospect Butcher Co is currently **closed** — they open at 11:30am.
But I can still show you the menu so you can decide what you want! Here's
what they have:
- PBC Roast Beef Sandwich — $15.00
- Italian Hero — $14.00

Would you like to schedule an order for when they open?

USER: Yes, roast beef please

(... preview with pickup_time, confirm, pay ...)
```

## Scenario 4: Spending Limit Hit

```
USER: Order me two sandwiches

(... menu, preview shows $35.64 total ...)

> npx awal@2.0.3 send 35.64 0xAbCd...1234
→ Transaction failed: Amount $35.64 exceeds per-request limit of $30.00.
  Adjust limits in the wallet app.

> npx awal@2.0.3 show

AGENT: Your wallet's per-transaction limit is $30, but this order is $35.64.
In the wallet window I just opened:
1. Click your email at the top
2. Click "Set spend limits"
3. Increase the per-transaction limit to at least $40
4. Click "Save changes"
Let me know when done!

USER: Updated

> npx awal@2.0.3 send 35.64 0xAbCd...1234
→ Transaction sent!

AGENT: Payment went through! Your order is confirmed.
```

## Scenario 5: Insufficient Funds

```
> npx awal@2.0.3 balance --json
→ { "balance": "5.00" }

AGENT: You have $5.00 in your wallet, but a typical order is $15-20.
Let me open the wallet so you can add funds.

> npx awal@2.0.3 show

AGENT: Click the **Fund** button in the wallet window to add money.
I'd suggest $25-50 to cover a few orders. It accepts Apple Pay, debit
cards, bank transfers, or Coinbase. Let me know when you're done!

USER: Added $50

> npx awal@2.0.3 balance --json
→ { "balance": "55.00" }

AGENT: I see $55 now. Ready to order!
```
