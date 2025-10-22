from flask import Flask, render_template, jsonify, request
import os
from werkzeug.utils import secure_filename
from transcribe import transcribe_audio
from utils import call_llm
UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title="Home Page", user="Alice")

@app.route('/upload')
def upload():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio']
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    question = transcribe_audio(filepath)
    answer = call_llm(question=question)
    return answer

   
if __name__ == '__main__':
    app.run(debug=True)