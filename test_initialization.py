#!/usr/bin/env python3
"""
Test if the Remote Sensing app can initialize without errors
"""
import sys
import os

# Add the workspace to path
sys.path.insert(0, '/workspaces/Remote_Sensing')

print("=" * 60)
print("Remote Sensing App - Initialization Test")
print("=" * 60)

# Step 1: Check imports
print("\n1. Checking imports...")
try:
    import streamlit as st
    print(f"   ✅ Streamlit {st.__version__}")
except ImportError as e:
    print(f"   ❌ Streamlit: {e}")
    sys.exit(1)

try:
    import numpy
    print("   ✅ NumPy")
except ImportError as e:
    print(f"   ❌ NumPy: {e}")

try:
    import pandas
    print("   ✅ Pandas")
except ImportError as e:
    print(f"   ❌ Pandas: {e}")

# Step 2: Check config
print("\n2. Checking config module...")
try:
    import config
    print(f"   ✅ Config module loaded")
    print(f"   - KM_CONVERSION: {config.KM_CONVERSION}")
    print(f"   - COLOR_PALETTE: {config.COLOR_PALETTE}")
except Exception as e:
    print(f"   ❌ Error loading config: {e}")
    import traceback
    traceback.print_exc()

# Step 3: Check app initialization
print("\n3. Checking app initialization...")
try:
    from app.main import setup_page_config, page_home, page_upload
    print("   ✅ Successfully imported app functions")
    
    # Check if we can call setup_page_config without errors
    # (We can't actually run st functions outside of Streamlit, but we can check if they're callable)
    print(f"   - setup_page_config is callable: {callable(setup_page_config)}")
    print(f"   - page_home is callable: {callable(page_home)}")
    
except Exception as e:
    print(f"   ❌ Error importing app functions: {e}")
    import traceback
    traceback.print_exc()

print("\n4. Attempting to parse and execute main() setup...")
try:
    from app.main import main
    print("   ✅ Successfully imported main function")
    print(f"   - main is callable: {callable(main)}")
except Exception as e:
    print(f"   ❌ Error importing main: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("All checks completed!")
print("=" * 60)
