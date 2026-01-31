# Quick Start: Deploy to AWS App Runner

## Prerequisites Checklist

- [ ] AWS Account with active credentials
- [ ] GitHub repository access
- [ ] AWS App Runner service created or service name chosen
- [ ] AWS IAM user with App Runner permissions

## 5-Minute Setup

### Option A: Add Secrets via GitHub Web UI (Fastest) ⚡

1. **Go to Repository Secrets Page:**
   ```
   https://github.com/Dmf-records-fly-hoolie-ent/dmf-music-platform-powered-by-Da-Riyah/settings/secrets/actions
   ```

2. **Add these 5 secrets** (click "New repository secret" for each):

   | Secret Name | Description | Example Value |
   |------------|-------------|---------------|
   | `AWS_ACCESS_KEY_ID` | Your AWS access key | `AKIAIOSFODNN7EXAMPLE` |
   | `AWS_SECRET_ACCESS_KEY` | Your AWS secret key | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
   | `AWS_REGION` | AWS region for deployment | `us-east-1` |
   | `APP_RUNNER_SERVICE_NAME` | Your service name | `dmf-music-platform` |
   | `AWS_SOURCE_CONNECTION_ARN` | App Runner connection ARN | `arn:aws:apprunner:us-east-1:123456789012:connection/my-connection/abc123` |

3. **Trigger Deployment:**
   ```bash
   git add .
   git commit -m "Trigger deployment"
   git push origin main
   ```

4. **Monitor Deployment:**
   - Go to: https://github.com/Dmf-records-fly-hoolie-ent/dmf-music-platform-powered-by-Da-Riyah/actions
   - Watch the "Deploy to AWS App Runner" workflow

### Option B: Add Secrets via GitHub API

**Requirements:**
- GitHub Personal Access Token (PAT) with `repo` scope
- Python 3 with PyNaCl library (`pip install pynacl`)

**Steps:**

1. **Create GitHub Token:**
   - Visit: https://github.com/settings/tokens
   - Generate new token (classic) with `repo` scope
   - Save the token (starts with `ghp_`)

2. **Run the setup script:**
   ```bash
   python3 setup-github-secrets.py
   ```
   (See DEPLOYMENT_SETUP.md for the full script)

## Where to Get Secret Values

### AWS_ACCESS_KEY_ID & AWS_SECRET_ACCESS_KEY
- AWS Console → IAM → Users → Your User → Security credentials → Create access key
- **Save these immediately** - you can't retrieve the secret key later!

### AWS_REGION
- Choose where to deploy: `us-east-1`, `us-west-2`, `eu-west-1`, etc.

### APP_RUNNER_SERVICE_NAME
- Choose a name: lowercase letters, numbers, hyphens only
- Example: `dmf-music-platform`

### AWS_SOURCE_CONNECTION_ARN
- AWS App Runner Console → Settings → Source code connections
- Or create new connection: Console → App Runner → Create service → GitHub

## What Happens After Push to Main?

1. ✅ GitHub Actions workflow triggers automatically
2. ✅ Code is checked out
3. ✅ AWS credentials are configured
4. ✅ App Runner service is deployed
5. ✅ Service URL is displayed in logs

## Verification Steps

After deployment completes:

```bash
# Get your App Runner service URL
aws apprunner describe-service \
  --service-arn $(aws apprunner list-services --region us-east-1 --query "ServiceSummaryList[?ServiceName=='dmf-music-platform'].ServiceArn" --output text) \
  --region us-east-1 \
  --query "Service.ServiceUrl" \
  --output text

# Test the service
curl https://your-service-url.us-east-1.awsapprunner.com
```

## Common Issues

| Issue | Solution |
|-------|----------|
| "Secret not found" error | Check all 5 secrets are added with exact names (case-sensitive) |
| AWS authentication fails | Verify AWS credentials, check IAM permissions |
| Service name already exists | Choose a different APP_RUNNER_SERVICE_NAME |
| Connection ARN invalid | Create GitHub connection in App Runner console first |

## Need Help?

- Full documentation: See [DEPLOYMENT_SETUP.md](./DEPLOYMENT_SETUP.md)
- AWS App Runner Docs: https://docs.aws.amazon.com/apprunner/
- GitHub Actions Docs: https://docs.github.com/en/actions

## Next Steps After Successful Deployment

1. ✅ Save your App Runner service URL
2. ✅ Configure custom domain (optional)
3. ✅ Set up monitoring in AWS CloudWatch
4. ✅ Review and adjust CPU/memory in workflow file
5. ✅ Enable auto-scaling if needed

---

**Pro Tip:** Use GitHub's workflow dispatch to manually trigger deployments without pushing code:
- Go to Actions → Deploy to AWS App Runner → Run workflow
