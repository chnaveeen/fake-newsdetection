import streamlit as st
import joblib
import pandas as pd
import os
import pytesseract
from PIL import Image

st.set_page_config(
    page_title="Fake News Detector",
    page_icon="📰",
    layout="centered"
)

# --- TESSERACT CONFIGURATION ---
# Point to the bundled Tesseract executable in the project root or system path
def get_tesseract_path():
    # Common installation paths for Tesseract on Windows
    possible_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        os.path.join(os.getcwd(), 'tesser.exe') # Fallback to local bundled version
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

tesseract_path = get_tesseract_path()
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
# -------------------------------

# Custom CSS for styling
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6
    }
    .stTextArea textarea {
        font-size: 1.1rem;
    }
    .prediction-box-fake {
        padding: 20px;
        border-radius: 10px;
        background-color: #ffcccc;
        color: #cc0000;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
    .prediction-box-true {
        padding: 20px;
        border-radius: 10px;
        background-color: #ccffcc;
        color: #008000;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    model_path = os.path.join('models', 'model.pkl')
    vec_path = os.path.join('models', 'vectorizer.pkl')
    if os.path.exists(model_path) and os.path.exists(vec_path):
        model = joblib.load(model_path)
        vectorizer = joblib.load(vec_path)
        return model, vectorizer
    return None, None

def main():

    st.title("📰 Fake News Detection System")
    st.write("Enter the text of a news article below or upload a text document to determine if it is likely **Real** or **Fake**.")
    
    model, vectorizer = load_model()
    
    if model is None or vectorizer is None:
        st.error("Error: Model or Vectorizer not found. Please run `train.py` first to generate them.")
        st.stop()
        
    uploaded_file = st.file_uploader("Upload an article document (.txt) or Image (.png, .jpg)", type=["txt", "png", "jpg", "jpeg"])
    user_input = ""
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".txt"):
                user_input = uploaded_file.getvalue().decode("utf-8")
                st.success("Text document successfully loaded!")
            else:
                # Handle image uploads
                with st.spinner("Extracting text from image..."):
                    img = Image.open(uploaded_file)
                    user_input = pytesseract.image_to_string(img)
                    if not user_input.strip():
                        st.error("Could not extract any recognizable text from this image.")
                    else:
                        st.success("Image text successfully extracted!")
                        
        except Exception as e:
            st.error(f"Error reading file at processing stage: {e}")
            
    # Text area for manual input, populated by file upload if present
    user_input = st.text_area("Article Text:", value=user_input, height=250, placeholder="Paste the news article text here...")
    
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        predict_button = st.button("Analyze Article", use_container_width=True, type="primary")
        
    if predict_button:
        if not user_input.strip():
             st.warning("Please enter some text to analyze.")
        else:
            with st.spinner("Analyzing text..."):
                try:
                    # Vectorize input
                    input_tfidf = vectorizer.transform([user_input])
                    
                    word_count = len(user_input.split())
                    if word_count < 10:
                        st.warning(f"⚠️ **Note:** Your input is extremely short ({word_count} words). This model was trained on full-length news articles. Predictions for single sentences will be highly unreliable.")
                        
                    if input_tfidf.nnz == 0:
                        st.error("❌ **Vocaubulary Error:** None of the words in your text were recognized by the AI's vocabulary (or they were ignored as common stop-words). Please paste a longer, more descriptive article text.")
                    else:
                        # Predict
                        prediction = model.predict(input_tfidf)[0]
                        
                        # Get probabilities if supported
                        try:
                            proba = model.predict_proba(input_tfidf)[0]
                            confidence = proba[prediction] * 100
                            conf_text = f"Confidence: {confidence:.1f}%"
                        except:
                            conf_text = ""
                        
                        # Display results
                        if prediction == 0:
                            st.markdown(f'<div class="prediction-box-fake">🚨 FAKE NEWS DETECTED<br><span style="font-size: 16px;">{conf_text}</span></div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="prediction-box-true">✅ TRUE NEWS<br><span style="font-size: 16px;">{conf_text}</span></div>', unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"An error occurred during prediction: {e}")

if __name__ == "__main__":
    main()
