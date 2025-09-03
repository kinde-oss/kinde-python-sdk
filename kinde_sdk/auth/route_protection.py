"""
Route Protection Engine for Kinde Python SDK.

This module provides role-based and permission-based route protection using YAML configuration files.
It integrates seamlessly with the existing Kinde authentication infrastructure to provide fine-grained
access control for web applications.

Features:
- YAML/JSON configuration files for route protection rules
- Role-based and permission-based access control
- Pattern matching for route paths (supports wildcards)
- HTTP method-specific protection
- Public route designation
- Integration with Kinde Roles and Permissions APIs

Usage:
    # Initialize with a configuration file
    engine = RouteProtectionEngine("routes_config.yaml")
    
    # Check access for a specific route
    result = await engine.validate_route_access("/admin/users", "GET")
    if result["allowed"]:
        # User has access
        pass
    else:
        # Access denied: result["reason"] contains details
        pass

Configuration Format:
    settings:
      default_allow: false  # Default behavior when no rule matches
      
    routes:
      admin_panel:
        path: "/admin/*"
        methods: ["GET", "POST", "PUT", "DELETE"]
        roles: ["admin"]
        
      api_users:
        path: "/api/users"
        methods: ["GET"]
        permissions: ["read:users"]
        
      public_content:
        path: "/public/*"
        methods: ["GET"]
        public: true
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple

from .config_loader import load_config
from .roles import Roles
from .permissions import Permissions
from .api_options import ApiOptions

logger = logging.getLogger(__name__)


class RouteProtectionEngine:
    """
    Core engine for route protection based on role and permission rules.
    
    This engine loads route protection configuration from YAML/JSON files and provides
    methods to validate user access to specific routes based on their roles and permissions.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the route protection engine.
        
        Args:
            config_file: Optional path to the route protection configuration file (YAML/JSON).
                        If None, no route protection is enabled.
        """
        self.routes = {}
        self.global_settings = {}
        self._roles_client = None
        self._permissions_client = None
        self._logger = logging.getLogger("kinde_sdk.route_protection")
        
        if config_file:
            self.load_route_config(config_file)
    
    def load_route_config(self, config_file: str) -> None:
        """
        Load route protection configuration from a YAML or JSON file.
        
        Args:
            config_file: Path to the configuration file
            
        Raises:
            ValueError: If configuration file cannot be loaded or contains invalid rules
        """
        try:
            config = load_config(config_file)
            self._logger.info(f"Loading route protection config from: {config_file}")
            if not config:
                self._logger.warning("Route protection config file is empty: %s", config_file)
                config = {}
            
            # Load global settings
            self.global_settings = config.get("settings", {})
            
            # Load route rules
            routes_config = config.get("routes", {})
            self.routes = {}
            
            for route_name, route_config in routes_config.items():
                # Validate required fields
                if "path" not in route_config:
                    raise ValueError(f"Route '{route_name}' missing required 'path' field")
                
                # Set defaults
                route_config.setdefault("methods", ["GET"])
                
                # Validate that route has either roles, permissions, or is public
                has_roles = route_config.get("roles")
                has_permissions = route_config.get("permissions")
                is_public = route_config.get("public", False)
                
                if not (has_roles or has_permissions or is_public):
                    self._logger.warning(
                        f"Route '{route_name}' has no access controls (no roles, permissions, or public flag). "
                        f"This route will be protected by default behavior."
                    )
                
                self.routes[route_name] = route_config
                self._logger.debug(f"Loaded route rule: {route_name} -> {route_config}")
            
            self._logger.info(f"Loaded {len(self.routes)} route protection rules")
            
        except FileNotFoundError as e:
            self._logger.exception("Route protection config file not found: %s", config_file)
            raise ValueError(
                f"Failed to load route protection configuration: Configuration file not found: {config_file}"
            ) from e
        except Exception as e:
            # Parsing or validation error from load_config
            self._logger.exception("Failed to load route protection config")
            raise ValueError("Failed to load route protection configuration") from e
    
    async def validate_route_access(
        self, 
        path: str, 
        method: str = "GET", 
        options: Optional[ApiOptions] = None
    ) -> Dict[str, Any]:
        """
        Validate if the current user has access to the specified route.
        
        Args:
            path: The request path to validate (e.g., "/admin/users")
            method: The HTTP method (default: "GET")
            options: Optional API options for force_api mode
            
        Returns:
            Dictionary containing validation result:
            {
                "allowed": bool,           # Whether access is granted
                "reason": str,            # Human-readable reason
                "required_roles": List[str],      # Required roles (if applicable)
                "required_permissions": List[str], # Required permissions (if applicable)
                "matched_rule": str       # Name of the matched rule (if any)
            }
        """
        if not self.routes:
            # No routes configured - use default behavior
            default_allow = self.global_settings.get("default_allow", True)
            return {
                "allowed": default_allow,
                "reason": f"No route protection rules configured, using default: {'allow' if default_allow else 'deny'}",
                "required_roles": [],
                "required_permissions": [],
                "matched_rule": None
            }
        
        # Find matching route rule
        matched_rule, rule_config = self._find_matching_route(path, method)
        
        if not matched_rule:
            # No matching rule found - use default behavior
            default_allow = self.global_settings.get("default_allow", True)
            return {
                "allowed": default_allow,
                "reason": f"No matching route rule found, using default: {'allow' if default_allow else 'deny'}",
                "required_roles": [],
                "required_permissions": [],
                "matched_rule": None
            }
        
        # Check if route is public (no authentication required)
        if rule_config.get("public", False):
            return {
                "allowed": True,
                "reason": "Public route",
                "required_roles": [],
                "required_permissions": [],
                "matched_rule": matched_rule
            }
        
        # Extract required roles and permissions
        required_roles = rule_config.get("roles", [])
        required_permissions = rule_config.get("permissions", [])
        
        # If no specific requirements, deny access for security
        if not required_roles and not required_permissions:
            return {
                "allowed": False,
                "reason": "Route requires authentication but no specific roles or permissions defined",
                "required_roles": [],
                "required_permissions": [],
                "matched_rule": matched_rule
            }
        
        # Check roles if specified
        if required_roles:
            role_check = await self._check_roles(required_roles, options)
            if not role_check["allowed"]:
                return {
                    "allowed": False,
                    "reason": role_check["reason"],
                    "required_roles": required_roles,
                    "required_permissions": required_permissions,
                    "matched_rule": matched_rule
                }
        
        # Check permissions if specified
        if required_permissions:
            permission_check = await self._check_permissions(required_permissions, options)
            if not permission_check["allowed"]:
                return {
                    "allowed": False,
                    "reason": permission_check["reason"],
                    "required_roles": required_roles,
                    "required_permissions": required_permissions,
                    "matched_rule": matched_rule
                }
        
        # All checks passed
        return {
            "allowed": True,
            "reason": "Access granted",
            "required_roles": required_roles,
            "required_permissions": required_permissions,
            "matched_rule": matched_rule
        }
    
    def _find_matching_route(self, path: str, method: str) -> Tuple[Optional[str], Dict[str, Any]]:
        """
        Find the first route rule that matches the given path and method.
        
        Args:
            path: Request path
            method: HTTP method
            
        Returns:
            Tuple of (rule_name, rule_config) or (None, {}) if no match
        """
        for rule_name, rule_config in self.routes.items():
            # Check if method matches
            allowed_methods = rule_config.get("methods", ["GET"])
            if method.upper() not in [m.upper() for m in allowed_methods]:
                continue
            
            # Check if path matches
            route_pattern = rule_config["path"]
            if self._path_matches(path, route_pattern):
                self._logger.debug(f"Route '{path}' {method} matches rule '{rule_name}' with pattern '{route_pattern}'")
                return rule_name, rule_config
        
        self._logger.debug(f"No route rule matches '{path}' {method}")
        return None, {}
    
    def _path_matches(self, request_path: str, route_pattern: str) -> bool:
        """
        Check if a request path matches a route pattern.
        
        Supports wildcards:
        - "/admin/*" matches "/admin/users", "/admin/settings/view", etc.
        - "/api/users" matches exactly "/api/users"
        
        Args:
            request_path: The actual request path
            route_pattern: The pattern from configuration (may contain wildcards)
            
        Returns:
            True if path matches the pattern
        """
        # Normalize paths (remove trailing slashes) but preserve root '/'
        if request_path != '/':
            request_path = request_path.rstrip('/')
        if route_pattern != '/':
            route_pattern = route_pattern.rstrip('/')
        
        # Handle exact matches
        if route_pattern == request_path:
            return True
        
        # Handle wildcard patterns
        if route_pattern.endswith('/*'):
            pattern_prefix = route_pattern[:-2]  # Remove /*
            # Ensure we're matching a path segment boundary
            return request_path == pattern_prefix or request_path.startswith(pattern_prefix + '/')
        
        # Handle regex patterns if route_pattern starts and ends with /
        if route_pattern.startswith('/') and route_pattern.count('/') > 1:
            try:
                # Convert route pattern to regex
                # Replace * with [^/]* (match any character except /)
                regex_pattern = route_pattern.replace('*', '[^/]*')
                return bool(re.match(f"^{regex_pattern}$", request_path))
            except re.error:
                self._logger.warning(f"Invalid regex pattern in route: {route_pattern}")
                return False
        
        return False
    
    async def _check_roles(self, required_roles: List[str], options: Optional[ApiOptions] = None) -> Dict[str, Any]:
        """
        Check if the current user has any of the required roles.
        
        Args:
            required_roles: List of role keys that would grant access
            options: Optional API options
            
        Returns:
            Dict with "allowed" bool and "reason" string
        """
        if not self._roles_client:
            self._roles_client = Roles()
        
        try:
            # Check each required role
            for role_key in required_roles:
                role_result = await self._roles_client.get_role(role_key, options)
                if role_result and role_result.get("isGranted", False):
                    return {
                        "allowed": True,
                        "reason": f"User has required role: {role_key}"
                    }
            
            return {
                "allowed": False,
                "reason": f"Missing required roles: {required_roles}"
            }
            
        except Exception as e:
            self._logger.exception("Error checking roles")
            return {
                "allowed": False,
                "reason": f"Error checking roles: {e!s}"
            }
    
    async def _check_permissions(self, required_permissions: List[str], options: Optional[ApiOptions] = None) -> Dict[str, Any]:
        """
        Check if the current user has any of the required permissions.
        
        Args:
            required_permissions: List of permission keys that would grant access
            options: Optional API options
            
        Returns:
            Dict with "allowed" bool and "reason" string
        """
        if not self._permissions_client:
            self._permissions_client = Permissions()
        
        try:
            # Check each required permission
            for permission_key in required_permissions:
                permission_result = await self._permissions_client.get_permission(permission_key, options)
                if permission_result and permission_result.get("isGranted", False):
                    return {
                        "allowed": True,
                        "reason": f"User has required permission: {permission_key}"
                    }
            
            return {
                "allowed": False,
                "reason": f"Missing required permissions: {required_permissions}"
            }
            
        except Exception as e:
            self._logger.exception("Error checking permissions")
            return {
                "allowed": False,
                "reason": f"Error checking permissions: {e!s}"
            }
    
    def get_route_info(self, path: str, method: str = "GET") -> Optional[Dict[str, Any]]:
        """
        Get information about protection rules for a specific route.
        
        Args:
            path: Request path
            method: HTTP method
            
        Returns:
            Dict containing route protection info or None if no matching rule
        """
        matched_rule, rule_config = self._find_matching_route(path, method)
        
        if not matched_rule:
            return None
        
        return {
            "rule_name": matched_rule,
            "path_pattern": rule_config["path"],
            "methods": rule_config.get("methods", ["GET"]),
            "required_roles": rule_config.get("roles", []),
            "required_permissions": rule_config.get("permissions", []),
            "is_public": rule_config.get("public", False)
        }
    
    def list_protected_routes(self) -> Dict[str, Any]:
        """
        Get a summary of all configured route protection rules.
        
        Returns:
            Dict containing route protection summary
        """
        return {
            "total_routes": len(self.routes),
            "global_settings": self.global_settings,
            "routes": [
                {
                    "name": rule_name,
                    "path": rule_config["path"],
                    "methods": rule_config.get("methods", ["GET"]),
                    "roles": rule_config.get("roles", []),
                    "permissions": rule_config.get("permissions", []),
                    "public": rule_config.get("public", False)
                }
                for rule_name, rule_config in self.routes.items()
            ]
        }


# Singleton instance for global usage
route_protection = RouteProtectionEngine()
