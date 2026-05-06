"""
Diagnostic version of the Remote Sensing app to find the blue page issue
"""
import streamlit as st
import sys

st.set_page_config(page_title="Debug", layout="wide")

st.markdown("## 🔍 Remote Sensing App Diagnostic")

# Check 1: Can we import the config?
try:
    import config
    st.success("✅ Config module imported successfully")
    st.write(f"KM_CONVERSION: {config.KM_CONVERSION}")
except Exception as e:
    st.error(f"❌ Error importing config: {e}")

# Check 2: Can we import app components?
try:
    from app import main
    st.success("✅ App main module imported successfully")
except Exception as e:
    st.error(f"❌ Error importing app.main: {e}")
    st.write(str(e))

# Check 3: Try to run the setup_page_config
try:
    st.markdown("---")
    st.write("Attempting to set up the main app...")
    
    # Import the functions
    sys.path.insert(0, '/workspaces/Remote_Sensing')
    from app.main import setup_page_config, page_home
    
    st.write("✅ Successfully imported setup_page_config and page_home")
    
    # Try to render a simple version of the app
    st.markdown("### Attempting to render app...")
    st.radio("Select Page", ["🏠 Home"], label_visibility="collapsed")
    
    st.markdown("### Rendering Home Page...")
    page_home()
    
except Exception as e:
    st.error(f"❌ Error: {e}")
    import traceback
    st.write(traceback.format_exc())

st.markdown("---")
st.write("If you see this message, the app is at least partially working!")
