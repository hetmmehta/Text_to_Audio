import os
import tempfile
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import PyPDF2
from docx import Document
from gtts import gTTS
import io
import base64

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['AUDIO_FOLDER'] = 'audio'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'doc'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(file_path, file_extension):
    """Extract text from different file formats"""
    text = ""
    
    try:
        if file_extension == 'txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        
        elif file_extension == 'pdf':
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        
        elif file_extension in ['docx', 'doc']:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        
        return text.strip()
    
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def text_to_speech(text, language='en'):
    """Convert text to speech and return audio data"""
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        
        # Save to a temporary file-like object
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        return audio_buffer
    
    except Exception as e:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_to_audio():
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not supported'}), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name
        
        # Extract text from file
        extracted_text = extract_text_from_file(temp_file_path, file_extension)
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        if not extracted_text or extracted_text.startswith("Error"):
            return jsonify({'error': extracted_text or 'No text could be extracted'}), 400
        
        # Convert text to speech
        audio_buffer = text_to_speech(extracted_text)
        
        if audio_buffer is None:
            return jsonify({'error': 'Failed to convert text to speech'}), 500
        
        # Convert audio to base64 for sending to frontend
        audio_data = base64.b64encode(audio_buffer.getvalue()).decode('utf-8')
        
        return jsonify({
            'success': True,
            'text': extracted_text,
            'audio_data': audio_data,
            'filename': filename
        })
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/convert-text', methods=['POST'])
def convert_text_to_audio():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Convert text to speech
        audio_buffer = text_to_speech(text)
        
        if audio_buffer is None:
            return jsonify({'error': 'Failed to convert text to speech'}), 500
        
        # Convert audio to base64 for sending to frontend
        audio_data = base64.b64encode(audio_buffer.getvalue()).decode('utf-8')
        
        return jsonify({
            'success': True,
            'audio_data': audio_data
        })
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)