import streamlit as st
import whisper
import librosa
import Levenshtein
import os
import tempfile
import re
st.set_page_config(page_title="DSST Web App", layout="centered")
st.markdown("""
    <style>
    .main {
        padding: 30px;
        font-family: 'Segoe UI', sans-serif;
        color: #222;
    }
    h1 {
        color: #356df3;
        text-align: center;
    }
    .stTextArea, .stFileUploader, .stButton {
        margin-top: 15px;
    }
    .stTextArea textarea {
        font-size: 16px;
    }
    .stCode {
        background-color: #f3f3f3;
        padding: 12px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.split()

def is_move_intent(tokens):
    keywords = ['move', 'go', 'forward', 'ascend', 'up', 'advance', 'fly', 'down', 'descend']
    return any(token in keywords for token in tokens)

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

# --- Streamlit UI ---
st.title("🧠 DSST - Domain Specific Speech Transcription")

col1, col2 = st.columns([2, 3])

with col1:
    uploaded_audio = st.file_uploader("🎤 Upload Audio File", type=["wav", "mp3", "m4a", "flac"])

with col2:
    ground_truth = st.text_area("📝 Paste Ground Truth (Optional)", height=120)

if uploaded_audio:
    with st.spinner("🔍 Transcribing..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(uploaded_audio.read())
            tmp_path = tmp.name
        transcription = transcribe_audio(tmp_path)
        os.remove(tmp_path)

    st.subheader("📄 Transcription")
    st.code(transcription)

    if ground_truth:
        cer = calculate_cer(transcription, ground_truth)
        st.metric(label="📉 Character Error Rate", value=f"{cer:.4f}")

    tokens = preprocess_text(transcription)
    if is_move_intent(tokens):
        commands = extract_commands(tokens)
        st.subheader("🤖 Extracted Robot Commands")
        st.json(commands)
    else:
        st.warning("⚠️ No movement intent detected.")
