import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io 

# --- Configuration ---
MODEL_PATH = 'best_model.h5' 
IMAGE_SIZE = (128, 128) 
CLASS_NAMES = ['Organic', 'Recyclable'] 
RESCALE_FACTOR = 1./255.0 

# --- Session State Initialization ---
# Initialize session state variables to manage UI state
if 'camera_mode_active' not in st.session_state:
    st.session_state['camera_mode_active'] = False # True if camera input should be shown
if 'captured_image_bytes' not in st.session_state:
    st.session_state['captured_image_bytes'] = None # Stores the bytes of the captured image
if 'input_option' not in st.session_state:
    st.session_state['input_option'] = "Upload Image" # Default selected option



# --- Load the pre-trained model ---
@st.cache_resource
def load_my_model():
    try:
        model = load_model(MODEL_PATH)
        return model
    except Exception as e:
        st.error(f"Error loading the model: {e}")
        st.stop()

model = load_my_model()

# --- Streamlit App Title ---
st.title("Waste Classification App")
st.write("Upload an image of waste or use your camera to classify it as Organic or Recyclable.")

# --- Choice between File Upload and Camera ---
current_option = st.radio("Choose input method:", ("Upload Image", "Use Camera"), key="input_method_radio", horizontal=True)

# --- Reset camera state when switching between options ---
if current_option != st.session_state['input_option']:
    st.session_state['input_option'] = current_option
    st.session_state['camera_mode_active'] = (current_option == "Use Camera") 
    st.session_state['captured_image_bytes'] = None 
    st.rerun() 

image_to_predict = None 

# --- Handle File Upload ---
if st.session_state['input_option'] == "Upload Image":
    uploaded_file = st.file_uploader("Choose an image...", type=("jpg", "jpeg", "png", "webp"))
    if uploaded_file is not None:
        image_to_predict = Image.open(uploaded_file).convert("RGB")
        st.image(image_to_predict, caption='Uploaded Image', use_container_width=True)

# --- Handle Camera Input ---
elif st.session_state['input_option'] == "Use Camera":
    if st.session_state['captured_image_bytes'] is None:
        img_file_buffer = st.camera_input("Take a picture")

        if img_file_buffer is not None:
            st.session_state['captured_image_bytes'] = img_file_buffer.getvalue()
            st.session_state['camera_mode_active'] = False 
            st.rerun() 
    else:
        image_to_predict = Image.open(io.BytesIO(st.session_state['captured_image_bytes'])).convert("RGB")
        st.image(image_to_predict, caption='Captured Image', use_container_width=True)

        # Show the "Clear image" button
        if st.button("Clear image"):
            st.session_state['captured_image_bytes'] = None 
            st.session_state['camera_mode_active'] = True 
            st.rerun() 

# --- Conditional Prediction Execution ---
if image_to_predict is not None:


    # --- Preprocessing and Prediction Logic ---
    try:
        img_array = tf.keras.utils.img_to_array(image_to_predict)
        img_resized = tf.image.resize(img_array, IMAGE_SIZE)
        normalized_img = img_resized * RESCALE_FACTOR
        input_data = tf.expand_dims(normalized_img, 0)

        predictions = model.predict(input_data)

        probability_for_class_0 = predictions[0][0]

        if probability_for_class_0 > 0.5:
            predicted_class_index = 1
            confidence = probability_for_class_0 * 100
        else:
            predicted_class_index = 0
            confidence = (1 - probability_for_class_0) * 100

        prediction_label = CLASS_NAMES[predicted_class_index]

        # --- Clean Prediction Display ---
        st.markdown("---")

        st.metric(label="Predicted Category", value=prediction_label)
        st.metric(label="Confidence", value=f"{confidence:.2f}%")

        if prediction_label == 'Organic':
            st.info("This looks like **organic waste**! It can be composted.")
        else: # Recyclable
            st.info("This looks like **recyclable material**! Please dispose of it responsibly.")

        st.markdown("---")
        st.markdown("Made with ❤️")

    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
else:
    # Only show this if no image is currently available for prediction
    if st.session_state['captured_image_bytes'] is None and st.session_state['input_option'] == "Use Camera":
        st.info("Take a picture to get a prediction.")
    elif st.session_state['input_option'] == "Upload Image":
        st.info("Upload an image to get a prediction.")