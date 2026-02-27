#!/bin/bash
# =============================================================================
# verify_access.sh — Verify secrets management platform access
#
# Detects which platform CLIs are installed, tests authentication, and
# attempts to list secrets. Prints clear pass/fail for each check.
#
# Usage: bash verify_access.sh
# =============================================================================

set -uo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PASS="${GREEN}✅ PASS${NC}"
FAIL="${RED}❌ FAIL${NC}"
WARN="${YELLOW}⚠️  WARN${NC}"
INFO="${BLUE}ℹ️ ${NC}"

# Track overall result
OVERALL_PASS=true
DETECTED_PLATFORM=""

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Secrets Manager — Access Verification"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# -----------------------------------------------------------------------------
# Step 1: Detect installed CLIs
# -----------------------------------------------------------------------------
echo "Step 1: Detecting installed secret management CLIs..."
echo "────────────────────────────────────────────────────────"

check_cli() {
  local name="$1"
  local cmd="$2"
  if command -v "$cmd" &>/dev/null; then
    local version
    version=$($3 2>&1 | head -1)
    echo -e "  ${PASS}  ${name} CLI found: ${version}"
    return 0
  else
    echo -e "  ${INFO} ${name} CLI not found"
    return 1
  fi
}

FOUND_ANY=false

if check_cli "GCP (gcloud)" "gcloud" "gcloud version"; then
  FOUND_ANY=true
  DETECTED_PLATFORM="gcp"
fi

if check_cli "AWS" "aws" "aws --version"; then
  FOUND_ANY=true
  [ -z "$DETECTED_PLATFORM" ] && DETECTED_PLATFORM="aws"
fi

if check_cli "Azure (az)" "az" "az version -o tsv"; then
  FOUND_ANY=true
  [ -z "$DETECTED_PLATFORM" ] && DETECTED_PLATFORM="azure"
fi

if check_cli "1Password (op)" "op" "op --version"; then
  FOUND_ANY=true
  [ -z "$DETECTED_PLATFORM" ] && DETECTED_PLATFORM="1password"
fi

if check_cli "Doppler" "doppler" "doppler --version"; then
  FOUND_ANY=true
  [ -z "$DETECTED_PLATFORM" ] && DETECTED_PLATFORM="doppler"
fi

if check_cli "HashiCorp Vault" "vault" "vault version"; then
  FOUND_ANY=true
  [ -z "$DETECTED_PLATFORM" ] && DETECTED_PLATFORM="vault"
fi

echo ""

if [ "$FOUND_ANY" = false ]; then
  echo -e "${FAIL}  No secrets management CLI detected."
  echo ""
  echo "  Install one of the following:"
  echo "    GCP:       brew install --cask google-cloud-sdk"
  echo "    AWS:       brew install awscli"
  echo "    Azure:     brew install azure-cli"
  echo "    1Password: brew install --cask 1password-cli"
  echo "    Doppler:   brew install dopplerhq/cli/doppler"
  echo "    Vault:     brew install hashicorp/tap/vault"
  echo ""
  exit 1
fi

# -----------------------------------------------------------------------------
# Step 2: Test authentication for detected platform
# -----------------------------------------------------------------------------
echo "Step 2: Testing authentication for detected platforms..."
echo "────────────────────────────────────────────────────────"

test_gcp_auth() {
  local account
  account=$(gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>/dev/null)
  if [ -n "$account" ]; then
    echo -e "  ${PASS}  GCP authenticated as: ${account}"
    return 0
  else
    echo -e "  ${FAIL}  GCP not authenticated. Run: gcloud auth login"
    OVERALL_PASS=false
    return 1
  fi
}

test_aws_auth() {
  local identity
  identity=$(aws sts get-caller-identity --query "Arn" --output text 2>/dev/null)
  if [ -n "$identity" ]; then
    echo -e "  ${PASS}  AWS authenticated as: ${identity}"
    return 0
  else
    echo -e "  ${FAIL}  AWS not authenticated. Run: aws configure"
    OVERALL_PASS=false
    return 1
  fi
}

test_azure_auth() {
  local account
  account=$(az account show --query "user.name" -o tsv 2>/dev/null)
  if [ -n "$account" ]; then
    echo -e "  ${PASS}  Azure authenticated as: ${account}"
    return 0
  else
    echo -e "  ${FAIL}  Azure not authenticated. Run: az login"
    OVERALL_PASS=false
    return 1
  fi
}

test_1password_auth() {
  if op vault list &>/dev/null; then
    echo -e "  ${PASS}  1Password authenticated (vault access confirmed)"
    return 0
  else
    echo -e "  ${FAIL}  1Password not authenticated. Run: op signin"
    echo -e "  ${INFO} For service accounts, set OP_SERVICE_ACCOUNT_TOKEN env var"
    OVERALL_PASS=false
    return 1
  fi
}

test_doppler_auth() {
  local me
  me=$(doppler me --json 2>/dev/null | grep -o '"name":"[^"]*"' | head -1)
  if [ -n "$me" ]; then
    echo -e "  ${PASS}  Doppler authenticated: ${me}"
    return 0
  else
    echo -e "  ${FAIL}  Doppler not authenticated. Run: doppler login"
    OVERALL_PASS=false
    return 1
  fi
}

