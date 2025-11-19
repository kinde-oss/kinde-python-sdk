from typing import Dict, Any, Optional, TypeVar, Generic

from kinde_sdk.auth.api_options import ApiOptions
from kinde_sdk.frontend.api.feature_flags_api import FeatureFlagsApi
from .base_auth import BaseAuth

T = TypeVar('T')

class FeatureFlag(Generic[T]):
    def __init__(self, code: str, type: str, value: T, is_default: bool = False):
        self.code = code
        self.type = type
        self.value = value
        self.is_default = is_default

class FeatureFlags(BaseAuth):
    def _parse_flag_value(
            self, 
            flag_data: Dict[str, Any], 
            expected_type: Optional[str] = None
            ) -> FeatureFlag:
        """
        Parse a feature flag value from the token format.
        
        Args:
            flag_data: The raw flag data from the token
            expected_type: Optional type to cast the value to
            
        Returns:
            FeatureFlag object with parsed value
        """
        if not isinstance(flag_data, dict):
            raise ValueError("flag_data must be a dictionary")

        # Extract raw type and value
        flag_type = flag_data.get("t", "")
        raw_value = flag_data.get("v")
        
        # Map token type codes to Python types
        type_map = {
            "s": "string",
            "b": "boolean",
            "i": "integer"
        }
        
        # Convert value based on type
        try:
            if flag_type == "s":
                # None → empty string
                value = str(raw_value) if raw_value is not None else ""
            elif flag_type == "b":
                value = bool(raw_value)
            elif flag_type == "i":
                # None → zero
                value = int(raw_value) if raw_value is not None else 0
            else:
                # Unknown type code: return raw as-is
                value = raw_value
        except (TypeError, ValueError) as e:
            raise ValueError(
                f"Cannot convert flag value {raw_value!r} to type {flag_type!r}: {e}"
            )
            
        return FeatureFlag(
            code=flag_data.get("code", ""),
            type=type_map.get(flag_type, "unknown"),
            value=value,
            is_default=False
        )

    async def get_flag(
            self, 
            flag_code: str, 
            default_value: Optional[T] = None,
            options: Optional[ApiOptions] = None
            ) -> FeatureFlag[T]:
        """
        Get a specific feature flag value.
        
        Args:
            flag_code: The code of the feature flag to retrieve
            default_value: Optional default value to use if flag is not found
            
        Returns:
            FeatureFlag object containing the flag value and metadata
        """
        
        # Check SDK-level force_api setting first, then fall back to options parameter
        force_api = self._get_force_api_setting()
        if options and options.force_api:
            force_api = True
        
        if force_api:
            result = await self._call_account_api(flag_code)
            if not isinstance(result, dict):
                return FeatureFlag(
                    code=flag_code,
                    type="unknown",
                    value=default_value,
                    is_default=False
                )
            # If shape is unexpected (no 't' and no 'v'), treat as missing
            if "t" not in result and "v" not in result:
                return FeatureFlag(
                    code=flag_code,
                    type="unknown",
                    value=default_value,
                    is_default=False
                )
            if "code" not in result:
                result = {**result, "code": flag_code}
            return self._parse_flag_value(result)

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
            
        return self._parse_flag_value({**feature_flags[flag_code], "code": flag_code})

    async def get_all_flags(
            self,
            options: Optional[ApiOptions] = None
            ) -> Dict[str, FeatureFlag]:
        """
        Get all feature flags for the current user.
        
        Args:
            options: Optional ApiOptions object (deprecated, use SDK-level force_api setting)
        
        Returns:
            Dict mapping flag codes to FeatureFlag objects
        """

        # Check SDK-level force_api setting first, then fall back to options parameter
        force_api = self._get_force_api_setting()
        if options and options.force_api:
            force_api = True

        if force_api:
            flags = await self._call_account_api()
            if not isinstance(flags, dict):
                return {}
            return {
                code: self._parse_flag_value({**(data or {}), "code": code})
                for code, data in flags.items()
            }
    
        token_manager = self._get_token_manager()
        if not token_manager:
            return {}

        claims = token_manager.get_claims()
        feature_flags = claims.get("feature_flags", {})
        
        return {
            code: self._parse_flag_value(flag_data)
            for code, flag_data in feature_flags.items()
        }
    
    async def _call_account_api(self, flag_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Calls the Kinde Account API to get feature flags.
        If flag_code is provided, returns only that flag's data.
        Otherwise, returns all flags as a dict.
        """
        try:
            # Create authenticated API client using shared method
            feature_flags_api = self._create_authenticated_api_client(FeatureFlagsApi)
            if not feature_flags_api:
                return {}
            
            response = feature_flags_api.get_feature_flags()
        except Exception as e:
            # Log error and return empty result
            if hasattr(self, '_logger'):
                self._logger.error(f"Failed to fetch feature flags from API: {str(e)}")
            return {}
        
        flags = {}
        if response and response.data and hasattr(response.data, "flags"):
            flags = response.data.flags or {}
        
        if flag_code is not None:
            return flags.get(flag_code, {})
        return flags

# Create a singleton instance
feature_flags = FeatureFlags() 