#!/bin/bash
# Quick launcher for Streamlit App

echo "🛰️ Starting Remote Sensing Land Classification App..."
echo ""
echo "⏳ Please wait while Streamlit loads..."
echo ""

cd /workspaces/Remote_Sensing

# Check if Streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found. Installing..."
    pip install streamlit numpy pandas scikit-learn
fi

echo ""
echo "✅ Starting Streamlit server on port 8501..."
echo ""
echo "📍 Local URL: http://localhost:8501"
echo "📍 Network URL: http://10.0.5.212:8501"
echo ""
echo "Click on one of the URLs above or press Ctrl+Click to open in browser"
echo ""

streamlit run app/main.py
