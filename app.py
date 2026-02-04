import streamlit as st
import librosa
import os
import tempfile
from core.robot_parser import is_robot_intent, extract_commands
from core.preprocessing import normalize
from core.asr import transcribe
from core.metrics import cer

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
    robot_mode = st.toggle(
        "🤖 Robot Command Mode",
        value=False,
        help="Turn ON for robot movement commands. Keep OFF for normal speech."
    )

    col1, col2 = st.columns([2, 3])
    with col1:
        uploaded_audio = st.file_uploader(
            "🎧 Upload Audio",
            type=["wav", "mp3", "m4a", "flac"]
        )
    with col2:
        ground_truth = st.text_area(
            "✍ Paste Ground Truth (Optional)",
            height=120
        )

    if uploaded_audio:
        with st.spinner("Transcribing..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(uploaded_audio.read())
                tmp_path = tmp.name

            transcription, segments = transcribe(tmp_path)

            try:
                os.remove(tmp_path)
            except Exception as e:
                st.warning(f"Could not delete temp file: {e}")

        # ---------- Transcription ----------
        st.subheader("📜 Transcription")
        st.code(transcription)

        # ---------- CER ----------
        if ground_truth:
            cer_score = cer(transcription, ground_truth)
            if cer_score is not None:
                st.metric(
                    "CER (Character Error Rate)",
                    f"{cer_score:.4f}"
                )

        # ---------- Robot Command Parsing (STRICTLY OPTIONAL) ----------
        if robot_mode:
            segmented_commands = []

            for seg in segments:
                seg_text = seg["text"]
                tokens = normalize(seg_text)

                if is_robot_intent(tokens):
                    cmds = extract_commands(tokens)
                    for c in cmds:
                        c["start_time"] = round(seg["start"], 2)
                        c["end_time"] = round(seg["end"], 2)
                        c["source_text"] = seg_text
                        segmented_commands.append(c)

            if segmented_commands:
                st.subheader("🤖 Segmented Robot Commands")
                st.json(segmented_commands)
            else:
                st.warning(
                    "Robot mode is ON, but no valid robot commands were detected."
                )

# ---------- ⚙️ Settings ----------
with tab3:
    st.header("App Settings")
    st.write("Model used: `base` (OpenAI Whisper)")
    st.write("Built with 💙 using Streamlit.")
    st.caption("For more, contact: arrush6674@gmail.com")
