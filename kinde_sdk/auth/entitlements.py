from typing import Optional, List
from kinde_sdk.frontend.models.get_entitlement_response import GetEntitlementResponse
from kinde_sdk.frontend.models.get_entitlements_response_data_entitlements_inner import GetEntitlementsResponseDataEntitlementsInner
from kinde_sdk.frontend.api.billing_api import BillingApi
from kinde_sdk.frontend.configuration import Configuration
from kinde_sdk.frontend.api_client import ApiClient

class Entitlements:
    """Client for Kinde Account API entitlements endpoints."""

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip('/')
        self.token = token
        
        # Configure the API client
        configuration = Configuration(
            host=self.base_url,
            access_token=self.token
        )
        
        # Create the API client
        api_client = ApiClient(configuration)
        
        # Create the billing API client
        self.billing_api = BillingApi(api_client)

    def get_all_entitlements(self) -> List[GetEntitlementsResponseDataEntitlementsInner]:
        """
        Returns all entitlements by automatically paging through all available pages.
        
        Returns:
            List of all entitlements across all pages.
        """
        all_entitlements: List[GetEntitlementsResponseDataEntitlementsInner] = []
        starting_after = None
        prev_cursor = object()  # sentinel
        has_more = True
        
        while has_more:
            # Use the generated API client
            result = self.billing_api.get_entitlements(
                page_size=None,  # Use default page size
                starting_after=starting_after
            )
            
            # Add entitlements from current page to our list
            if result.data and result.data.entitlements:
                all_entitlements.extend(result.data.entitlements)
            
            # Check if there are more pages
            if result.metadata:
                # Handle both boolean and string values for has_more
                has_more_value = result.metadata.has_more
                if isinstance(has_more_value, str):
                    has_more = has_more_value.lower() == 'true'
                else:
                    has_more = bool(has_more_value)
                next_cursor = result.metadata.next_page_starting_after
                # break if cursor didn't advance to avoid infinite loop
                if has_more and (next_cursor is None or next_cursor == starting_after):
                    has_more = False
                prev_cursor, starting_after = starting_after, next_cursor
            else:
                has_more = False
        
        return all_entitlements

    def get_entitlement(self, key: str) -> GetEntitlementResponse:
        """
        Returns a single entitlement by the feature key.
        """
        # Use the generated API client
        return self.billing_api.get_entitlement(key=key)
