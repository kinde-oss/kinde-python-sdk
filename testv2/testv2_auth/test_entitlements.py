import pytest
from unittest.mock import Mock, patch, MagicMock
from kinde_sdk.auth.entitlements import Entitlements
from kinde_sdk.frontend.models.get_entitlement_response import GetEntitlementResponse
from kinde_sdk.frontend.models.get_entitlements_response import GetEntitlementsResponse
from kinde_sdk.frontend.models.get_entitlements_response_data import GetEntitlementsResponseData
from kinde_sdk.frontend.models.get_entitlements_response_data_entitlements_inner import GetEntitlementsResponseDataEntitlementsInner
from kinde_sdk.frontend.models.get_entitlements_response_metadata import GetEntitlementsResponseMetadata
from kinde_sdk.frontend.models.get_entitlement_response_data import GetEntitlementResponseData
from kinde_sdk.frontend.models.get_entitlement_response_data_entitlement import GetEntitlementResponseDataEntitlement

@pytest.fixture
def mock_billing_api():
    """Mock BillingApi for testing."""
    return Mock()

@pytest.fixture
def mock_configuration():
    """Mock Configuration for testing."""
    return Mock()

@pytest.fixture
def sample_entitlement():
    """Sample entitlement data for testing."""
    return GetEntitlementsResponseDataEntitlementsInner(
        id="entitlement_123",
        feature_key="pro_feature",
        feature_name="Pro Feature",
        price_name="Pro Plan",
        unit_amount=1000,
        fixed_charge=10,
        entitlement_limit_max=100,
        entitlement_limit_min=1
    )

@pytest.fixture
def sample_entitlement_response_data(sample_entitlement):
    """Sample entitlements response data for testing."""
    return GetEntitlementsResponseData(
        org_code="org_123",
        plans=[],
        entitlements=[sample_entitlement]
    )

@pytest.fixture
def sample_entitlements_response(sample_entitlement_response_data):
    """Sample entitlements response for testing."""
    return GetEntitlementsResponse(
        data=sample_entitlement_response_data,
        metadata=GetEntitlementsResponseMetadata(
            has_more=False,
            next_page_starting_after=None
        )
    )

@pytest.fixture
def sample_single_entitlement():
    """Sample single entitlement for get_entitlement testing."""
    return GetEntitlementResponseDataEntitlement(
        id="entitlement_456",
        feature_key="premium_feature",
        feature_name="Premium Feature",
        price_name="Premium Plan",
        unit_amount=2000,
        fixed_charge=20,
        entitlement_limit_max=200,
        entitlement_limit_min=5
    )

@pytest.fixture
def sample_single_entitlement_response_data(sample_single_entitlement):
    """Sample single entitlement response data for testing."""
    return GetEntitlementResponseData(
        org_code="org_123",
        entitlement=sample_single_entitlement
    )

@pytest.fixture
def sample_single_entitlement_response(sample_single_entitlement_response_data):
    """Sample single entitlement response for testing."""
    return GetEntitlementResponse(
        data=sample_single_entitlement_response_data
    )

