#!/usr/bin/env python3
"""
Simple launcher script for SkillLink application
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from skilllink_app import main

    if __name__ == "__main__":
        print("Starting SkillLink Application...")
        print("=" * 50)
        print("Make sure PostgreSQL is running and configured!")
        print("=" * 50)
        main()

except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("\nPlease install required dependencies:")
    print("  pip install -r requirements.txt")
    sys.exit(1)

except Exception as e:
    print(f"Error starting application: {e}")
    sys.exit(1)
