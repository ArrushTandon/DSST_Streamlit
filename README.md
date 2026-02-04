# 🧠 DSST – Domain-Specific Speech Transcription using Whisper

This project implements a **Domain-Specific Speech Transcription (DSST)** system using OpenAI’s **Whisper** model.  
It supports **general speech transcription** as well as **robot command transcription**, optional **command extraction**, and **Character Error Rate (CER)** evaluation — all through a **Streamlit-based web application**.

---

## 🌐 Live App

👉 **DSST Web App**  
https://dsstapp.streamlit.app/

---

## 📦 Key Features

- 🎙 **Speech transcription** using OpenAI Whisper (`base` model)
- 🔀 **Explicit mode selection**
  - **General Speech Mode** – transcription only
  - **Robot Command Mode** – transcription + command extraction
- 🤖 **Rule-based robot command extraction**
  - Action, direction, distance
  - Segment-level timestamps
- 📉 **Character Error Rate (CER)** calculation (optional)
- 🧪 Ground-truth comparison for evaluation
- 🧵 **Modular, production-style Python architecture**
- 💻 **Streamlit web UI**, deployed on Streamlit Cloud
- 🎨 Clean, tab-based interface

---

## 🗂️ Project Structure

```
dsst_streamlit/
├── app.py                    # Streamlit UI (entry point)
├── requirements.txt          # Dependencies
├── README.md
├── .streamlit/
│   └── config.toml           # Streamlit configuration
│
├── core/
│   ├── asr.py                # Whisper loading & transcription
│   ├── preprocessing.py      # Text normalization
│   ├── robot_parser.py       # Robot intent & command extraction
│   └── metrics.py            # CER calculation
│
└── utils/                    # (Reserved for future utilities)
```

---

## 🚀 Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/ArrushTandon/DSST_Streamlit.git
cd DSST_Streamlit
```

### 2️⃣ Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Launch the app
```bash
streamlit run app.py
```

---

## 🧭 How the System Works

### 🎤 Audio Input
Upload an audio file (`.wav`, `.mp3`, `.m4a`, `.flac`) containing spoken speech or commands.

---

### 🔀 Mode Selection

The user explicitly selects the processing mode:

- **General Speech Mode**
  - Transcription only
  - No intent detection or command parsing

- **Robot Command Mode**
  - Transcription
  - Segment-wise command extraction
  - Structured robot instructions with timestamps

This explicit toggle avoids accidental command parsing of normal speech.

---

### 🔎 Transcription (ASR)

Whisper transcribes the audio using the `"base"` model and produces:
- Full transcription text
- Time-aligned speech segments

---

### 🤖 Robot Command Extraction (Optional)

When **Robot Command Mode** is enabled:
- Each Whisper segment is processed independently
- Rule-based NLP extracts:
  - `action`
  - `direction`
  - `distance`
  - `start_time` / `end_time`
  - `source_text`

Example output:
```json
{
  "action": "move",
  "direction": "forward",
  "distance": 3,
  "start_time": 0.0,
  "end_time": 2.3
}
```

---

### 📉 Character Error Rate (CER)

If ground truth text is provided, **CER** is computed as:

```
CER = (Insertions + Deletions + Substitutions) / Total Characters
```

Lower CER indicates better transcription accuracy.

---

## 💻 Streamlit Interface

| Tab | Purpose |
|----|--------|
| 🏠 **Welcome** | Project overview and usage |
| 📤 **Upload & Transcribe** | Audio upload, mode selection, results |
| ⚙️ **Settings** | Model info and app details |

---

## ⚠️ Known Design Limitation

When **Robot Command Mode** is enabled, the system assumes **literal command intent**.  
As a result, metaphorical or abstract language (e.g., *“move forward as a team”*) may be parsed as robot commands.

This is an intentional design trade-off, prioritizing determinism and simplicity.

---

## ⚙️ Tech Stack

- 🧠 OpenAI Whisper
- 🔊 Librosa
- ✂️ Python-Levenshtein
- 🐍 Python 3.11
- 🌐 Streamlit

---

## 📄 License

MIT License

---

## 🙋‍♂️ Author

**Arrush Tandon**  
📧 arrush6674@gmail.com  
🔗 https://www.linkedin.com/in/arrush-tandon/

---

> *Turning speech into structured understanding — one domain at a time.* 🎙️🤖
