#!/usr/bin/env python3
"""
Example usage of the Kinde Management Client.

This example demonstrates how to use the ManagementClient to interact with
the Kinde Management API for various operations like managing users, organizations,
roles, permissions, and feature flags.

Prerequisites:
1. A Kinde account with Management API access
2. Management API credentials (client_id and client_secret)
3. Your Kinde domain
4. A .env file with your credentials

Usage:
    python management_client_example.py
"""

import os
import sys
import json
from typing import Dict, Any
from pathlib import Path

# Add the parent directory to the path so we can import the SDK
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to load python-dotenv if available
try:
    from dotenv import load_dotenv
    # Load .env file from the project root
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Loaded .env file from: {env_path}")
    else:
        print(f"⚠️  .env file not found at: {env_path}")
        print("   You can still use environment variables or set credentials manually.")
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
    print("   You can still use environment variables or set credentials manually.")

from kinde_sdk.management.management_client import ManagementClient


def print_response(title: str, response: Dict[str, Any]):
    """Print a formatted API response."""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(json.dumps(response, indent=2, default=str))


def test_management_client():
    """Test the management client with various API operations."""
    
    # Configuration - Load from .env file or use defaults
    DOMAIN = os.getenv("KINDE_DOMAIN", "your-domain.kinde.com")
    CLIENT_ID = os.getenv("KINDE_MANAGEMENT_CLIENT_ID", "your-management-client-id")
    CLIENT_SECRET = os.getenv("KINDE_MANAGEMENT_CLIENT_SECRET", "your-management-client-secret")
    
    print(f"Testing Management Client with domain: {DOMAIN}")
    print(f"Client ID: {CLIENT_ID[:10]}..." if len(CLIENT_ID) > 10 else f"Client ID: {CLIENT_ID}")
    
    # Check if we have real credentials
    if DOMAIN == "your-domain.kinde.com" or CLIENT_ID == "your-management-client-id":
        print("\n⚠️  Using default/test credentials. Set up your .env file with real credentials for full testing.")
        print("   Expected .env format:")
        print("   KINDE_DOMAIN=your-domain.kinde.com")
        print("   KINDE_MANAGEMENT_CLIENT_ID=your-management-client-id")
        print("   KINDE_MANAGEMENT_CLIENT_SECRET=your-management-client-secret")
    
    # Initialize the management client
    try:
        client = ManagementClient(
            domain=DOMAIN,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )
        print("✅ Management client initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize management client: {e}")
        return
    
    # Test 1: Get timezones (simple GET request)
    print("\n🧪 Test 1: Getting timezones")
    try:
        timezones = client.get_timezones()
        print_response("Timezones Response", timezones)
        print("✅ Timezones API call successful")
    except Exception as e:
        print(f"❌ Failed to get timezones: {e}")
    
    # Test 2: Get industries (simple GET request)
    print("\n🧪 Test 2: Getting industries")
    try:
        industries = client.get_industries()
        print_response("Industries Response", industries)
        print("✅ Industries API call successful")
    except Exception as e:
        print(f"❌ Failed to get industries: {e}")
    
    # Test 3: Get users with pagination
    print("\n🧪 Test 3: Getting users with pagination")
    try:
        users = client.get_users(page_size=5)
        print_response("Users Response (First 5)", users)
        print("✅ Users API call successful")
    except Exception as e:
        print(f"❌ Failed to get users: {e}")
    
    # Test 4: Get organizations
    print("\n🧪 Test 4: Getting organizations")
    try:
        organizations = client.get_organizations()
        print_response("Organizations Response", organizations)
        print("✅ Organizations API call successful")
    except Exception as e:
        print(f"❌ Failed to get organizations: {e}")
    
    # Test 5: Get roles
    print("\n🧪 Test 5: Getting roles")
    try:
        roles = client.get_roles()
        print_response("Roles Response", roles)
        print("✅ Roles API call successful")
    except Exception as e:
        print(f"❌ Failed to get roles: {e}")
    
    # Test 6: Get permissions
    print("\n🧪 Test 6: Getting permissions")
    try:
        permissions = client.get_permissions()
        print_response("Permissions Response", permissions)
        print("✅ Permissions API call successful")
    except Exception as e:
        print(f"❌ Failed to get permissions: {e}")
    
    # Test 7: Get feature flags
    print("\n🧪 Test 7: Getting feature flags")
    try:
        feature_flags = client.get_feature_flags()
        print_response("Feature Flags Response", feature_flags)
        print("✅ Feature Flags API call successful")
    except Exception as e:
        print(f"❌ Failed to get feature flags: {e}")
    
    # Test 8: Get subscribers
    print("\n🧪 Test 8: Getting subscribers")
    try:
        subscribers = client.get_subscribers()
        print_response("Subscribers Response", subscribers)
        print("✅ Subscribers API call successful")
    except Exception as e:
        print(f"❌ Failed to get subscribers: {e}")
    
    # Test 9: Get API applications
    print("\n🧪 Test 9: Getting API applications")
    try:
        api_applications = client.get_api_applications()
        print_response("API Applications Response", api_applications)
        print("✅ API Applications call successful")
    except Exception as e:
        print(f"❌ Failed to get API applications: {e}")
    
    # Test 10: Get connected apps
    print("\n🧪 Test 10: Getting connected apps")
    try:
        connected_apps = client.get_connected_apps()
        print_response("Connected Apps Response", connected_apps)
        print("✅ Connected Apps API call successful")
    except Exception as e:
        print(f"❌ Failed to get connected apps: {e}")
    
    # Test 11: Get specific user (if users exist)
    print("\n🧪 Test 11: Getting specific user")
    try:
        # First get users to find a user ID
        users_response = client.get_users(page_size=1)
        if users_response and 'users' in users_response and users_response['users']:
            user_id = users_response['users'][0].get('id')
            if user_id:
                user = client.get_user(id=user_id)
                print_response(f"User {user_id} Response", user)
                print("✅ Get specific user API call successful")
            else:
                print("⚠️  No user ID found in users response")
        else:
            print("⚠️  No users found to test get_user")
    except Exception as e:
        print(f"❌ Failed to get specific user: {e}")
    
    # Test 12: Get specific organization (if organizations exist)
    print("\n🧪 Test 12: Getting specific organization")
    try:
        # First get organizations to find an org code
        orgs_response = client.get_organizations()
        if orgs_response and 'organizations' in orgs_response and orgs_response['organizations']:
            org_code = orgs_response['organizations'][0].get('code')
            if org_code:
                organization = client.get_organization(org_code)
                print_response(f"Organization {org_code} Response", organization)
                print("✅ Get specific organization API call successful")
            else:
                print("⚠️  No organization code found in organizations response")
        else:
            print("⚠️  No organizations found to test get_organization")
    except Exception as e:
        print(f"❌ Failed to get specific organization: {e}")
    
    print(f"\n{'='*50}")
    print("🎉 Management Client Testing Complete!")
    print(f"{'='*50}")


