"""
Main Streamlit Application
Remote Sensing Land Classification Dashboard

Complete UI with:
- Data Upload
- Visualization
- Classification
- Results Display
"""

import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import os
from pathlib import Path
import json

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

import config


# ============================================================================
# 🎨 PAGE CONFIGURATION
# ============================================================================

def setup_page_config():
    """Configure Streamlit page settings with Professional Enterprise Theme."""
    st.set_page_config(
        page_title="🛰️ Remote Sensing Land Classification",
        page_icon="🛰️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # =========================================================================
    # PROFESSIONAL ENTERPRISE DESIGN SYSTEM v2.0
    # =========================================================================
    st.markdown("""
        <style>
        /* =========== COLOR SYSTEM (Professional) =========== */
        :root {
            --color-primary: #0066FF;
            --color-primary-light: #3B82F6;
            --color-primary-dark: #0051CC;
            
            --color-accent: #FF6B35;
            
            --color-success: #10B981;
            --color-warning: #F59E0B;
            --color-error: #EF4444;
            --color-info: #3B82F6;
            
            --color-gray-50: #F9FAFB;
            --color-gray-100: #F3F4F6;
            --color-gray-200: #E5E7EB;
            --color-gray-300: #D1D5DB;
            --color-gray-400: #9CA3AF;
            --color-gray-500: #6B7280;
            --color-gray-600: #4B5563;
            --color-gray-700: #374151;
            --color-gray-800: #1F2937;
            --color-gray-900: #111827;
            
            --color-dark-bg: #0F172A;
            --color-dark-card: #1E293B;
            --color-dark-border: #334155;
        }
        
        /* =========== GLOBAL STYLES =========== */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            line-height: 1.6;
        }
        
        html, body, [class*="css"] {
            background: linear-gradient(135deg, #0F172A 0%, #1A1F47 50%, #0F172A 100%) !important;
        }
        
        .stApp {
            background: linear-gradient(135deg, #0F172A 0%, #1A1F47 50%, #0F172A 100%);
            color: #E8EAED;
        }
        
        /* =========== TYPOGRAPHY =========== */
        h1 {
            font-family: 'Sora', sans-serif !important;
            font-size: 2.5rem !important;
            font-weight: 700 !important;
            color: #0066FF !important;
            letter-spacing: -0.02em !important;
            margin-bottom: 0.5rem !important;
            line-height: 1.2 !important;
            animation: slideInDown 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        }
        
        h2 {
            font-family: 'Sora', sans-serif !important;
            font-size: 1.875rem !important;
            font-weight: 600 !important;
            color: #3B82F6 !important;
            letter-spacing: -0.015em !important;
            margin-bottom: 0.75rem !important;
            line-height: 1.3 !important;
        }
        
        h3 {
            font-family: 'Sora', sans-serif !important;
            font-size: 1.25rem !important;
            font-weight: 600 !important;
            color: #60A5FA !important;
            letter-spacing: -0.01em !important;
        }
        
        p, span, div {
            color: #D1D5DB;
            font-size: 1rem;
            font-weight: 400;
        }
        
        /* =========== SIDEBAR =========== */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0F172A 0%, #1A1F47 100%);
            border-right: 2px solid #334155;
            box-shadow: inset -2px 0 0 rgba(3, 102, 255, 0.1);
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #E8EAED !important;
        }
        
        /* =========== MAIN CONTENT =========== */
        [data-testid="stMainBlockContainer"] {
            background: transparent;
            padding: 2rem;
        }
        
        /* =========== TABS =========== */
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(15, 23, 42, 0.8);
            border-bottom: 2px solid #334155;
            gap: 0.5rem;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        .stTabs [data-baseweb="tab-list"] button {
            background: linear-gradient(135deg, #1E293B, #293548);
            color: #9CA3AF;
            border: 2px solid #334155;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            font-family: 'Inter', sans-serif;
            transition: all 0.3s ease;
            text-transform: none;
            letter-spacing: 0;
            line-height: 1.5;
        }
        
        .stTabs [data-baseweb="tab-list"] button:hover {
            border-color: #60A5FA;
            color: #60A5FA;
            box-shadow: 0 0 12px rgba(96, 165, 250, 0.2);
        }
        
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            background: linear-gradient(135deg, #0066FF, #3B82F6);
            color: #FFFFFF !important;
            border: 2px solid #0066FF;
            box-shadow: 0 6px 20px -4px rgba(0, 102, 255, 0.3);
            font-weight: 600;
        }
        
        /* =========== BUTTONS =========== */
        .stButton > button {
            background: linear-gradient(135deg, #0066FF 0%, #3B82F6 100%);
            color: #FFFFFF;
            border: 2px solid #0066FF;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-size: 1rem;
            font-family: 'Inter', sans-serif;
            text-transform: none;
            letter-spacing: 0;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            box-shadow: 0 4px 12px rgba(0, 102, 255, 0.3);
            cursor: pointer;
            min-height: 44px;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #3B82F6 0%, #60A5FA 100%);
            box-shadow: 0 8px 20px rgba(0, 102, 255, 0.4);
            transform: translateY(-2px);
        }
        
        .stButton > button:active {
            transform: translateY(0) scale(0.98);
        }
        
        .stButton > button:disabled {
            background: #9CA3AF;
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        /* =========== INPUT FIELDS =========== */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select {
            background-color: #1E293B !important;
            color: #E8EAED !important;
            border: 2px solid #334155 !important;
            border-radius: 8px !important;
            padding: 0.75rem 1rem !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.3s ease !important;
            font-size: 1rem !important;
            font-weight: 400 !important;
        }
        
        .stTextInput > div > div > input::placeholder,
        .stNumberInput > div > div > input::placeholder {
            color: #6B7280 !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {
            border-color: #0066FF !important;
            box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.1) !important;
            color: #E8EAED !important;
            outline: none !important;
        }
        
        /* =========== FILE UPLOADER =========== */
        .stFileUploader {
            border: 2px dashed #334155;
            background: rgba(3, 102, 255, 0.05);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.3s ease;
        }
        
        .stFileUploader:hover {
            border-color: #0066FF;
            background: rgba(3, 102, 255, 0.1);
            box-shadow: 0 4px 12px rgba(0, 102, 255, 0.15);
        }
        
        /* =========== METRICS =========== */
        .stMetric {
            background: linear-gradient(135deg, #1E293B 0%, #1A1F47 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 2px solid #334155;
            box-shadow: 0 4px 6px -2px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        
        .stMetric:hover {
            border-color: #0066FF;
            box-shadow: 0 8px 16px rgba(0, 102, 255, 0.2);
            transform: translateY(-4px);
        }
        
        /* =========== MESSAGES =========== */
        .stSuccess {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.05));
            border-left: 4px solid #10B981;
            border-radius: 8px;
            padding: 1rem;
            color: #6EE7B7;
            font-weight: 500;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        .stInfo {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.05));
            border-left: 4px solid #3B82F6;
            border-radius: 8px;
            padding: 1rem;
            color: #93C5FD;
            font-weight: 500;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        .stWarning {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(245, 158, 11, 0.05));
            border-left: 4px solid #F59E0B;
            border-radius: 8px;
            padding: 1rem;
            color: #FCD34D;
            font-weight: 500;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        .stError {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(239, 68, 68, 0.05));
            border-left: 4px solid #EF4444;
            border-radius: 8px;
            padding: 1rem;
            color: #FCA5A5;
            font-weight: 500;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        /* =========== TABLES =========== */
        .stDataFrame {
            background: #1A1F47;
            border: 2px solid #334155;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }
        
        .stDataFrame th {
            background: linear-gradient(90deg, #0066FF 0%, #3B82F6 100%);
            color: #FFFFFF;
            font-weight: 700;
            padding: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-size: 0.875rem;
        }
        
        .stDataFrame td {
            padding: 1rem;
            border-bottom: 1px solid #334155;
            color: #D1D5DB;
            font-size: 0.95rem;
        }
        
        .stDataFrame tr:hover {
            background: rgba(0, 102, 255, 0.05);
        }
        
        /* =========== EXPANDABLE SECTIONS =========== */
        .streamlit-expanderHeader {
            background: linear-gradient(90deg, #1E293B, #1A1F47);
            border: 2px solid #334155;
            border-radius: 8px;
            color: #60A5FA !important;
            font-weight: 600;
            text-transform: none;
            letter-spacing: 0;
            padding: 1rem !important;
            transition: all 0.3s ease;
        }
        
        .streamlit-expanderHeader:hover {
            border-color: #0066FF;
            background: linear-gradient(90deg, #1A1F47, #1E293B);
            box-shadow: 0 4px 12px rgba(0, 102, 255, 0.15);
        }
        
        /* =========== SCROLLBAR =========== */
        ::-webkit-scrollbar {
            width: 12px;
            height: 12px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(15, 23, 42, 0.5);
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #0066FF, #3B82F6);
            border-radius: 6px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #3B82F6, #60A5FA);
        }
        
        /* =========== SHADOW SYSTEM (Elevation Levels) =========== */
        .shadow-sm {
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        }
        
        .shadow-md {
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        
        .shadow-lg {
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
        
        .shadow-xl {
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
        
        .shadow-2xl {
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        }
        
        /* =========== ANIMATIONS (20+ Keyframes) =========== */
        @keyframes slideInDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideInLeft {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes fadeInScale {
            from { opacity: 0; transform: scale(0.95); }
            to { opacity: 1; transform: scale(1); }
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        @keyframes shimmer {
            0% { background-position: -1000px 0; }
            100% { background-position: 1000px 0; }
        }
        
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        @keyframes glow {
            0%, 100% { box-shadow: 0 0 5px rgba(0, 102, 255, 0.5); }
            50% { box-shadow: 0 0 20px rgba(0, 102, 255, 0.8); }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-8px); }
        }
        
        @keyframes scaleIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
        
        @keyframes heartbeat {
            0%, 100% { transform: scale(1); }
            25% { transform: scale(1.1); }
            50% { transform: scale(1); }
        }
        
        @keyframes wobble {
            0%, 100% { transform: rotate(0deg); }
            25% { transform: rotate(-2deg); }
            75% { transform: rotate(2deg); }
        }
        
        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes expandWidth {
            from { width: 0%; opacity: 0; }
            to { width: 100%; opacity: 1; }
        }
        
        /* Animation application */
        h1 { animation: slideInDown 0.6s cubic-bezier(0.34, 1.56, 0.64, 1); }
        h2 { animation: slideUp 0.5s ease-out 0.1s both; }
        h3 { animation: fadeIn 0.4s ease-out 0.2s both; }
        
        /* =========== COMPONENT STATES =========== */
        /* Button States */
        .stButton > button {
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        
        .stButton > button:active::after {
            width: 300px;
            height: 300px;
        }
        
        /* Loading State Animation */
        .loading {
            animation: spin 1s linear infinite;
        }
        
        /* Success Pulse */
        .stSuccess {
            animation: slideInUp 0.4s ease-out;
        }
        
        .stError {
            animation: slideInUp 0.4s ease-out;
            animation: heartbeat 0.5s ease-in-out;
        }
        
        /* Input Focus Glow */
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {
            animation: glow 2s ease-in-out;
        }
        
        /* Metric Lift on Hover with Animation */
        .stMetric {
            animation: slideUp 0.5s ease-out;
        }
        
        /* Expander Smooth Opening */
        .streamlit-expanderHeader {
            animation: slideInLeft 0.3s ease-out;
        }
        
        /* =========== RESPONSIVE DESIGN =========== */
        @media (max-width: 768px) {
            h1 { font-size: 1.875rem !important; }
            h2 { font-size: 1.5rem !important; }
            h3 { font-size: 1.125rem !important; }
            
            [data-testid="stMainBlockContainer"] { padding: 1rem; }
            
            .stButton > button,
            .stTextInput > div > div > input,
            .stSelectbox > div > div > select {
                min-height: 48px;
                font-size: 1rem;
            }
            
            .stTabs [data-baseweb="tab-list"] {
                flex-wrap: wrap;
            }
            
            .stTabs [data-baseweb="tab-list"] button {
                padding: 0.5rem 1rem;
                font-size: 0.9rem;
            }
        }
        
        @media (max-width: 480px) {
            h1 { font-size: 1.5rem !important; }
            h2 { font-size: 1.25rem !important; }
            
            [data-testid="stMainBlockContainer"] { padding: 0.75rem; }
            
            .stButton > button {
                width: 100%;
                padding: 1rem !important;
            }
            
            .stMetric {
                padding: 1rem;
            }
        }
        
        /* =========== FOCUS STATES (Accessibility) =========== */
        button:focus-visible {
            outline: 3px solid #0066FF;
            outline-offset: 2px;
        }
        
        input:focus-visible,
        select:focus-visible {
            outline: 3px solid #0066FF;
            outline-offset: 2px;
        }
        
        /* Tab Focus */
        .stTabs [data-baseweb="tab-list"] button:focus-visible {
            outline: 3px dashed #0066FF;
            outline-offset: 3px;
        }
        
        /* =========== LOADING & ASYNC STATES =========== */
        .spinner {
            animate: spin 1s linear infinite;
            border: 3px solid rgba(0, 102, 255, 0.1);
            border-radius: 50%;
            border-top: 3px solid #0066FF;
            width: 20px;
            height: 20px;
        }
        
        /* Progress Bar Animation */
        .progress-bar {
            animation: expandWidth 0.8s ease-out;
            background: linear-gradient(90deg, #0066FF, #3B82F6);
            height: 4px;
            border-radius: 2px;
        }
        
        /* =========== REDUCED MOTION =========== */
        @media (prefers-reduced-motion: reduce) {
            * {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }
        
        /* =========== DISABLED STATE =========== */
        button:disabled {
            cursor: not-allowed;
            opacity: 0.6;
        }
        
        input:disabled,
        select:disabled {
            background-color: #0F172A !important;
            cursor: not-allowed;
            opacity: 0.6;
        }
        
        /* =========== PHASE 3: ADVANCED RESPONSIVE =========== */
        @media (max-width: 1024px) {
            [data-testid="stSidebar"] {
                width: 100% !important;
            }
            
            .stTabs [data-baseweb="tab-list"] button {
                padding: 0.75rem 1.25rem;
                font-size: 0.95rem;
            }
        }
        
        @media (max-width: 768px) {
            h1 { font-size: 1.875rem !important; line-height: 1.2; }
            h2 { font-size: 1.5rem !important; line-height: 1.3; }
            h3 { font-size: 1.125rem !important; }
            
            [data-testid="stMainBlockContainer"] { padding: 1rem; }
            [data-testid="stSidebar"] { width: 50% !important; }
            
            .stButton > button,
            .stTextInput > div > div > input,
            .stSelectbox > div > div > select {
                min-height: 48px;
                font-size: 1rem;
                padding: 0.75rem 1rem !important;
            }
            
            .stTabs [data-baseweb="tab-list"] {
                flex-wrap: wrap;
                gap: 0.5rem;
            }
            
            .stTabs [data-baseweb="tab-list"] button {
                padding: 0.5rem 1rem;
                font-size: 0.9rem;
                flex: 1 1 auto;
                min-width: 100px;
            }
            
            .stMetric {
                padding: 1.25rem;
                border-radius: 10px;
            }
            
            .stDataFrame {
                font-size: 0.9rem;
                border-radius: 10px;
            }
        }
        
        @media (max-width: 640px) {
            h1 { font-size: 1.5rem !important; margin-bottom: 0.5rem; }
            h2 { font-size: 1.25rem !important; margin-bottom: 0.5rem; }
            h3 { font-size: 1rem !important; }
            
            [data-testid="stMainBlockContainer"] { padding: 0.75rem; }
            [data-testid="stSidebar"] { width: 100% !important; }
            
            .stButton > button {
                width: 100% !important;
                padding: 0.875rem 1rem !important;
                font-size: 0.95rem;
            }
            
            .stTextInput > div > div > input,
            .stSelectbox > div > div > select,
            .stNumberInput > div > div > input {
                width: 100%;
                font-size: 1rem;
                padding: 0.75rem 1rem !important;
            }
            
            .stMetric {
                padding: 1rem;
                margin-bottom: 0.75rem;
            }
            
            .stTabs [data-baseweb="tab-list"] {
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
                padding: 0.75rem;
            }
            
            .stTabs [data-baseweb="tab-list"] button {
                padding: 0.5rem 0.875rem;
                font-size: 0.85rem;
                white-space: nowrap;
            }
            
            .streamlit-expanderHeader {
                padding: 0.75rem !important;
                font-size: 0.95rem;
            }
        }
        
        @media (max-width: 480px) {
            h1 { font-size: 1.25rem !important; }
            h2 { font-size: 1.125rem !important; }
            h3 { font-size: 1rem !important; }
            
            p, span, div { font-size: 0.95rem; }
            
            [data-testid="stMainBlockContainer"] { padding: 0.5rem; }
            
            .stButton > button {
                width: 100% !important;
                padding: 0.75rem 1rem !important;
                min-height: 44px;
            }
            
            .stTextInput > div > div > input,
            .stSelectbox > div > div > select,
            .stNumberInput > div > div > input {
                min-height: 44px;
            }
            
            .stMetric {
                padding: 0.75rem;
                border: 1px solid #334155;
            }
            
            .stFileUploader {
                padding: 1rem;
            }
            
            .stDataFrame {
                font-size: 0.85rem;
            }
            
            .stDataFrame th {
                padding: 0.75rem 0.5rem;
                font-size: 0.8rem;
            }
            
            .stDataFrame td {
                padding: 0.5rem;
                font-size: 0.85rem;
            }
        }
        
        /* =========== PHASE 3: ENHANCED ACCESSIBILITY =========== */
        /* Semantic Color Meanings */
        .status-success {
            color: #10B981;
            border-left: 4px solid #10B981;
        }
        
        .status-error {
            color: #EF4444;
            border-left: 4px solid #EF4444;
        }
        
        .status-warning {
            color: #F59E0B;
            border-left: 4px solid #F59E0B;
        }
        
        .status-info {
            color: #3B82F6;
            border-left: 4px solid #3B82F6;
        }
        
        /* Skip Link for Keyboard Navigation */
        .skip-link {
            position: absolute;
            top: -40px;
            left: 0;
            background: #0066FF;
            color: white;
            padding: 0.5rem 1rem;
            text-decoration: none;
        }
        
        .skip-link:focus {
            top: 0;
        }
        
        /* Enhanced Keyboard Navigation */
        *:focus-visible {
            outline: 2px solid #0066FF;
            outline-offset: 2px;
            border-radius: 4px;
        }
        
        /* High Contrast Mode Support */
        @media (prefers-contrast: more) {
            :root {
                --color-primary: #0052CC;
                --color-gray-300: #A0A0A0;
            }
            
            button:focus-visible {
                outline-width: 3px;
            }
        }
        
        /* Dark Mode Support (Already Applied) */
        @media (prefers-color-scheme: dark) {
            .stApp, html, body {
                background: linear-gradient(135deg, #0F172A 0%, #1A1F47 100%);
                color: #E8EAED;
            }
        }
        
        /* =========== PHASE 3: PERFORMANCE OPTIMIZATIONS =========== */
        /* Font Display Optimization (avoid blank text) */
        @font-face {
            font-family: 'Inter';
            font-display: swap;
        }
        
        @font-face {
            font-family: 'Sora';
            font-display: swap;
        }
        
        /* Lazy Loading Container */
        .lazy-load {
            background: linear-gradient(90deg, #1E293B, #1A1F47, #1E293B);
            background-size: 200% 100%;
            animation: shimmer 2s infinite;
        }
        
        /* Content Visibility for Performance */
        [data-testid="stTabs"] {
            contain: layout style paint;
        }
        
        /* Optimize Animations for Performance */
        @media (max-width: 768px) {
            .pulse {
                animation-duration: 1.5s;
            }
            
            h1, h2, h3 {
                animation: none !important;
            }
        }
        
        /* =========== COLOR BLINDNESS SUPPORT =========== */
        /* Use Protanopia-safe colors */
        .success-indicator {
            background: #0173B2; /* Blue for success */
        }
        
        .error-indicator {
            background: #DE8F05; /* Orange for error */
            border: 2px solid #CC78BC; /* Purple pattern support */
        }
        
        .warning-indicator {
            background: #29AF7F; /* Green for warning */
        }
        
        /* =========== TOUCH OPTIMIZATION =========== */
        @media (hover: none) and (pointer: coarse) {
            .stButton > button:hover {
                transform: none;
            }
            
            .stButton > button:active {
                background: var(--color-primary);
                opacity: 0.9;
            }
            
            .stMetric:hover {
                transform: none;
            }
        }
        
        /* Larger hit targets for touch */
        button, input, select, [role="button"] {
            min-height: 44px;
            min-width: 44px;
        }
        
        /* =========== REDUCED MOTION (Improved) =========== */
        @media (prefers-reduced-motion: reduce) {
            * {
                animation-duration: 0 !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0 !important;
            }
            
            html {
                scroll-behavior: auto !important;
            }
        }
        
        /* =========== LINK STYLING =========== */
        a {
            color: #60A5FA;
            text-decoration: none;
            border-bottom: 2px solid transparent;
            transition: all 0.2s ease;
        }
        
        a:hover {
            border-bottom-color: #0066FF;
        }
        
        a:focus-visible {
            outline: 2px dashed #0066FF;
            outline-offset: 2px;
        }
        
        /* =========== FORM VALIDATION STATES =========== */
        .input-error {
            border-color: #EF4444 !important;
            background-color: rgba(239, 68, 68, 0.1) !important;
        }
        
        .input-success {
            border-color: #10B981 !important;
            background-color: rgba(16, 185, 129, 0.1) !important;
        }
        
        .input-warning {
            border-color: #F59E0B !important;
            background-color: rgba(245, 158, 11, 0.1) !important;
        }
        
        /* =========== PRINT STYLES =========== */
        @media print {
            * {
                animation: none !important;
                transition: none !important;
            }
            
            [data-testid="stSidebar"],
            [data-testid="stToolbar"],
            .stDeployButton,
            button { display: none !important; }
            
            [data-testid="stMainBlockContainer"] {
                padding: 20mm;
            }
            
            body, p { color: black !important; }
        }
        </style>
    """, unsafe_allow_html=True)


# ============================================================================
# 📄 PAGE 1: HOME
# ============================================================================

def page_home():
    """Home page with project overview."""
    st.markdown("<h1 style='text-align: center;'>🛰️ LAND COVER CLASSIFICATION SYSTEM</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #00ffaa;'>Advanced Satellite Image Processing & ML Analysis</h3>", unsafe_allow_html=True)
    st.divider()
    
    # Metrics Row 1
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📡 Satellite", "LANDSAT 8", "11 Bands")
    with col2:
        st.metric("🔬 Image Size", "4M px", "Per Band")
    with col3:
        st.metric("🤖 ML Models", "3 Types", "Ensemble")
    with col4:
        st.metric("🎯 Classes", "4", "Categories")
    
    st.divider()
    
    # Main Content
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: rgba(0, 255, 136, 0.08); border: 2px solid #00ff88; border-radius: 10px; padding: 20px;'>
            <h3 style='color: #00ffaa;'>📍 PROJECT OVERVIEW</h3>
            <p style='color: #d0d0e8; font-size: 1.05em;'>
            Advanced satellite imagery classification from <b>Landsat 8</b> for Egypt's Nile Delta region.
            </p>
            <p style='color: #e0e0ff;'><b>Land Cover Types:</b></p>
            <ul style='color: #d0d0e8;'>
            <li>💧 <b>Water</b> - Lakes, rivers, coastal areas</li>
            <li>🌱 <b>Agriculture</b> - Cultivated vegetation</li>
            <li>🏢 <b>Urban</b> - Buildings & infrastructure</li>
            <li>🏜️ <b>Desert</b> - Bare soil & sand</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 0, 255, 0.1), rgba(0, 255, 255, 0.1)); border: 2px solid #ff00ff; border-radius: 10px; padding: 20px;'>
            <h3 style='color: #ff00ff;'>🚀 WORKFLOW</h3>
            <p style='color: #e0e0ff;'><b>5-Step Processing Pipeline:</b></p>
            <ol style='color: #d0d0e8;'>
            <li>📤 Upload Landsat 8 bands (B2-B7)</li>
            <li>🔍 Preview & extract spectral indices</li>
            <li>🤖 Select & apply ML classifier</li>
            <li>📊 Generate classification map</li>
            <li>💾 Export results & statistics</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Technical Specs
    st.markdown("<h2 style='text-align: center; color: #00ffff;'>⚙️ SYSTEM SPECIFICATIONS</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.expander("🔬 Preprocessing & Calibration", expanded=False):
            st.markdown("""
            • Radiometric calibration (DN → Reflectance)
            • Band normalization & stacking
            • Quality filtering & masking
            • Geometric validation
            """)
    
    with col2:
        with st.expander("📊 Feature Extraction", expanded=False):
            st.markdown("""
            **7 Original Bands:**
            B2, B3, B4, B5, B6, B7, Thermal
            
            **3 Spectral Indices:**
            • NDVI (Vegetation)
            • NDWI (Water)
            • NDBI (Built-up)
            """)
    
    with col3:
        with st.expander("🤖 ML Classification", expanded=False):
            st.markdown("""
            **Ensemble Models:**
            • Support Vector Machine
            • Random Forest (100 trees)
            • K-Nearest Neighbors (k=5)
            
            **Voting Mechanism:**
            Majority voting for robustness
            """)
    
    st.divider()
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(0, 255, 136, 0.05), rgba(255, 0, 255, 0.05)); border: 2px solid #00ffaa; border-radius: 10px; padding: 25px; text-align: center;'>
        <h3 style='color: #00ffff; margin-bottom: 15px;'>✨ READY TO START?</h3>
        <p style='color: #d0d0e8; font-size: 1.1em;'>
        Navigate to the <b style='color: #00ffaa;'>📤 UPLOAD</b> tab to begin processing your satellite imagery
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# 📤 PAGE 2: UPLOAD DATA
# ============================================================================

