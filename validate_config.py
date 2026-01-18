#!/usr/bin/env python3
"""
Helper script to validate the .env configuration file.
"""

import os
from dotenv import load_dotenv


def validate_config():
    """Validate that all required configuration is set."""
    load_dotenv()
    
    print("=" * 60)
    print("Amazon Kids Plus Content Deactivator - Configuration Check")
    print("=" * 60)
    print()
    
    # Required fields
    required = {
        'AMAZON_EMAIL': os.getenv('AMAZON_EMAIL'),
        'AMAZON_PASSWORD': os.getenv('AMAZON_PASSWORD'),
    }
    
    # Optional fields
    optional = {
        'PAGE_LOAD_TIMEOUT': os.getenv('PAGE_LOAD_TIMEOUT', '30'),
        'ELEMENT_WAIT_TIMEOUT': os.getenv('ELEMENT_WAIT_TIMEOUT', '10'),
        'HEADLESS': os.getenv('HEADLESS', 'false'),
    }
    
    # Check required fields
    print("Required Configuration:")
    print("-" * 60)
    all_valid = True
    for key, value in required.items():
        if value:
            masked_value = value[:3] + '*' * (len(value) - 3) if len(value) > 3 else '***'
            print(f"✓ {key:25} = {masked_value}")
        else:
            print(f"✗ {key:25} = NOT SET")
            all_valid = False
    
    print()
    print("Optional Configuration:")
    print("-" * 60)
    for key, value in optional.items():
        print(f"  {key:25} = {value}")
    
    print()
    print("=" * 60)
    
    if all_valid:
        print("✓ Configuration is valid! You can run the script.")
        return 0
    else:
        print("✗ Configuration is incomplete. Please set all required fields in .env")
        print()
        print("To fix:")
        print("1. Copy .env.example to .env: cp .env.example .env")
        print("2. Edit .env and add your Amazon credentials")
        return 1


if __name__ == "__main__":
    exit(validate_config())