def test_error_handling():
    """Test error handling with invalid credentials."""
    print("\n🧪 Testing Error Handling")
    
    # Test with invalid credentials
    try:
        client = ManagementClient(
            domain="invalid-domain.kinde.com",
            client_id="invalid-client-id",
            client_secret="invalid-client-secret"
        )
        print("❌ Should have failed with invalid credentials")
    except Exception as e:
        print(f"✅ Correctly handled invalid credentials: {e}")


def create_sample_env_file():
    """Create a sample .env file if it doesn't exist."""
    env_path = Path(__file__).parent.parent / '.env'
    if not env_path.exists():
        print(f"\n📝 Creating sample .env file at: {env_path}")
        sample_content = """# Kinde Management API Configuration
# Replace these values with your actual credentials

# Your Kinde domain (e.g., your-company.kinde.com)
KINDE_DOMAIN=your-domain.kinde.com

# Management API Client ID
KINDE_MANAGEMENT_CLIENT_ID=your-management-client-id

# Management API Client Secret
KINDE_MANAGEMENT_CLIENT_SECRET=your-management-client-secret

# Optional: Other Kinde configuration
# KINDE_CLIENT_ID=your-regular-client-id
# KINDE_CLIENT_SECRET=your-regular-client-secret
# KINDE_REDIRECT_URI=http://localhost:3000/callback
"""
        try:
            with open(env_path, 'w') as f:
                f.write(sample_content)
            print("✅ Sample .env file created successfully!")
            print("   Please edit the file with your actual credentials.")
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")


if __name__ == "__main__":
    print("🚀 Starting Kinde Management Client Tests")
    print("=" * 60)
    
    # Check if .env file exists and create sample if not
    env_path = Path(__file__).parent.parent / '.env'
    if not env_path.exists():
        create_sample_env_file()
    
    # Check if we have the required environment variables
    if (os.getenv("KINDE_DOMAIN") and 
        os.getenv("KINDE_MANAGEMENT_CLIENT_ID") and 
        os.getenv("KINDE_MANAGEMENT_CLIENT_SECRET")):
        
        print("✅ Environment variables found, running full tests")
        test_management_client()
    else:
        print("⚠️  Required environment variables not found in .env file.")
        print("   Please set up your .env file with:")
        print("   - KINDE_DOMAIN")
        print("   - KINDE_MANAGEMENT_CLIENT_ID") 
        print("   - KINDE_MANAGEMENT_CLIENT_SECRET")
        print("\nRunning error handling tests only...")
        test_error_handling()
    
    print("\n📝 Setup Instructions:")
    print("1. Install python-dotenv: pip install python-dotenv")
    print("2. Edit the .env file with your credentials:")
    print("   KINDE_DOMAIN=your-domain.kinde.com")
    print("   KINDE_MANAGEMENT_CLIENT_ID=your-management-client-id")
    print("   KINDE_MANAGEMENT_CLIENT_SECRET=your-management-client-secret")
    print("3. Run: python examples/management_client_example.py") 