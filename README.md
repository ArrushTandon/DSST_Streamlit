
# 🧠 DSST - Domain-Specific Speech Transcription Using Whisper

This project implements **Domain-Specific Speech Transcription (DSST)** using OpenAI's Whisper model. It transcribes audio commands, extracts **robot movement instructions**, calculates **Character Error Rate (CER)**, and presents everything through a **Streamlit-powered web app**.

---

## 🌐 Live App

👉 [Launch DSST Web App](https://dsst-streamlit-yourusername.streamlit.app)

---

## 📦 Features

- 🎙 **Whisper-based transcription** for `.wav`, `.mp3`, `.flac`, etc.
- 🤖 **NLP-based command extraction** for robotics use cases
- 📉 **CER evaluation** using Levenshtein distance
- 🧪 Optional ground truth comparison for accuracy checking
- 🧵 Modular Python architecture with reusable components
- 💻 Web UI built with **Streamlit** and deployed on **Streamlit Cloud**
- 🎨 Tab-based UI with landing page, upload interface, and settings

---

## 🗂️ Folder Structure

```
dsst_streamlit/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Theme config (dark mode)
├── core/
│   ├── transcriber.py
│   ├── cer_calculator.py
│   ├── nlp_processor.py
│   └── file_utils.py
├── main/
│   ├── robot_runner.py
│   ├── batch_nptel_runner.py
│   └── folder_eval_runner.py
```

---

## 🚀 Try It Locally

### 1. Clone the repository
```bash
git clone https://github.com/ArrushTandon/DSST_Streamlit.git
cd DSST_Streamlit
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

### 3. Install requirements
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

---

## 📋 How It Works

### 🎤 Audio Input
Upload an audio file containing natural spoken commands (e.g., "move forward by 3 meters").

### 🔎 Transcription
Whisper transcribes audio using the `"base"` model.

### 🧠 Command Extraction
Natural Language Processing extracts structured robot commands using rules.

### 📉 CER Calculation (Optional)
If ground truth is provided, CER is calculated for evaluation.

---

## 💻 Streamlit UI

| Tab | Description |
|-----|-------------|
| 🏠 **Welcome** | Intro, project info, usage |
| 📤 **Upload & Transcribe** | Upload audio + ground truth, see results |
| ⚙️ **Settings** | About, model details |

---

## ⚙️ Tech Stack

- [x] 🧠 Whisper (OpenAI)
- [x] 🔊 Librosa for audio loading
- [x] ✂ Levenshtein for CER
- [x] ⚙ Python 3.11
- [x] 🌐 Streamlit for the web app

---

## 📈 Evaluation Metric

**Character Error Rate (CER)**:
```text
CER = (Insertions + Deletions + Substitutions) / Total Characters
```

Lower CER = Better transcription accuracy ✅

---

## 📄 License

MIT License (or your preferred license here)

---

## 🤝 Contributing

Got ideas? Found a bug?  
Feel free to fork this repo, submit an issue, or create a pull request.

---

## 🙋‍♂️ Author

**Arrush Tandon**  
📧 arrush6674@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/arrush-tandon/)

---

> “Turning voice into understanding — one command at a time.” 🎙️🤖
