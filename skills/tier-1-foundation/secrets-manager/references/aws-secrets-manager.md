# AWS Secrets Manager — Full Setup Guide

## Table of Contents
- [1. Account Setup](#1-account-setup)
- [2. CLI Installation](#2-cli-installation)
- [3. Authentication](#3-authentication)
- [4. Creating Your First Secret](#4-creating-your-first-secret)
- [5. Granting AI Agent Access](#5-granting-ai-agent-access)
- [6. Gateway Wrapper Script](#6-gateway-wrapper-script)
- [7. Common Issues & Troubleshooting](#7-common-issues--troubleshooting)

---

## 1. Account Setup

### Prerequisites
- An AWS account: https://aws.amazon.com/free/
- AWS Secrets Manager is available in all regions by default — no API to enable.

### Navigate to Secrets Manager
1. Open the AWS Console: https://console.aws.amazon.com
2. Search "Secrets Manager" in the top search bar
3. Select your preferred region from the top-right dropdown

**What you should see:** The Secrets Manager dashboard with a "Store a new secret" button.

### Note Your Region
You'll reference your region in CLI commands. Common choices:
- `us-east-1` (Virginia)
- `us-west-2` (Oregon)
- `eu-west-1` (Ireland)

---

## 2. CLI Installation

### Install AWS CLI v2

**macOS (Homebrew):**
```bash
brew install awscli
```

**macOS (Package):**
```bash
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
rm AWSCLIV2.pkg
```

**Linux (x86_64):**
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
rm -rf awscliv2.zip aws/
```

**Linux (ARM):**
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
rm -rf awscliv2.zip aws/
```

### Verify Installation

```bash
aws --version
```

**What you should see:** Version info like:
```
aws-cli/2.15.30 Python/3.11.8 Darwin/23.4.0 exe/x86_64 prompt/off
```

---

## 3. Authentication

### Configure AWS CLI

```bash
aws configure
```

You'll be prompted for:
- **AWS Access Key ID** — From IAM console (see below)
- **AWS Secret Access Key** — From IAM console
- **Default region** — e.g., `us-east-1`
- **Default output format** — Enter `json`

### Get Access Keys from IAM

1. Go to https://console.aws.amazon.com/iam/
2. Click **Users** → Select your user
3. Click **Security credentials** tab
4. Click **Create access key**
5. Select "Command Line Interface (CLI)"
6. Copy the Access Key ID and Secret Access Key

**⚠️ The Secret Access Key is shown ONLY ONCE. Copy it immediately.**

### Verify Authentication

```bash
aws sts get-caller-identity
```

**What you should see:**
```json
{
    "UserId": "AIDAEXAMPLE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/your-username"
}
```

### Required Permissions

Attach this IAM policy to your user or role:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:CreateSecret",
                "secretsmanager:GetSecretValue",
                "secretsmanager:ListSecrets",
                "secretsmanager:UpdateSecret",
                "secretsmanager:DeleteSecret",
                "secretsmanager:DescribeSecret"
            ],
            "Resource": "*"
        }
    ]
}
```

Or use the managed policy: `SecretsManagerReadWrite`

---

## 4. Creating Your First Secret

### Create a Secret

```bash
aws secretsmanager create-secret \
  --name "my-first-secret" \
  --secret-string "my-super-secret-value" \
  --region us-east-1
```

**What you should see:**
```json
{
    "ARN": "arn:aws:secretsmanager:us-east-1:123456789012:secret:my-first-secret-AbCdEf",
    "Name": "my-first-secret",
    "VersionId": "a1b2c3d4-e5f6-..."
}
```

### Read a Secret

```bash
aws secretsmanager get-secret-value \
  --secret-id "my-first-secret" \
  --query SecretString \
  --output text \
  --region us-east-1
```

**What you should see:** `my-super-secret-value`

### Update a Secret

```bash
aws secretsmanager update-secret \
  --secret-id "my-first-secret" \
  --secret-string "updated-value" \
  --region us-east-1
```

**What you should see:** JSON with updated ARN and VersionId.

### List All Secrets

```bash
aws secretsmanager list-secrets --region us-east-1 --query "SecretList[].Name" --output table
```

**What you should see:** A table of secret names.

### Delete a Secret

```bash
aws secretsmanager delete-secret \
  --secret-id "my-first-secret" \
  --force-delete-without-recovery \
  --region us-east-1
```

**What you should see:** JSON confirming deletion with `DeletionDate`.

> **Note:** Without `--force-delete-without-recovery`, AWS schedules deletion after a 7-30 day recovery window (default 30 days).

---

## 5. Granting AI Agent Access

### Create a Dedicated IAM User

```bash
aws iam create-user --user-name clawdbot-agent
```

### Attach the Secrets Policy

```bash
aws iam attach-user-policy \
  --user-name clawdbot-agent \
  --policy-arn arn:aws:iam::aws:policy/SecretsManagerReadWrite
```

For read-only agent access, create a custom policy:
```bash
aws iam create-policy --policy-name ClawdbotSecretsRead --policy-document '{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["secretsmanager:GetSecretValue", "secretsmanager:ListSecrets"],
    "Resource": "*"
  }]
}'
```

### Create Access Keys for the Agent

```bash
aws iam create-access-key --user-name clawdbot-agent
```

**What you should see:** JSON with `AccessKeyId` and `SecretAccessKey`. Save both securely.

### Configure a Named Profile

```bash
aws configure --profile clawdbot
# Enter the agent's Access Key ID and Secret
```

Use in scripts with `--profile clawdbot` or `export AWS_PROFILE=clawdbot`.

### If Running on EC2

No access keys needed. Attach an IAM role to the EC2 instance:
1. Create IAM role with `SecretsManagerReadWrite` policy
2. Attach it to the EC2 instance via console or CLI

---

## 6. Gateway Wrapper Script

Create `~/.clawdbot/gateway-wrapper.sh`:

```bash
#!/bin/bash
set -euo pipefail

