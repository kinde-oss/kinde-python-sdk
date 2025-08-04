import os
import subprocess
import sys
import shutil
import tempfile

# OpenAPI spec URL from Kinde
OPENAPI_SPEC_URL = "https://kinde.com/api/kinde-mgmt-api-specs.yaml"
OUTPUT_DIR = "kinde_sdk/management"
GENERATOR_DIR = "generator"
CONFIG_FILE = f"{GENERATOR_DIR}/config.yaml"

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
                    
                    # Fix imports for the management package structure
                    original_content = content
                    
                    # Fix all kinde_sdk imports to use management module
                    content = content.replace('from kinde_sdk import schemas', 'from kinde_sdk.management import schemas')
                    content = content.replace('from kinde_sdk import api_client', 'from kinde_sdk.management import api_client')
                    content = content.replace('from kinde_sdk import exceptions', 'from kinde_sdk.management import exceptions')
                    content = content.replace('from kinde_sdk import configuration', 'from kinde_sdk.management import configuration')
                    content = content.replace('from kinde_sdk import rest', 'from kinde_sdk.management import rest')
                    
                    # Fix combined imports
                    content = content.replace('from kinde_sdk import api_client, exceptions', 'from kinde_sdk.management import api_client, exceptions')
                    content = content.replace('from kinde_sdk import exceptions, api_client', 'from kinde_sdk.management import exceptions, api_client')
                    
                    # Fix import statements
                    content = content.replace('from kinde_sdk import', 'from kinde_sdk.management import')
                    content = content.replace('import kinde_sdk.schemas', 'import kinde_sdk.management.schemas')
                    content = content.replace('kinde_sdk.schemas', 'kinde_sdk.management.schemas')
                    
                    # Fix any remaining references to root kinde_sdk modules
                    content = content.replace('kinde_sdk.api_client', 'kinde_sdk.management.api_client')
                    content = content.replace('kinde_sdk.exceptions', 'kinde_sdk.management.exceptions')
                    content = content.replace('kinde_sdk.configuration', 'kinde_sdk.management.configuration')
                    content = content.replace('kinde_sdk.rest', 'kinde_sdk.management.rest')
                    
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
        "# Custom imports for Kinde Management Client",
        "from .management_client import ManagementClient",
        "from .management_token_manager import ManagementTokenManager",
        "",
        "# Re-export for convenience",
        "__all__ = ['ManagementClient', 'ManagementTokenManager']",
        ""
    ]
    
    try:
        with open(init_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if custom imports are already present
        if "from .management_client import ManagementClient" in content:
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
        "kinde_sdk/api_client.py",
        "kinde_sdk/configuration.py", 
        "kinde_sdk/exceptions.py",
        "kinde_sdk/rest.py",
        "kinde_sdk/schemas.py"
    ]
    
    for file_path in old_files_to_remove:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Removed old file: {file_path}")
            except Exception as e:
                print(f"Warning: Could not remove {file_path}: {e}")
    
    # Remove old generated directories that might conflict
    old_dirs_to_remove = [
        "kinde_sdk/paths",
        "kinde_sdk/model",
        "kinde_sdk/apis"
    ]
    
    for dir_path in old_dirs_to_remove:
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                print(f"Removed old directory: {dir_path}")
            except Exception as e:
                print(f"Warning: Could not remove {dir_path}: {e}")

