from flask import render_template, jsonify, request, send_file
import os
from werkzeug.utils import secure_filename
from . import app
from .audio import text_to_speech, transcribe_audio
from .utils import call_llm
import io

UPLOAD_FOLDER = 'uploads'

@app.route('/')
def home():
    return render_template('index.html', title="Home Page", user="Alice")


@app.route('/upload', methods=['POST'])
def upload():
    """Accept an uploaded audio file, transcribe it, call the LLM and return JSON.

    Expects form field named 'file' (matching the client-side FormData key).
    """
    try:
        # Ensure upload folder exists
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        if 'file' not in request.files:
            return jsonify({'error': 'No audio file provided (expected form key "file")'}), 400

        file = request.files.get('file')
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        app.logger.info(f"File saved to {filepath}")

        # Transcribe and call LLM
        question = transcribe_audio(filepath)
        answer = call_llm(question=question)
        app.logger.info(f"Q: {question}\nA: {answer}")

        # Try to return MP3 bytes; if TTS fails, return JSON for speechSynthesis fallback
        try:
            audio_bytes = text_to_speech(answer, lang='en')
            if hasattr(audio_bytes, 'read'):
                # It's already a BytesIO-like object
                audio_bytes.seek(0)
                return send_file(audio_bytes, mimetype='audio/mpeg', as_attachment=False, download_name='answer.mp3')
            else:
                # It's raw bytes, wrap in BytesIO
                mp3_io = io.BytesIO(audio_bytes)
                mp3_io.seek(0)
                return send_file(mp3_io, mimetype='audio/mpeg', as_attachment=False, download_name='answer.mp3')
        except Exception as tts_error:
            # TTS failed (network issue, gTTS error, etc.)
            # Return JSON so frontend can use Web Speech API (speechSynthesis)
            app.logger.warning(f"TTS failed ({tts_error}), returning text for speechSynthesis")
            return jsonify({'answer': answer})

    except Exception as e:
        app.logger.exception("Error handling upload")
        return jsonify({'error': str(e)}), 500