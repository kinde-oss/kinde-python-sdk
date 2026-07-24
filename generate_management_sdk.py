#!/usr/bin/env python3
"""
Kinde Management SDK Generator from OpenAPI specification.

This script automates the generation of the Management API SDK
using OpenAPI Generator. It provides:
- Prerequisites checking
- SDK generation with proper configuration
- Import path fixing
- Custom file preservation
- Code validation
- Test execution
- Git diff review

Usage:
    python3 generate_management_sdk.py [--skip-tests] [--no-diff]
"""

import argparse
import logging
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any

from _sdk_generator_utils import (
    DYNAMIC_VERSION_IMPORT,
    PACKAGE_VERSION_PLACEHOLDER,
    SDK_VERSION,
    make_version_dynamic,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


# Re-export under the domain-specific name used in this script's log
# messages, docstrings, and the comments inside ``openapitools.json``.
# This is just an alias for ``_sdk_generator_utils.PACKAGE_VERSION_PLACEHOLDER``
# - the shared constant remains the single source of truth, so the two
# generator scripts cannot drift on the placeholder value.
OPENAPITOOLS_PACKAGE_VERSION_PLACEHOLDER = PACKAGE_VERSION_PLACEHOLDER


# =============================================================================
# SDK CONFIGURATION
# =============================================================================

SDK_CONFIG = {
    "name": "Management API",
    "spec_url": "https://api-spec.kinde.com/kinde-management-api-spec.yaml",
    "output_dir": "kinde_sdk/management",
    "package_name": "kinde_sdk.management",
    "openapi_tools_config": "openapitools.json",
    "openapi_tools_generator_name": "management",
    "custom_files": [
        "management_client.py",
        "management_token_manager.py",
        "custom_exceptions.py",
        "kinde_api_client.py",
        "README.md"
    ],
    "custom_imports": [
        "",
        "# Custom imports for Kinde Management Client",
        "from .management_client import ManagementClient",
        "from .management_token_manager import ManagementTokenManager",
        "",
        "# Extend __all__ with custom exports (preserves generator-populated entries)",
        "__all__.extend(['ManagementClient', 'ManagementTokenManager'])",
        ""
    ],
    # Run the full management regression suite after regeneration (not only
    # the original client smoke file). Directory path is intentional.
    "test_path": "testv2/testv2_management"
}


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def print_subsection(title: str):
    """Print a formatted subsection header."""
    print(f"\n{'-'*60}")
    print(f"  {title}")
    print('-'*60)


# =============================================================================
# PREREQUISITES
# =============================================================================

def check_prerequisites() -> bool:
    """
    Verify required tools are installed.
    
    Returns:
        True if all prerequisites are met, False otherwise
    """
    print_section("Checking Prerequisites")
    
    all_ok = True
    
    # Check for npx (comes with Node.js)
    try:
        result = subprocess.run(
            ["npx", "--version"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            print("❌ npx not found. Please install Node.js and npm.")
            all_ok = False
        else:
            print(f"✓ npx: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ npx not found. Please install Node.js and npm.")
        all_ok = False
    
    # Check for openapi-generator-cli
    try:
        result = subprocess.run(
            ["npx", "@openapitools/openapi-generator-cli", "version"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            print("❌ openapi-generator-cli not found")
            print("Install with: npm install @openapitools/openapi-generator-cli -g")
            all_ok = False
        else:
            print(f"✓ openapi-generator-cli: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ openapi-generator-cli not accessible via npx")
        all_ok = False
    
    # Check for Python
    print(f"✓ Python: {sys.version.split()[0]}")
    
    # Check for pytest (optional but recommended)
    try:
        result = subprocess.run(
            ["pytest", "--version"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            print(f"✓ pytest: {result.stdout.strip().split()[1]}")
        else:
            print("⚠️  pytest not found (tests will be skipped)")
    except FileNotFoundError:
        print("⚠️  pytest not found (tests will be skipped)")
    
    # Check for git (optional but useful)
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            print(f"✓ git: {result.stdout.strip().split()[2]}")
        else:
            print("⚠️  git not found (diff review will be skipped)")
    except FileNotFoundError:
        print("⚠️  git not found (diff review will be skipped)")
    
    return all_ok


# =============================================================================
# CONFIGURATION MANAGEMENT
# =============================================================================

def ensure_root_openapi_generator_ignore():
    """
    Ensure root-level .openapi-generator-ignore exists to protect project files.
    
    This is critical to prevent OpenAPI Generator from overwriting packaging
    configuration files when generating SDKs.
    """
    root_ignore_file = Path(".openapi-generator-ignore")
    
    # Critical project files that must never be overwritten
    critical_files = [
        "# CRITICAL: Project packaging files - never overwrite these!",
        "pyproject.toml",
        "setup.py",
        "setup.cfg",
        "MANIFEST.in",
        "requirements.txt",
        "README.md",
        "",
        "# Prevent root-level generation artifacts",
        "*.yml",
        "*.yaml",
        "tox.ini",
        "",
    ]
    
    if root_ignore_file.exists():
        # Check if critical files are protected
        content = root_ignore_file.read_text(encoding='utf-8')
        if "pyproject.toml" in content:
            logger.debug("✓ Root .openapi-generator-ignore already protects critical files")
            return
        
        # Append critical files to existing file
        with open(root_ignore_file, 'a', encoding='utf-8') as f:
            f.write("\n" + "\n".join(critical_files))
        print("✓ Updated root .openapi-generator-ignore to protect packaging files")
    else:
        # Create new file with critical protections
        ignore_content = [
            "# OpenAPI Generator Ignore",
            "# This file tells the generator which files to NOT overwrite.",
            "# Works like .gitignore - list files/patterns to preserve.",
            "",
        ] + critical_files + [
            "# Python cache",
            "__pycache__/",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            ".Python",
            "",
            "# IDE files",
            ".vscode/",
            ".idea/",
            "*.swp",
            "*.swo",
            "*~",
            "",
            "# Test files",
            "test/",
            ""
        ]
        root_ignore_file.write_text("\n".join(ignore_content), encoding='utf-8')
        print("✓ Created root .openapi-generator-ignore to protect project files")


def ensure_openapi_generator_ignore(config: Dict[str, Any]):
    """
    Ensure .openapi-generator-ignore file exists in the output directory.
    
    Args:
        config: SDK configuration dictionary
    """
    output_dir = Path(config["output_dir"])
    ignore_file = output_dir / ".openapi-generator-ignore"
    
    if ignore_file.exists():
        logger.debug(f"✓ .openapi-generator-ignore already exists at {ignore_file}")
        return
    
    # Create the ignore file
    ignore_content = [
        "# OpenAPI Generator Ignore",
        "# This file tells the generator which files to NOT overwrite.",
        "# Works like .gitignore - list files/patterns to preserve.",
        "",
        "# Custom Kinde SDK files - never overwrite these"
    ]
    
    # Add custom files from config
    for custom_file in config["custom_files"]:
        ignore_content.append(custom_file)
    
    ignore_content.extend([
        "",
        "# Python cache",
        "__pycache__/",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        ".Python",
        "",
        "# IDE files",
        ".vscode/",
        ".idea/",
        "*.swp",
        "*.swo",
        "*~",
        "",
        "# Test files",
        "test/",
        ""
    ])
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write the ignore file
    ignore_file.write_text("\n".join(ignore_content), encoding='utf-8')
    print(f"✓ Created .openapi-generator-ignore at {ignore_file}")


def ensure_openapitools_config(config: Dict[str, Any]):
    """
    Authoritatively (re)write ``openapitools.json`` so the committed file is
    always self-evidently a *template*, never a second source of truth for
    the SDK version.

    Design: the ``packageVersion`` field in the file is set to the literal
    placeholder ``"SDK_VERSION"`` (the same name as the Python constant in
    this script that holds the resolved value). Anyone reading the file
    sees immediately that this is a placeholder, not a version literal.

    The resolved version is supplied at runtime via
    ``--additional-properties=packageVersion=<SDK_VERSION>`` on the
    ``openapi-generator-cli`` command line (see ``generate_sdk``), which
    overrides the file's placeholder. As an additional safety net,
    ``make_version_dynamic`` rewrites the generator-emitted
    ``__version__ = "..."`` line in the produced ``__init__.py`` to import
    from ``kinde_sdk._version``, so the placeholder never reaches a
    wrapper-generated artifact.

    Direct ``openapi-generator-cli`` invocations that bypass the wrapper
    (and therefore don't pass ``--additional-properties``) will produce a
    ``configuration.py`` whose user-agent reads ``"OpenAPI-Generator/SDK_VERSION/python"``.
    That is intentionally obvious-broken: it loudly signals "use the
    wrapper script" rather than silently shipping a stale version.

    ``testv2/testv2_core/test_version_sync.py`` asserts this placeholder
    invariant in CI so the file cannot regress to a literal version.

    Args:
        config: SDK configuration dictionary
    """
    import json
    
    config_file = Path(config["openapi_tools_config"])
    generator_name = config["openapi_tools_generator_name"]
    
    expected_generator_config = {
        "generatorName": "python",
        "inputSpec": config["spec_url"],
        "output": ".",
        "glob": "**/*",
        "additionalProperties": {
            "packageName": config["package_name"],
            "projectName": "kinde-python-sdk",
            # Self-documenting placeholder; resolved version is supplied at
            # runtime via --additional-properties (see generate_sdk).
            "packageVersion": OPENAPITOOLS_PACKAGE_VERSION_PLACEHOLDER,
            "library": "urllib3",
            "generateSourceCodeOnly": True  # CRITICAL: Only generate source code, not project templates
        },
        "skipValidateSpec": True,
        "files": {}
    }
    
    previous_package_version = None
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            openapitools_config = json.load(f)
        previous_package_version = (
            openapitools_config
            .get("generator-cli", {})
            .get("generators", {})
            .get(generator_name, {})
            .get("additionalProperties", {})
            .get("packageVersion")
        )
    else:
        openapitools_config = {
            "$schema": "https://raw.githubusercontent.com/OpenAPITools/openapi-generator-cli/master/apps/generator-cli/src/config.schema.json",
            "spaces": 2,
            "generator-cli": {
                "version": "7.9.0",
                "storageDir": "~/.openapi-generator",
                "generators": {}
            }
        }
    
    if "generator-cli" not in openapitools_config:
        openapitools_config["generator-cli"] = {
            "version": "7.9.0",
            "storageDir": "~/.openapi-generator",
            "generators": {}
        }
    
    if "generators" not in openapitools_config["generator-cli"]:
        openapitools_config["generator-cli"]["generators"] = {}
    
    openapitools_config["generator-cli"]["generators"][generator_name] = expected_generator_config
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(openapitools_config, f, indent=2)
    
    if (
        previous_package_version
        and previous_package_version != OPENAPITOOLS_PACKAGE_VERSION_PLACEHOLDER
    ):
        print(
            f"✓ Reset {config_file} packageVersion from {previous_package_version!r} "
            f"back to the {OPENAPITOOLS_PACKAGE_VERSION_PLACEHOLDER!r} placeholder. "
            f"The resolved version ({SDK_VERSION}) is injected via "
            f"--additional-properties at openapi-generator-cli invocation time."
        )
    else:
        print(
            f"✓ Confirmed {config_file} packageVersion is the "
            f"{OPENAPITOOLS_PACKAGE_VERSION_PLACEHOLDER!r} placeholder "
            f"(resolved version {SDK_VERSION} supplied via CLI --additional-properties)"
        )


# =============================================================================
# SDK GENERATION
# =============================================================================

def generate_sdk(config: Dict[str, Any]) -> bool:
    """
    Generate SDK using OpenAPI Generator.
    
    Args:
        config: SDK configuration dictionary
        
    Returns:
        True if generation succeeded, False otherwise
    """
    print_section(f"Generating {config['name']} SDK")
    
    # Ensure root-level protections exist first
    ensure_root_openapi_generator_ignore()
    
    # Ensure configuration files are up to date
    ensure_openapi_generator_ignore(config)
    ensure_openapitools_config(config)
    
    # Build command with additionalProperties passed directly
    # This ensures the package name and other settings are applied correctly
    additional_props = ",".join([
        f"packageName={config['package_name']}",
        "projectName=kinde-python-sdk",
        f"packageVersion={SDK_VERSION}",
        "library=urllib3",
        "generateSourceCodeOnly=true"
    ])
    
    cmd = [
        "npx", "@openapitools/openapi-generator-cli", "generate",
        "-i", config["spec_url"],
        "-g", "python",
        "-o", ".",
        f"--additional-properties={additional_props}",
        "--skip-validate-spec"
    ]
    
    print(f"Spec: {config['spec_url']}")
    print(f"Output: {config['output_dir']}")
    print(f"Package: {config['package_name']}")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ Generation completed successfully")
        
        # Clean up unwanted template files that OpenAPI Generator creates at root level
        cleanup_generated_templates(config)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Generation failed: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def cleanup_generated_templates(config: Dict[str, Any] = None):
    """
    Remove template files that OpenAPI Generator creates.
    
    These files are meant for standalone packages but are not needed in this
    multi-package repository that has its own packaging setup.
    
    Args:
        config: Optional SDK configuration to also clean up output directory
    """
    import shutil
    
    template_files = [
        ".travis.yml",
        ".gitlab-ci.yml",
        "tox.ini",
        "git_push.sh",
        "test-requirements.txt",
        "setup.py",
        "setup.cfg",
        ".github/workflows/python.yml",
    ]
    
    template_dirs = [
        "docs",  # Root-level docs generated by OpenAPI (we keep SDK-specific docs in kinde_sdk/docs)
        "test",  # Root-level test stubs (we use testv2/)
    ]
    
    # Also clean up docs/test directories inside the output directory
    if config and "output_dir" in config:
        output_dir = config["output_dir"]
        template_dirs.extend([
            f"{output_dir}/docs",
            f"{output_dir}/test",
        ])
    
    removed_count = 0
    
    # Remove template files
    for template_file in template_files:
        file_path = Path(template_file)
        if file_path.exists():
            file_path.unlink()
            removed_count += 1
    
    # Remove template directories
    for template_dir in template_dirs:
        dir_path = Path(template_dir)
        if dir_path.exists() and dir_path.is_dir():
            shutil.rmtree(dir_path)
            removed_count += 1
    
    if removed_count > 0:
        print(f"✓ Cleaned up {removed_count} template file(s) and directory(ies)")
    else:
        logger.debug("✓ No template files to clean up")


# =============================================================================
# IMPORT FIXING
# =============================================================================

def fix_imports(config: Dict[str, Any]):
    """
    Fix import paths in generated files to use correct package namespace.
    
    Uses regex-based approach to handle various import patterns.
    
    Args:
        config: SDK configuration dictionary
    """
    print_section("Fixing Imports")
    
    output_dir = Path(config["output_dir"])
    package_name = config["package_name"]
    fixed_count = 0
    
    for py_file in output_dir.rglob("*.py"):
        # Skip custom files (they're already correct)
        if py_file.name in config["custom_files"]:
            continue
        
        try:
            content = py_file.read_text(encoding='utf-8')
            original_content = content
            
            # Extract the base package name (e.g., "kinde_sdk")
            base_package = package_name.split('.')[0]
            subpackage = package_name.split('.')[-1]  # e.g., "management" or "frontend"
            
            # Pattern 1: Fix "from kinde_sdk import X" to include the subpackage
            # But ONLY if kinde_sdk is NOT followed by a dot (which would indicate a submodule)
            # This ensures we don't change "from kinde_sdk.core" or "from kinde_sdk.management"
            # We only change bare "from kinde_sdk import X"
            pattern = f'\\bfrom {base_package}(?!\\.)\\b'
            content = re.sub(pattern, f'from {package_name}', content)
            
            # Pattern 2: Fix "import kinde_sdk.X" statements
            # Only fix if subpackage is not already in the path
            lines = content.split('\n')
            fixed_lines = []
            for line in lines:
                if line.strip().startswith(f'import {base_package}.'):
                    # Only fix if our subpackage is not already in the import path
                    subpackage = package_name.split('.')[-1]
                    if f'.{subpackage}' not in line:
                        line = line.replace(f'import {base_package}.', f'import {package_name}.')
                fixed_lines.append(line)
            content = '\n'.join(fixed_lines)
            
            # Only write if changed
            if content != original_content:
                py_file.write_text(content, encoding='utf-8')
                fixed_count += 1
                print(f"  Fixed: {py_file.relative_to('.')}")
        
        except Exception as e:
            print(f"  ⚠️  Warning: Could not fix {py_file}: {e}")
    
    if fixed_count > 0:
        print(f"✓ Fixed imports in {fixed_count} files")
    else:
        print("✓ No import fixes needed")


# =============================================================================
# CUSTOM IMPORTS
# =============================================================================

def add_custom_imports(config: Dict[str, Any]):
    """
    Add custom imports to __init__.py if not already present.
    
    Args:
        config: SDK configuration dictionary
    """
    print_section("Adding Custom Imports")
    
    output_dir = Path(config["output_dir"])
    init_file = output_dir / "__init__.py"
    
    if not init_file.exists():
        print("⚠️  Warning: __init__.py not found")
        return
    
    content = init_file.read_text(encoding='utf-8')
    
    # Check if custom imports are already present (check first import line)
    first_custom_import = config["custom_imports"][1]  # Skip empty line
    if first_custom_import.lstrip('# ') in content:
        print("✓ Custom imports already present")
        return
    
    # Add custom imports at the end
    custom_imports_text = "\n".join(config["custom_imports"])
    updated_content = content + "\n" + custom_imports_text
    init_file.write_text(updated_content, encoding='utf-8')
    print("✓ Added custom imports to __init__.py")


# =============================================================================
# VALIDATION
# =============================================================================

def validate_generation(config: Dict[str, Any]) -> bool:
    """
    Validate that generated code is syntactically correct.
    
    Args:
        config: SDK configuration dictionary
        
    Returns:
        True if validation passed, False otherwise
    """
    print_section("Validating Generated Code")
    
    output_dir = Path(config["output_dir"])
    init_file = output_dir / "__init__.py"
    
    # Basic Python syntax check
    try:
        subprocess.run(
            ["python3", "-m", "py_compile", str(init_file)],
            check=True,
            capture_output=True
        )
        print("✓ Python syntax validation passed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Python syntax validation failed")
        return False


# =============================================================================
# TESTING
# =============================================================================

def run_tests(config: Dict[str, Any]) -> bool:
    """
    Run tests to ensure generation didn't break anything.
    
    Args:
        config: SDK configuration dictionary
        
    Returns:
        True if tests passed or were skipped, False if tests failed
    """
    print_section("Running Tests")
    
    test_path = config.get("test_path")
    if not test_path:
        print("⚠️  No tests configured for this SDK")
        return True
    
    if not Path(test_path).exists():
        print(f"⚠️  Test path not found: {test_path}")
        return True
    
    # Check if pytest is available
    try:
        subprocess.run(["pytest", "--version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("⚠️  pytest not available, skipping tests")
        return True
    
    # Run tests (file or directory)
    print(f"Running tests from {test_path}...")
    result = subprocess.run(
        ["pytest", test_path, "-v", "--no-cov"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✓ All tests passed")
        return True
    else:
        print("❌ Some tests failed:")
        print(result.stdout)
        print("\n⚠️  Warning: Generated code may have broken existing functionality")
        print("Review the test failures before committing changes.")
        return False


# =============================================================================
# GIT DIFF
# =============================================================================

def show_diff(config: Dict[str, Any]):
    """
    Show git diff of generated files for review.
    
    Args:
        config: SDK configuration dictionary
    """
    print_section("Changes Review")
    
    output_dir = config["output_dir"]
    
    # Check if git is available
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("⚠️  git not available, skipping diff")
        return
    
    # Show summary of changes
    result = subprocess.run(
        ["git", "diff", "--stat", output_dir],
        capture_output=True,
        text=True
    )
    
    if result.stdout.strip():
        print("Modified files:")
        print(result.stdout)
        print("\nTo see detailed changes, run:")
        print(f"  git diff {output_dir}")
    else:
        print("✓ No changes detected")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def generate_single_sdk(skip_tests: bool, no_diff: bool) -> bool:
    """
    Generate the Management SDK.
    
    Args:
        skip_tests: Whether to skip running tests
        no_diff: Whether to skip showing git diff
        
    Returns:
        True if generation succeeded, False otherwise
    """
    config = SDK_CONFIG
    
    print_subsection(f"Processing {config['name']}")
    
    # Step 1: Generate SDK
    if not generate_sdk(config):
        return False
    
    # Step 2: Fix imports
    fix_imports(config)

    # Step 2b: Replace the OpenAPI-emitted literal __version__ with an import
    # from kinde_sdk._version, so this sub-package never drifts from the SDK.
    make_version_dynamic(Path(config["output_dir"]) / "__init__.py")

    # Step 3: Add custom imports
    add_custom_imports(config)
    
    # Step 4: Validate
    if not validate_generation(config):
        return False
    
    # Step 5: Run tests (unless skipped)
    tests_passed = True
    if not skip_tests:
        tests_passed = run_tests(config)
    
    # Step 6: Show diff (unless skipped)
    if not no_diff:
        show_diff(config)
    
    return tests_passed


def main():
    """Main execution flow."""
    parser = argparse.ArgumentParser(
        description="Generate Kinde Management SDK from OpenAPI specification",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 generate_management_sdk.py
  python3 generate_management_sdk.py --skip-tests
  python3 generate_management_sdk.py --no-diff
        """
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip running tests"
    )
    parser.add_argument(
        "--no-diff",
        action="store_true",
        help="Skip showing git diff"
    )
    args = parser.parse_args()
    
    print("🔧 Kinde Management SDK Generator")
    
    # Step 1: Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites check failed")
        print("Please install required tools and try again")
        return 1
    
    # Step 2: Generate SDK
    all_passed = generate_single_sdk(args.skip_tests, args.no_diff)
    
    # Final summary
    print_section("Summary")
    
    if all_passed:
        print("✓ SDK generation completed successfully")
    else:
        print("⚠️  SDK generation completed with warnings/failures")
        print("Review the output above for details")
    
    print("\nNext steps:")
    sdk_dir = SDK_CONFIG["output_dir"]
    print(f"  1. Review changes: git diff {sdk_dir}")
    print("  2. Test manually if needed")
    print("  3. Commit changes when satisfied")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