test_vault_auth() {
  if [ -z "${VAULT_ADDR:-}" ]; then
    echo -e "  ${WARN} VAULT_ADDR not set. Run: export VAULT_ADDR='http://127.0.0.1:8200'"
    OVERALL_PASS=false
    return 1
  fi
  local status
  status=$(vault status -format=json 2>/dev/null | grep '"sealed"' | grep -o 'false\|true')
  if [ "$status" = "false" ]; then
    echo -e "  ${PASS}  Vault server reachable and unsealed at ${VAULT_ADDR}"
    # Check token
    if vault token lookup &>/dev/null; then
      echo -e "  ${PASS}  Vault token is valid"
      return 0
    else
      echo -e "  ${FAIL}  Vault token invalid or missing. Run: vault login"
      OVERALL_PASS=false
      return 1
    fi
  elif [ "$status" = "true" ]; then
    echo -e "  ${FAIL}  Vault is sealed. Run: vault operator unseal"
    OVERALL_PASS=false
    return 1
  else
    echo -e "  ${FAIL}  Cannot reach Vault at ${VAULT_ADDR}"
    OVERALL_PASS=false
    return 1
  fi
}

# Run auth tests for all detected CLIs
command -v gcloud &>/dev/null && test_gcp_auth
command -v aws &>/dev/null && test_aws_auth
command -v az &>/dev/null && test_azure_auth
command -v op &>/dev/null && test_1password_auth
command -v doppler &>/dev/null && test_doppler_auth
command -v vault &>/dev/null && test_vault_auth

echo ""

# -----------------------------------------------------------------------------
# Step 3: Test secret listing for the primary detected platform
# -----------------------------------------------------------------------------
echo "Step 3: Testing secret access (${DETECTED_PLATFORM})..."
echo "────────────────────────────────────────────────────────"

case "$DETECTED_PLATFORM" in
  gcp)
    PROJECT=$(gcloud config get-value project 2>/dev/null)
    if [ -n "$PROJECT" ]; then
      echo -e "  ${INFO} Project: ${PROJECT}"
      COUNT=$(gcloud secrets list --project="$PROJECT" --format="value(name)" 2>/dev/null | wc -l | tr -d ' ')
      if [ "$?" -eq 0 ]; then
        echo -e "  ${PASS}  Can list secrets. Found ${COUNT} secret(s)."
      else
        echo -e "  ${FAIL}  Cannot list secrets. Check Secret Manager API is enabled."
        echo "         Run: gcloud services enable secretmanager.googleapis.com"
        OVERALL_PASS=false
      fi
    else
      echo -e "  ${FAIL}  No GCP project set. Run: gcloud config set project YOUR_PROJECT_ID"
      OVERALL_PASS=false
    fi
    ;;
  aws)
    REGION=$(aws configure get region 2>/dev/null)
    REGION=${REGION:-us-east-1}
    echo -e "  ${INFO} Region: ${REGION}"
    COUNT=$(aws secretsmanager list-secrets --region "$REGION" --query "length(SecretList)" --output text 2>/dev/null)
    if [ "$?" -eq 0 ]; then
      echo -e "  ${PASS}  Can list secrets. Found ${COUNT} secret(s)."
    else
      echo -e "  ${FAIL}  Cannot list secrets. Check IAM permissions."
      OVERALL_PASS=false
    fi
    ;;
  azure)
    # Try to find a vault
    VAULT=$(az keyvault list --query "[0].name" -o tsv 2>/dev/null)
    if [ -n "$VAULT" ]; then
      echo -e "  ${INFO} Using vault: ${VAULT}"
      COUNT=$(az keyvault secret list --vault-name "$VAULT" --query "length([])" 2>/dev/null)
      if [ "$?" -eq 0 ]; then
        echo -e "  ${PASS}  Can list secrets. Found ${COUNT} secret(s)."
      else
        echo -e "  ${FAIL}  Cannot list secrets in vault '${VAULT}'. Check access policies."
        OVERALL_PASS=false
      fi
    else
      echo -e "  ${WARN} No Key Vault found. Create one first."
      OVERALL_PASS=false
    fi
    ;;
  1password)
    COUNT=$(op item list --format=json 2>/dev/null | grep -c '"id"' || echo "0")
    if [ "$?" -eq 0 ]; then
      echo -e "  ${PASS}  Can list items. Found ${COUNT} item(s)."
    else
      echo -e "  ${FAIL}  Cannot list items. Check vault permissions."
      OVERALL_PASS=false
    fi
    ;;
  doppler)
    COUNT=$(doppler secrets --json 2>/dev/null | grep -c '"raw"' || echo "0")
    if [ "$?" -eq 0 ]; then
      echo -e "  ${PASS}  Can list secrets. Found ${COUNT} secret(s)."
    else
      echo -e "  ${FAIL}  Cannot list secrets. Run: doppler setup"
      OVERALL_PASS=false
    fi
    ;;
  vault)
    LIST_OUTPUT=$(vault kv list secret/ 2>/dev/null)
    if [ "$?" -eq 0 ]; then
      COUNT=$(echo "$LIST_OUTPUT" | grep -c "." || echo "0")
      echo -e "  ${PASS}  Can list secrets. Found ${COUNT} path(s) under secret/."
    else
      echo -e "  ${FAIL}  Cannot list secrets. Check KV engine is enabled at secret/."
      echo "         Run: vault secrets enable -path=secret kv-v2"
      OVERALL_PASS=false
    fi
    ;;
esac

echo ""

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
echo "═══════════════════════════════════════════════════════════════"
if [ "$OVERALL_PASS" = true ]; then
  echo -e "  ${GREEN}🎉 ALL CHECKS PASSED${NC}"
  echo ""
  echo "  Your secrets management is configured and accessible."
  echo "  You're ready to integrate with Clawdbot's gateway."
else
  echo -e "  ${RED}⚠️  SOME CHECKS FAILED${NC}"
  echo ""
  echo "  Fix the issues above, then run this script again."
  echo "  Need help? Ask your AI agent — it knows how to fix each issue."
fi
echo "═══════════════════════════════════════════════════════════════"
echo ""
