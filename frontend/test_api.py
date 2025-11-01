"""
Simple test page to verify API connectivity
"""
import streamlit as st
import requests
import os
from datetime import datetime

st.set_page_config(page_title="API Connection Test", page_icon="🔍")

st.title("🔍 API Connection Test")
st.write(f"**Current Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")
st.write(f"**API Endpoint:** `{API_URL}`")

st.markdown("---")

if st.button("🧪 Test Connection Now", type="primary"):
    with st.spinner("Testing connection..."):
        try:
            st.write(f"Attempting to connect to: `{API_URL}/info`")
            response = requests.get(f"{API_URL}/info", timeout=5)
            
            st.success(f"✅ **SUCCESS!** Status Code: {response.status_code}")
            st.write("**Response Data:**")
            st.json(response.json())
            
        except requests.exceptions.Timeout:
            st.error("❌ **TIMEOUT** - Request took too long")
            
        except requests.exceptions.ConnectionError as e:
            st.error(f"❌ **CONNECTION ERROR**")
            st.code(str(e))
            
        except Exception as e:
            st.error(f"❌ **ERROR**: {type(e).__name__}")
            st.code(str(e))

st.markdown("---")
st.caption("This is a simple test page. If you see SUCCESS above, the API is working correctly.")
st.caption(f"If you see this page, Streamlit is running. Page loaded at: {datetime.now()}")

