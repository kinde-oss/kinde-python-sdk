import os
import re
import subprocess
import sys
import shutil
import tempfile
from pathlib import Path

# OpenAPI spec URL from Kinde Frontend API
OPENAPI_SPEC_URL = "https://api-spec.kinde.com/kinde-frontend-api-spec.yaml"
OUTPUT_DIR = "kinde_sdk/frontend"
GENERATOR_DIR = "generator"
CONFIG_FILE = f"{GENERATOR_DIR}/frontend_config.yaml"


def _read_sdk_version() -> str:
    """
    Read the canonical SDK version from ``kinde_sdk/_version.py``.

    The OpenAPI generator's ``packageVersion`` is set from this value so that
    artifacts which embed the version literally (e.g. user-agent headers in
    the generated ``configuration.py``) stay in lockstep with the SDK.

    The generated ``kinde_sdk/frontend/__init__.py`` doesn't keep a literal
    copy of the version - it re-exports ``kinde_sdk._version.__version__``,
    and ``make_version_dynamic`` (called below after generation) rewrites the
    OpenAPI-emitted ``__version__ = "..."`` line back to that import on every
    regeneration.
    """
    version_path = Path(__file__).resolve().parent / "kinde_sdk" / "_version.py"
    text = version_path.read_text(encoding="utf-8")
    match = re.search(r'^__version__\s*=\s*["\']([^"\']+)["\']', text, re.MULTILINE)
    if not match:
        raise RuntimeError(
            f"Could not parse __version__ from {version_path}; "
            "the generator can't derive packageVersion."
        )
    return match.group(1)


SDK_VERSION = _read_sdk_version()


DYNAMIC_VERSION_IMPORT = (
    "from kinde_sdk._version import __version__  "
    "# single source of truth; see kinde_sdk/_version.py"
)


def make_version_dynamic(init_file):
    """
    Replace the OpenAPI-emitted ``__version__ = "X"`` line in the generated
    ``__init__.py`` with an import from ``kinde_sdk._version``, so the
    sub-package never holds a literal version that can drift.

    Idempotent: a no-op if the file already imports from ``kinde_sdk._version``.
    """
    init_path = Path(init_file)
    if not init_path.exists():
        print(f"Warning: cannot rewrite __version__: {init_path} does not exist")
        return

    text = init_path.read_text(encoding="utf-8")

    if "from kinde_sdk._version import __version__" in text:
        print(f"{init_path} already imports __version__ from kinde_sdk._version")
        return

    new_text, n = re.subn(
        r'^__version__\s*=\s*["\'][^"\']+["\']\s*$',
        DYNAMIC_VERSION_IMPORT,
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if n == 0:
        print(
            f"Warning: could not find literal __version__ in {init_path} to replace; "
            "is the OpenAPI generator template still emitting one?"
        )
        return

    init_path.write_text(new_text, encoding="utf-8")
    print(f"Rewrote __version__ in {init_path} to import from kinde_sdk._version")

def fix_imports(directory):
    """Fix import paths in generated Python files."""
    print(f"Fixing imports in {directory}")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Fix imports for the frontend package structure
                    original_content = content
                    
                    # Fix all kinde_sdk imports to use frontend module
                    content = content.replace('from kinde_sdk import schemas', 'from kinde_sdk.frontend import schemas')
                    content = content.replace('from kinde_sdk import api_client', 'from kinde_sdk.frontend import api_client')
                    content = content.replace('from kinde_sdk import exceptions', 'from kinde_sdk.frontend import exceptions')
                    content = content.replace('from kinde_sdk import configuration', 'from kinde_sdk.frontend import configuration')
                    content = content.replace('from kinde_sdk import rest', 'from kinde_sdk.frontend import rest')
                    
                    # Fix combined imports
                    content = content.replace('from kinde_sdk import api_client, exceptions', 'from kinde_sdk.frontend import api_client, exceptions')
                    content = content.replace('from kinde_sdk import exceptions, api_client', 'from kinde_sdk.frontend import exceptions, api_client')
                    
                    # Fix import statements
                    content = content.replace('from kinde_sdk import', 'from kinde_sdk.frontend import')
                    content = content.replace('import kinde_sdk.schemas', 'import kinde_sdk.frontend.schemas')
                    content = content.replace('kinde_sdk.schemas', 'kinde_sdk.frontend.schemas')
                    
                    # Fix any remaining references to root kinde_sdk modules
                    content = content.replace('kinde_sdk.api_client', 'kinde_sdk.frontend.api_client')
                    content = content.replace('kinde_sdk.exceptions', 'kinde_sdk.frontend.exceptions')
                    content = content.replace('kinde_sdk.configuration', 'kinde_sdk.frontend.configuration')
                    content = content.replace('kinde_sdk.rest', 'kinde_sdk.frontend.rest')
                    
                    # Only write if content changed
                    if content != original_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"Fixed imports in: {filepath}")
                except Exception as e:
                    print(f"Warning: Could not fix imports in {filepath}: {e}")

