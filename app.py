import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("Error: OPENAI_API_KEY is missing from your .env file!")
    st.stop()

client = OpenAI(api_key=api_key)

class Scene(BaseModel):
    scene_number: int = Field(description="The chronological index of the scene starting at 1.")
    narration: str = Field(description="The text to be spoken or displayed for this specific segment.")
    image_prompt: str = Field(description="A highly detailed, visually descriptive text prompt optimized for image generation. Include artistic style instructions (e.g., 'digital 3D Pixar style illustration') to maintain visual consistency across all scenes.")

class Storyboard(BaseModel):
    scenes: List[Scene]

st.set_page_config(page_title="AI Audio Storyboard Engine", layout="wide")
st.title("🎙️ Generative Audio-to-Visual Educational Storytelling System")
st.write("Upload an audio lecture or short story summary to instantly map out an illustrated storyboard.")

with st.sidebar:
    st.header("Pipeline Configurations")
    art_style = st.selectbox(
        "Choose Visual Consistency Style",
        ["Pixar 3D Digital Art", "Watercolor Storybook Illustration", "Retro Comic Book Style", "Realistic Cinematic Concept Art"]
    )

audio_file = st.file_uploader("Upload your educational narration (MP3, WAV, or M4A)", type=["mp3", "wav", "m4a"])

if audio_file:
    with open("temp_audio_input.mp3", "wb") as f:
        f.write(audio_file.read())
        
    st.audio("temp_audio_input.mp3", format="audio/mp3")
    
    if st.button("🚀 Process & Generate Storyboard"):
        with st.spinner("Step 1/3: Transcribing your audio via Whisper..."):
            try:
                with open("temp_audio_input.mp3", "rb") as audio_data:
                    transcript_response = client.audio.transcriptions.create(
                        model="whisper-1", 
                        file=audio_data
                    )
                transcript_text = transcript_response.text
                st.success("Audio successfully transcribed!")
                with st.expander("View Full Transcription Text"):
                    st.write(transcript_text)
            except Exception as e:
                st.error(f"Whisper Transcription Failed: {e}")
                st.stop()

        with st.spinner("Step 2/3: Structuring script and generating image prompts..."):
            try:
                system_prompt = f"You are an expert storyboard designer. Segment the following educational text into sequential, logical scenes. For each scene, create a detailed image generation prompt. To ensure visual continuity, force the image model to use the '{art_style}' style for all generated scenes."
                
                completion = client.beta.chat.completions.parse(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": transcript_text},
                    ],
                    response_format=Storyboard,
                )
                storyboard_data = completion.choices.message.parsed
            except Exception as e:
                st.error(f"LLM Scene Structuring Failed: {e}")
                st.stop()

        with st.spinner("Step 3/3: Rendering your custom AI artwork..."):
            st.subheader("🖼️ Generated Storyboard Canvas")
            
            for scene in storyboard_data.scenes:
                col1, col2 = st.columns()
                
                with col1:
                    st.markdown(f"### Scene {scene.scene_number}")
                    st.info(f"**Narration:** {scene.narration}")
                    with st.expander("View Meta Prompt"):
                        st.caption(scene.image_prompt)
                        
                with col2:
                    try:
                        image_response = client.images.generate(
                            model="dall-e-3",
                            prompt=scene.image_prompt,
                            n=1,
                            size="1024x1024"
                        )
                        image_url = image_response.data.url
                        st.image(image_url, use_column_width=True)
                    except Exception as e:
                        st.error(f"Failed to generate asset for Scene {scene.scene_number}: {e}")
                st.markdown("---")

    if os.path.exists("temp_audio_input.mp3"):
        os.remove("temp_audio_input.mp3")
