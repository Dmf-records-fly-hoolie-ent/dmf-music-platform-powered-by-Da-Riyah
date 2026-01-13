#!/usr/bin/env python3
"""
GitHub Secrets Setup Script for AWS App Runner Deployment

This script helps you add the required GitHub secrets programmatically.
You'll need a GitHub Personal Access Token with 'repo' scope.
"""

import base64
import json
import sys
from getpass import getpass
try:
    import requests
    from nacl import encoding, public
except ImportError:
    print("Missing required packages. Install them with:")
    print("  pip install requests pynacl")
    sys.exit(1)

# Repository configuration
REPO_OWNER = "Dmf-records-fly-hoolie-ent"
REPO_NAME = "dmf-music-platform-powered-by-Da-Riyah"

# Required secrets
REQUIRED_SECRETS = [
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_REGION",
    "APP_RUNNER_SERVICE_NAME",
    "AWS_SOURCE_CONNECTION_ARN"
]

def get_public_key(github_token):
    """Get repository public key for encrypting secrets."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/secrets/public-key"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error getting public key: {response.status_code}")
        print(response.text)
        return None
    
    return response.json()

def encrypt_secret(public_key_data, secret_value):
    """Encrypt a secret using the repository's public key."""
    public_key_bytes = encoding.Base64Encoder.decode(public_key_data)
    sealed_box = public.SealedBox(public.PublicKey(public_key_bytes))
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")

def add_secret(github_token, secret_name, secret_value, public_key_info):
    """Add or update a secret in the repository."""
    encrypted_value = encrypt_secret(public_key_info["key"], secret_value)
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/secrets/{secret_name}"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "encrypted_value": encrypted_value,
        "key_id": public_key_info["key_id"]
    }
    
    response = requests.put(url, headers=headers, json=data)
    if response.status_code in [201, 204]:
        return True
    else:
        print(f"Error adding secret {secret_name}: {response.status_code}")
        print(response.text)
        return False

def main():
    print("=" * 70)
    print("GitHub Secrets Setup for AWS App Runner Deployment")
    print("=" * 70)
    print()
    print(f"Repository: {REPO_OWNER}/{REPO_NAME}")
    print()
    print("This script will help you add 5 required secrets:")
    for secret in REQUIRED_SECRETS:
        print(f"  - {secret}")
    print()
    
    # Get GitHub token
    print("Step 1: GitHub Authentication")
    print("-" * 70)
    print("You need a GitHub Personal Access Token with 'repo' scope.")
    print("Create one at: https://github.com/settings/tokens")
    print()
    github_token = getpass("Enter your GitHub token (starts with ghp_): ").strip()
    
    if not github_token.startswith("ghp_"):
        print("Warning: Token should start with 'ghp_'. Continuing anyway...")
    
    # Get public key
    print("\nVerifying access and getting repository public key...")
    public_key_info = get_public_key(github_token)
    if not public_key_info:
        print("Failed to get repository public key. Please check your token and try again.")
        sys.exit(1)
    
    print("✓ Successfully authenticated!")
    print()
    
    # Collect secret values
    print("Step 2: Enter Secret Values")
    print("-" * 70)
    print("Enter the values for each secret. Leave blank to skip.")
    print()
    
    secrets = {}
    
    # AWS Access Key ID
    print("1. AWS_ACCESS_KEY_ID")
    print("   (AWS IAM access key, e.g., AKIAIOSFODNN7EXAMPLE)")
    secrets["AWS_ACCESS_KEY_ID"] = getpass("   Value: ").strip()
    
    # AWS Secret Access Key
    print("\n2. AWS_SECRET_ACCESS_KEY")
    print("   (AWS IAM secret key)")
    secrets["AWS_SECRET_ACCESS_KEY"] = getpass("   Value: ").strip()
    
    # AWS Region
    print("\n3. AWS_REGION")
    print("   (AWS region, e.g., us-east-1, us-west-2, eu-west-1)")
    secrets["AWS_REGION"] = input("   Value: ").strip()
    
    # App Runner Service Name
    print("\n4. APP_RUNNER_SERVICE_NAME")
    print("   (Service name, e.g., dmf-music-platform)")
    secrets["APP_RUNNER_SERVICE_NAME"] = input("   Value: ").strip()
    
    # AWS Source Connection ARN
    print("\n5. AWS_SOURCE_CONNECTION_ARN")
    print("   (App Runner connection ARN, e.g., arn:aws:apprunner:region:account:connection/name/id)")
    secrets["AWS_SOURCE_CONNECTION_ARN"] = input("   Value: ").strip()
    
    # Filter out empty secrets
    secrets = {k: v for k, v in secrets.items() if v}
    
    if not secrets:
        print("\nNo secrets provided. Exiting.")
        sys.exit(0)
    
    # Confirm before adding
    print()
    print("Step 3: Confirm")
    print("-" * 70)
    print(f"Ready to add {len(secrets)} secret(s):")
    for secret_name in secrets.keys():
        print(f"  ✓ {secret_name}")
    print()
    confirm = input("Proceed? (yes/no): ").strip().lower()
    
    if confirm not in ["yes", "y"]:
        print("Cancelled.")
        sys.exit(0)
    
    # Add secrets
    print()
    print("Step 4: Adding Secrets")
    print("-" * 70)
    
    success_count = 0
    for secret_name, secret_value in secrets.items():
        print(f"Adding {secret_name}...", end=" ")
        if add_secret(github_token, secret_name, secret_value, public_key_info):
            print("✓")
            success_count += 1
        else:
            print("✗")
    
    print()
    print("=" * 70)
    print(f"Completed: {success_count}/{len(secrets)} secrets added successfully")
    print("=" * 70)
    
    if success_count == 5:
        print()
        print("🎉 All secrets added! You can now trigger deployment by:")
        print("   1. Pushing to main branch: git push origin main")
        print("   2. Or manually trigger workflow in GitHub Actions")
        print()
        print(f"   Monitor deployment at:")
        print(f"   https://github.com/{REPO_OWNER}/{REPO_NAME}/actions")
    elif success_count > 0:
        print()
        print("⚠️  Some secrets were added, but not all.")
        print("   You can add the remaining secrets via GitHub UI:")
        print(f"   https://github.com/{REPO_OWNER}/{REPO_NAME}/settings/secrets/actions")
    else:
        print()
        print("❌ No secrets were added. Please check the errors above.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