def preserve_custom_imports():
    """Preserve custom imports in the __init__.py file after generation."""
    init_file = os.path.join(OUTPUT_DIR, "__init__.py")
    if not os.path.exists(init_file):
        print("Warning: __init__.py file not found, cannot preserve custom imports")
        return
    
    # Custom imports to preserve
    custom_imports = [
        "# Custom imports for Kinde Frontend Client",
        "from .frontend_client import FrontendClient",
        "",
        "# Re-export for convenience",
        "__all__ = ['FrontendClient']",
        ""
    ]
    
    try:
        with open(init_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if custom imports are already present
        if "from .frontend_client import FrontendClient" in content:
            print("Custom imports already present in __init__.py")
            return
        
        # Add custom imports at the end of the file
        custom_imports_text = "\n".join(custom_imports)
        updated_content = content + "\n" + custom_imports_text
        
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("Added custom imports to __init__.py")
        
    except Exception as e:
        print(f"Warning: Could not preserve custom imports in {init_file}: {e}")

def cleanup_old_generated_files():
    """Clean up old generated files that might conflict with our new structure."""
    print("Cleaning up old generated files...")
    
    # Remove old generated files from root kinde_sdk directory
    old_files_to_remove = [
        "api_client.py",
        "configuration.py",
        "exceptions.py",
        "rest.py"
    ]
    
    for file in old_files_to_remove:
        filepath = os.path.join("kinde_sdk", file)
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Removed old file: {filepath}")
    
    # Remove old schemas directory if it exists
    old_schemas_dir = os.path.join("kinde_sdk", "schemas")
    if os.path.exists(old_schemas_dir):
        shutil.rmtree(old_schemas_dir)
        print(f"Removed old schemas directory: {old_schemas_dir}")

def preserve_custom_files():
    """Preserve custom files before generation."""
    backup_dir = None
    if os.path.exists(OUTPUT_DIR):
        backup_dir = f"{OUTPUT_DIR}_backup"
        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir)
        shutil.copytree(OUTPUT_DIR, backup_dir)
        print(f"Backed up existing files to: {backup_dir}")
    return backup_dir

def restore_custom_files(backup_dir):
    """Restore custom files after generation."""
    if backup_dir and os.path.exists(backup_dir):
        # Restore custom files that should not be overwritten
        custom_files = [
            "frontend_client.py",
            "frontend_token_manager.py"
        ]
        
        for file in custom_files:
            backup_file = os.path.join(backup_dir, file)
            target_file = os.path.join(OUTPUT_DIR, file)
            if os.path.exists(backup_file):
                shutil.copy2(backup_file, target_file)
                print(f"Restored custom file: {file}")
        
        # Clean up backup directory
        shutil.rmtree(backup_dir)
        print("Cleaned up backup directory")

