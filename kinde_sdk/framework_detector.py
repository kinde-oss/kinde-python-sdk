# framework_detector.py
import importlib.metadata
import importlib
from typing import Optional

class FrameworkDetector:
    def __init__(self):
        self.framework = None

    def detect_framework(self, modules_to_check: list) -> Optional[str]:
        """
        Detect the framework being used by checking installed modules.

        Args:
            modules_to_check (list): List of framework module names to check (e.g., ["flask", "fastapi", "django"]).

        Returns:
            Optional[str]: The name of the detected framework, or None if no framework is found.
        """
        # Get a set of installed packages
        installed_packages = {dist.metadata["Name"].lower() for dist in importlib.metadata.distributions()}

        for module_name in modules_to_check:
            if module_name.lower() in installed_packages:
                try:
                    module = importlib.import_module(module_name)
                    print(f"Detected framework: {module_name}")
                    self.framework = module_name
                    return module_name
                except ImportError:
                    print(f"Failed to load {module_name}")
            else:
                print(f"{module_name} is not installed.")
        return None

    def get_framework(self) -> Optional[str]:
        """
        Get the detected framework.

        Returns:
            Optional[str]: The name of the detected framework, or None if no framework is found.
        """
        return self.framework