import requests
from typing import Optional
from kinde_sdk.management.models.get_entitlements_response import GetEntitlementsResponse

class Entitlements:
    """Client for Kinde Account API entitlements endpoints."""

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }

    def get_entitlements(self, page_size: Optional[int] = None, starting_after: Optional[str] = None) -> GetEntitlementsResponse:
        """
        Returns all the entitlements the user currently has access to.
        """
        params = {}
        if page_size is not None:
            params['page_size'] = page_size
        if starting_after is not None:
            params['starting_after'] = starting_after
        url = f"{self.base_url}/account_api/v1/entitlements"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return GetEntitlementsResponse.model_validate(response.json())

    def get_entitlement(self, key: str) -> GetEntitlementsResponse:
        """
        Returns a single entitlement by the feature key.
        """
        url = f"{self.base_url}/account_api/v1/entitlement/{key}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return GetEntitlementsResponse.model_validate(response.json())
