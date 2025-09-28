# music_generator.py
import os
import google.generativeai as genai
import requests
from PIL import Image
from io import BytesIO

def analyze_image_with_gemini(image: Image.Image) -> str:
    """
    Analyzes an image using Gemini 2.5 Pro and generates a descriptive prompt for a music model.
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
    Generates music using the Stable Audio API based on a descriptive prompt.
    """
    api_key = os.getenv("STABILITY_API_KEY")
    if not api_key:
        raise ValueError("STABILITY_API_KEY not found in .env file.")
    
    # NOTE: As of late 2024/early 2025, Stable Audio 2.0 is the leading model.
    # The API endpoint might change. This reflects a common structure.
    api_host = "https://api.stability.ai"
    url = f"{api_host}/v1/generation/stable-audio/generate"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "audio/mpeg",
    }
    
    data = {
        "prompt": prompt,
        "seconds": "29", # Keep it under 30s for faster generation on free tiers
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        raise Exception(f"Stability AI API Error: {response.text}")

    # Return the audio content as a BytesIO object
    return BytesIO(response.content)

def image_to_music_pipeline(image: Image.Image):
    """
    The main pipeline that orchestrates the image-to-music process.
    """
    # Step 1: Analyze the image to create a music prompt
    music_prompt = analyze_image_with_gemini(image)
    
    # Step 2: Generate music based on the created prompt
    audio_io = generate_music_with_stable_audio(music_prompt)
    
    return audio_io, music_prompt