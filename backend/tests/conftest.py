"""
Test configuration for Open HAMS backend tests.

This file sets up the Python path so tests can import
backend modules correctly.
"""

import sys
import os

# Add the parent directory (backend) to Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir) 