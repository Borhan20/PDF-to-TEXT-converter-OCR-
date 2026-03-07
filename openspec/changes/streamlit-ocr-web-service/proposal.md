## Why

The existing OCR PDF-to-Text tool is currently a CLI application, which limits its accessibility to non-technical users and lacks real-time interactive verification features. Transitioning to a Streamlit-based web service will provide a "zero-install" experience, allow for side-by-side visual verification of OCR results, and enable broader public usage with necessary safety constraints (file size and page limits).

## What Changes

*   **New Web UI**: Implementation of a Streamlit interface replacing the Typer-based CLI for public usage.
*   **Side-by-Side Viewer**: A new interactive layout allowing users to see the original PDF page next to the extracted and editable text.
*   **Public Usage Constraints**: Enforcement of a 20MB file size limit and a 50-page count limit per upload.
*   **Session-Based Persistence**: Implementation of client-side state management using Streamlit's session state to persist data across refreshes without server-side storage.
*   **Language Selection**: A UI component to select the document language for optimized OCR processing.
*   **Download Capability**: A dedicated button to export the finalized text as a `.txt` file.

## Capabilities

### New Capabilities
- `web-ui-scaffolding`: Basic Streamlit app structure with file upload and validation logic.
- `interactive-ocr-viewer`: Side-by-side layout for PDF page rendering and text editing.
- `session-state-persistence`: Management of uploaded content and OCR results within the browser session.
- `multilingual-ocr-config`: UI and backend logic for selecting and applying Tesseract language packs.

### Modified Capabilities
- `ocr-engine-core`: Updating the existing OCR engine to support single-page processing triggered by UI events rather than just batch CLI commands.
- `pdf-processing-service`: Adapting the PDF processor to handle in-memory file objects from Streamlit and providing fast page-to-image conversion for the UI.

## Impact

*   **src/ocr_pdf_converter/cli.py**: Will be superseded by a new `app.py` for the web interface (though the CLI core logic may remain as a library).
*   **src/ocr_pdf_converter/pdf_processor.py**: Needs to handle `UploadedFile` objects from Streamlit.
*   **src/ocr_pdf_converter/ocr_engine.py**: Needs to expose methods for granular, page-by-page OCR.
*   **Dependencies**: Addition of `streamlit` and potentially `streamlit-pydantic` or other UI helpers.
*   **Docker Configuration**: Update to expose the Streamlit port (8501) and include Tesseract language packs.
