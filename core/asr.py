import whisper
import streamlit as st

@st.cache_resource(show_spinner="Loading Whisper model...")
def load_model():
    return whisper.load_model("base")

def transcribe(audio_path):
    model = load_model()
    result = model.transcribe(
        audio_path,
        language="en",
        fp16=False
    )
    return result["text"].strip(), result["segments"]
