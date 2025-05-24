# ♻️ Waste Classification App 🗑️

This Streamlit web application allows users to classify images of waste into two categories: **Organic** or **Recyclable**. It leverages a pre-trained TensorFlow/Keras deep learning model to provide real-time predictions directly in your browser, either through image upload or live camera feed.

---

## ✨ Features

- **Dual Input Modes**: Seamlessly switch between uploading an image file (JPG, JPEG, PNG, WEBP) or capturing a live picture using your device's camera.
- **Instant Classification**: Get immediate predictions (Organic or Recyclable) with a confidence score.
- **Dynamic UI**: The prediction section automatically clears when you switch between input methods, ensuring a clean user experience.
- **Clear Camera Image**: A dedicated button to clear the captured camera image and reactivate the camera.
- **Simple Interface**: Built with Streamlit for an intuitive and user-friendly web interface.

---

## 🚀 How to Run Locally

Follow these steps to get the app running on your local machine.

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### 1. Clone the Repository

```bash
git clone https://github.com/Roshians/Waste-Classification.git
cd Waste-Classification
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows
.\venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt` content:**
```
tensorflow==2.19.0
streamlit==1.45.1
numpy==2.1.3
pillow==11.1.0
```

### 4. Place Your Model File

Ensure your pre-trained Keras model file (`best_model.h5`) is in the same directory as `app.py`.  
If your model is elsewhere, update the `MODEL_PATH` variable in `app.py` accordingly.

### 5. Run the Streamlit App

```bash
streamlit run app.py
```

This command will open the Streamlit app in your default web browser.

---

## 🛠️ Model Information

The application uses a deep learning model to perform the classification.

- **Model File**: `best_model.h5`
- **Image Size**: Resized to (128, 128) pixels (`IMAGE_SIZE`)
- **Normalization**: Pixel values are divided by `255.0` (`RESCALE_FACTOR`) to scale them to the 0–1 range.
- **Classes**:
  - `Recyclable` (Assumed index 0)
  - `Organic` (Assumed index 1)


> ⚠️ Note: The prediction logic in `app.py` assumes `predictions[0][0]` is the probability for 'Recyclable'. If your model's output order differs, adjust the `predicted_class_index` logic accordingly.

---

## 💡 Usage

1. **Launch the app**:
   ```bash
   streamlit run app.py
   ```

2. **Choose Input Method**:
   - "Upload Image" or
   - "Use Camera" (via radio buttons)

3. **Provide Image**:
   - **Upload Image**: Click "Choose an image..." and select a file.
   - **Use Camera**: Click "Take a picture" to capture via webcam.

4. **View Prediction**:
   - The app classifies the image and displays the predicted category with a confidence score.

5. **Reset**:
   - Switching input methods automatically clears the image and prediction.
   - Use "Clear image" in camera mode to retake a picture.

---

## 🤝 Contributing

Contributions are welcome! If you find a bug or have an idea for improvement, please [open an issue](https://github.com/Roshians/Waste-Classification/issues) or submit a pull request.

---

## 📄 License

This project is open-sourced under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- Built with [Streamlit](https://streamlit.io)
- Deep learning powered by [TensorFlow](https://www.tensorflow.org/) and [Keras](https://keras.io)
- Image processing with [Pillow](https://python-pillow.org/)
- Thanks to your friend for contributing to the stable code!