
#!/usr/bin/env python3
"""
Migration runner script to properly execute the clean migration.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db.clean_migration import clean_migration

if __name__ == "__main__":
    clean_migration()
