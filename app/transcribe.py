import whisper
import sys
from pathlib import Path

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

    # Załaduj model (można też 'small', 'medium', 'large' w zależności od wydajności)
    model = whisper.load_model("base")
    
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
