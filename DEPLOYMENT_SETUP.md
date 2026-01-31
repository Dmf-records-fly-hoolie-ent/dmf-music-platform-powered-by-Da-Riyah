# GitHub Secrets Setup for AWS App Runner Deployment

This document explains how to set up the required GitHub secrets for AWS App Runner deployment.

## Required GitHub Secrets

You need to add the following 5 secrets to your GitHub repository:

1. **AWS_ACCESS_KEY_ID** - Your AWS IAM access key ID
2. **AWS_SECRET_ACCESS_KEY** - Your AWS IAM secret access key
3. **AWS_REGION** - The AWS region where your App Runner service is deployed (e.g., `us-east-1`)
4. **APP_RUNNER_SERVICE_NAME** - The name of your App Runner service
5. **AWS_SOURCE_CONNECTION_ARN** - The ARN of your AWS App Runner source connection

## How to Add Secrets via GitHub Web UI (Recommended)

### Step 1: Navigate to Repository Secrets

1. Go to your repository on GitHub
2. Click on **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click the **New repository secret** button

### Step 2: Add Each Secret

For each of the 5 secrets listed above:

1. Click **New repository secret**
2. Enter the **Name** (exactly as shown above, e.g., `AWS_ACCESS_KEY_ID`)
3. Enter the **Value** (the actual secret value)
4. Click **Add secret**

Repeat this process for all 5 secrets.

### Step 3: Verify Secrets Are Added

After adding all secrets, you should see them listed on the Secrets page (values will be hidden).

## How to Get the Secret Values

### AWS Access Keys (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY)

1. Log in to the [AWS Console](https://console.aws.amazon.com/)
2. Go to **IAM** → **Users**
3. Select your user or create a new user with appropriate permissions
4. Go to **Security credentials** tab
5. Click **Create access key**
6. Choose **Application running outside AWS**
7. Save the **Access key ID** and **Secret access key** (you won't be able to see the secret key again)

**Required IAM Permissions:**
- `apprunner:*` (or more specific App Runner permissions)
- `iam:PassRole` (if using service roles)
- `ecr:*` (if using ECR for container images)

### AWS Region (AWS_REGION)

Choose the AWS region where you want to deploy your App Runner service:
- Examples: `us-east-1`, `us-west-2`, `eu-west-1`, `ap-southeast-1`
- See [AWS Regions](https://docs.aws.amazon.com/general/latest/gr/apprunner.html) for available regions

### App Runner Service Name (APP_RUNNER_SERVICE_NAME)

This is the name you want to give to your App Runner service:
- Must be unique in your AWS account and region
- Can contain lowercase letters, numbers, and hyphens
- Example: `dmf-music-platform`

### AWS Source Connection ARN (AWS_SOURCE_CONNECTION_ARN)

If deploying from GitHub:

1. Go to [AWS App Runner Console](https://console.aws.amazon.com/apprunner/)
2. Click **Create service**
3. Choose **Source code repository**
4. Click **Add new** under GitHub connections
5. Follow the prompts to connect your GitHub account
6. After creating the connection, go to **Settings** → **Source code connections**
7. Copy the **ARN** of your connection (format: `arn:aws:apprunner:region:account-id:connection/name/id`)

Alternatively, use AWS CLI:
```bash
aws apprunner list-connections --region your-region
```

## Alternative: Add Secrets Programmatically

If you have a GitHub Personal Access Token with `repo` scope, you can add secrets via the GitHub API.

### Create a GitHub Token

1. Go to [GitHub Settings → Tokens](https://github.com/settings/tokens)
2. Click **Generate new token (classic)**
3. Select scopes: `repo` (full control of private repositories)
4. Generate and save the token (starts with `ghp_`)

### Use the GitHub API Script

Create a file named `add-secrets.sh`:

```bash
#!/bin/bash

GITHUB_TOKEN="your_github_token_here"
REPO_OWNER="Dmf-records-fly-hoolie-ent"
REPO_NAME="dmf-music-platform-powered-by-Da-Riyah"

# Function to encrypt and add secret
add_secret() {
  local secret_name=$1
  local secret_value=$2
  
  # Get public key
  pub_key_response=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
    "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/secrets/public-key")
  
  key_id=$(echo "$pub_key_response" | jq -r '.key_id')
  public_key=$(echo "$pub_key_response" | jq -r '.key')
  
  # Encrypt secret (requires libsodium)
  encrypted_value=$(echo -n "$secret_value" | \
    python3 -c "
import sys
import base64
from nacl import encoding, public

secret_value = sys.stdin.read()
public_key = encoding.Base64Encoder.decode('$public_key')
sealed_box = public.SealedBox(public.PublicKey(public_key))
encrypted = sealed_box.encrypt(secret_value.encode('utf-8'))
print(base64.b64encode(encrypted).decode('utf-8'))
")
  
  # Add secret
  curl -X PUT \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/secrets/$secret_name" \
    -d "{\"encrypted_value\":\"$encrypted_value\",\"key_id\":\"$key_id\"}"
}

# Add your secrets
add_secret "AWS_ACCESS_KEY_ID" "your_aws_access_key_id"
add_secret "AWS_SECRET_ACCESS_KEY" "your_aws_secret_access_key"
add_secret "AWS_REGION" "us-east-1"
add_secret "APP_RUNNER_SERVICE_NAME" "dmf-music-platform"
add_secret "AWS_SOURCE_CONNECTION_ARN" "your_connection_arn"
```

Run:
```bash
chmod +x add-secrets.sh
./add-secrets.sh
```

## Triggering the Deployment

Once all secrets are added:

1. Push any change to the `main` branch:
   ```bash
   git add .
   git commit -m "Trigger deployment"
   git push origin main
   ```

2. Or manually trigger the workflow:
   - Go to **Actions** tab in GitHub
   - Select **Deploy to AWS App Runner** workflow
   - Click **Run workflow** → **Run workflow**

## Verifying the Deployment

1. Go to the **Actions** tab in your GitHub repository
2. Click on the most recent workflow run
3. Monitor the deployment progress
4. Once complete, the App Runner URL will be displayed in the logs

## Troubleshooting

### Workflow fails with "Secret not found"
- Verify all 5 secrets are added with exact names (case-sensitive)
- Check for typos in secret names

### Workflow fails with AWS authentication error
- Verify AWS credentials are correct
- Check IAM user has required permissions
- Ensure access key is active (not deleted or expired)

### App Runner service creation fails
- Verify the service name is valid and not already in use
- Check the source connection ARN is correct
- Ensure your AWS account has App Runner enabled in the selected region

## Next Steps

After successfully deploying:
1. Note the App Runner service URL from the deployment logs
2. Configure your custom domain (if needed) in AWS App Runner console
3. Set up monitoring and alarms in AWS CloudWatch
4. Review and adjust CPU/memory settings in the workflow file

## Security Best Practices

- Never commit secrets to your repository
- Rotate AWS access keys regularly
- Use IAM roles with minimum required permissions
- Enable AWS CloudTrail for audit logging
- Review GitHub Actions logs carefully before making them public
