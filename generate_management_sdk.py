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
                    content = content.replace('from kinde_sdk import schemas', 'from kinde_sdk.management import schemas')
                    content = content.replace('from kinde_sdk import', 'from kinde_sdk.management import')
                    content = content.replace('import kinde_sdk.schemas', 'import kinde_sdk.management.schemas')
                    content = content.replace('kinde_sdk.schemas', 'kinde_sdk.management.schemas')
                    
                    # Only write if content changed
                    if content != original_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"Fixed imports in: {filepath}")
                except Exception as e:
                    print(f"Warning: Could not fix imports in {filepath}: {e}")

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
        
        # Fix imports in the management directory
        fix_imports(OUTPUT_DIR)
        
        # Also fix imports in the main kinde_sdk directory if it exists
        main_kinde_sdk = "kinde_sdk"
        if os.path.exists(main_kinde_sdk):
            print("Fixing imports in main kinde_sdk directory...")
            fix_imports(main_kinde_sdk)
    else:
        print(f"Warning: Generated management directory not found at {generated_management}")
        print(f"Available directories in {temp_dir}: {os.listdir(temp_dir)}")
        if os.path.exists(generated_kinde_sdk):
            print(f"Available directories in {generated_kinde_sdk}: {os.listdir(generated_kinde_sdk)}")

print(f"OpenAPI Python SDK files copied to {OUTPUT_DIR}") 