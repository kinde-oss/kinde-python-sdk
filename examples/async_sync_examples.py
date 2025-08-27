#!/usr/bin/env python3
"""
Examples demonstrating the new async/sync consistency patterns in the Kinde Python SDK.

This example shows how to use the three different client types:
1. OAuth (sync only)
2. AsyncOAuth (async only) 
3. SmartOAuth (context-aware)

Prerequisites:
1. A Kinde account
2. Environment variables set up
3. FastAPI and Flask installed for framework examples
"""

import os
import asyncio
from typing import Dict, Any
from pathlib import Path

# Add the parent directory to the path so we can import the SDK
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to load python-dotenv if available
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Loaded .env file from: {env_path}")
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")

from kinde_sdk import OAuth, AsyncOAuth, SmartOAuth, create_oauth_client
from kinde_sdk.auth import claims, permissions, roles, feature_flags

def example_sync_oauth():
    """Example using the sync OAuth client."""
    print("\n" + "="*50)
    print("SYNC OAUTH EXAMPLE")
    print("="*50)
    
    # Initialize sync OAuth client
    oauth = OAuth(
        framework="flask",  # or None for no framework
        client_id=os.getenv("KINDE_CLIENT_ID"),
        client_secret=os.getenv("KINDE_CLIENT_SECRET"),
        redirect_uri=os.getenv("KINDE_REDIRECT_URI"),
        host=os.getenv("KINDE_HOST", "https://app.kinde.com")
    )
    
    print("✅ Sync OAuth client initialized")
    
    # All methods are sync
    is_auth = oauth.is_authenticated()
    print(f"🔐 Is authenticated: {is_auth}")
    
    if is_auth:
        user_info = oauth.get_user_info()
        print(f"👤 User info: {user_info.get('email', 'N/A')}")
    
    # Note: login, register, logout are still async even in sync client
    # This is the inconsistency we're addressing
    print("⚠️  Note: login/register/logout methods are still async in sync client")
    
    return oauth

async def example_async_oauth():
    """Example using the async OAuth client."""
    print("\n" + "="*50)
    print("ASYNC OAUTH EXAMPLE")
    print("="*50)
    
    # Initialize async OAuth client
    oauth = AsyncOAuth(
        framework="fastapi",  # or None for no framework
        client_id=os.getenv("KINDE_CLIENT_ID"),
        client_secret=os.getenv("KINDE_CLIENT_SECRET"),
        redirect_uri=os.getenv("KINDE_REDIRECT_URI"),
        host=os.getenv("KINDE_HOST", "https://app.kinde.com")
    )
    
    print("✅ Async OAuth client initialized")
    
    # All methods are async
    is_auth = oauth.is_authenticated()
    print(f"🔐 Is authenticated: {is_auth}")
    
    if is_auth:
        user_info = await oauth.get_user_info_async()
        print(f"👤 User info: {user_info.get('email', 'N/A')}")
    
    # All methods are consistently async
    print("✅ All methods are consistently async")
    
    return oauth

async def example_smart_oauth():
    """Example using the smart OAuth client."""
    print("\n" + "="*50)
    print("SMART OAUTH EXAMPLE")
    print("="*50)
    
    # Initialize smart OAuth client
    oauth = SmartOAuth(
        framework="fastapi",  # or None for no framework
        client_id=os.getenv("KINDE_CLIENT_ID"),
        client_secret=os.getenv("KINDE_CLIENT_SECRET"),
        redirect_uri=os.getenv("KINDE_REDIRECT_URI"),
        host=os.getenv("KINDE_HOST", "https://app.kinde.com")
    )
    
    print("✅ Smart OAuth client initialized")
    
    # Works in both sync and async contexts
    is_auth = oauth.is_authenticated()
    print(f"🔐 Is authenticated: {is_auth}")
    
    if is_auth:
        # In async context, prefer async methods
        user_info = await oauth.get_user_info_async()
        print(f"👤 User info (async): {user_info.get('email', 'N/A')}")
        
        # Sync methods work but show warnings in async context
        user_info_sync = oauth.get_user_info()
        print(f"👤 User info (sync): {user_info_sync.get('email', 'N/A')}")
    
    return oauth

def example_factory_function():
    """Example using the factory function."""
    print("\n" + "="*50)
    print("FACTORY FUNCTION EXAMPLE")
    print("="*50)
    
    # Create explicit sync client
    sync_oauth = create_oauth_client(
        async_mode=False,
        framework="flask",
        client_id=os.getenv("KINDE_CLIENT_ID"),
        client_secret=os.getenv("KINDE_CLIENT_SECRET"),
        redirect_uri=os.getenv("KINDE_REDIRECT_URI"),
        host=os.getenv("KINDE_HOST", "https://app.kinde.com")
    )
    print("✅ Created explicit sync client")
    
    # Create explicit async client
    async_oauth = create_oauth_client(
        async_mode=True,
        framework="fastapi",
        client_id=os.getenv("KINDE_CLIENT_ID"),
        client_secret=os.getenv("KINDE_CLIENT_SECRET"),
        redirect_uri=os.getenv("KINDE_REDIRECT_URI"),
        host=os.getenv("KINDE_HOST", "https://app.kinde.com")
    )
    print("✅ Created explicit async client")
    
    # Create smart client (default)
    smart_oauth = create_oauth_client(
        framework="fastapi",
        client_id=os.getenv("KINDE_CLIENT_ID"),
        client_secret=os.getenv("KINDE_CLIENT_SECRET"),
        redirect_uri=os.getenv("KINDE_REDIRECT_URI"),
        host=os.getenv("KINDE_HOST", "https://app.kinde.com")
    )
    print("✅ Created smart client")
    
    return sync_oauth, async_oauth, smart_oauth

