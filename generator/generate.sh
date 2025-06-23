#!/bin/bash

# This script regenerates the Kinde Python SDK v1.
# It uses openapi-generator-cli to generate the SDK based on the Kinde Management API specification.

# Ensure openapi-generator-cli is installed.
if ! command -v openapi-generator-cli &> /dev/null
then
    echo "openapi-generator-cli could not be found. Please install it."
    echo "See: https://openapi-generator.tech/docs/installation"
    exit
fi

# Move to the script's directory to ensure paths are correct.
cd "$(dirname "$0")"

echo "Generating Kinde Python SDK v1..."

# The output directory is set to '..' which is the root of kinde-python-sdk-v1.
# This will overwrite the existing SDK with the newly generated one.
_JAVA_OPTIONS="--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED" \
openapi-generator-cli generate \
    -g python \
    -i https://kinde.com/api/kinde-mgmt-api-specs.yaml \
    --additional-properties=packageName=kinde_sdk \
    -c config.yaml \
    -o ../ \
    --skip-validate-spec

echo "SDK generation complete." 