def preserve_custom_files():
    """Preserve custom files that should not be overwritten during generation."""
    print("Preserving custom files...")
    
    # Files to preserve (backup and restore after generation)
    custom_files = [
        "management_client.py",
        "management_token_manager.py", 
        "README.md",
        "kinde_api_client.py"
    ]
    
    # Create backup directory
    backup_dir = os.path.join(OUTPUT_DIR, "backup")
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Backup custom files
    for file_name in custom_files:
        source = os.path.join(OUTPUT_DIR, file_name)
        backup = os.path.join(backup_dir, file_name)
        if os.path.exists(source):
            shutil.copy2(source, backup)
            print(f"Backed up: {file_name}")
    
    # Also preserve Kinde-specific exceptions in exceptions.py
    exceptions_file = os.path.join(OUTPUT_DIR, "exceptions.py")
    if os.path.exists(exceptions_file):
        with open(exceptions_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract Kinde-specific exceptions
        kinde_exceptions = []
        lines = content.split('\n')
        in_kinde_exceptions = False
        for line in lines:
            if line.strip() == "# Kinde-specific exceptions":
                in_kinde_exceptions = True
                kinde_exceptions.append(line)
            elif in_kinde_exceptions and line.strip().startswith('class ') and 'Exception' in line:
                kinde_exceptions.append(line)
            elif in_kinde_exceptions and line.strip() == "pass":
                kinde_exceptions.append(line)
            elif in_kinde_exceptions and line.strip() == "" and kinde_exceptions:
                # Stop when we hit an empty line after finding exceptions
                break
        
        if kinde_exceptions:
            kinde_exceptions_text = "\n".join(kinde_exceptions)
            with open(os.path.join(backup_dir, "kinde_exceptions.txt"), 'w', encoding='utf-8') as f:
                f.write(kinde_exceptions_text)
            print("Backed up: Kinde-specific exceptions")
    
    return backup_dir

def restore_custom_files(backup_dir):
    """Restore custom files after generation."""
    print("Restoring custom files...")
    
    custom_files = [
        "management_client.py",
        "management_token_manager.py",
        "README.md",
        "kinde_api_client.py"
    ]
    
    # Restore custom files
    for file_name in custom_files:
        backup = os.path.join(backup_dir, file_name)
        destination = os.path.join(OUTPUT_DIR, file_name)
        if os.path.exists(backup):
            shutil.copy2(backup, destination)
            print(f"Restored: {file_name}")
    
    # Restore Kinde-specific exceptions
    kinde_exceptions_backup = os.path.join(backup_dir, "kinde_exceptions.txt")
    if os.path.exists(kinde_exceptions_backup):
        with open(kinde_exceptions_backup, 'r', encoding='utf-8') as f:
            kinde_exceptions_text = f.read()
        
        exceptions_file = os.path.join(OUTPUT_DIR, "exceptions.py")
        if os.path.exists(exceptions_file):
            with open(exceptions_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if Kinde-specific exceptions are already present
            if "# Kinde-specific exceptions" not in content:
                # Add Kinde-specific exceptions at the end
                kinde_exceptions_section = f"""

{kinde_exceptions_text}"""
                
                content += kinde_exceptions_section
                with open(exceptions_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print("Restored: Kinde-specific exceptions")
            else:
                print("Kinde-specific exceptions already present in exceptions.py")
    
    # Clean up backup directory
    if os.path.exists(backup_dir):
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

# Create config.yaml if it doesn't exist
if not os.path.isfile(CONFIG_FILE):
    config_content = """# openapi-generator-cli config for python

packageName: kinde_sdk.management
projectName: kinde-python-sdk
packageVersion: 2.0.0
# It is recommended to use a released version of the generator.
# For example:
# generatorVersion: "7.13.0"
"""
    with open(CONFIG_FILE, 'w') as f:
        f.write(config_content)
    print(f"Created config file: {CONFIG_FILE}")

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
    
    # Ensure management directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")
    
    # Look for the generated management directory structure
    # The generator creates: temp_dir/kinde_sdk/management/
    generated_kinde_sdk = os.path.join(temp_dir, "kinde_sdk")
    generated_management = os.path.join(generated_kinde_sdk, "management")
    
    if os.path.exists(generated_management):
        print(f"Copying files from {generated_management} to {OUTPUT_DIR}")
        
        # Copy all files and directories from generated management to our management directory
        for item in os.listdir(generated_management):
            source = os.path.join(generated_management, item)
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
        
        # Fix imports in the management directory
        fix_imports(OUTPUT_DIR)
        
        # Preserve custom imports
        preserve_custom_imports()
        
        print("Generation completed successfully!")
    else:
        print(f"Warning: Generated management directory not found at {generated_management}")
        print(f"Available directories in {temp_dir}: {os.listdir(temp_dir)}")
        if os.path.exists(generated_kinde_sdk):
            print(f"Available directories in {generated_kinde_sdk}: {os.listdir(generated_kinde_sdk)}")
        sys.exit(1)

print(f"OpenAPI Python SDK files copied to {OUTPUT_DIR}") 