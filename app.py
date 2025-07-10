import os
import tempfile
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import PyPDF2
from docx import Document
from gtts import gTTS
import io
import base64
from ebooklib import epub

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['AUDIO_FOLDER'] = 'audio'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'doc', 'epub'}

# gTTS voice options (limited by language/accent)
# 'en' (default, female), 'en-uk' (UK female), 'en-us' (US female), 'en-au' (AU female), 'en-in' (Indian female), 'en-uk-rp' (UK male), 'en-uk-north' (UK male), 'en-uk-rp' (UK male), 'en-uk-wmids' (UK male), 'en-scotland' (Scottish), 'en-uk-london' (London), 'en-uk-leeds' (Leeds), 'en-uk-manc' (Manchester), 'en-uk-lancashire' (Lancashire), 'en-uk-liverpool' (Liverpool), 'en-uk-geordie' (Geordie)
# gTTS does not support true male/female selection, but some accents sound more male/female.
VOICE_OPTIONS = [
    {"label": "English (US, Female)", "value": "en"},
    {"label": "English (UK, Female)", "value": "en-uk"},
    {"label": "English (US, Male)", "value": "en-us"},
    {"label": "English (UK, Male)", "value": "en-uk-rp"},
    {"label": "English (AU, Female)", "value": "en-au"},
    {"label": "English (IN, Female)", "value": "en-in"},
    {"label": "English (UK, North)", "value": "en-uk-north"},
    {"label": "English (UK, Scotland)", "value": "en-scotland"},
    {"label": "English (UK, London)", "value": "en-uk-london"},
    {"label": "English (UK, Leeds)", "value": "en-uk-leeds"},
    {"label": "English (UK, Manchester)", "value": "en-uk-manc"},
    {"label": "English (UK, Lancashire)", "value": "en-uk-lancashire"},
    {"label": "English (UK, Liverpool)", "value": "en-uk-liverpool"},
    {"label": "English (UK, Geordie)", "value": "en-uk-geordie"},
]

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
        elif file_extension == 'epub':
            book = epub.read_epub(file_path)
            for item in book.get_items():
                if item.get_type() == epub.ITEM_DOCUMENT:
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    text += ' '.join([t for t in soup.stripped_strings]) + "\n"
        return text.strip()
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def text_to_speech(text, language='en'):
    """Convert text to speech and return audio data"""
    try:
        tts = gTTS(text=text, lang=language, tld='com', slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer
    except Exception as e:
        return None

def get_voice_params(voice_value):
    # Map UI voice value to gTTS language/accent
    # gTTS uses 'lang' and 'tld' (top-level domain) for accent
    # We'll use 'lang' for main language, and tld for accent if needed
    # Example: 'en', 'en-uk', 'en-us', etc.
    # For gTTS, tld can be 'com', 'co.uk', 'com.au', 'co.in', etc.
    # We'll map accordingly
    mapping = {
        'en': ('en', 'com'),
        'en-uk': ('en', 'co.uk'),
        'en-us': ('en', 'com'),
        'en-au': ('en', 'com.au'),
        'en-in': ('en', 'co.in'),
        'en-uk-rp': ('en', 'co.uk'),
        'en-uk-north': ('en', 'co.uk'),
        'en-scotland': ('en', 'co.uk'),
        'en-uk-london': ('en', 'co.uk'),
        'en-uk-leeds': ('en', 'co.uk'),
        'en-uk-manc': ('en', 'co.uk'),
        'en-uk-lancashire': ('en', 'co.uk'),
        'en-uk-liverpool': ('en', 'co.uk'),
        'en-uk-geordie': ('en', 'co.uk'),
    }
    return mapping.get(voice_value, ('en', 'com'))

def text_to_speech_with_voice(text, voice_value):
    lang, tld = get_voice_params(voice_value)
    try:
        tts = gTTS(text=text, lang=lang, tld=tld, slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer
    except Exception as e:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/voice-options')
def voice_options():
    return jsonify(VOICE_OPTIONS)

@app.route('/convert', methods=['POST'])
def convert_to_audio():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not supported'}), 400
        voice = request.form.get('voice', 'en')
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name
        extracted_text = extract_text_from_file(temp_file_path, file_extension)
        os.unlink(temp_file_path)
        if not extracted_text or extracted_text.startswith("Error"):
            return jsonify({'error': extracted_text or 'No text could be extracted'}), 400
        audio_buffer = text_to_speech_with_voice(extracted_text, voice)
        if audio_buffer is None:
            return jsonify({'error': 'Failed to convert text to speech'}), 500
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
        voice = data.get('voice', 'en')
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        audio_buffer = text_to_speech_with_voice(text, voice)
        if audio_buffer is None:
            return jsonify({'error': 'Failed to convert text to speech'}), 500
        audio_data = base64.b64encode(audio_buffer.getvalue()).decode('utf-8')
        return jsonify({
            'success': True,
            'audio_data': audio_data
        })
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)