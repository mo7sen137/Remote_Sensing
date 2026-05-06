import streamlit as st
print(f"Streamlit version: {st.__version__}")
print("Importing main app...")
try:
    from app import main
    print("✅ Successfully imported app.main")
except Exception as e:
    print(f"❌ Error importing app.main: {e}")
    import traceback
    traceback.print_exc()
