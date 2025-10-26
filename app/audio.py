""" Module for managing audio functionalities such as speech-to-text and text-to-speech. """
from gtts import gTTS
import os
import warnings
import whisper
import sys
from pathlib import Path
import torch

def text_to_speech(text: str, lang: str = 'en') -> bytes:
    """ Convert text to speech using gTTS and return audio data as raw bytes (MP3). """
    from gtts import gTTS
    from io import BytesIO

    tts = gTTS(text=text, lang=lang)
    audio_io = BytesIO()
    tts.write_to_fp(audio_io)
    audio_io.seek(0)
    return audio_io.getvalue()

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes audio file (MP3, WAV, etc.) into text using Whisper.

    Args:
        file_path (str): Path to audio file.

    Returns:
        str: Transcribed text.
    """
    file = Path(file_path)
    if not file.exists():
        return f"File not found: {file_path}"

    # Choose model via env var so it's easy to lower resource usage on CPU-only hosts
    model_name = os.getenv("TRANSCRIBE_MODEL", "small")
    print(f"Loading Whisper model '{model_name}'...")

    # Suppress FP16->FP32 CPU warning from whisper (harmless on CPU but noisy)
    warnings.filterwarnings(
        "ignore",
        message="FP16 is not supported on CPU; using FP32 instead"
    )

    model = whisper.load_model(model_name)
    # Ensure model parameters are float32 (avoid any half-precision surprises)
    try:
        model.float()
    except Exception:
        # If the model object doesn't support .float(), ignore silently
        pass
    
    # Transkrypcja
    result = model.transcribe(str(file))
    
    return result['text']

# Pozwala uruchomić z konsoli: python transcribe.py audio.mp3
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py path_to_audio")
    else:
        audio_file = sys.argv[1]
        transcription = transcribe_audio(audio_file)
        print("Transcription:\n", transcription)
