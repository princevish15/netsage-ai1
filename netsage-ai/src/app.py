"""
NetSage AI: Automated Network Diagnostic Platform
Mirror entry point in src/
"""
import os
import sys
from pathlib import Path

# Ensure root directory is in sys.path
root_dir = Path(__file__).parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Execute main app
from app import *
