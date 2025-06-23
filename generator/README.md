# Kinde Python SDK v1 Generator

This directory contains the necessary files to regenerate the Kinde Python SDK for v1.

## Prequisites

You must have `openapi-generator-cli` installed. If you do not have it, please see the installation instructions: [https://openapi-generator.tech/docs/installation](https://openapi-generator.tech/docs/installation)

A simple way to install it on macOS is with Homebrew:
```bash
brew install openapi-generator
```

## How to Generate

1.  Navigate to this directory (`kinde-python-sdk-v1/generator`).
2.  Make the `generate.sh` script executable:
    ```bash
    chmod +x generate.sh
    ```
3.  Run the script:
    ```bash
    ./generate.sh
    ```

The script will regenerate the SDK in the `kinde-python-sdk-v1` directory, overwriting the existing files. This will update the API client, models, and other generated code to be compatible with the version of `openapi-generator-cli` you are using, which should resolve the Python 3.13 compatibility issues. 