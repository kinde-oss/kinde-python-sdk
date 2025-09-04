from .oauth import OAuth
from .token_manager import TokenManager
from .user_session import UserSession
from .api_options import ApiOptions
from .permissions import permissions
from .claims import claims
from .feature_flags import feature_flags
from .portals import portals
from .tokens import tokens
from .roles import roles

# Route Protection Components (optional imports with graceful fallback)
try:
    from .route_protection import RouteProtectionEngine, route_protection
    from .route_middleware import (
        RouteProtectionMiddleware,
        FlaskRouteProtectionMiddleware,
        FastAPIRouteProtectionMiddleware,
        create_route_protection_middleware
    )
    ROUTE_PROTECTION_AVAILABLE = True
    _route_protection_components = [
        "RouteProtectionEngine", "route_protection",
        "RouteProtectionMiddleware", "create_route_protection_middleware"
    ]
    # Add framework-specific middleware if available
    if FlaskRouteProtectionMiddleware:
        _route_protection_components.append("FlaskRouteProtectionMiddleware")
    if FastAPIRouteProtectionMiddleware:
        _route_protection_components.append("FastAPIRouteProtectionMiddleware")
        
except ImportError:
    ROUTE_PROTECTION_AVAILABLE = False
    _route_protection_components = []

__all__ = [
    "OAuth", "TokenManager", "UserSession", "permissions", "ApiOptions", 
    "claims", "feature_flags", "portals", "tokens", "roles"
] + _route_protection_components
