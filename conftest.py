# Root conftest.py
# This file ensures that pytest only collects tests from our tests directory
# and ignores any tests in temporary directories or installed packages

import os
import sys

# Add the 'src' directory to the path so imports work correctly
# This ensures that the in-development code is used, not the installed version
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

def pytest_ignore_collect(collection_path, config):
    """
    Configure pytest to ignore certain paths when collecting tests.
    
    Returns:
        bool: True if the path should be ignored, False otherwise.
    """
    # Skip the temp directory
    if "temp/" in str(collection_path):
        return True
    
    return False