#!/usr/bin/env python3
"""
Test runner for the new async/sync consistency tests.

This script runs all the tests for the new SmartOAuth, AsyncOAuth, and factory function
to ensure the async/sync consistency solution works correctly.
"""

import sys
import os
import subprocess
import pytest
from pathlib import Path

def run_tests():
    """Run all the async/sync consistency tests."""
    
    # Add the parent directory to the path so we can import the SDK
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    print("🧪 Running Async/Sync Consistency Tests")
    print("=" * 50)
    
    # Define test files to run
    test_files = [
        "testv2/testv2_auth/test_smart_oauth.py",
        "testv2/testv2_auth/test_async_oauth.py", 
        "testv2/testv2_auth/test_factory_function.py"
    ]
    
    # Check if test files exist
    missing_files = []
    for test_file in test_files:
        if not Path(test_file).exists():
            missing_files.append(test_file)
    
    if missing_files:
        print(f"❌ Missing test files: {missing_files}")
        return False
    
    # Run tests with pytest
    test_args = [
        sys.executable, "-m", "pytest",
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--color=yes",  # Colored output
        "--durations=10",  # Show 10 slowest tests
    ]
    
    # Add test files
    test_args.extend(test_files)
    
    print(f"Running: {' '.join(test_args)}")
    print()
    
    try:
        # Run the tests
        result = subprocess.run(
            test_args,
            cwd=project_root,
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print("\n✅ All tests passed!")
            return True
        else:
            print(f"\n❌ Tests failed with return code: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        return False

def run_individual_test_suites():
    """Run individual test suites separately for detailed output."""
    
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    test_suites = [
        ("SmartOAuth Tests", "testv2/testv2_auth/test_smart_oauth.py"),
        ("AsyncOAuth Tests", "testv2/testv2_auth/test_async_oauth.py"),
        ("Factory Function Tests", "testv2/testv2_auth/test_factory_function.py")
    ]
    
    all_passed = True
    
    for suite_name, test_file in test_suites:
        print(f"\n{'='*60}")
        print(f"Running {suite_name}")
        print(f"{'='*60}")
        
        if not Path(test_file).exists():
            print(f"❌ Test file not found: {test_file}")
            all_passed = False
            continue
        
        test_args = [
            sys.executable, "-m", "pytest",
            "-v",
            "--tb=short",
            "--color=yes",
            test_file
        ]
        
        try:
            result = subprocess.run(
                test_args,
                cwd=project_root,
                capture_output=False,
                text=True
            )
            
            if result.returncode == 0:
                print(f"✅ {suite_name} passed!")
            else:
                print(f"❌ {suite_name} failed!")
                all_passed = False
                
        except Exception as e:
            print(f"❌ Error running {suite_name}: {e}")
            all_passed = False
    
    return all_passed

def run_coverage_tests():
    """Run tests with coverage reporting."""
    
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    print("\n📊 Running Tests with Coverage")
    print("=" * 50)
    
    test_files = [
        "testv2/testv2_auth/test_smart_oauth.py",
        "testv2/testv2_auth/test_async_oauth.py", 
        "testv2/testv2_auth/test_factory_function.py"
    ]
    
    coverage_args = [
        sys.executable, "-m", "pytest",
        "--cov=kinde_sdk.auth.smart_oauth",
        "--cov=kinde_sdk.auth.async_oauth", 
        "--cov=kinde_sdk.auth.base_oauth",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
        "-v",
        "--tb=short",
        "--color=yes",
    ]
    
    coverage_args.extend(test_files)
    
    try:
        result = subprocess.run(
            coverage_args,
            cwd=project_root,
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print("\n✅ Coverage tests completed!")
            print("📁 Coverage report generated in htmlcov/")
            return True
        else:
            print(f"\n❌ Coverage tests failed!")
            return False
            
    except Exception as e:
        print(f"\n❌ Error running coverage tests: {e}")
        return False

def main():
    """Main function to run tests."""
    
    print("🚀 Kinde Python SDK Async/Sync Consistency Test Runner")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("kinde_sdk").exists():
        print("❌ Error: kinde_sdk directory not found.")
        print("   Please run this script from the project root directory.")
        return 1
    
    # Check if pytest is available
    try:
        import pytest
    except ImportError:
        print("❌ Error: pytest not installed.")
        print("   Install with: pip install pytest")
        return 1
    
    # Check if coverage is available
    try:
        import coverage
        coverage_available = True
    except ImportError:
        print("⚠️  coverage not installed. Install with: pip install coverage")
        coverage_available = False
    
    # Run tests
    print("\n1. Running all tests together...")
    all_tests_passed = run_tests()
    
    print("\n2. Running individual test suites...")
    individual_tests_passed = run_individual_test_suites()
    
    # Run coverage if available
    if coverage_available:
        print("\n3. Running tests with coverage...")
        coverage_passed = run_coverage_tests()
    else:
        coverage_passed = True  # Skip coverage if not available
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    print(f"✅ All tests together: {'PASSED' if all_tests_passed else 'FAILED'}")
    print(f"✅ Individual test suites: {'PASSED' if individual_tests_passed else 'FAILED'}")
    print(f"✅ Coverage tests: {'PASSED' if coverage_passed else 'FAILED'}")
    
    if all_tests_passed and individual_tests_passed and coverage_passed:
        print("\n🎉 All tests passed! The async/sync consistency solution is working correctly.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the output above for details.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
