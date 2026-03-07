# 📄 OCR PDF-to-Text Web Service

An interactive web application built with **Streamlit** to convert scanned PDF documents into plain text using **Tesseract OCR**. Features a side-by-side verification viewer and support for multiple languages.

## ✨ Features

-   **Interactive Web UI**: Drag-and-drop PDF upload with real-time feedback.
-   **Side-by-Side Viewer**: View the original PDF page next to the editable OCR result.
-   **Batch Processing**: Run OCR for all pages at once or on a page-by-page basis.
-   **Multi-Language Support**: Optimized for English, Spanish, French, and German.
-   **Text Layer Extraction**: Instantly extract text from searchable PDFs without full OCR.
-   **Session Persistence**: Your work persists across browser refreshes (client-side state).
-   **Privacy-First**: No files are stored permanently on the server.

## 🛠️ System Dependencies

Before running the application, ensure you have the following installed on your system:

### **Linux (Ubuntu/Debian)**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-spa tesseract-ocr-fra tesseract-ocr-deu poppler-utils
```

### **macOS**
```bash
brew install tesseract poppler
```

### **Windows**
1.  Download and install the **Tesseract OCR** installer from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
2.  Add the Tesseract installation folder (usually `C:\Program Files\Tesseract-OCR`) to your system **PATH**.

---

## 🚀 Setup & Usage

### 1. Local Environment
Create a virtual environment and install the Python dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows

pip install .
```

### 2. Run the Web Application
Launch the Streamlit app:
```bash
streamlit run src/ocr_pdf_converter/app.py
```
The app will open in your default browser at `http://localhost:8501`.

### 3. Run the CLI Tool (Legacy)
The original CLI tool is still available for automated batch processing:
```bash
ocr-pdf convert path/to/document.pdf --output result.txt
```

---

## 🐳 Docker Support

Build and run the application using Docker:

```bash
docker build -t ocr-pdf-web .
docker run -p 8501:8501 ocr-pdf-web
```
Visit `http://localhost:8501` to use the application.

## 📁 Project Structure

-   `src/ocr_pdf_converter/app.py`: Streamlit web interface and session management.
-   `src/ocr_pdf_converter/ocr_engine.py`: Tesseract wrapper and text sanitization.
-   `src/ocr_pdf_converter/pdf_processor.py`: PDF rendering and text layer extraction.
-   `src/ocr_pdf_converter/cli.py`: Legacy Typer-based CLI interface.
