# app.py
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from music_generator import image_to_music_pipeline

# Load environment variables from .env file for local development
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
        st.image(image, caption="Your uploaded image.", use_column_width=False, width=512)
        
        st.header("2. Generate Music")
        if st.button("Create Music from Image"):
            with st.spinner("AI is analyzing your image and composing music... This may take a minute."):
                try:
                    # Run the full pipeline
                    generated_audio, music_prompt = image_to_music_pipeline(image)
                    
                    st.success("Music generated successfully!")
                    
                    # Display the prompt that was created by Gemini
                    st.subheader("Generated Music Prompt:")
                    st.info(music_prompt)
                    
                    # Display the audio player for the generated music
                    st.subheader("Listen to Your Music:")
                    st.audio(generated_audio, format='audio/mpeg')

                except Exception as e:
                    st.error(f"An error occurred: {e}")
    except Exception as e:
        st.error(f"An error occurred while handling the image file: {e}")