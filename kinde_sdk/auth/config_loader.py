# config_loader.py
import yaml
import json
from typing import Dict, Any

def load_config(file_path: str) -> Dict[str, Any]:
    """
    Load configuration from a YAML or JSON file.

    Args:
        file_path (str): Path to the configuration file.

    Returns:
        Dict[str, Any]: Configuration dictionary.
    """
    with open(file_path, "r") as file:
        if file_path.endswith(".yaml") or file_path.endswith(".yml"):
            return yaml.safe_load(file)
        elif file_path.endswith(".json"):
            return json.load(file)
        else:
            raise ValueError("Unsupported file format. Use YAML or JSON.")