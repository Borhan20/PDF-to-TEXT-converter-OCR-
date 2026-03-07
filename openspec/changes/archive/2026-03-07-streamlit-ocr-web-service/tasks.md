## 1. Environment & Dependency Setup

- [ ] 1.1 Add `streamlit` and `Pillow` to `pyproject.toml` dependencies.
- [ ] 1.2 Update `Dockerfile` to install Tesseract language packs (spa, fra, deu) and expose port 8501.
- [ ] 1.3 Install new dependencies in the local `.venv`.

## 2. Web UI Scaffolding

- [ ] 2.1 Create `src/ocr_pdf_converter/app.py` with basic Streamlit page configuration.
- [ ] 2.2 Implement `st.file_uploader` with 20MB size and 50-page limit validation logic.
- [ ] 2.3 Implement sidebar with language selection dropdown.

## 3. Interactive Viewer & State Management

- [ ] 3.1 Initialize `st.session_state` keys for `pdf_content`, `page_index`, and `ocr_results`.
- [ ] 3.2 Implement side-by-side columns (`st.columns([1, 1])`).
- [ ] 3.3 Add logic to render the current PDF page image using `PyMuPDF` in the left column.
- [ ] 3.4 Add navigation buttons (Previous/Next) with bounds checking.

## 4. OCR Integration & Download

- [ ] 4.1 Update `OCREngine` to accept a bytes-like object or integrate with Streamlit's file buffer.
- [ ] 4.2 Implement "Run OCR" button that triggers processing for the current page only.
- [ ] 4.3 Implement "Download Results" button that aggregates all session text into a `.txt` file.

## 5. Verification & Finalization

- [ ] 5.1 Manual verification of upload limits and error messages.
- [ ] 5.2 Verify persistence of OCR results across page navigation and refreshes.
- [ ] 5.3 Verify Docker build and containerized application launch.
