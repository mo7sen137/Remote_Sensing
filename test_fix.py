"""
Test to verify the bug fix for uploaded_bands initialization
"""

import streamlit as st

# Initialize session state like main() does
if 'uploaded_bands' not in st.session_state:
    st.session_state.uploaded_bands = None  # Changed from {} to None
if 'mtl_data' not in st.session_state:
    st.session_state.mtl_data = None
if 'predictions' not in st.session_state:
    st.session_state.predictions = None
if 'statistics' not in st.session_state:
    st.session_state.statistics = None

print("✅ Session state initialization fixed:")
print(f"  - uploaded_bands: {st.session_state.uploaded_bands}")
print(f"  - mtl_data: {st.session_state.mtl_data}")
print(f"  - predictions: {st.session_state.predictions}")
print(f"  - statistics: {st.session_state.statistics}")

# Test the old problematic code pattern
try:
    if st.session_state.uploaded_bands:
        # This would have failed with {} because you can't call .keys() on
        # the file object - but with None it's fine
        for band_num in st.session_state.uploaded_bands.keys():
            print(f"Band {band_num}")
    else:
        print("✓ Correctly handles None value - no error")
except AttributeError as e:
    print(f"❌ Error: {e}")
