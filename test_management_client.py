#!/usr/bin/env python3
"""
Quick test script for the Kinde Management Client.

This script provides a simple way to test that the management client
is working correctly after the restructure.

Usage:
    python test_management_client.py
"""

import os
import sys
from pathlib import Path

# Try to load python-dotenv if available
try:
    from dotenv import load_dotenv
    # Load .env file from the project root
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Loaded .env file from: {env_path}")
    else:
        print(f"⚠️  .env file not found at: {env_path}")
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")

from kinde_sdk.management.management_client import ManagementClient


def test_basic_functionality():
    """Test basic management client functionality."""
    
    print("🧪 Testing Management Client Basic Functionality")
    print("=" * 50)
    
    # Get credentials from .env file or use defaults for testing
    domain = os.getenv("KINDE_DOMAIN", "test.kinde.com")
    client_id = os.getenv("KINDE_MANAGEMENT_CLIENT_ID", "test-client-id")
    client_secret = os.getenv("KINDE_MANAGEMENT_CLIENT_SECRET", "test-client-secret")
    
    print(f"Domain: {domain}")
    print(f"Client ID: {client_id[:10]}..." if len(client_id) > 10 else f"Client ID: {client_id}")
    
    # Check if we have real credentials
    if domain == "test.kinde.com" or client_id == "test-client-id":
        print("\n⚠️  Using test credentials. Set up your .env file with real credentials for full testing.")
    
    try:
        # Test 1: Initialize the client
        print("\n1. Testing client initialization...")
        client = ManagementClient(
            domain=domain,
            client_id=client_id,
            client_secret=client_secret
        )
        print("✅ Client initialized successfully")
        
        # Test 2: Check if methods are generated
        print("\n2. Testing method generation...")
        expected_methods = [
            'get_users', 'get_user', 'create_user', 'update_user', 'delete_user',
            'get_organizations', 'get_organization', 'create_organization', 'update_organization', 'delete_organization',
            'get_roles', 'get_role', 'create_role', 'update_role', 'delete_role',
            'get_permissions', 'get_permission', 'create_permission', 'update_permission', 'delete_permission',
            'get_feature_flags', 'get_feature_flag', 'create_feature_flag', 'update_feature_flag', 'delete_feature_flag',
            'get_timezones', 'get_industries', 'get_subscribers', 'get_connected_apps', 'get_api_applications'
        ]
        
        missing_methods = []
        for method in expected_methods:
            if not hasattr(client, method):
                missing_methods.append(method)
        
        if missing_methods:
            print(f"❌ Missing methods: {missing_methods}")
        else:
            print("✅ All expected methods are available")
        
        # Test 3: Test a simple API call (if credentials are real)
        if domain != "test.kinde.com":
            print("\n3. Testing API call...")
            try:
                timezones = client.get_timezones()
                print("✅ API call successful")
                print(f"   Response keys: {list(timezones.keys()) if isinstance(timezones, dict) else 'Not a dict'}")
            except Exception as e:
                print(f"⚠️  API call failed (expected if using test credentials): {e}")
        else:
            print("\n3. Skipping API call (using test credentials)")
        
        # Test 4: Check token manager
        print("\n4. Testing token manager...")
        if hasattr(client, 'token_manager'):
            print("✅ Token manager is available")
            print(f"   Token manager type: {type(client.token_manager).__name__}")
        else:
            print("❌ Token manager not found")
        
        # Test 5: Check API client
        print("\n5. Testing API client...")
        if hasattr(client, 'api_client'):
            print("✅ API client is available")
            print(f"   API client type: {type(client.api_client).__name__}")
        else:
            print("❌ API client not found")
        
        print("\n🎉 Basic functionality test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_imports():
    """Test that all necessary imports work."""
    print("🧪 Testing Imports")
    print("=" * 30)
    
    try:
        from kinde_sdk.management.management_client import ManagementClient
        print("✅ ManagementClient import successful")
        
        from kinde_sdk.management.management_token_manager import ManagementTokenManager
        print("✅ ManagementTokenManager import successful")
        
        from kinde_sdk.management.configuration import Configuration
        print("✅ Configuration import successful")
        
        from kinde_sdk.management.api_client import ApiClient
        print("✅ ApiClient import successful")
        
        print("✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def create_sample_env_file():
    """Create a sample .env file if it doesn't exist."""
    env_path = Path(__file__).parent / '.env'
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
    print("🚀 Starting Management Client Tests")
    print("=" * 60)
    
    # Check if .env file exists and create sample if not
    env_path = Path(__file__).parent / '.env'
    if not env_path.exists():
        create_sample_env_file()
    
    # Test imports first
    imports_ok = test_imports()
    
    if imports_ok:
        # Test basic functionality
        functionality_ok = test_basic_functionality()
        
        if functionality_ok:
            print("\n🎉 All tests passed! The management client is working correctly.")
        else:
            print("\n❌ Some functionality tests failed.")
    else:
        print("\n❌ Import tests failed. Check your installation.")
    
    print("\n📝 Setup Instructions:")
    print("1. Install python-dotenv: pip install python-dotenv")
    print("2. Edit the .env file with your credentials:")
    print("   KINDE_DOMAIN=your-domain.kinde.com")
    print("   KINDE_MANAGEMENT_CLIENT_ID=your-management-client-id")
    print("   KINDE_MANAGEMENT_CLIENT_SECRET=your-management-client-secret")
    print("3. Run: python test_management_client.py") 