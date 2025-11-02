import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import tempfile
import os
import ultralytics

# Check Ultralytics version
REQUIRED_VERSION = "8.3.0"
current_version = ultralytics.__version__

# Page configuration
st.set_page_config(
    page_title="License Plate Detection",
    page_icon="🚗",
    layout="wide"
)

# Title and description
st.title("🚗 License Plate Detection with YOLOv11")
st.markdown("""
This app uses a fine-tuned YOLOv11 model to detect license plates in images.
Upload an image to detect license plates automatically.
""")

# Version check warning
try:
    from packaging import version
    if version.parse(current_version) < version.parse(REQUIRED_VERSION):
        st.error(f"""
        ⚠️ **Outdated Ultralytics Version Detected!**
        
        Your version: {current_version} | Required: {REQUIRED_VERSION}+
        
        Please upgrade by running:
        ```bash
        pip install --upgrade ultralytics
        ```
        """)
except:
    pass

    # Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Model selection (disabled for now since we load from HF Hub)
    st.info("Using YOLOv11 model from Hugging Face Hub")
    model_variant = "yolov11n"  # Fixed to nano for now
    
    # Confidence threshold
    confidence_threshold = st.slider(
        "Confidence Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.25,
        step=0.05,
        help="Minimum confidence for detection"
    )
    
    st.markdown("---")
    st.markdown("""
    ### About
    - **Model**: YOLOv11 License Plate Detection
    - **Source**: [Hugging Face](https://huggingface.co/morsetechlab/yolov11-license-plate-detection)
    - **License**: AGPLv3
    """)

# Cache the model loading
@st.cache_resource
def load_model(model_name):
    """
    Load the YOLO model from Hugging Face Hub
    
    Usage:
        model = load_model("yolov11n")
    
    This function tries multiple methods to load the model from Hugging Face Hub.
    """
    repo_id = "morsetechlab/yolov11-license-plate-detection"
    
    st.info(f"📥 Loading model from Hugging Face Hub...")
    
    # Method 1: Try from_pretrained (if available in newer Ultralytics versions)
    try:
        if hasattr(YOLO, 'from_pretrained'):
            st.write("Trying YOLO.from_pretrained()...")
            model = YOLO.from_pretrained(repo_id)
            st.success(f"✅ Model loaded successfully!")
            return model
    except Exception as e:
        st.warning(f"from_pretrained failed: {str(e)}")
    
    # Method 2: Try loading directly with repo path
    try:
        st.write("Trying direct YOLO load...")
        model = YOLO(repo_id)
        st.success(f"✅ Model loaded successfully!")
        return model
    except Exception as e:
        st.warning(f"Direct load failed: {str(e)}")
    
    # Method 3: Download specific files using hf_hub_download
    from huggingface_hub import hf_hub_download, list_repo_files
    
    try:
        st.write("Listing available files in repository...")
        files = list_repo_files(repo_id)
        pt_files = [f for f in files if f.endswith('.pt')]
        st.write(f"Found model files: {pt_files}")
        
        if pt_files:
            # Try the first .pt file found
            filename = pt_files[0]
            st.write(f"Downloading {filename}...")
            model_file = hf_hub_download(
                repo_id=repo_id,
                filename=filename
            )
            model = YOLO(model_file)
            st.success(f"✅ Model loaded successfully from {filename}!")
            return model
        else:
            st.error("No .pt model files found in repository")
            return None
            
    except Exception as e:
        st.error(f"❌ All loading methods failed: {str(e)}")
        st.info("💡 Please check the model repository or use a local model file.")
        return None

def process_image(image, model, conf_threshold):
    """Process image and detect license plates"""
    # Convert PIL Image to numpy array
    img_array = np.array(image)
    
    # Run inference
    results = model.predict(
        source=img_array,
        conf=conf_threshold,
        verbose=False
    )
    
    # Get the first result
    result = results[0]
    
    # Draw bounding boxes on the image
    annotated_img = result.plot()
    
    # Convert BGR to RGB (OpenCV uses BGR, PIL uses RGB)
    annotated_img_rgb = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
    
    return annotated_img_rgb, result

# Main app
col1, col2 = st.columns(2)

with col1:
    st.header("📤 Upload Image")
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=["jpg", "jpeg", "png", "bmp"],
        help="Upload an image containing vehicles with license plates"
    )
    
    # Option to use sample image
    use_sample = st.button("Use Sample Image")
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
    elif use_sample:
        # Create a placeholder for sample image
        st.info("To use a sample image, please upload your own image or provide a URL.")
        uploaded_file = None

with col2:
    st.header("🎯 Detection Results")
    
    if uploaded_file is not None:
        with st.spinner("Loading model..."):
            model = load_model(model_variant)
        
        if model is not None:
            with st.spinner("Detecting license plates..."):
                try:
                    image = Image.open(uploaded_file)
                    annotated_img, result = process_image(image, model, confidence_threshold)
                    
                    # Display annotated image
                    st.image(annotated_img, caption="Detected License Plates", use_column_width=True)
                    
                    # Display detection statistics
                    num_detections = len(result.boxes)
                    st.success(f"✅ Found {num_detections} license plate(s)")
                    
                    # Show detection details
                    if num_detections > 0:
                        with st.expander("📊 Detection Details"):
                            for idx, box in enumerate(result.boxes):
                                conf = float(box.conf[0])
                                coords = box.xyxy[0].cpu().numpy()
                                st.write(f"**Plate {idx + 1}:**")
                                st.write(f"- Confidence: {conf:.2%}")
                                st.write(f"- Coordinates: ({coords[0]:.0f}, {coords[1]:.0f}) → ({coords[2]:.0f}, {coords[3]:.0f})")
                                st.write("---")
                    
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")
        else:
            st.error("Failed to load model. Please check your internet connection.")
    else:
        st.info("👈 Upload an image to start detection")

# Footer
st.markdown("---")
st.markdown("""
### 📝 Notes
- This model is trained on 10,125 images and achieves 98.1% mAP@50
- Best for: Smart parking, tollgates, traffic surveillance, ALPR systems
- Model performance: Precision: 98.93%, Recall: 95.08%
- **License**: AGPLv3 - If you use this model in a service, you must open source your code.

**Credits**: Model by [MorseTechLab](https://huggingface.co/morsetechlab), powered by [Ultralytics YOLOv11](https://github.com/ultralytics/ultralytics)
""")

