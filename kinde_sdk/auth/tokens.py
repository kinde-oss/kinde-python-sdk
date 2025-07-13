# kinde_sdk/auth/tokens.py
from typing import Optional
import jwt
import time

class Tokens:
    _access_token: Optional[str] = None
    _refresh_token: Optional[str] = None

    @classmethod
    def set_access_token(cls, token: str) -> None:
        cls._access_token = token

    @classmethod
    def get_access_token(cls) -> Optional[str]:
        return cls._access_token

    @classmethod
    def set_refresh_token(cls, token: str) -> None:
        cls._refresh_token = token

    @classmethod
    def get_refresh_token(cls) -> Optional[str]:
        return cls._refresh_token

    @classmethod
    def is_token_valid(cls, token: Optional[str]) -> bool:
        if not token:
            return False
        try:
            decoded = jwt.decode(token, options={"verify_signature": False})
            return decoded.get("exp", 0) > time.time()
        except jwt.InvalidTokenError:
            return False