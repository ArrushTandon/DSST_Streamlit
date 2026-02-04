import whisper

_model = None

def load_model():
    global _model
    if _model is None:
        _model = whisper.load_model("base")
    return _model

def transcribe(audio_path):
    model = load_model()
    result = model.transcribe(
        audio_path,
        language="en",
        fp16=False
    )
    return result["text"].strip(), result["segments"]
