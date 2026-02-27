# Google Ads API Setup

Complete guide for setting up Google Ads API access.

## Why Use the API?

**Browser automation works, but API is better for:**
- Bulk operations (pause 100 keywords at once)
- Scheduled tasks (daily performance checks)
- Programmatic reporting
- Automated optimizations

**The trade-off:** API requires upfront setup (1-2 hours), but pays off immediately for regular users.

---

## Prerequisites

### What You Need

1. **Google Ads account** (or MCC access for multiple accounts)
2. **Developer token** - Takes 1-3 days to get approved
3. **OAuth 2.0 credentials** - From Google Cloud Console
4. **Python 3.8+** with `google-ads` package

### Timeline

| Step | Time Required |
|------|--------------|
| Create GCP project | 5 minutes |
| Apply for developer token | 1-3 days (approval) |
| Set up OAuth | 15 minutes |
| Generate refresh token | 5 minutes |
| Write config file | 5 minutes |

---

## Step-by-Step Setup

### 1. Apply for Developer Token (Do This First — Takes Time)

1. Sign in to your Google Ads account
2. Go to Tools & Settings → API Center
3. Apply for "Basic Access" developer token
4. Fill out the form (describe your use case honestly)
5. Wait for approval (usually 1-3 business days)

**Test tokens exist but are limited:** They only work on test accounts, not real ones.

### 2. Create GCP Project & Enable API

```
1. Go to console.cloud.google.com
2. Create new project (e.g., "Google Ads Management")
3. Search for "Google Ads API" → Enable it
4. APIs & Services → Library → Enable
```

### 3. Create OAuth Credentials

```
1. APIs & Services → Credentials
2. Create Credentials → OAuth Client ID
3. Configure consent screen first (if prompted):
   - User type: Internal (or External if not in org)
   - App name: Your tool name
   - Scopes: Add https://www.googleapis.com/auth/adwords
4. Create OAuth Client ID:
   - Application type: Desktop app
   - Name: "Google Ads CLI" (or whatever)
5. Download JSON (save as client_secret.json)
```

### 4. Generate Refresh Token

```python
# oauth_setup.py
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/adwords']

flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret.json', scopes=SCOPES)

# Opens browser for consent
credentials = flow.run_local_server(port=8080)

print(f"Refresh token: {credentials.refresh_token}")
# SAVE THIS — you'll need it for the config file
```

Run this once. It opens a browser, you authorize, and it prints your refresh token.

### 5. Create Configuration File

Create `~/.google-ads.yaml`:

```yaml
# Required
developer_token: INSERT_YOUR_DEVELOPER_TOKEN
client_id: INSERT_YOUR_CLIENT_ID.apps.googleusercontent.com
client_secret: INSERT_YOUR_CLIENT_SECRET
refresh_token: INSERT_YOUR_REFRESH_TOKEN

# Only needed for MCC accounts managing multiple clients
# login_customer_id: INSERT_MCC_ID

# Optional: enable logging
# logging:
#   version: 1
#   handlers:
#     default:
#       class: logging.StreamHandler
#   loggers:
#     "":
#       level: WARNING
```

### 6. Install SDK

```bash
pip install google-ads

# Verify installation
python -c "from google.ads.googleads.client import GoogleAdsClient; print('OK')"
```

---

## Configuration Options

### File Locations (checked in order)

1. `./google-ads.yaml` (current directory)
2. `~/.google-ads.yaml` (home directory)
3. Environment variables (see below)

### Environment Variables

Alternative to YAML file:

```bash
export GOOGLE_ADS_DEVELOPER_TOKEN="your-token"
export GOOGLE_ADS_CLIENT_ID="your-client-id"
export GOOGLE_ADS_CLIENT_SECRET="your-client-secret"
export GOOGLE_ADS_REFRESH_TOKEN="your-refresh-token"
# export GOOGLE_ADS_LOGIN_CUSTOMER_ID="mcc-id"  # Only for MCC
```

Then use:
```python
client = GoogleAdsClient.load_from_env()
```

---

## Finding Your Customer ID

**Single account:** Your 10-digit account number (shown in top-right of Google Ads UI)  
**Format:** 1234567890 (no dashes)

**MCC (multiple accounts):**
- `login_customer_id`: The MCC account ID (for authentication)
- `customer_id` in queries: The specific account you're querying

---

## Testing Your Setup

```python
from google.ads.googleads.client import GoogleAdsClient

client = GoogleAdsClient.load_from_storage()
ga_service = client.get_service("GoogleAdsService")

# Simple test query
CUSTOMER_ID = "1234567890"  # Your account ID
query = "SELECT campaign.name FROM campaign LIMIT 5"

try:
    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)
    for row in response:
        print(f"Campaign: {row.campaign.name}")
    print("✅ API working!")
except Exception as e:
    print(f"❌ Error: {e}")
```

---

## Common Setup Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `DEVELOPER_TOKEN_NOT_APPROVED` | Test token on real account | Wait for approval or use test account |
| `USER_PERMISSION_DENIED` | No access to account | Add yourself to Google Ads account |
| `OAUTH_TOKEN_INVALID` | Bad refresh token | Regenerate with oauth_setup.py |
| `CUSTOMER_NOT_FOUND` | Wrong customer ID format | Use 10 digits, no dashes |
| `ModuleNotFoundError` | SDK not installed | `pip install google-ads` |

---

## Secure Token Storage

**Don't put tokens in code.** Options:

1. **Environment variables** - Good for dev
2. **Secret manager** (GCP, AWS, HashiCorp) - Good for prod
3. **YAML file with restricted permissions** - Acceptable

```bash
# Secure your config file
chmod 600 ~/.google-ads.yaml
```

---

## Next Steps

Once set up:
1. Test with a simple query (above)
2. Return to SKILL.md for common operations
3. Start with read-only queries before mutations
