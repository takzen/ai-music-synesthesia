# app.py
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
# --- ZMIANA: Dodajemy obsługę błędów wokół importu ---
try:
    from music_generator import image_to_music_pipeline
except ImportError as e:
    st.error(f"Failed to import a required module. Please check your installation. Details: {e}")
    st.stop() # Zatrzymuje aplikację, jeśli import się nie uda

# Load environment variables from .env file at the very start
# This is the ONLY place we need to call it.
load_dotenv()

st.set_page_config(layout="wide")
st.title("AI Music Synesthesia 🎵")
st.write("Turn your images into original music.")

st.header("1. Upload an Image")
uploaded_image = st.file_uploader(
    "Choose an image file (PNG, JPG)",
    type=["png", "jpg", "jpeg"]
)

if uploaded_image:
    try:
        image = Image.open(uploaded_image)
        st.image(image, caption="Your uploaded image.", use_container_width=True)
        
        st.header("2. Generate Music")
        if st.button("Create Music from Image"):
            with st.spinner("AI is analyzing your image and composing music... This may take a minute."):
                try:
                    generated_audio, music_prompt = image_to_music_pipeline(image)
                    
                    st.success("Music generated successfully!")
                    
                    st.subheader("Generated Music Prompt:")
                    st.info(music_prompt)
                    
                    st.subheader("Listen to Your Music:")
                    st.audio(generated_audio, format='audio/mpeg')
                except Exception as e:
                    st.error(f"An error occurred during generation: {e}")
    except Exception as e:
        st.error(f"An error occurred while handling the image file: {e}")