class TestEntitlements:
    """Test cases for the Entitlements class."""

    def test_init_with_trailing_slash(self):
        """Test initialization with trailing slash in base_url."""
        with patch('kinde_sdk.auth.entitlements.Configuration') as mock_config_class, \
             patch('kinde_sdk.auth.entitlements.ApiClient') as mock_api_client_class, \
             patch('kinde_sdk.auth.entitlements.BillingApi') as mock_billing_class:
            
            mock_config = Mock()
            mock_config_class.return_value = mock_config
            mock_api_client = Mock()
            mock_api_client_class.return_value = mock_api_client
            mock_billing = Mock()
            mock_billing_class.return_value = mock_billing
            
            entitlements = Entitlements("https://test.kinde.com/", "test_token")
            
            # Check that trailing slash was removed
            assert entitlements.base_url == "https://test.kinde.com"
            assert entitlements.token == "test_token"
            
            # Check that Configuration was called correctly
            mock_config_class.assert_called_once_with(
                host="https://test.kinde.com",
                access_token="test_token"
            )
            
            # Check that ApiClient was created
            mock_api_client_class.assert_called_once_with(mock_config)
            
            # Check that BillingApi was created
            mock_billing_class.assert_called_once_with(mock_api_client)

    def test_init_without_trailing_slash(self):
        """Test initialization without trailing slash in base_url."""
        with patch('kinde_sdk.auth.entitlements.Configuration') as mock_config_class, \
             patch('kinde_sdk.auth.entitlements.ApiClient') as mock_api_client_class, \
             patch('kinde_sdk.auth.entitlements.BillingApi') as mock_billing_class:
            
            mock_config = Mock()
            mock_config_class.return_value = mock_config
            mock_api_client = Mock()
            mock_api_client_class.return_value = mock_api_client
            mock_billing = Mock()
            mock_billing_class.return_value = mock_billing
            
            entitlements = Entitlements("https://test.kinde.com", "test_token")
            
            # Check that base_url is unchanged
            assert entitlements.base_url == "https://test.kinde.com"
            assert entitlements.token == "test_token"

    def test_get_all_entitlements_single_page(self, sample_entitlements_response):
        """Test get_all_entitlements with single page of results."""
        with patch('kinde_sdk.auth.entitlements.Configuration') as mock_config_class, \
             patch('kinde_sdk.auth.entitlements.ApiClient') as mock_api_client_class, \
             patch('kinde_sdk.auth.entitlements.BillingApi') as mock_billing_class:
            
            mock_config = Mock()
            mock_config_class.return_value = mock_config
            mock_api_client = Mock()
            mock_api_client_class.return_value = mock_api_client
            mock_billing = Mock()
            mock_billing.get_entitlements.return_value = sample_entitlements_response
            mock_billing_class.return_value = mock_billing
            
            entitlements = Entitlements("https://test.kinde.com", "test_token")
            result = entitlements.get_all_entitlements()
            
            # Verify the API was called correctly
            mock_billing.get_entitlements.assert_called_once_with(
                page_size=None,
                starting_after=None
            )
            
            # Verify the result
            assert len(result) == 1
            assert result[0].id == "entitlement_123"
            assert result[0].feature_key == "pro_feature"

    def test_get_all_entitlements_multiple_pages(self, sample_entitlement):
        """Test get_all_entitlements with multiple pages of results."""
        with patch('kinde_sdk.auth.entitlements.Configuration') as mock_config_class, \
             patch('kinde_sdk.auth.entitlements.ApiClient') as mock_api_client_class, \
             patch('kinde_sdk.auth.entitlements.BillingApi') as mock_billing_class:
            
            mock_config = Mock()
            mock_config_class.return_value = mock_config
            mock_api_client = Mock()
            mock_api_client_class.return_value = mock_api_client
            mock_billing = Mock()
            
            # First page response
            first_page_data = GetEntitlementsResponseData(
                org_code="org_123",
                plans=[],
                entitlements=[sample_entitlement]
            )
            first_page_response = GetEntitlementsResponse(
                data=first_page_data,
                metadata=GetEntitlementsResponseMetadata(
                    has_more=True,
                    next_page_starting_after="entitlement_123"
                )
            )
            
            # Second page response
            second_entitlement = GetEntitlementsResponseDataEntitlementsInner(
                id="entitlement_456",
                feature_key="another_feature",
                feature_name="Another Feature",
                price_name="Another Plan",
                unit_amount=500,
                fixed_charge=5,
                entitlement_limit_max=50,
                entitlement_limit_min=1
            )
            second_page_data = GetEntitlementsResponseData(
                org_code="org_123",
                plans=[],
                entitlements=[second_entitlement]
            )
            second_page_response = GetEntitlementsResponse(
                data=second_page_data,
                metadata=GetEntitlementsResponseMetadata(
                    has_more=False,
                    next_page_starting_after=None
                )
            )
            
            # Configure mock to return different responses
            mock_billing.get_entitlements.side_effect = [first_page_response, second_page_response]
            mock_billing_class.return_value = mock_billing
            
            entitlements = Entitlements("https://test.kinde.com", "test_token")
            result = entitlements.get_all_entitlements()
            
            # Verify the API was called twice with correct parameters
            assert mock_billing.get_entitlements.call_count == 2
            mock_billing.get_entitlements.assert_any_call(
                page_size=None,
                starting_after=None
            )
            mock_billing.get_entitlements.assert_any_call(
                page_size=None,
                starting_after="entitlement_123"
            )
            
            # Verify the result contains both entitlements
            assert len(result) == 2
            assert result[0].id == "entitlement_123"
            assert result[1].id == "entitlement_456"

    def test_get_all_entitlements_empty_response(self):
        """Test get_all_entitlements with empty response."""
        with patch('kinde_sdk.auth.entitlements.Configuration') as mock_config_class, \
             patch('kinde_sdk.auth.entitlements.ApiClient') as mock_api_client_class, \
             patch('kinde_sdk.auth.entitlements.BillingApi') as mock_billing_class:
            
            mock_config = Mock()
            mock_config_class.return_value = mock_config
            mock_api_client = Mock()
            mock_api_client_class.return_value = mock_api_client
            mock_billing = Mock()
            
            # Empty response
            empty_data = GetEntitlementsResponseData(
                org_code="org_123",
                plans=[],
                entitlements=[]
            )
            empty_response = GetEntitlementsResponse(
                data=empty_data,
                metadata=GetEntitlementsResponseMetadata(
                    has_more=False,
                    next_page_starting_after=None
                )
            )
            
            mock_billing.get_entitlements.return_value = empty_response
            mock_billing_class.return_value = mock_billing
            
            entitlements = Entitlements("https://test.kinde.com", "test_token")
            result = entitlements.get_all_entitlements()
            
            # Verify the result is empty
            assert len(result) == 0

    def test_get_all_entitlements_no_metadata(self):
        """Test get_all_entitlements when response has no metadata."""
        with patch('kinde_sdk.auth.entitlements.Configuration') as mock_config_class, \
             patch('kinde_sdk.auth.entitlements.ApiClient') as mock_api_client_class, \
             patch('kinde_sdk.auth.entitlements.BillingApi') as mock_billing_class:
            
            mock_config = Mock()
            mock_config_class.return_value = mock_config
            mock_api_client = Mock()
            mock_api_client_class.return_value = mock_api_client
            mock_billing = Mock()
            
            # Response without metadata
            data = GetEntitlementsResponseData(
                org_code="org_123",
                plans=[],
                entitlements=[]
            )
            response = GetEntitlementsResponse(
                data=data,
                metadata=None
            )
            
            mock_billing.get_entitlements.return_value = response
            mock_billing_class.return_value = mock_billing
            
            entitlements = Entitlements("https://test.kinde.com", "test_token")
            result = entitlements.get_all_entitlements()
            
            # Verify the API was called only once
            mock_billing.get_entitlements.assert_called_once()
            assert len(result) == 0

    def test_get_all_entitlements_no_data(self):
        """Test get_all_entitlements when response has no data."""
        with patch('kinde_sdk.auth.entitlements.Configuration') as mock_config_class, \
             patch('kinde_sdk.auth.entitlements.ApiClient') as mock_api_client_class, \
             patch('kinde_sdk.auth.entitlements.BillingApi') as mock_billing_class:
            
            mock_config = Mock()
            mock_config_class.return_value = mock_config
            mock_api_client = Mock()
            mock_api_client_class.return_value = mock_api_client
            mock_billing = Mock()
            
            # Response without data
            response = GetEntitlementsResponse(
                data=None,
                metadata=GetEntitlementsResponseMetadata(
                    has_more=False,
                    next_page_starting_after=None
                )
            )
            
            mock_billing.get_entitlements.return_value = response
            mock_billing_class.return_value = mock_billing
            
            entitlements = Entitlements("https://test.kinde.com", "test_token")
            result = entitlements.get_all_entitlements()
            
            # Verify the result is empty
            assert len(result) == 0

    def test_get_entitlement_success(self, sample_single_entitlement_response):
        """Test get_entitlement with successful response."""
        with patch('kinde_sdk.auth.entitlements.Configuration') as mock_config_class, \
             patch('kinde_sdk.auth.entitlements.ApiClient') as mock_api_client_class, \
             patch('kinde_sdk.auth.entitlements.BillingApi') as mock_billing_class:
            
            mock_config = Mock()
            mock_config_class.return_value = mock_config
            mock_api_client = Mock()
            mock_api_client_class.return_value = mock_api_client
            mock_billing = Mock()
            mock_billing.get_entitlement.return_value = sample_single_entitlement_response
            mock_billing_class.return_value = mock_billing
            
            entitlements = Entitlements("https://test.kinde.com", "test_token")
            result = entitlements.get_entitlement("premium_feature")
            
            # Verify the API was called correctly
            mock_billing.get_entitlement.assert_called_once_with(key="premium_feature")
            
            # Verify the result
            assert result == sample_single_entitlement_response
            assert result.data.entitlement.id == "entitlement_456"
            assert result.data.entitlement.feature_key == "premium_feature"

    def test_get_entitlement_with_empty_key(self):
        """Test get_entitlement with empty key."""
        with patch('kinde_sdk.auth.entitlements.Configuration') as mock_config_class, \
             patch('kinde_sdk.auth.entitlements.ApiClient') as mock_api_client_class, \
             patch('kinde_sdk.auth.entitlements.BillingApi') as mock_billing_class:
            
            mock_config = Mock()
            mock_config_class.return_value = mock_config
            mock_api_client = Mock()
            mock_api_client_class.return_value = mock_api_client
            mock_billing = Mock()
            mock_billing_class.return_value = mock_billing
            
            entitlements = Entitlements("https://test.kinde.com", "test_token")
            
            # This should still work as the API client handles validation
            entitlements.get_entitlement("")
            
            # Verify the API was called with empty key
            mock_billing.get_entitlement.assert_called_once_with(key="")

    def test_get_entitlement_with_special_characters(self):
        """Test get_entitlement with special characters in key."""
        with patch('kinde_sdk.auth.entitlements.Configuration') as mock_config_class, \
             patch('kinde_sdk.auth.entitlements.ApiClient') as mock_api_client_class, \
             patch('kinde_sdk.auth.entitlements.BillingApi') as mock_billing_class:
            
            mock_config = Mock()
            mock_config_class.return_value = mock_config
            mock_api_client = Mock()
            mock_api_client_class.return_value = mock_api_client
            mock_billing = Mock()
            mock_billing_class.return_value = mock_billing
            
            entitlements = Entitlements("https://test.kinde.com", "test_token")
            
            # Test with special characters
            special_key = "feature-with-dashes_and_underscores"
            entitlements.get_entitlement(special_key)
            
            # Verify the API was called with the special key
            mock_billing.get_entitlement.assert_called_once_with(key=special_key)

    def test_api_error_handling(self):
        """Test that API errors are properly propagated."""
        with patch('kinde_sdk.auth.entitlements.Configuration') as mock_config_class, \
             patch('kinde_sdk.auth.entitlements.ApiClient') as mock_api_client_class, \
             patch('kinde_sdk.auth.entitlements.BillingApi') as mock_billing_class:
            
            mock_config = Mock()
            mock_config_class.return_value = mock_config
            mock_api_client = Mock()
            mock_api_client_class.return_value = mock_api_client
            mock_billing = Mock()
            mock_billing.get_entitlements.side_effect = Exception("API Error")
            mock_billing_class.return_value = mock_billing
            
            entitlements = Entitlements("https://test.kinde.com", "test_token")
            
            # Verify that the exception is propagated
            with pytest.raises(Exception, match="API Error"):
                entitlements.get_all_entitlements()

    def test_get_entitlement_api_error_handling(self):
        """Test that API errors in get_entitlement are properly propagated."""
        with patch('kinde_sdk.auth.entitlements.Configuration') as mock_config_class, \
             patch('kinde_sdk.auth.entitlements.ApiClient') as mock_api_client_class, \
             patch('kinde_sdk.auth.entitlements.BillingApi') as mock_billing_class:
            
            mock_config = Mock()
            mock_config_class.return_value = mock_config
            mock_api_client = Mock()
            mock_api_client_class.return_value = mock_api_client
            mock_billing = Mock()
            mock_billing.get_entitlement.side_effect = Exception("API Error")
            mock_billing_class.return_value = mock_billing
            
            entitlements = Entitlements("https://test.kinde.com", "test_token")
            
            # Verify that the exception is propagated
            with pytest.raises(Exception, match="API Error"):
                entitlements.get_entitlement("test_key")

    def test_metadata_has_more_false_string(self):
        """Test get_all_entitlements when has_more is False as string."""
        with patch('kinde_sdk.auth.entitlements.Configuration') as mock_config_class, \
             patch('kinde_sdk.auth.entitlements.ApiClient') as mock_api_client_class, \
             patch('kinde_sdk.auth.entitlements.BillingApi') as mock_billing_class:
            
            mock_config = Mock()
            mock_config_class.return_value = mock_config
            mock_api_client = Mock()
            mock_api_client_class.return_value = mock_api_client
            mock_billing = Mock()
            
                        # Create a mock response where has_more might be a string "false"
            mock_response = Mock()
            mock_response.data = Mock()
            mock_response.data.entitlements = []
            mock_response.metadata = Mock()
            mock_response.metadata.has_more = "false"  # String instead of boolean
            mock_response.metadata.next_page_starting_after = None

            # Configure the mock to return the response immediately
            mock_billing.get_entitlements = Mock(return_value=mock_response)
            mock_billing_class.return_value = mock_billing
            
            entitlements = Entitlements("https://test.kinde.com", "test_token")
            result = entitlements.get_all_entitlements()
            
            # Should still work and return empty list
            assert len(result) == 0
            # Should only call API once since has_more is falsy
            assert mock_billing.get_entitlements.call_count == 1
