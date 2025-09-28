# music_generator.py
import os
import google.generativeai as genai
import requests
from PIL import Image
from io import BytesIO

def analyze_image_with_gemini(image: Image.Image) -> str:
    """
    Analyzes an image using the Gemini 2.5 Pro model and generates a descriptive prompt for a music model.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env file.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-2.5-pro')

    prompt_text = """
    Analyze this image and describe it as a detailed prompt for a music generation AI.
    Focus on:
    - The overall mood and emotion (e.g., melancholic, joyful, epic, serene).
    - The setting and elements (e.g., futuristic city, calm nature, abstract shapes).
    - The colors and textures, translating them into musical concepts (e.g., "warm orange tones" could be "warm synth pads").
    - The tempo and energy (e.g., "dynamic, fast-paced scene" could be "high-energy, 140 BPM").
    
    Your output should be a single, concise paragraph of comma-separated keywords and phrases, perfect for a text-to-music model.
    Example output: "A futuristic cityscape at night, neon lights, driving electronic beat, 120 BPM, synthwave, Blade Runner soundtrack, energetic, cinematic."
    """
    response = model.generate_content([prompt_text, image])
    return response.text

def generate_music_with_stable_audio(prompt: str) -> BytesIO:
    """
    Generates music using the correct, v2beta Stable Audio API endpoint with multipart/form-data.
    """
    api_key = os.getenv("STABILITY_API_KEY")
    if not api_key:
        raise ValueError("STABILITY_API_KEY not found in .env file.")
    
    url = "https://api.stability.ai/v2beta/audio/stable-audio-2/text-to-audio"

    headers = {
        "Authorization": f"Bearer {api_key}",
        # The 'Accept' header tells the server what content type we expect in return
        "Accept": "audio/*"
    }
    
    # --- FINAL, CORRECT PAYLOAD STRUCTURE FOR MULTIPART/FORM-DATA ---
    # We use the 'files' parameter in requests to correctly build a multipart/form-data request.
    # The format for each field is (None, <value>).
    files = {
        'prompt': (None, prompt),
        'duration': (None, '29'),
    }

    # By using `files`, requests will automatically set the correct 'Content-Type' header
    response = requests.post(url, headers=headers, files=files)

    if response.status_code != 200:
        raise Exception(f"Stability AI API Error (Status {response.status_code}): {response.text}")

    # Return the audio content as a BytesIO object
    return BytesIO(response.content)

def image_to_music_pipeline(image: Image.Image):
    """
    The main pipeline that orchestrates the image-to-music process.
    """
    music_prompt = analyze_image_with_gemini(image)
    audio_io = generate_music_with_stable_audio(music_prompt)
    return audio_io, music_prompt