## Context

The `ocr-pdf-converter` tool is designed to provide an efficient and free (offline) solution for extracting text from non-searchable or scanned PDF documents. This is a common requirement for digitizing physical archives and enabling text-based search on scanned materials.

## Goals / Non-Goals

**Goals:**
- Extract machine-readable text from PDF pages (both scanned and searchable).
- Provide a robust CLI interface for single and batch file processing.
- Ensure the system is portable using Docker to manage complex external dependencies like Tesseract and Poppler.

**Non-Goals:**
- **Layout Preservation**: Maintaining complex layouts like multi-column structures or tables is out of scope for the MVP.
- **Cloud Integration**: Direct integration with cloud OCR services (Google Vision, AWS Textract) is deferred to future versions.
- **Handwriting Recognition**: The tool is primarily optimized for machine-printed text.

## Decisions

- **Language: Python 3.11**: Chosen for its wide availability of OCR and PDF manipulation libraries.
- **OCR Engine: Tesseract 5**: Best-in-class open-source OCR engine with multi-language support.
- **Image Conversion: pdf2image (Poppler)**: Converts PDF pages to high-quality images (300 DPI) to optimize Tesseract's recognition accuracy.
- **PDF Layer Extraction: PyMuPDF**: Enables fast extraction of existing text layers for "searchable" PDFs, bypassing slow OCR when possible.
- **CLI Framework: Typer**: Provides a modern, easy-to-use CLI with automatic help generation and type validation.
- **Architecture: Sequential Pipeline**:
  1.  Validate input path (file or directory).
  2.  Extract existing text layer using PyMuPDF (if available).
  3.  If text is missing or poor quality, convert PDF page to image (pdf2image).
  4.  Perform OCR on the image (pytesseract).
  5.  Write aggregated text to a `.txt` file.

## Risks / Trade-offs

- **[Risk] Low OCR Accuracy on Poor Scans** → [Mitigation] Enforce a minimum 300 DPI resolution during conversion and provide a language selection flag.
- **[Risk] Heavy System Dependencies (Tesseract, Poppler)** → [Mitigation] Provide a Dockerfile and a `docker-compose.yml` for simplified setup across different operating systems.
- **[Risk] Performance on Large PDFs** → [Mitigation] Implement page-by-page processing with intermittent status updates to the user.