# Check if openapi-generator-cli is available
if not any(
    os.access(os.path.join(path, 'openapi-generator-cli'), os.X_OK)
    or os.access(os.path.join(path, 'openapi-generator-cli.bat'), os.X_OK)
    for path in os.environ["PATH"].split(os.pathsep)
):
    print("Error: openapi-generator-cli is not installed or not in your PATH.")
    print("Install it from https://openapi-generator.tech/docs/installation or with 'npm install @openapitools/openapi-generator-cli -g'")
    sys.exit(1)

# Create generator directory if it doesn't exist
if not os.path.exists(GENERATOR_DIR):
    os.makedirs(GENERATOR_DIR)
    print(f"Created directory: {GENERATOR_DIR}")

# Always (re)write the frontend config so packageVersion stays in lockstep
# with the SDK version on every regeneration; otherwise a stale local file
# would silently override the SDK version.
config_content = f"""# openapi-generator-cli config for python frontend API
# NOTE: this file is regenerated by generate_frontend_sdk.py on every run.
# packageVersion is derived from kinde_sdk/__init__.py's __version__.

packageName: kinde_sdk.frontend
projectName: kinde-python-sdk
packageVersion: {SDK_VERSION}
# It is recommended to use a released version of the generator.
# For example:
# generatorVersion: "7.13.0"
"""
with open(CONFIG_FILE, 'w') as f:
    f.write(config_content)
print(f"Wrote config file: {CONFIG_FILE} (packageVersion={SDK_VERSION})")

# Create temporary directory for generation
with tempfile.TemporaryDirectory() as temp_dir:
    print(f"Generating to temporary directory: {temp_dir}")
    
    cmd = [
        "openapi-generator-cli", "generate",
        "-i", OPENAPI_SPEC_URL,
        "-g", "python",
        "-o", temp_dir,
        "-c", CONFIG_FILE,
        "--skip-validate-spec"
    ]

    print(f"Using config file: {CONFIG_FILE}")
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    
    # Clean up old generated files first
    cleanup_old_generated_files()
    
    # Preserve custom files before generation
    backup_dir = preserve_custom_files()
    
    # Ensure frontend directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")
    
    # Look for the generated frontend directory structure
    # The generator creates: temp_dir/kinde_sdk/frontend/
    generated_kinde_sdk = os.path.join(temp_dir, "kinde_sdk")
    generated_frontend = os.path.join(generated_kinde_sdk, "frontend")
    
    if os.path.exists(generated_frontend):
        print(f"Copying files from {generated_frontend} to {OUTPUT_DIR}")
        
        # Copy all files and directories from generated frontend to our frontend directory
        for item in os.listdir(generated_frontend):
            source = os.path.join(generated_frontend, item)
            destination = os.path.join(OUTPUT_DIR, item)
            
            if os.path.isfile(source):
                shutil.copy2(source, destination)
                print(f"Copied file: {item}")
            elif os.path.isdir(source):
                if os.path.exists(destination):
                    shutil.rmtree(destination)
                shutil.copytree(source, destination)
                print(f"Copied directory: {item}")
        
        # Restore custom files after generation
        restore_custom_files(backup_dir)
        
        # Fix imports in the frontend directory
        fix_imports(OUTPUT_DIR)

        # Replace the OpenAPI-emitted literal __version__ with an import from
        # kinde_sdk._version, so the sub-package never drifts from the SDK.
        make_version_dynamic(os.path.join(OUTPUT_DIR, "__init__.py"))

        # Preserve custom imports
        preserve_custom_imports()
        
        print("Generation completed successfully!")
    else:
        print(f"Warning: Generated frontend directory not found at {generated_frontend}")
        print(f"Available directories in {temp_dir}: {os.listdir(temp_dir)}")
        if os.path.exists(generated_kinde_sdk):
            print(f"Available directories in {generated_kinde_sdk}: {os.listdir(generated_kinde_sdk)}")
        sys.exit(1)

print(f"OpenAPI Python SDK files copied to {OUTPUT_DIR}")
