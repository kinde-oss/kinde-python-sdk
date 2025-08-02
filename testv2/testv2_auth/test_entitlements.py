import pytest
from unittest.mock import patch, Mock
from kinde_sdk.auth.entitlements import Entitlements
from kinde_sdk.model.get_entitlements_response import GetEntitlementsResponse
from kinde_sdk.model.get_entitlement_response import GetEntitlementResponse

class TestEntitlements:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.entitlements = Entitlements(base_url="https://api.example.com", token="test_token")

    @patch("kinde_sdk.auth.entitlements.requests.get")
    def test_get_entitlements_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "org_code": "test_org",
                "entitlements": [],
                "plans": []
            },
            "metadata": {
                "has_more": False
            }
        }
        mock_get.return_value = mock_response
        result = self.entitlements.get_entitlements(page_size=10, starting_after="abc")
        assert isinstance(result, GetEntitlementsResponse)

    @patch("kinde_sdk.auth.entitlements.requests.get")
    def test_get_entitlements_no_params(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "org_code": "test_org",
                "entitlements": [],
                "plans": []
            },
            "metadata": {
                "has_more": False
            }
        }
        mock_get.return_value = mock_response
        result = self.entitlements.get_entitlements()
        assert isinstance(result, GetEntitlementsResponse)

    @patch("kinde_sdk.auth.entitlements.requests.get")
    def test_get_entitlement_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "org_code": "test_org",
                "entitlement": {
                    "id": "entl_123",
                    "price_name": "Pro",
                    "feature_key": "feature-123",
                    "feature_name": "Test Feature"
                }
            },
            "metadata": {}
        }
        mock_get.return_value = mock_response
        result = self.entitlements.get_entitlement("feature-123")
        assert isinstance(result, GetEntitlementResponse)

    @patch("kinde_sdk.auth.entitlements.requests.get")
    def test_get_entitlements_http_error(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("HTTP error")
        mock_get.return_value = mock_response
        with pytest.raises(Exception, match="HTTP error"):
            self.entitlements.get_entitlements()

    @patch("kinde_sdk.auth.entitlements.requests.get")
    def test_get_entitlement_http_error(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("HTTP error")
        mock_get.return_value = mock_response
        with pytest.raises(Exception, match="HTTP error"):
            self.entitlements.get_entitlement("feature-123")

    @patch("kinde_sdk.auth.entitlements.requests.get")
    def test_get_entitlement_model_validation_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "org_code": "test_org",
                "entitlement": {
                    "id": "entl_123",
                    "price_name": "Pro",
                    "feature_key": "feature-123",
                    "feature_name": "Test Feature"
                }
            },
            "metadata": {}
        }
        mock_get.return_value = mock_response
        with patch("kinde_sdk.model.get_entitlement_response.GetEntitlementResponse.model_validate") as mock_validate:
            mock_validate.side_effect = ValueError("validation error")
            with pytest.raises(ValueError, match="validation error"):
                self.entitlements.get_entitlement("feature-123")

    @patch("kinde_sdk.auth.entitlements.requests.get")
    def test_get_entitlements_model_validation_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "org_code": "test_org",
                "entitlements": [
                    {
                        "id": "entl_123",
                        "price_name": "Pro",
                        "feature_key": "feature-123",
                        "feature_name": "Test Feature"
                    }
                ],
                "plans": []
            },
            "metadata": {
                "has_more": False
            }
        }
        mock_get.return_value = mock_response
        with patch("kinde_sdk.model.get_entitlements_response.GetEntitlementsResponse.model_validate") as mock_validate:
            mock_validate.side_effect = ValueError("validation error")
            with pytest.raises(ValueError, match="validation error"):
                self.entitlements.get_entitlements()