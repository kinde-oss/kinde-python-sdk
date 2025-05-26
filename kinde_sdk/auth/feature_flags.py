from typing import Dict, Any, Optional, TypeVar, Generic, Union
import logging
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from kinde_sdk.auth.user_session import UserSession

T = TypeVar('T')

class FeatureFlag(Generic[T]):
    def __init__(self, code: str, type: str, value: T, is_default: bool = False):
        self.code = code
        self.type = type
        self.value = value
        self.is_default = is_default

class FeatureFlags:
    def __init__(self):
        self._logger = logging.getLogger("kinde_sdk")
        self._logger.setLevel(logging.INFO)
        self._framework = None
        self._session_manager = UserSession()

    def _get_framework(self):
        """Get the framework instance using singleton pattern."""
        if not self._framework:
            self._framework = FrameworkFactory.get_framework_instance()
        return self._framework

    def _get_token_manager(self) -> Optional[Any]:
        """
        Get the token manager for the current user.
        
        Returns:
            Optional[Any]: The token manager if available, None otherwise
        """
        framework = self._get_framework()
        if not framework:
            return None

        user_id = framework.get_user_id()
        if not user_id:
            return None

        return self._session_manager.get_token_manager(user_id)

    def _parse_flag_value(self, flag_data: Dict[str, Any], expected_type: Optional[str] = None) -> FeatureFlag:
        """
        Parse a feature flag value from the token format.
        
        Args:
            flag_data: The raw flag data from the token
            expected_type: Optional type to cast the value to
            
        Returns:
            FeatureFlag object with parsed value
        """
        flag_type = flag_data.get("t", "")
        raw_value = flag_data.get("v")
        
        # Map token type codes to Python types
        type_map = {
            "s": "string",
            "b": "boolean",
            "i": "integer"
        }
        
        # Convert value based on type
        if flag_type == "s":
            value = str(raw_value)
        elif flag_type == "b":
            value = bool(raw_value)
        elif flag_type == "i":
            value = int(raw_value)
        else:
            value = raw_value
            
        return FeatureFlag(
            code=flag_data.get("code", ""),
            type=type_map.get(flag_type, "unknown"),
            value=value,
            is_default=False
        )

    async def get_flag(self, flag_code: str, default_value: Optional[T] = None) -> FeatureFlag[T]:
        """
        Get a specific feature flag value.
        
        Args:
            flag_code: The code of the feature flag to retrieve
            default_value: Optional default value to use if flag is not found
            
        Returns:
            FeatureFlag object containing the flag value and metadata
        """
        token_manager = self._get_token_manager()
        if not token_manager:
            return FeatureFlag(
                code=flag_code,
                type="unknown",
                value=default_value,
                is_default=True
            )

        claims = token_manager.get_claims()
        feature_flags = claims.get("feature_flags", {})
        
        if flag_code not in feature_flags:
            return FeatureFlag(
                code=flag_code,
                type="unknown",
                value=default_value,
                is_default=True
            )
            
        return self._parse_flag_value(feature_flags[flag_code])

    async def get_all_flags(self) -> Dict[str, FeatureFlag]:
        """
        Get all feature flags for the current user.
        
        Returns:
            Dict mapping flag codes to FeatureFlag objects
        """
        token_manager = self._get_token_manager()
        if not token_manager:
            return {}

        claims = token_manager.get_claims()
        feature_flags = claims.get("feature_flags", {})
        
        return {
            code: self._parse_flag_value(flag_data)
            for code, flag_data in feature_flags.items()
        }

# Create a singleton instance
feature_flags = FeatureFlags() 