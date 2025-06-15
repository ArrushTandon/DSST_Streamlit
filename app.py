import streamlit as st
import whisper
import librosa
import Levenshtein
import os
import tempfile
import re

st.set_page_config(page_title="DSST Web App", layout="centered")

# 🌐 Custom Style
st.markdown("""
    <style>
    h1, h2, h3 {
        color: #356df3;
    }
    .main {
        padding: 20px;
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# 📦 Load Whisper once
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

# 🔧 Helper Functions
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.split()

def is_move_intent(tokens):
    return any(token in tokens for token in ['move', 'go', 'forward', 'ascend', 'up', 'advance', 'fly', 'down', 'descend'])

def extract_commands(tokens):
    actions = []
    i = 0
    while i < len(tokens):
        if tokens[i] in ['move', 'go', 'advance', 'fly', 'ascend', 'descend']:
            action = {'action': tokens[i]}
            if i+1 < len(tokens) and tokens[i+1] in ['up', 'forward', 'backward', 'down']:
                action['direction'] = tokens[i+1]
                i += 2
            else:
                action['direction'] = None
                i += 1
            if i < len(tokens) and tokens[i] == 'by':
                if i+2 < len(tokens) and tokens[i+1].isdigit():
                    action['distance'] = int(tokens[i+1])
                    i += 3
                else:
                    action['distance'] = None
                    i += 1
            else:
                action['distance'] = None
            actions.append(action)
        else:
            i += 1
    return actions

def calculate_cer(predicted, reference):
    if not reference.strip():
        return None
    return Levenshtein.distance(predicted.lower(), reference.lower()) / len(reference)

def transcribe_audio(audio_path):
    audio, sr = librosa.load(audio_path, sr=None)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    result = whisper.decode(model, mel, whisper.DecodingOptions(fp16=False))
    return result.text.strip()

# -------------------- UI Layout --------------------

st.title("🧠 DSST - Domain-Specific Speech Transcription")

tab1, tab2, tab3 = st.tabs(["🏠 Welcome", "📤 Upload & Transcribe", "⚙️ Settings"])

# ---------- 🏠 Welcome ----------
with tab1:
    st.header("Welcome to the DSST Web App")
    st.write("""
    This tool allows you to:
    - 🎙 Upload an audio command (e.g. "move forward by 3 meters")
    - 📜 Automatically transcribe it using OpenAI's Whisper
    - 🧠 Extract robot movement instructions from natural speech
    - 📉 (Optional) Compare with ground truth and calculate CER

    Built by **Arrush Tandon** using Python, Whisper, Streamlit, and 💡 a passion for innovation.
    """)
    st.info("Head to the **Upload & Transcribe** tab to get started!")

# ---------- 📤 Upload & Transcribe ----------
with tab2:
    col1, col2 = st.columns([2, 3])
    with col1:
        uploaded_audio = st.file_uploader("🎧 Upload Audio", type=["wav", "mp3", "m4a", "flac"])
    with col2:
        ground_truth = st.text_area("✍ Paste Ground Truth (Optional)", height=120)

    if uploaded_audio:
        with st.spinner("Transcribing..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(uploaded_audio.read())
                tmp_path = tmp.name
            transcription = transcribe_audio(tmp_path)
            try:
                os.remove(tmp_path)
            except Exception as e:
                st.warning(f"Could not delete temp file: {e}")

        st.subheader("📜 Transcription")
        st.code(transcription)

        if ground_truth:
            cer = calculate_cer(transcription, ground_truth)
            st.metric("CER (Character Error Rate)", f"{cer:.4f}")

        tokens = preprocess_text(transcription)
        if is_move_intent(tokens):
            commands = extract_commands(tokens)
            st.subheader("🤖 Extracted Robot Commands")
            st.json(commands)
        else:
            st.warning("No movement intent detected.")

# ---------- ⚙️ Settings ----------
with tab3:
    st.header("App Settings")
    st.write("Model used: `base` (OpenAI Whisper)")
    st.write("Built with 💙 using Streamlit.")
    st.caption("For more, contact: arrushtandon@gmail.com")
