## 1. Project Setup

- [x] 1.1 Initialize Python project structure (src, tests, docs).
- [x] 1.2 Create `pyproject.toml` with dependencies (`pytesseract`, `pdf2image`, `PyMuPDF`, `typer`).
- [x] 1.3 Create a `Dockerfile` to install Tesseract OCR and Poppler system-level dependencies.
- [x] 1.4 Set up a basic `docker-compose.yml` for local development.

## 2. PDF Processing & Image Conversion

- [x] 2.1 Implement `PDFProcessor` class to manage PDF reading and metadata.
- [x] 2.2 Add functionality to `PDFProcessor` for extracting existing searchable text layers.
- [x] 2.3 Implement the page-to-image conversion logic using `pdf2image` with a 300 DPI default.

## 3. OCR Core Engine

- [x] 3.1 Implement `OCREngine` class to wrap `pytesseract`.
- [x] 3.2 Add multi-language support to `OCREngine` through language selection flags.
- [x] 3.3 Implement text sanitization and basic cleanup after extraction.

## 4. CLI Interface Development

- [x] 4.1 Scaffold the CLI using `Typer` with a `convert` command.
- [x] 4.2 Implement the single-file conversion workflow in the CLI.
- [x] 4.3 Implement the directory (batch) processing workflow in the CLI.
- [x] 4.4 Add logging and progress bars to the CLI output.

## 5. Verification & Testing

- [x] 5.1 Create unit tests for `PDFProcessor` and `OCREngine`.
- [x] 5.2 Create integration tests for the full pipeline using a sample PDF.
- [x] 5.3 Verify batch processing correctly handles mixed (searchable vs. scanned) PDF files.
