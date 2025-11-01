import streamlit as st
import requests
import os
from datetime import datetime

st.title("Minimal API Test")
st.write(f"Time: {datetime.now()}")

API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")
st.write(f"API URL: {API_URL}")

try:
    response = requests.get(f"{API_URL}/info", timeout=5)
    st.success(f"✅ SUCCESS! Status: {response.status_code}")
    st.json(response.json())
except Exception as e:
    st.error(f"❌ ERROR: {e}")

