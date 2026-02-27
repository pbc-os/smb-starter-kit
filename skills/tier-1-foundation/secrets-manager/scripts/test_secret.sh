#!/bin/bash
# =============================================================================
# test_secret.sh — Round-trip test: create, read, verify, delete a test secret
#
# Creates "clawdbot-test-secret" with value "hello-from-clawdbot", reads it
# back, verifies the value matches, then cleans up.
#
# Usage: bash test_secret.sh [platform]
#   platform: gcp | aws | azure | 1password | doppler | vault
#   If omitted, auto-detects based on installed CLIs.
# =============================================================================

set -uo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PASS="${GREEN}✅ PASS${NC}"
FAIL="${RED}❌ FAIL${NC}"
INFO="${BLUE}ℹ️ ${NC}"

SECRET_NAME="clawdbot-test-secret"
SECRET_VALUE="hello-from-clawdbot"
PLATFORM="${1:-}"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Secrets Manager — Round-Trip Test"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# -----------------------------------------------------------------------------
# Auto-detect platform if not specified
# -----------------------------------------------------------------------------
if [ -z "$PLATFORM" ]; then
  echo -e "${INFO} Auto-detecting platform..."
  if command -v gcloud &>/dev/null && gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>/dev/null | grep -q "@"; then
    PLATFORM="gcp"
  elif command -v aws &>/dev/null && aws sts get-caller-identity &>/dev/null; then
    PLATFORM="aws"
  elif command -v az &>/dev/null && az account show &>/dev/null; then
    PLATFORM="azure"
  elif command -v op &>/dev/null && op vault list &>/dev/null; then
    PLATFORM="1password"
  elif command -v doppler &>/dev/null && doppler me &>/dev/null; then
    PLATFORM="doppler"
  elif command -v vault &>/dev/null && vault status &>/dev/null; then
    PLATFORM="vault"
  else
    echo -e "${FAIL}  No authenticated secrets platform detected."
    echo "  Run verify_access.sh first, or specify: bash test_secret.sh <platform>"
    exit 1
  fi
fi

echo -e "${INFO} Platform: ${PLATFORM}"
echo -e "${INFO} Secret name: ${SECRET_NAME}"
echo -e "${INFO} Secret value: ${SECRET_VALUE}"
echo ""

# -----------------------------------------------------------------------------
# Platform-specific functions
# -----------------------------------------------------------------------------

# -- GCP --
gcp_create() {
  echo -n "$SECRET_VALUE" | gcloud secrets create "$SECRET_NAME" --data-file=- --project="$GCP_PROJECT" 2>&1
}
gcp_read() {
  gcloud secrets versions access latest --secret="$SECRET_NAME" --project="$GCP_PROJECT" 2>/dev/null
}
gcp_delete() {
  gcloud secrets delete "$SECRET_NAME" --project="$GCP_PROJECT" --quiet 2>&1
}

# -- AWS --
aws_create() {
  aws secretsmanager create-secret --name "$SECRET_NAME" --secret-string "$SECRET_VALUE" --region "$AWS_REGION" 2>&1
}
aws_read() {
  aws secretsmanager get-secret-value --secret-id "$SECRET_NAME" --query SecretString --output text --region "$AWS_REGION" 2>/dev/null
}
aws_delete() {
  aws secretsmanager delete-secret --secret-id "$SECRET_NAME" --force-delete-without-recovery --region "$AWS_REGION" 2>&1
}

# -- Azure --
azure_create() {
  az keyvault secret set --vault-name "$AZ_VAULT" --name "$SECRET_NAME" --value "$SECRET_VALUE" 2>&1
}
azure_read() {
  az keyvault secret show --vault-name "$AZ_VAULT" --name "$SECRET_NAME" --query value -o tsv 2>/dev/null
}
azure_delete() {
  az keyvault secret delete --vault-name "$AZ_VAULT" --name "$SECRET_NAME" 2>&1
  # Purge to fully remove (if purge protection allows)
  sleep 2
  az keyvault secret purge --vault-name "$AZ_VAULT" --name "$SECRET_NAME" 2>/dev/null || true
}

# -- 1Password --
op_create() {
  op item create --category="Secure Note" --title="$SECRET_NAME" --vault="Private" "notesPlain=$SECRET_VALUE" 2>&1
}
op_read() {
  op read "op://Private/${SECRET_NAME}/notesPlain" 2>/dev/null
}
op_delete() {
  op item delete "$SECRET_NAME" --vault="Private" 2>&1
}

# -- Doppler --
doppler_create() {
  doppler secrets set CLAWDBOT_TEST_SECRET="$SECRET_VALUE" --silent 2>&1
}
doppler_read() {
  doppler secrets get CLAWDBOT_TEST_SECRET --plain 2>/dev/null
}
doppler_delete() {
  doppler secrets delete CLAWDBOT_TEST_SECRET --silent --yes 2>&1
}

# -- Vault --
vault_create() {
  vault kv put "secret/$SECRET_NAME" value="$SECRET_VALUE" 2>&1
}
vault_read() {
  vault kv get -field=value "secret/$SECRET_NAME" 2>/dev/null
}
vault_delete() {
  vault kv delete "secret/$SECRET_NAME" 2>&1
  vault kv destroy -versions=all "secret/$SECRET_NAME" 2>/dev/null || true
  vault kv metadata delete "secret/$SECRET_NAME" 2>/dev/null || true
}

