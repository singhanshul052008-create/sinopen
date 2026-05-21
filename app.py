from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Image as RLImage, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import os
from werkzeug.utils import secure_filename
import logging

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    """Convert uploaded images to PDF"""
    try:
        if 'images' not in request.files:
            return jsonify({'error': 'No files provided'}), 400

        files = request.files.getlist('images')
        
        if not files or files[0].filename == '':
            return jsonify({'error': 'No selected files'}), 400

        # Validate files
        valid_files = []
        for file in files:
            if file and allowed_file(file.filename):
                valid_files.append(file)

        if not valid_files:
            return jsonify({'error': 'No valid image files'}), 400

        # Create PDF
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=A4,
            rightMargin=20,
            leftMargin=20,
            topMargin=20,
            bottomMargin=20
        )

        elements = []
        styles = getSampleStyleSheet()

        for idx, file in enumerate(valid_files):
            try:
                # Open image
                img = Image.open(file)
                
                # Optimize image size
                max_width, max_height = 550, 750
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

                # Save to bytes
                img_buffer = BytesIO()
                img.save(img_buffer, format='PNG')
                img_buffer.seek(0)

                # Add to PDF
                rl_img = RLImage(img_buffer, width=550, height=410)
                elements.append(rl_img)

                if idx < len(valid_files) - 1:
                    elements.append(PageBreak())
            
            except Exception as e:
                logger.error(f"Error processing file {file.filename}: {str(e)}")
                continue

        if not elements:
            return jsonify({'error': 'Could not process any images'}), 400

        # Build PDF
        doc.build(elements)
        pdf_buffer.seek(0)

        logger.info(f"Successfully converted {len(valid_files)} images to PDF")
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='converted-images.pdf'
        )

    except Exception as e:
        logger.error(f"Error converting images: {str(e)}")
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