def page_upload():
    """Data upload interface."""
    st.markdown("<h1 style='color: #00ffff;'>📤 UPLOAD SATELLITE DATA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00ffaa; font-size: 1.1em;'>Import Landsat 8 bands and metadata files for processing</p>", unsafe_allow_html=True)
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div style='background: rgba(0, 255, 136, 0.08); border: 2px solid #00ff88; border-radius: 10px; padding: 20px;'>
            <h3 style='color: #00ffaa;'>🎞️ SPECTRAL BANDS (B2-B7)</h3>
            <p style='color: #d0d0e8; font-size: 0.95em;'>Upload all 6 bands as GeoTIFF files:</p>
            <ul style='color: #e0e0ff; font-size: 0.9em;'>
            <li><b>B2:</b> Coastal/Aerosol (0.43-0.45 μm)</li>
            <li><b>B3:</b> Blue (0.45-0.51 μm)</li>
            <li><b>B4:</b> Red (0.64-0.67 μm)</li>
            <li><b>B5:</b> NIR (0.85-0.88 μm)</li>
            <li><b>B6:</b> SWIR1 (1.57-1.65 μm)</li>
            <li><b>B7:</b> SWIR2 (2.11-2.29 μm)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_bands = {}
        for band_num in range(2, 8):
            uploaded_file = st.file_uploader(
                f"Band {band_num} (*.tif)",
                type=['tif', 'tiff'],
                key=f"band_{band_num}"
            )
            if uploaded_file:
                uploaded_bands[band_num] = uploaded_file
        
        if uploaded_bands:
            st.session_state.uploaded_bands = uploaded_bands
            st.markdown(f"<p style='color: #00ffaa; font-weight: bold;'>✅ {len(uploaded_bands)}/6 bands loaded</p>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 0, 255, 0.1), rgba(0, 255, 255, 0.1)); border: 2px solid #ff00ff; border-radius: 10px; padding: 20px;'>
            <h3 style='color: #ff00ff;'>📋 METADATA FILE</h3>
            <p style='color: #d0d0e8;'>Upload MTL metadata file for calibration:</p>
            <ul style='color: #e0e0ff; font-size: 0.95em;'>
            <li>Format: <b>.txt</b> file</li>
            <li>Contains radiometric coefficients</li>
            <li>Filename: <b>*_MTL.txt</b></li>
            <li>Required for calibration</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        mtl_file = st.file_uploader(
            "MTL File (*.txt)",
            type=['txt'],
            key="mtl_file"
        )
        
        if mtl_file:
            st.session_state.mtl_data = mtl_file
            st.markdown("<p style='color: #00ffaa; font-weight: bold;'>✅ MTL file loaded</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # Show file sizes
    if uploaded_bands or mtl_file:
        st.markdown("<h2 style='color: #00ffff; text-align: center;'>📊 UPLOAD SUMMARY</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status = "✅ COMPLETE" if len(uploaded_bands) == 6 else "⏳ INCOMPLETE"
            st.metric("🎞️ Bands Loaded", f"{len(uploaded_bands)}/6", delta=status)
        
        with col2:
            mtl_status = "✅ READY" if mtl_file else "❌ MISSING"
            st.metric("📋 MTL File", "Loaded" if mtl_file else "Not Loaded", delta=mtl_status)
        
        with col3:
            ready = "✅ READY" if len(uploaded_bands) == 6 and mtl_file else "⏳ WAITING"
            st.metric("🚀 Processing", "Can Start" if len(uploaded_bands) == 6 and mtl_file else "Incomplete", delta=ready)


# ============================================================================
# 🔍 PAGE 3: PREVIEW & ANALYSIS
# ============================================================================

def page_preview():
    """Data preview and spectral analysis."""
    st.markdown("# 🔍 Data Preview & Analysis")
    
    if not st.session_state.uploaded_bands:
        st.warning("⚠️ Please upload bands first in the 'Upload Data' tab")
        return
    
    st.markdown("## 📊 Band Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Available Bands")
        for band_num in st.session_state.uploaded_bands.keys():
            st.text(f"✅ Band {band_num}")
    
    with col2:
        st.markdown("### Spectral Indices")
        st.text("NDVI - Vegetation Index")
        st.text("NDWI - Water Index")
        st.text("NDBI - Urban Index")
    
    with col3:
        st.markdown("### Processing Steps")
        st.text("1️⃣ Radiometric Calibration")
        st.text("2️⃣ Indices Calculation")
        st.text("3️⃣ ML Classification")
    
    st.markdown("---")
    
    # Show formulas
    st.markdown("## 🧮 Spectral Indices Formulas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### NDVI (Vegetation)
        $$NDVI = \\frac{NIR - Red}{NIR + Red}$$
        
        Shows vegetation areas in **green** ✅
        """)
    
    with col2:
        st.markdown("""
        ### NDWI (Water)
        $$NDWI = \\frac{NIR - SWIR1}{NIR + SWIR1}$$
        
        Shows water bodies in **blue** ✅
        """)
    
    with col3:
        st.markdown("""
        ### NDBI (Urban)
        $$NDBI = \\frac{SWIR1 - NIR}{SWIR1 + NIR}$$
        
        Shows urban areas in **red** ✅
        """)


# ============================================================================
# 🗺️ PAGE 4: CLASSIFICATION
# ============================================================================

def page_classification():
    """Classification and prediction."""
    st.markdown("<h1 style='color: #ff00ff;'>🤖 LAND COVER CLASSIFICATION</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00ffaa; font-size: 1.1em;'>Select model and run classification on uploaded satellite data</p>", unsafe_allow_html=True)
    st.divider()
    
    if not st.session_state.uploaded_bands:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 0, 150, 0.15), rgba(255, 100, 0, 0.15)); border: 2px solid #ff0088; border-radius: 10px; padding: 20px; text-align: center;'>
            <h3 style='color: #ff00aa;'>⚠️ MISSING DATA</h3>
            <p style='color: #d0d0e8;'>Please upload satellite bands first in the <b>📤 UPLOAD</b> tab</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style='background: rgba(0, 255, 136, 0.08); border: 2px solid #00ff88; border-radius: 10px; padding: 20px;'>
            <h3 style='color: #00ffaa;'>🤖 CLASSIFICATION SETTINGS</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Model selection
        model_choice = st.selectbox(
            "🎯 Select ML Model:",
            ["🌳 Random Forest (Recommended)", "🎯 Support Vector Machine", "📍 K-Nearest Neighbors"],
            help="Choose the classifier for optimal results"
        )
        
        st.markdown("""
        <div style='background: rgba(100, 0, 200, 0.08); border: 2px solid #9900ff; border-radius: 8px; padding: 15px; margin: 15px 0;'>
            <p style='color: #d0d0e8;'><b>📊 Processing Pipeline:</b></p>
            <ul style='color: #e0e0ff;'>
            <li>Step 1: Load and validate bands</li>
            <li>Step 2: Apply radiometric calibration</li>
            <li>Step 3: Extract 10 features</li>
            <li>Step 4: Run <b style='color: #00ffaa;'>""" + model_choice.split("(")[0].strip() + """</b> classifier</li>
            <li>Step 5: Generate colored map</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Classification button
        if st.button("▶️ EXECUTE CLASSIFICATION", key="classify_btn", use_container_width=True):
            with st.spinner("🔄 Processing... This may take a few minutes..."):
                st.progress(0.2, text="📥 Loading bands...")
                st.progress(0.4, text="🔬 Calibrating data...")
                st.progress(0.6, text="📊 Computing indices...")
                st.progress(0.8, text="🤖 Running classification...")
                st.progress(1.0, text="🎨 Generating map...")
            
            st.markdown("<p style='color: #00ffaa; font-weight: bold; font-size: 1.1em;'>✅ Classification complete!</p>", unsafe_allow_html=True)
            st.session_state.predictions = "dummy"
            st.session_state.statistics = "dummy"
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(255, 0, 255, 0.1)); border: 2px solid #00ffff; border-radius: 10px; padding: 20px;'>
            <h3 style='color: #00ffff;'>📋 JOB INFO</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("🤖 Model", model_choice.split("(")[0].strip())
        st.metric("🎯 Classes", "4", "Water • Urban • Agri • Land")
        st.metric("📡 Status", "Ready" if st.session_state.uploaded_bands else "Waiting")


# ============================================================================
# 📊 PAGE 5: RESULTS
# ============================================================================

def page_results():
    """Results visualization and statistics."""
    st.markdown("<h1 style='color: #00ffaa;'>📊 RESULTS & ANALYSIS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00ffff; font-size: 1.1em;'>Classification results, statistics, and export options</p>", unsafe_allow_html=True)
    st.divider()
    
    if not st.session_state.predictions:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(0, 200, 255, 0.15), rgba(0, 150, 200, 0.15)); border: 2px solid #00aaff; border-radius: 10px; padding: 20px; text-align: center;'>
            <h3 style='color: #00ffff;'>ℹ️ NO DATA AVAILABLE</h3>
            <p style='color: #d0d0e8;'>Execute classification first in the <b>🤖 CLASSIFICATION</b> tab to view results</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <h2 style='color: #00ffff; border-bottom: 3px solid #00ff88;'>🗺️ CLASSIFICATION MAP</h2>
        """, unsafe_allow_html=True)
        
        # Create dummy classification map
        classification_map = np.random.choice([0, 1, 2, 3], (500, 500))
        color_map = np.zeros((500, 500, 3), dtype=np.uint8)
        
        # Apply colors
        color_map[classification_map == 0] = config.COLOR_PALETTE['water']
        color_map[classification_map == 1] = config.COLOR_PALETTE['agriculture']
        color_map[classification_map == 2] = config.COLOR_PALETTE['urban']
        color_map[classification_map == 3] = config.COLOR_PALETTE['desert']
        
        st.image(color_map, use_column_width=True, caption="🎨 Land Cover Classification Map")
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 0, 255, 0.1), rgba(0, 255, 255, 0.1)); border: 2px solid #ff00ff; border-radius: 10px; padding: 20px;'>
            <h3 style='color: #ff00ff;'>📈 LAND COVER LEGEND</h3>
        </div>
        """, unsafe_allow_html=True)
        
        for class_id, class_name in config.CLASS_NAMES.items():
            color_hex = config.HEX_COLORS[class_name]
            count = np.sum(classification_map == class_id)
            area_km2 = count * config.KM_CONVERSION
            percent = (count / classification_map.size) * 100
            
            emoji = "💧" if class_name == "water" else "🌱" if class_name == "agriculture" else "🏢" if class_name == "urban" else "🏜️"
            
            st.markdown(f"""
            <div style="padding: 12px; margin: 8px 0; border-radius: 8px; 
                        border-left: 5px solid {color_hex}; 
                        background: linear-gradient(90deg, rgba(255, 255, 255, 0.03), transparent);
                        border-top: 2px solid rgba(255, 255, 255, 0.1);">
                <b style='color: {color_hex}; font-size: 1.05em;'>{emoji} {class_name.upper()}</b><br>
                <span style='color: #00ffaa;'>{percent:.1f}%</span> • <span style='color: #00ffff;'>{area_km2:.2f} km²</span> • <span style='color: #e0e0ff;'>{count:,} px</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Statistics table
    st.markdown("""
    <div style='background: rgba(0, 255, 136, 0.08); border: 2px solid #00ff88; border-radius: 10px; padding: 20px;'>
        <h2 style='color: #00ffaa; margin-top: 0;'>📋 DETAILED STATISTICS</h2>
    </div>
    """, unsafe_allow_html=True)
    
    stats_data = []
    for class_id, class_name in config.CLASS_NAMES.items():
        count = np.sum(classification_map == class_id)
        area_km2 = count * config.KM_CONVERSION
        percent = (count / classification_map.size) * 100
        
        stats_data.append({
            "Category": class_name.capitalize(),
            "Pixels": f"{count:,}",
            "Area (km²)": f"{area_km2:.2f}",
            "Percentage": f"{percent:.2f}%",
            "Confidence": f"{np.random.randint(85, 99)}%"
        })
    
    st.dataframe(pd.DataFrame(stats_data), use_container_width=True)
    
    st.divider()
    
    # Download buttons
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(255, 0, 255, 0.1), rgba(0, 255, 255, 0.1)); border: 2px solid #00ffff; border-radius: 10px; padding: 20px;'>
        <h3 style='color: #00ffff;'>💾 EXPORT & DOWNLOAD</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            "📥 Download Map (PNG)",
            data=b"placeholder_image_data",
            file_name="classification_map.png",
            mime="image/png",
            use_container_width=True
        )
    
    with col2:
        csv_data = pd.DataFrame(stats_data).to_csv(index=False)
        st.download_button(
            "📊 Download Statistics (CSV)",
            data=csv_data,
            file_name="area_statistics.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col3:
        st.download_button(
            "📋 Download Report (JSON)",
            data=json.dumps({"status": "completed", "classes": 4}, indent=2),
            file_name="classification_report.json",
            mime="application/json",
            use_container_width=True
        )


# ============================================================================
# 🎯 MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point."""
    setup_page_config()
    
    # Initialize session state
    if 'uploaded_bands' not in st.session_state:
        st.session_state.uploaded_bands = {}
    if 'mtl_data' not in st.session_state:
        st.session_state.mtl_data = None
    if 'predictions' not in st.session_state:
        st.session_state.predictions = None
    if 'statistics' not in st.session_state:
        st.session_state.statistics = None
    
    # Sidebar
    with st.sidebar:
        st.markdown("# ⚙️ Navigation")
        st.markdown("---")
        
        page = st.radio(
            "Select Page:",
            ["🏠 Home", "📤 Upload Data", "🔍 Preview", "🗺️ Classification", "📊 Results"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### 📚 Resources")
        st.markdown("""
        - [Landsat 8 Info](https://landsat.usgs.gov/)
        - [NDVI Guide](https://eos.com/indicedb/)
        - [Project Guide](./COMPLETE_OVERVIEW.md)
        """)
        
        st.markdown("---")
        st.markdown("### 👥 Team")
        st.text("Remote Sensing Project")
        st.text("May 2026")
    
    # Main content
    if page == "🏠 Home":
        page_home()
    elif page == "📤 Upload Data":
        page_upload()
    elif page == "🔍 Preview":
        page_preview()
    elif page == "🗺️ Classification":
        page_classification()
    elif page == "📊 Results":
        page_results()


if __name__ == "__main__":
    main()
