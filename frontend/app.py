"""Streamlit frontend for image anonymization"""

import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image
import os

# Page configuration
st.set_page_config(
    page_title="HTW Emerging Photo - Anonymization",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# API endpoint
API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")

# Debug info (can be removed in production)
print(f"[DEBUG] API_URL configured as: {API_URL}")


def main():
    """Main Streamlit application"""
    
    # Header
    st.title("🔒 HTW Emerging Photo")
    st.subheader("Face and License Plate Anonymization System")
    
    # Add timestamp to force cache refresh
    import datetime
    st.caption(f"Page loaded: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This system automatically detects and anonymizes:
        - 👤 **Human Faces** (using RetinaFace)
        - 🚗 **License Plates** (using YOLO)
        
        **Anonymization Method:**
        - Solid yellow color fill (#FFFF00)
        - Complete obscuration of sensitive regions
        
        **Supported Formats:**
        - JPG, PNG
        - Max file size: 10MB
        """)
        
        st.markdown("---")
        
        # API info
        st.caption(f"🔗 API Endpoint: `{API_URL}`")
        
        # Add refresh button
        if st.button("🔄 Refresh Connection", key="refresh_api"):
            st.rerun()
        
        try:
            print(f"[DEBUG] Attempting to connect to {API_URL}/info")
            response = requests.get(f"{API_URL}/info", timeout=5)
            print(f"[DEBUG] Response status: {response.status_code}")
            if response.status_code == 200:
                info = response.json()
                st.success("✅ API Connected")
                with st.expander("API Details"):
                    st.json(info)
            else:
                st.error(f"❌ API Error: Status {response.status_code}")
                st.caption(f"Response: {response.text[:200]}")
        except Exception as e:
            print(f"[DEBUG] Connection error: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            st.error(f"❌ Cannot connect to API")
            st.caption(f"Error: {type(e).__name__}: {str(e)}")
            st.caption("Please ensure the backend is running.")
            st.caption("Click 'Refresh Connection' button above to retry.")
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload Image")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an image file (JPG or PNG)",
            type=["jpg", "jpeg", "png"],
            help="Maximum file size: 10MB"
        )
        
        if uploaded_file is not None:
            # Display original image
            st.subheader("Original Image")
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)
            
            # Image info
            file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
            st.info(
                f"📊 **Image Info:**\n"
                f"- Size: {image.size[0]} x {image.size[1]} pixels\n"
                f"- Format: {image.format}\n"
                f"- File size: {file_size_mb:.2f} MB"
            )
            
            # Anonymize button
            if st.button("🔒 Anonymize Image", type="primary", use_container_width=True):
                anonymize_image(uploaded_file, col2)
    
    with col2:
        st.header("🔒 Anonymized Result")
        st.info("👈 Upload an image and click 'Anonymize Image' to see results")


def anonymize_image(uploaded_file, result_column):
    """
    Send image to API for anonymization and display results
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        result_column: Streamlit column for displaying results
    """
    with result_column:
        # Show progress
        with st.spinner("🔄 Processing image... (First request may take 1-2 minutes to download models)"):
            try:
                # Prepare file for upload
                uploaded_file.seek(0)
                files = {
                    "file": (uploaded_file.name, uploaded_file, uploaded_file.type)
                }
                
                # Send request to API (increased timeout for model download on first request)
                response = requests.post(
                    f"{API_URL}/anonymize",
                    files=files,
                    timeout=300  # 5 minutes to allow for model download
                )
                
                # Handle response
                if response.status_code == 200:
                    result = response.json()
                    display_results(result)
                    
                elif response.status_code == 400:
                    st.error(f"❌ Invalid image: {response.json().get('detail', 'Unknown error')}")
                    
                elif response.status_code == 413:
                    st.error("❌ File too large! Maximum size is 10MB.")
                    
                else:
                    st.error(f"❌ Error {response.status_code}: {response.json().get('detail', 'Unknown error')}")
                    
            except requests.exceptions.Timeout:
                st.error("❌ Request timeout. The backend may still be downloading models. Please wait a moment and try again.")
                
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to API. Please ensure the backend is running.")
                
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")


def display_results(result):
    """
    Display anonymization results
    
    Args:
        result: API response dictionary
    """
    if not result.get("success"):
        st.error(f"❌ Anonymization failed: {result.get('error', 'Unknown error')}")
        return
    
    # Processing time
    processing_time = result.get("processing_time", 0)
    st.success(f"✅ Anonymization completed in {processing_time:.2f} seconds")
    
    # Summary statistics
    summary = result.get("summary", {})
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "👤 Faces Anonymized",
            summary.get("total_faces", 0)
        )
    
    with col2:
        st.metric(
            "🚗 Plates Anonymized",
            summary.get("total_plates", 0)
        )
    
    with col3:
        st.metric(
            "🔒 Total Anonymized",
            summary.get("total_anonymized", 0)
        )
    
    st.markdown("---")
    
    # Display anonymized image
    st.subheader("Anonymized Image")
    anonymized_image_b64 = result.get("anonymized_image")
    
    if anonymized_image_b64:
        # Decode base64 image
        image_bytes = base64.b64decode(anonymized_image_b64)
        image = Image.open(BytesIO(image_bytes))
        st.image(image, use_column_width=True)
        
        # Download button
        st.download_button(
            label="💾 Download Anonymized Image",
            data=image_bytes,
            file_name="anonymized_image.png",
            mime="image/png",
            use_container_width=True
        )
    
    st.markdown("---")
    
    # Detection details
    with st.expander("📋 View Detection Details", expanded=False):
        # Face detections
        faces = result.get("faces_anonymized", [])
        if faces:
            st.subheader("👤 Face Detections")
            for face in faces:
                bbox = face.get("bbox", {})
                st.markdown(
                    f"**Face {face.get('id')}:** "
                    f"Confidence: {face.get('confidence', 0):.2f} | "
                    f"Position: ({bbox.get('x')}, {bbox.get('y')}) | "
                    f"Size: {bbox.get('width')}x{bbox.get('height')} | "
                    f"Color: {face.get('anonymization_color', '#FFFF00')}"
                )
        else:
            st.info("No faces detected")
        
        st.markdown("---")
        
        # Plate detections
        plates = result.get("plates_anonymized", [])
        if plates:
            st.subheader("🚗 License Plate Detections")
            for plate in plates:
                bbox = plate.get("bbox", {})
                st.markdown(
                    f"**Plate {plate.get('id')}:** "
                    f"Confidence: {plate.get('confidence', 0):.2f} | "
                    f"Position: ({bbox.get('x')}, {bbox.get('y')}) | "
                    f"Size: {bbox.get('width')}x{bbox.get('height')} | "
                    f"Color: {plate.get('anonymization_color', '#FFFF00')}"
                )
        else:
            st.info("No license plates detected")
    
    # Full JSON response
    with st.expander("🔍 View Full API Response", expanded=False):
        st.json(result)


if __name__ == "__main__":
    main()

