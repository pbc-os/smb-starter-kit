# Agentic Wallet CLI Reference

Quick reference for `awal` CLI commands used in the FoodCourts ordering flow.

---

## Authentication

```bash
# Check wallet status
npx awal@2.0.3 status --json

# Start login (sends OTP to email)
npx awal@2.0.3 auth login user@example.com

# Complete login with OTP code
npx awal@2.0.3 auth verify <flowId> <6-digit-code>
```

## Balance & Address

```bash
# Check USDC balance
npx awal@2.0.3 balance --json

# Get wallet address
npx awal@2.0.3 address --json
```

## Payments

```bash
# Send USDC (gasless on Base)
npx awal@2.0.3 send <amount> <recipient>

# Example: pay for a food order
npx awal@2.0.3 send 18.49 0xAbCd...1234
```

**Input validation:**
- `amount`: Must match `^\$?[\d.]+$` — digits with optional decimal and `$` prefix. Single-quote amounts with `$` to prevent bash expansion.
- `recipient`: Must be a valid `0x` hex address (`^0x[0-9a-fA-F]{40}$`).

## Companion UI

```bash
# Open the wallet companion window
npx awal@2.0.3 show
```

Used for:
- **Funding:** Click Fund button → Apple Pay, debit card, bank, Coinbase account
- **Spending limits:** Click email → Set spend limits → adjust → Save changes

## Spending Limits

Two limits (both default to $5):

| Limit | Default | Recommended |
|-------|---------|-------------|
| Total session spending limit | $5 | $50 |
| Max spend per API call | $5 | $30 |

**Only the human can change limits** via the companion UI (`npx awal@2.0.3 show`). There is no CLI command to adjust limits.

## Error: Spending Limit Exceeded

```
Transaction failed: Amount $X exceeds per-request limit of $Y. Adjust limits in the wallet app.
```

Recovery:
1. `npx awal@2.0.3 show`
2. User clicks email → Set spend limits → increase → Save changes
3. Retry `npx awal@2.0.3 send`
4. If >10 min pass, re-POST `/api/order` for fresh deposit address

## Key Facts

- Transactions on Base are **gasless** — no ETH needed
- Finality: ~2 seconds
- Auth persists across restarts (tied to device + email)
- Works across all AI agents on the device
- All commands support `--json` for machine-readable output
