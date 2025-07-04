from typing import Dict, Any, Optional, TypeVar, Generic
from .base_auth import BaseAuth

T = TypeVar('T')

class FeatureFlag(Generic[T]):
    def __init__(self, code: str, type: str, value: T, is_default: bool = False):
        self.code = code
        self.type = type
        self.value = value
        self.is_default = is_default

class FeatureFlags(BaseAuth):
    def _parse_flag_value(self, flag_data: Dict[str, Any], expected_type: Optional[str] = None) -> FeatureFlag:
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