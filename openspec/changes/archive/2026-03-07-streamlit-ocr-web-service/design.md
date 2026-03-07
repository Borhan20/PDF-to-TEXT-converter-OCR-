## Context

The current system is a Python-based CLI tool using `pytesseract` and `PyMuPDF`. While functional, it is not accessible to the general public. We are migrating to a web-based architecture using Streamlit to provide an interactive, visual-first experience for OCR tasks.

## Goals / Non-Goals

**Goals:**
*   **Web Accessibility**: Provide a browser-based UI for PDF-to-text conversion.
*   **Interactive Verification**: Allow users to see PDF pages and OCR results side-by-side and edit the text.
*   **Session Management**: Persist state (uploaded files, results) across browser refreshes without server-side storage.
*   **Safety**: Limit resource consumption (file size, page counts) for public users.

**Non-Goals:**
*   **Persistent Storage**: We will not implement a database or disk-based storage for user files.
*   **User Accounts**: No authentication or user profiles are required for this phase.
*   **Complex Layout Extraction**: We are focusing on plain text extraction, not full PDF reconstruction.

## Decisions

### 1. Framework Choice: Streamlit over React/FastAPI
*   **Rationale**: Streamlit allows for rapid development of data-centric web apps in pure Python. It natively handles session state and provides built-in components for file uploads and layouts, which perfectly aligns with our interactive requirements.
*   **Alternatives Considered**: React + FastAPI (too much overhead for this scope), Flask + Jinja2 (harder to manage reactive state).

### 2. State Management: Streamlit Session State
*   **Rationale**: We need to keep the uploaded PDF and extracted text in memory to allow for refreshes. `st.session_state` provides a dictionary-like interface bound to the user's session.
*   **Alternatives Considered**: LocalStorage (requires JS bridge in Streamlit), Redis (requires additional infrastructure).

### 3. Image Rendering: PyMuPDF for Live Preview
*   **Rationale**: We will use `PyMuPDF` (fitz) to render PDF pages as images on-the-fly. This is faster and more flexible than pre-converting all pages to images.
*   **Alternatives Considered**: `pdf2image` (slower, requires Poppler system calls for every page rendering).

### 4. Layout: Split-Column UI
*   **Rationale**: A `st.columns([1, 1])` layout will provide the required side-by-side view. The left column will display the page image, and the right column will contain a text area for OCR results.

## Risks / Trade-offs

*   **[Risk] Memory Consumption** → **Mitigation**: Implement strict file size (20MB) and page (50) limits to prevent OOM errors on the server.
*   **[Risk] OCR Latency** → **Mitigation**: Use `st.spinner` and `st.progress` to provide feedback. Implement page-level OCR to avoid long waits for entire documents.
*   **[Risk] Session Timeout** → **Mitigation**: Streamlit sessions time out after inactivity. We will inform users that work is lost if the tab is closed or inactive for too long.