# -----------------------------------------------------------------------------
# Set platform-specific variables
# -----------------------------------------------------------------------------
case "$PLATFORM" in
  gcp)
    GCP_PROJECT=$(gcloud config get-value project 2>/dev/null)
    if [ -z "$GCP_PROJECT" ]; then
      echo -e "${FAIL}  No GCP project set. Run: gcloud config set project YOUR_PROJECT_ID"
      exit 1
    fi
    echo -e "${INFO} GCP Project: ${GCP_PROJECT}"
    CREATE_FN="gcp_create"
    READ_FN="gcp_read"
    DELETE_FN="gcp_delete"
    ;;
  aws)
    AWS_REGION=$(aws configure get region 2>/dev/null)
    AWS_REGION=${AWS_REGION:-us-east-1}
    echo -e "${INFO} AWS Region: ${AWS_REGION}"
    CREATE_FN="aws_create"
    READ_FN="aws_read"
    DELETE_FN="aws_delete"
    ;;
  azure)
    AZ_VAULT=$(az keyvault list --query "[0].name" -o tsv 2>/dev/null)
    if [ -z "$AZ_VAULT" ]; then
      echo -e "${FAIL}  No Azure Key Vault found. Create one first."
      exit 1
    fi
    echo -e "${INFO} Azure Vault: ${AZ_VAULT}"
    CREATE_FN="azure_create"
    READ_FN="azure_read"
    DELETE_FN="azure_delete"
    ;;
  1password)
    CREATE_FN="op_create"
    READ_FN="op_read"
    DELETE_FN="op_delete"
    ;;
  doppler)
    CREATE_FN="doppler_create"
    READ_FN="doppler_read"
    DELETE_FN="doppler_delete"
    ;;
  vault)
    if [ -z "${VAULT_ADDR:-}" ]; then
      echo -e "${FAIL}  VAULT_ADDR not set. Run: export VAULT_ADDR='http://127.0.0.1:8200'"
      exit 1
    fi
    echo -e "${INFO} Vault Address: ${VAULT_ADDR}"
    CREATE_FN="vault_create"
    READ_FN="vault_read"
    DELETE_FN="vault_delete"
    ;;
  *)
    echo -e "${FAIL}  Unknown platform: ${PLATFORM}"
    echo "  Supported: gcp, aws, azure, 1password, doppler, vault"
    exit 1
    ;;
esac

echo ""

# -----------------------------------------------------------------------------
# Step 1: Create
# -----------------------------------------------------------------------------
echo "Step 1: Creating test secret..."
echo "────────────────────────────────────────────────────────"

CREATE_OUTPUT=$($CREATE_FN 2>&1)
CREATE_STATUS=$?

if [ $CREATE_STATUS -eq 0 ]; then
  echo -e "  ${PASS}  Secret '${SECRET_NAME}' created successfully."
else
  echo -e "  ${FAIL}  Failed to create secret."
  echo "  Output: ${CREATE_OUTPUT}"
  echo ""
  echo "  This might mean the secret already exists. Try deleting it first:"
  echo "  bash test_secret.sh ${PLATFORM}  (it will clean up at the end)"
  exit 1
fi

echo ""

# -----------------------------------------------------------------------------
# Step 2: Read and verify
# -----------------------------------------------------------------------------
echo "Step 2: Reading back and verifying..."
echo "────────────────────────────────────────────────────────"

READ_VALUE=$($READ_FN 2>/dev/null)
READ_STATUS=$?

if [ $READ_STATUS -eq 0 ] && [ "$READ_VALUE" = "$SECRET_VALUE" ]; then
  echo -e "  ${PASS}  Read back value: '${READ_VALUE}'"
  echo -e "  ${PASS}  Value matches expected: '${SECRET_VALUE}'"
else
  echo -e "  ${FAIL}  Value mismatch or read failed."
  echo "  Expected: '${SECRET_VALUE}'"
  echo "  Got:      '${READ_VALUE}'"
  # Still try to clean up
fi

echo ""

# -----------------------------------------------------------------------------
# Step 3: Delete (cleanup)
# -----------------------------------------------------------------------------
echo "Step 3: Cleaning up (deleting test secret)..."
echo "────────────────────────────────────────────────────────"

DELETE_OUTPUT=$($DELETE_FN 2>&1)
DELETE_STATUS=$?

if [ $DELETE_STATUS -eq 0 ]; then
  echo -e "  ${PASS}  Secret '${SECRET_NAME}' deleted successfully."
else
  echo -e "  ${FAIL}  Failed to delete secret. You may need to clean up manually."
  echo "  Output: ${DELETE_OUTPUT}"
fi

echo ""

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
echo "═══════════════════════════════════════════════════════════════"
if [ $CREATE_STATUS -eq 0 ] && [ "$READ_VALUE" = "$SECRET_VALUE" ] && [ $DELETE_STATUS -eq 0 ]; then
  echo -e "  ${GREEN}🎉 ROUND-TRIP TEST PASSED${NC}"
  echo ""
  echo "  ✅ Created secret in ${PLATFORM}"
  echo "  ✅ Read it back successfully"
  echo "  ✅ Value matched"
  echo "  ✅ Cleaned up"
  echo ""
  echo "  Your secrets platform is fully operational."
  echo "  You're ready to store real secrets and integrate with Clawdbot!"
else
  echo -e "  ${RED}⚠️  ROUND-TRIP TEST HAD ISSUES${NC}"
  echo ""
  echo "  Review the output above for details."
  echo "  Run verify_access.sh to check authentication and permissions."
fi
echo "═══════════════════════════════════════════════════════════════"
echo ""
