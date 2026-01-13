# Da'Riyah Monorepo (Scaffold)

## Services
- `services/dariyah-core`: Da'Riyah Core (Strategy/Music/Video/Distribution/Learning/Build stubs)
- `services/streamgod-presenceos`: StreamGod (PresenceOS) (campaign exec/bot runtime/live DSP stubs)
- `libs/security`: API Wall (API key hashing, signature verification, replay guard, scope enforcement)

## Quickstart (Docker)
1) Copy env:
   - `cp .env.example .env`

2) Start:
   - `docker compose up --build`

## Deployment to AWS App Runner

This repository is configured for automatic deployment to AWS App Runner when code is pushed to the `main` branch.

### Quick Setup (5 minutes)
1. **Add GitHub Secrets** - See [QUICK_START.md](./QUICK_START.md) for step-by-step instructions
2. **Push to main** - Deployment triggers automatically

### Required GitHub Secrets
- `AWS_ACCESS_KEY_ID` - AWS IAM access key
- `AWS_SECRET_ACCESS_KEY` - AWS IAM secret key
- `AWS_REGION` - AWS region (e.g., `us-east-1`)
- `APP_RUNNER_SERVICE_NAME` - Your App Runner service name
- `AWS_SOURCE_CONNECTION_ARN` - App Runner GitHub connection ARN

### Setup Options
- **Option A (Recommended):** Add secrets manually via [GitHub Settings](https://github.com/Dmf-records-fly-hoolie-ent/dmf-music-platform-powered-by-Da-Riyah/settings/secrets/actions)
- **Option B:** Use the automated script: `python3 setup-github-secrets.py`

📖 **Full Documentation:** [DEPLOYMENT_SETUP.md](./DEPLOYMENT_SETUP.md)

## API Wall (Client Requirements)
Every request must include:
- `X-Api-Key`: `dgk_<key_id>_<raw_key_material>`
- `X-Timestamp`: unix seconds (int)
- `X-Nonce`: random unique string (uuid recommended)
- `X-Signature`: hex HMAC-SHA256 signature

Signature input:
`{timestamp}.{nonce}.{method}.{path}.{body_sha256}`

Signature key:
- service-side stored `api_secret` tied to key_id

Body hash:
- SHA256 hex of raw body bytes (empty body => SHA256 of empty bytes)

## Create an API key (dev/admin)
- `POST /admin/api-keys` with header:
  - `X-Admin-Token: <ADMIN_TOKEN>`
- Response includes the raw API key **once**.

## Example curl (Core)
1) Create key:
```bash
curl -s -X POST http://localhost:8001/admin/api-keys \
  -H "X-Admin-Token: dev_admin_token" \
  -H "Content-Type: application/json" \
  -d '{"name":"local-dev","scopes":["campaigns:read","campaigns:write","analytics:read"]}'
