"""
Flask Route Protection Example

This example demonstrates how to use the Kinde Python SDK's route protection feature
to secure Flask application routes based on user roles and permissions.
"""

import os
from flask import Flask, jsonify, render_template_string
from kinde_sdk.auth import OAuth

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-change-in-production')

# Initialize Kinde OAuth with route protection
oauth = OAuth(
    framework="flask",
    app=app,
    route_protection_file="route_protection_config.yaml"  # Enable route protection
)

# Simple HTML template for demonstration
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Route Protection Example</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; }
        .success { background-color: #d4edda; border-color: #c3e6cb; }
        .error { background-color: #f8d7da; border-color: #f5c6cb; }
        a { color: #007bff; text-decoration: none; margin-right: 15px; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>🛡️ Kinde Route Protection Example</h1>
    
    <div class="section success">
        <h2>✅ Public Routes (No Authentication Required)</h2>
        <a href="/public/info">Public Information</a>
        <a href="/docs">Documentation</a>
        <a href="/health">Health Check</a>
    </div>
    
    <div class="section">
        <h2>🔒 Protected Routes (Authentication Required)</h2>
        <p><strong>User Level:</strong></p>
        <a href="/profile/settings">Profile Settings</a>
        <a href="/dashboard">User Dashboard</a>
        
        <p><strong>Manager Level:</strong></p>
        <a href="/manage/users">User Management</a>
        <a href="/reports">Reports</a>
        
        <p><strong>Admin Only:</strong></p>
        <a href="/admin/dashboard">Admin Dashboard</a>
        <a href="/admin/system">System Settings</a>
    </div>
    
    <div class="section">
        <h2>🔑 API Endpoints (Permission-based)</h2>
        <a href="/api/v1/users">Users API (read:users)</a>
        <a href="/api/v1/reports">Reports API (read:reports)</a>
    </div>
    
    <div class="section">
        <h2>🔍 Debug Information</h2>
        <p><strong>Route Protection Enabled:</strong> {{ protection_enabled }}</p>
        <p><strong>Total Protected Routes:</strong> {{ total_routes }}</p>
        <a href="/protection-info">View Protection Rules</a>
    </div>
    
    {% if user %}
    <div class="section success">
        <h2>👤 Current User</h2>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Name:</strong> {{ user.given_name }} {{ user.family_name }}</p>
        <a href="/logout">Logout</a>
    </div>
    {% else %}
    <div class="section error">
        <h2>🚪 Not Authenticated</h2>
        <p>You are not currently logged in. Many routes will be protected.</p>
        <a href="/login">Login with Kinde</a>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def home():
    """Home page showing route protection example."""
    user = None
    if oauth.is_authenticated():
        user = oauth.get_user_info()
    
    protection_info = oauth.get_route_protection_info()
    
    return render_template_string(HTML_TEMPLATE, 
                                 user=user,
                                 protection_enabled=oauth.is_route_protection_enabled(),
                                 total_routes=protection_info['total_routes'] if protection_info else 0)

# === PUBLIC ROUTES (No Authentication Required) ===

@app.route('/public/info')
def public_info():
    """Public information page."""
    return jsonify({
        "message": "This is public information available to everyone!",
        "type": "public",
        "protection": "none"
    })

@app.route('/docs')
def documentation():
    """Public documentation."""
    return jsonify({
        "title": "API Documentation",
        "message": "This documentation is publicly accessible",
        "routes": [
            {"path": "/api/v1/users", "method": "GET", "requires": "read:users permission"},
            {"path": "/admin/*", "method": "ALL", "requires": "admin role"}
        ]
    })

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "route_protection": oauth.is_route_protection_enabled(),
        "timestamp": "2024-01-01T00:00:00Z"
    })

# === USER-LEVEL PROTECTED ROUTES ===

@app.route('/profile/settings')
def profile_settings():
    """User profile settings (requires user role)."""
    return jsonify({
        "message": "Welcome to your profile settings!",
        "type": "user_content",
        "required_roles": ["user", "manager", "admin"],
        "user": oauth.get_user_info() if oauth.is_authenticated() else None
    })

@app.route('/dashboard')
def user_dashboard():
    """User dashboard (requires user role)."""
    return jsonify({
        "message": "Welcome to your personal dashboard!",
        "type": "user_dashboard",
        "widgets": ["Recent Activity", "Profile Summary", "Notifications"]
    })

# === MANAGER-LEVEL PROTECTED ROUTES ===

@app.route('/manage/users')
def manage_users():
    """User management (requires manager or admin role)."""
    return jsonify({
        "message": "User Management Panel",
        "type": "manager_content",
        "required_roles": ["manager", "admin"],
        "actions": ["view_users", "edit_users", "manage_roles"]
    })

@app.route('/reports')
def reports():
    """Reports section (requires manager or admin role)."""
    return jsonify({
        "message": "Business Reports Dashboard",
        "type": "manager_content", 
        "reports": ["User Analytics", "Performance Metrics", "Financial Summary"]
    })

# === ADMIN-ONLY PROTECTED ROUTES ===

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard (requires admin role)."""
    return jsonify({
        "message": "Administrator Dashboard - Top Secret!",
        "type": "admin_content",
        "required_roles": ["admin"],
        "admin_tools": ["System Settings", "User Management", "Security Center"]
    })

@app.route('/admin/system')
def admin_system():
    """System settings (requires admin role)."""
    return jsonify({
        "message": "System Configuration Panel",
        "type": "admin_content",
        "settings": ["Database Config", "Security Policies", "Feature Flags"]
    })

# === PERMISSION-BASED API ROUTES ===

@app.route('/api/v1/users')
def api_users():
    """Users API (requires read:users permission)."""
    return jsonify({
        "users": [
            {"id": 1, "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
        ],
        "type": "api_response",
        "required_permission": "read:users"
    })

@app.route('/api/v1/reports')
def api_reports():
    """Reports API (requires read:reports permission)."""
    return jsonify({
        "reports": [
            {"id": 1, "title": "Monthly Analytics", "status": "ready"},
            {"id": 2, "title": "User Engagement", "status": "processing"}
        ],
        "type": "api_response",
        "required_permission": "read:reports"
    })

# === DEBUG/INFO ROUTES ===

@app.route('/protection-info')
def protection_info():
    """Show route protection configuration."""
    if not oauth.is_route_protection_enabled():
        return jsonify({"error": "Route protection not enabled"})
    
    info = oauth.get_route_protection_info()
    return jsonify(info)

@app.route('/check-route/<path:route_path>')
def check_route_access(route_path):
    """Check access to a specific route."""
    if not oauth.is_route_protection_enabled():
        return jsonify({"error": "Route protection not enabled"})
    
    # Synchronous route access check
    has_access = oauth.check_route_access(f"/{route_path}", "GET")
    
    return jsonify({
        "path": f"/{route_path}",
        "method": "GET",
        "has_access": has_access,
        "user_authenticated": oauth.is_authenticated()
    })

# === ERROR HANDLERS ===

@app.errorhandler(403)
def forbidden(error):
    """Handle 403 Forbidden errors."""
    return jsonify({
        "error": "Access Denied",
        "message": "You don't have permission to access this resource",
        "status": 403
    }), 403

@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors."""
    return jsonify({
        "error": "Not Found", 
        "message": "The requested resource was not found",
        "status": 404
    }), 404

if __name__ == '__main__':
    # Check if route protection is properly configured
    if not oauth.is_route_protection_enabled():
        print("⚠️  WARNING: Route protection is not enabled!")
        print("   Make sure 'route_protection_config.yaml' exists and is valid.")
        print("   Routes will not be protected!")
    else:
        info = oauth.get_route_protection_info()
        print(f"✅ Route protection enabled with {info['total_routes']} protected routes")
    
    print("\n🚀 Starting Flask Route Protection Example...")
    print("📝 Visit http://127.0.0.1:5000 to see the example")
    print("🔧 Configure your Kinde settings in environment variables")
    
    app.run(debug=True, port=5000)
