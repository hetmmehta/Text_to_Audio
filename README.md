# 🎵 Text to Speech Converter

A modern web application that converts text, PDF, Word, and EPUB documents into high-quality audio recordings with customizable voice options. Built with Flask and featuring a beautiful, responsive UI.

## ✨ Features

- **Multiple File Formats**: Support for PDF, Word (.docx, .doc), EPUB (.epub), and plain text files
- **Voice Selection**: Choose from multiple voices including male/female options and regional accents
- **Direct Text Input**: Convert text directly by typing or pasting
- **Drag & Drop**: Easy file upload with drag and drop functionality
- **High-Quality Audio**: Uses Google Text-to-Speech (gTTS) for natural-sounding audio
- **Download Audio**: Download converted audio files as MP3
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Real-time Preview**: Play audio directly in the browser
- **Modern UI**: Beautiful gradient design with smooth animations

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
text-to-speech-converter/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
├── uploads/              # Temporary file upload directory
└── audio/                # Generated audio files directory
```

## 🛠️ How It Works

### Backend (Flask)
- **File Processing**: Extracts text from PDF, Word, EPUB, and text files
- **Text-to-Speech**: Converts extracted text to audio using gTTS with voice selection
- **API Endpoints**: 
  - `/convert` - Handles file uploads and conversion
  - `/convert-text` - Handles direct text input conversion
  - `/voice-options` - Provides available voice options

### Frontend (HTML/CSS/JavaScript)
- **Modern UI**: Responsive design with gradient backgrounds and smooth animations
- **File Upload**: Drag-and-drop interface with visual feedback
- **Voice Selection**: Dropdown menus for choosing different voices and accents
- **Audio Player**: Built-in audio player for immediate playback
- **Download Functionality**: One-click audio download

## 📋 Supported Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| PDF | `.pdf` | Portable Document Format |
| Word | `.docx`, `.doc` | Microsoft Word documents |
| EPUB | `.epub` | Electronic Publication format |
| Text | `.txt` | Plain text files |

## 🎤 Voice Options

The application supports multiple voice options with different accents and regional variations:

### Female Voices
- **English (US, Female)** - Standard American English
- **English (UK, Female)** - British English
- **English (AU, Female)** - Australian English
- **English (IN, Female)** - Indian English

### Male Voices & Regional Accents
- **English (US, Male)** - American English
- **English (UK, Male)** - British English (RP)
- **English (UK, North)** - Northern British accent
- **English (UK, Scotland)** - Scottish accent
- **English (UK, London)** - London accent
- **English (UK, Leeds)** - Leeds accent
- **English (UK, Manchester)** - Manchester accent
- **English (UK, Lancashire)** - Lancashire accent
- **English (UK, Liverpool)** - Liverpool accent
- **English (UK, Geordie)** - Geordie accent

## 🎯 Usage

### Converting Files
1. Click the "Upload File" tab
2. Drag and drop a file or click to browse
3. Select your preferred voice from the dropdown
4. Click "Convert to Audio"
5. Wait for processing to complete
6. Play the audio or download it

### Converting Text
1. Click the "Enter Text" tab
2. Type or paste your text
3. Select your preferred voice from the dropdown
4. Click "Convert to Audio"
5. Play the audio or download it

## 🔧 Configuration

### File Size Limits
- Maximum file size: 16MB (configurable in `app.py`)
- Supported file types: PDF, Word, EPUB, Text

### Audio Settings
- Language: English (multiple accents)
- Speed: Normal
- Format: MP3
- Voice Selection: Multiple options available

## 🐛 Troubleshooting

### Common Issues

1. **"No text could be extracted"**
   - Ensure the file contains readable text
   - Check if the file is corrupted
   - Try a different file format

2. **"Failed to convert text to speech"**
   - Check your internet connection (gTTS requires internet)
   - Ensure the text is not empty
   - Try with shorter text first

3. **File upload issues**
   - Check file size (max 16MB)
   - Ensure file format is supported
   - Try refreshing the page

4. **EPUB extraction issues**
   - Ensure the EPUB file is not DRM-protected
   - Check if the EPUB contains text (not just images)
   - Try a different EPUB file

### Dependencies Issues
If you encounter dependency issues:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 🌟 Features in Detail

### Text Extraction
- **PDF**: Uses PyPDF2 to extract text from all pages
- **Word**: Uses python-docx to extract text from paragraphs
- **EPUB**: Uses EbookLib and BeautifulSoup to extract text from chapters
- **Text**: Direct file reading with UTF-8 encoding

### Audio Generation
- **Engine**: Google Text-to-Speech (gTTS)
- **Quality**: High-quality natural-sounding speech
- **Format**: MP3 for broad compatibility
- **Voice Options**: Multiple accents and regional variations
- **Delivery**: Base64 encoded for browser playback

### User Experience
- **Loading States**: Visual feedback during processing
- **Error Handling**: Clear error messages
- **Responsive Design**: Works on all screen sizes
- **Accessibility**: Keyboard navigation and screen reader friendly
- **Voice Selection**: Intuitive dropdown interface

## 🔒 Security Features

- File type validation
- Secure filename handling
- Temporary file cleanup
- Input sanitization
- Maximum file size limits

## 📈 Performance

- Asynchronous file processing
- Efficient text extraction
- Optimized audio generation
- Minimal memory footprint
- Fast voice switching

## 🤝 Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Improving documentation
- Submitting pull requests

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Google Text-to-Speech (gTTS) for audio generation
- Flask for the web framework
- PyPDF2 for PDF text extraction
- python-docx for Word document processing
- EbookLib for EPUB file processing
- BeautifulSoup for HTML parsing

---

**Enjoy converting your documents to audio with your favorite voice! 🎵**