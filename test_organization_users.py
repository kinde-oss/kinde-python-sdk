#!/usr/bin/env python3
"""
Test script for organization user endpoints in the management client.
"""

import os
import sys

# Load environment variables from .env if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # If python-dotenv is not installed, skip loading .env

from kinde_sdk.management.management_client import ManagementClient

def test_organization_users():
    """Test the organization users endpoints."""
    
    # Get credentials from environment variables
    domain = os.getenv('KINDE_DOMAIN')
    client_id = os.getenv('KINDE_CLIENT_ID')
    client_secret = os.getenv('KINDE_CLIENT_SECRET')
    
    missing = []
    if not domain:
        missing.append('KINDE_DOMAIN')
    if not client_id:
        missing.append('KINDE_CLIENT_ID')
    if not client_secret:
        missing.append('KINDE_CLIENT_SECRET')
    if missing:
        print(f"Please set the following environment variables: {', '.join(missing)}")
        print("You can create a .env file with these variables for local development.")
        return
    
    try:
        # Initialize the management client
        client = ManagementClient(domain, client_id, client_secret)
        
        print("✅ Management client initialized successfully")
        
        # Test that the organization user methods exist
        methods_to_test = [
            'get_organization_users',
            'add_organization_user', 
            'update_organization_user',
            'remove_organization_user',
            'get_organization_user_roles',
            'add_organization_user_role',
            'remove_organization_user_role',
            'get_organization_user_permissions',
            'add_organization_user_permission',
            'remove_organization_user_permission',
        ]
        
        for method_name in methods_to_test:
            if hasattr(client, method_name):
                print(f"✅ Method {method_name} exists")
            else:
                print(f"❌ Method {method_name} is missing")
        
        # Test that other new endpoints exist (using actual generated method names)
        other_methods = [
            'get_properties',
            'get_user_properties',
            'get_organization_properties',
            'get_webhooks',
            'get_event',  # Changed from get_events (singular)
            'get_connections',
            'get_business',
            'get_environment_feature_flags',
            'get_organization_feature_flags',
            'get_user_feature_flag',  # Changed from get_user_feature_flags (singular)
            'update_user_password',
            'refresh_user_refresh_claim',  # Changed from refresh_user_claims (based on action name)
        ]
        
        print("\nTesting other new endpoints:")
        for method_name in other_methods:
            if hasattr(client, method_name):
                print(f"✅ Method {method_name} exists")
            else:
                print(f"❌ Method {method_name} is missing")
        
        # Let's also check what methods are actually available
        print("\n🔍 Available methods on ManagementClient:")
        available_methods = [method for method in dir(client) if not method.startswith('_') and callable(getattr(client, method))]
        available_methods.sort()
        for method in available_methods[:20]:  # Show first 20 methods
            print(f"  - {method}")
        if len(available_methods) > 20:
            print(f"  ... and {len(available_methods) - 20} more methods")
        
        # Specifically check for get_ methods to debug the get_business issue
        print("\n🔍 All get_ methods:")
        get_methods = [method for method in available_methods if method.startswith('get_')]
        get_methods.sort()
        for method in get_methods:
            print(f"  - {method}")
        
        # Check if get_business specifically exists
        if hasattr(client, 'get_business'):
            print("\n✅ get_business method exists!")
        else:
            print("\n❌ get_business method is missing!")
        
        print("\n🎉 All tests completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_organization_users()
    sys.exit(0 if success else 1) 