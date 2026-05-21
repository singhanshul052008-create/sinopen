# 📸 Image to PDF Converter

A simple and elegant web application to convert multiple images into a single PDF document with download functionality.

## Features

- ✅ Convert multiple images to PDF
- ✅ Drag & drop image upload
- ✅ Image preview before conversion
- ✅ One-click PDF download
- ✅ Support for PNG, JPG, GIF, BMP, WebP formats
- ✅ Automatic image optimization
- ✅ Responsive design
- ✅ Error handling

## Requirements

- Python 3.7+
- Flask
- Pillow
- ReportLab

## Installation

1. Clone the repository:
```bash
git clone https://github.com/singhanshul052008-create/sinopen.git
cd sinopen
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Upload images using:
   - Click to select files
   - Drag and drop images
   - Multiple image selection

4. Click "Convert to PDF" to generate and download the PDF

## API Endpoints

### POST /convert
Converts uploaded images to PDF

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Parameter: `images` (multiple files)

**Response:**
- Success: PDF file download
- Error: JSON with error message

### GET /health
Health check endpoint

**Response:**
```json
{
  "status": "ok"
}
```

## Supported Image Formats

- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- BMP (.bmp)
- WebP (.webp)

## File Size Limits

- Maximum file size: 10MB per image
- Maximum total request size: 50MB

## Project Structure

```
sinopen/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
└── templates/
    └── index.html        # Frontend UI
```

## Deployment

### Using Gunicorn (Production)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t img2pdf .
docker run -p 5000:5000 img2pdf
```

## Troubleshooting

**Issue: "No module named 'flask'"**
- Solution: Install dependencies with `pip install -r requirements.txt`

**Issue: "Address already in use"**
- Solution: Change the port in `app.py` or kill the process using port 5000

**Issue: Images not converting**
- Check file format is supported
- Verify image file is not corrupted
- Check browser console for errors

## Browser Compatibility

- Chrome/Edge (Latest)
- Firefox (Latest)
- Safari (Latest)
- Mobile browsers

## License

MIT License

## Author

Anshul Singh
