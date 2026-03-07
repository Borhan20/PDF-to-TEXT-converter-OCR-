## Why

Users need an efficient, cost-effective (offline) method to extract text from non-searchable or scanned PDF documents to enable searchability, data extraction, and archival.

## What Changes

- Implement a Python-based CLI tool to convert PDF files into plain text.
- Integrate **Tesseract OCR** for text recognition in images and scanned pages.
- Utilize **PyMuPDF** and **pdf2image** for handling PDF document layers and page-to-image conversion.
- Support for single-file and directory-level (batch) processing.

## Capabilities

### New Capabilities
- `ocr-engine`: Core logic for image-to-text extraction using Tesseract with support for multiple languages.
- `pdf-processor`: Module for extracting metadata, existing text layers, and converting PDF pages into high-resolution images for OCR.
- `cli-interface`: Typer-based command-line interface for managing input/output paths and processing options.

### Modified Capabilities
- (none)

## Impact

- **Dependencies**: Requires `pytesseract`, `pdf2image` (with Poppler), and `PyMuPDF`.
- **Infrastructure**: New Docker container definition to bundle Tesseract and Poppler system dependencies.
- **Environment**: Local file system access for reading PDFs and writing `.txt` files.