AWS_REGION="us-east-1"

fetch_secret() {
  aws secretsmanager get-secret-value \
    --secret-id "$1" \
    --query SecretString \
    --output text \
    --region "$AWS_REGION" 2>/dev/null
}

export SLACK_BOT_TOKEN=$(fetch_secret "slack-bot-token")
export SQUARE_ACCESS_TOKEN=$(fetch_secret "square-access-token")
# Add more as needed...

exec clawdbot gateway start
```

```bash
chmod +x ~/.clawdbot/gateway-wrapper.sh
```

---

## 7. Common Issues & Troubleshooting

### "AccessDeniedException"

**Cause:** IAM user/role lacks required permissions.

**Fix:**
```bash
aws iam attach-user-policy \
  --user-name YOUR_USER \
  --policy-arn arn:aws:iam::aws:policy/SecretsManagerReadWrite
```

### "aws: command not found"

**Cause:** AWS CLI not installed or not in PATH.

**Fix (macOS):**
```bash
# Check if installed somewhere
which aws || find / -name "aws" -type f 2>/dev/null

# Reinstall via brew
brew install awscli
```

### "Unable to locate credentials"

**Cause:** `aws configure` was never run, or credentials expired.

**Fix:**
```bash
aws configure
# Re-enter your Access Key ID and Secret Access Key
```

### "ResourceNotFoundException"

**Cause:** Secret doesn't exist, or wrong region.

**Fix:**
```bash
# List secrets in your region
aws secretsmanager list-secrets --region us-east-1

# Check if you're in the right region
aws configure get region
```

### "InvalidRequestException: You can't create this secret because a secret with this name is already scheduled for deletion"

**Fix:**
```bash
# Restore the scheduled-for-deletion secret
aws secretsmanager restore-secret --secret-id "secret-name" --region us-east-1
```

---

**Ask me anything about AWS Secrets Manager. I'll walk you through it.**
