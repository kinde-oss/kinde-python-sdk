"""
Test cases for SDK tracking header functionality.

Tests the implementation of Kinde-SDK tracking headers as per specification requirements.
"""

import pytest
import sys
import unittest
from unittest.mock import patch, Mock, MagicMock
import importlib.metadata

from kinde_sdk.management.management_token_manager import ManagementTokenManager


class TestSDKTracking(unittest.TestCase):
    """Test cases for SDK tracking header functionality."""
    
    def setUp(self):
        """Reset instances before each test."""
        ManagementTokenManager.reset_instances()
    
    def tearDown(self):
        """Clean up after each test."""
        ManagementTokenManager.reset_instances()

    def test_sdk_version_detection(self):
        """Test SDK version detection."""
        manager = ManagementTokenManager("test.kinde.com", "client_id", "client_secret")
        
        # Test that version detection works
        version = manager._get_sdk_version()
        
        # Should return either the actual version or the dev fallback
        assert isinstance(version, str)
        assert len(version) > 0
        
        # Version should be in semantic version format or dev format
        assert any([
            version.count('.') >= 2,  # Semantic version (e.g., "2.0.0")
            'dev' in version.lower()   # Development version
        ])

    def test_python_version_detection(self):
        """Test Python version detection."""
        manager = ManagementTokenManager("test.kinde.com", "client_id", "client_secret")
        
        version = manager._get_python_version()
        
        # Should return current Python version
        expected = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        assert version == expected
        
        # Version should have at least 2 dots (major.minor.micro)
        assert version.count('.') >= 2

    def test_framework_detection_no_framework(self):
        """Test framework detection when no framework is present."""
        manager = ManagementTokenManager("test.kinde.com", "client_id", "client_secret")
        
        # Mock importlib to simulate no frameworks installed
        with patch('importlib.import_module') as mock_import:
            mock_import.side_effect = ImportError("No module found")
            
            framework = manager._detect_framework()
            assert framework is None

    def test_framework_detection_with_flask(self):
        """Test framework detection when Flask is present."""
        manager = ManagementTokenManager("test.kinde.com", "client_id", "client_secret")
        
        # Mock importlib to simulate Flask being installed
        with patch('importlib.import_module') as mock_import:
            def mock_import_func(module_name):
                if module_name == 'flask':
                    return Mock()  # Simulate successful import
                else:
                    raise ImportError("Module not found")
            
            mock_import.side_effect = mock_import_func
            
            framework = manager._detect_framework()
            assert framework == "Flask"

    def test_framework_detection_with_django(self):
        """Test framework detection when Django is present."""
        manager = ManagementTokenManager("test.kinde.com", "client_id", "client_secret")
        
        # Mock importlib to simulate Django being installed
        with patch('importlib.import_module') as mock_import:
            def mock_import_func(module_name):
                if module_name == 'django':
                    return Mock()  # Simulate successful import
                else:
                    raise ImportError("Module not found")
            
            mock_import.side_effect = mock_import_func
            
            framework = manager._detect_framework()
            assert framework == "Django"

    def test_tracking_header_no_framework_four_segments(self):
        """Test tracking header generation when no framework is detected - should have 4 segments."""
        manager = ManagementTokenManager("test.kinde.com", "client_id", "client_secret")
        
        # Mock version methods and framework detection
        with patch.object(manager, '_get_sdk_version', return_value='2.0.0'):
            with patch.object(manager, '_get_python_version', return_value='3.11.0'):
                with patch.object(manager, '_detect_framework', return_value=None):
                    
                    header = manager._generate_tracking_header()
                    
                    # Should be in format: Python/[SDK_VERSION]/[PYTHON_VERSION]/python
                    assert header == "Python/2.0.0/3.11.0/python"
                    
                    # Verify it has exactly 4 segments
                    segments = header.split('/')
                    assert len(segments) == 4
                    assert segments[0] == "Python"
                    assert segments[1] == "2.0.0"
                    assert segments[2] == "3.11.0"
                    assert segments[3] == "python"

    def test_tracking_header_with_framework_four_segments(self):
        """Test tracking header generation with framework detected - should have 4 segments."""
        manager = ManagementTokenManager("test.kinde.com", "client_id", "client_secret")
        
        # Mock version methods and framework detection
        with patch.object(manager, '_get_sdk_version', return_value='2.0.0'):
            with patch.object(manager, '_get_python_version', return_value='3.11.0'):
                with patch.object(manager, '_detect_framework', return_value='Flask'):
                    
                    header = manager._generate_tracking_header()
                    
                    # Should be in format: Python-[framework]/[SDK_VERSION]/[PYTHON_VERSION]/python
                    assert header == "Python-Flask/2.0.0/3.11.0/python"
                    
                    # Verify it has exactly 4 segments
                    segments = header.split('/')
                    assert len(segments) == 4
                    assert segments[0] == "Python-Flask"
                    assert segments[1] == "2.0.0"
                    assert segments[2] == "3.11.0"
                    assert segments[3] == "python"

    def test_tracking_header_format_compliance_all_cases(self):
        """Test that all tracking header formats comply with 4-segment requirement."""
        manager = ManagementTokenManager("test.kinde.com", "client_id", "client_secret")
        
        test_cases = [
            (None, "Python/2.0.0/3.11.0/python"),
            ("Flask", "Python-Flask/2.0.0/3.11.0/python"),
            ("Django", "Python-Django/2.0.0/3.11.0/python"),
            ("FastAPI", "Python-FastAPI/2.0.0/3.11.0/python"),
        ]
        
        for framework, expected_header in test_cases:
            with self.subTest(framework=framework):
                with patch.object(manager, '_get_sdk_version', return_value='2.0.0'):
                    with patch.object(manager, '_get_python_version', return_value='3.11.0'):
                        if framework:
                            # Test with explicit framework
                            header = manager._generate_tracking_header(framework=framework)
                        else:
                            # Test with no framework detected
                            with patch.object(manager, '_detect_framework', return_value=None):
                                header = manager._generate_tracking_header()
                        
                        assert header == expected_header
                        
                        # Verify 4-segment format
                        segments = header.split('/')
                        assert len(segments) == 4, f"Header {header} should have 4 segments, got {len(segments)}"
                        assert segments[3] == "python", f"Last segment should be 'python', got '{segments[3]}'"

    @patch('kinde_sdk.management.management_token_manager.requests.post')
    def test_tracking_header_in_token_request_four_segments(self, mock_post):
        """Test that tracking header in actual token requests has 4 segments."""
        manager = ManagementTokenManager("test.kinde.com", "client_id", "client_secret")
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {
            "access_token": "test_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Make token request
        manager.request_new_token()
        
        # Get the actual header sent
        headers = mock_post.call_args[1]['headers']
        tracking_header = headers.get('Kinde-SDK')
        
        # Verify header exists and has 4 segments
        assert tracking_header is not None
        segments = tracking_header.split('/')
        assert len(segments) == 4, f"Tracking header should have 4 segments, got {len(segments)}: {tracking_header}"
        
        # Verify format
        assert segments[0].startswith('Python'), f"First segment should start with 'Python', got '{segments[0]}'"
        assert segments[3] == 'python', f"Last segment should be 'python', got '{segments[3]}'"
        
        print(f"✅ Generated 4-segment tracking header: {tracking_header}")

    def test_real_environment_four_segments(self):
        """Test tracking header generation in real environment has 4 segments."""
        manager = ManagementTokenManager("test.kinde.com", "client_id", "client_secret")
        
        # Generate header with real environment values
        header = manager._generate_tracking_header()
        
        # Should be a valid string with 4 segments
        assert isinstance(header, str)
        assert len(header) > 0
        
        segments = header.split('/')
        assert len(segments) == 4, f"Real environment header should have 4 segments, got {len(segments)}: {header}"
        
        # Should follow the pattern
        assert segments[0].startswith("Python"), f"First segment should start with 'Python', got '{segments[0]}'"
        assert segments[3] == "python", f"Last segment should be 'python', got '{segments[3]}'"
        
        # Should contain version information
        assert any(char.isdigit() for char in segments[1]), f"Second segment should contain version numbers: '{segments[1]}'"
        assert any(char.isdigit() for char in segments[2]), f"Third segment should contain version numbers: '{segments[2]}'"
        
        print(f"✅ Real environment 4-segment header: {header}")

    @patch('kinde_sdk.management.management_token_manager.requests.post')
    def test_tracking_header_format_compliance(self, mock_post):
        """Test that tracking header format complies with specification."""
        manager = ManagementTokenManager("test.kinde.com", "client_id", "client_secret")
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {
            "access_token": "test_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Make token request
        manager.request_new_token()
        
        # Get the actual header sent
        headers = mock_post.call_args[1]['headers']
        tracking_header = headers.get('Kinde-SDK')
        
        # Verify header format compliance
        assert tracking_header is not None
        assert tracking_header.startswith('Python')
        
        # Check if it's one of the two expected formats:
        # Format 1: Python/[version]
        # Format 2: Python-[framework]/[sdk_version]/[python_version]/python
        
        if '/' in tracking_header:
            parts = tracking_header.split('/')
            assert len(parts) >= 2  # At minimum: Python/version
            
            if len(parts) == 4:  # Full format with framework
                assert parts[0].startswith('Python-')  # Python-[framework]
                assert parts[3] == 'python'  # Should end with 'python'
        
        print(f"Generated tracking header: {tracking_header}")

    def test_multiple_managers_same_tracking(self):
        """Test that multiple managers generate consistent tracking headers."""
        manager1 = ManagementTokenManager("test1.kinde.com", "client1", "secret1")
        manager2 = ManagementTokenManager("test2.kinde.com", "client2", "secret2")
        
        header1 = manager1._generate_tracking_header()
        header2 = manager2._generate_tracking_header()
        
        # Headers should be identical since they're from the same environment
        assert header1 == header2


if __name__ == '__main__':
    print("TESTING SDK TRACKING HEADER FUNCTIONALITY")
    print("=" * 55)
    print("Testing compliance with Kinde SDK tracking specification")
    print("=" * 55)
    
    unittest.main(verbosity=2)