async def example_auth_modules():
    """Example using the auth modules (claims, permissions, roles, feature_flags)."""
    print("\n" + "="*50)
    print("AUTH MODULES EXAMPLE")
    print("="*50)
    
    # All auth modules are async
    print("📋 Getting user claims...")
    try:
        user_claims = await claims.get_all_claims()
        print(f"✅ Claims: {len(user_claims)} claims found")
    except Exception as e:
        print(f"❌ Failed to get claims: {e}")
    
    print("🔐 Getting user permissions...")
    try:
        user_permissions = await permissions.get_permissions()
        print(f"✅ Permissions: {len(user_permissions.get('permissions', []))} permissions found")
    except Exception as e:
        print(f"❌ Failed to get permissions: {e}")
    
    print("👥 Getting user roles...")
    try:
        user_roles = await roles.get_roles()
        print(f"✅ Roles: {len(user_roles.get('roles', []))} roles found")
    except Exception as e:
        print(f"❌ Failed to get roles: {e}")
    
    print("🚩 Getting feature flags...")
    try:
        user_flags = await feature_flags.get_all_flags()
        print(f"✅ Feature flags: {len(user_flags.get('feature_flags', []))} flags found")
    except Exception as e:
        print(f"❌ Failed to get feature flags: {e}")

def example_framework_integration():
    """Example showing framework integration patterns."""
    print("\n" + "="*50)
    print("FRAMEWORK INTEGRATION EXAMPLE")
    print("="*50)
    
    print("Flask Integration (Sync):")
    print("""
    from flask import Flask
    from kinde_sdk import OAuth
    
    app = Flask(__name__)
    oauth = OAuth(framework="flask", app=app)
    
    @app.route('/')
    def home():
        if oauth.is_authenticated():
            user_info = oauth.get_user_info()
            return f"Welcome, {user_info['email']}!"
        return "Please login"
    """)
    
    print("\nFastAPI Integration (Async):")
    print("""
    from fastapi import FastAPI
    from kinde_sdk import AsyncOAuth
    
    app = FastAPI()
    oauth = AsyncOAuth(framework="fastapi", app=app)
    
    @app.get('/')
    async def home():
        if oauth.is_authenticated():
            user_info = await oauth.get_user_info_async()
            return {"message": f"Welcome, {user_info['email']}!"}
        return {"message": "Please login"}
    """)
    
    print("\nFastAPI with Smart Client:")
    print("""
    from fastapi import FastAPI
    from kinde_sdk import SmartOAuth
    
    app = FastAPI()
    oauth = SmartOAuth(framework="fastapi", app=app)
    
    @app.get('/')
    async def home():
        if oauth.is_authenticated():
            user_info = await oauth.get_user_info_async()
            return {"message": f"Welcome, {user_info['email']}!"}
        return {"message": "Please login"}
    """)

async def main():
    """Run all examples."""
    print("🚀 Kinde Python SDK Async/Sync Consistency Examples")
    print("="*60)
    
    # Check environment variables
    required_vars = ["KINDE_CLIENT_ID", "KINDE_CLIENT_SECRET", "KINDE_REDIRECT_URI"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {missing_vars}")
        print("   Set these in your .env file or environment:")
        for var in missing_vars:
            print(f"   {var}=your_value")
        print("\n   Examples will run but may not work properly without authentication.")
    else:
        print("✅ All required environment variables are set")
    
    # Run examples
    try:
        # Sync OAuth example
        sync_oauth = example_sync_oauth()
        
        # Async OAuth example
        async_oauth = await example_async_oauth()
        
        # Smart OAuth example
        smart_oauth = await example_smart_oauth()
        
        # Factory function example
        factory_sync, factory_async, factory_smart = example_factory_function()
        
        # Auth modules example
        await example_auth_modules()
        
        # Framework integration example
        example_framework_integration()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("\nKey Takeaways:")
        print("1. Use OAuth for sync applications")
        print("2. Use AsyncOAuth for async applications")
        print("3. Use SmartOAuth for mixed contexts")
        print("4. All auth modules (claims, permissions, roles, feature_flags) are async")
        print("5. Factory function provides explicit control")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("   This is expected if you don't have proper authentication set up.")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
