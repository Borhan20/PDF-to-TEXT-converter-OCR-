# Project Requirements: OCR PDF-to-Text Web Service

## 1. Executive Summary
**Goal:** Transform the existing OCR PDF-to-Text CLI tool into a public-facing, interactive web application.
**Vision:** A seamless, "zero-install" experience where users can upload PDFs, perform OCR, and verify results in a side-by-side viewer before downloading the extracted text.
**Core Technology:** Python-based implementation using **Streamlit** for the frontend and session management.

## 2. User Personas
*   **General Public User:** Needs to extract text from a scanned PDF or image-based document without installing specialized software.
*   **Researcher/Student:** Requires a tool to quickly digitize document segments for citation or analysis, with a preference for visual verification.

## 3. User Stories
*   **Upload & Limit:** As a user, I want to upload a PDF (up to 20MB or 50 pages) so that the system remains responsive and fair for all public users.
*   **Interactive OCR:** As a user, I want to trigger OCR processing manually so that I can control when the server consumes resources.
*   **Side-by-Side Verification:** As a user, I want to see the original PDF page next to the extracted text so that I can manually verify and correct the OCR output.
*   **Session Persistence:** As a user, I want my uploaded PDF and extracted text to persist if I refresh the browser page, without requiring a login or permanent server-side storage.
*   **Download:** As a user, I want to download the finalized text as a `.txt` file once processing is complete.

## 4. Functional Requirements
### 4.1 Web Interface (Streamlit)
*   **File Uploader:** Drag-and-drop support for `.pdf` files.
*   **Validation:** Enforcement of file size (< 20MB) and page count (< 50 pages) before processing.
*   **Side-by-Side Layout:** A split-pane view showing the PDF page image on the left and a text area for the OCR result on the right.
*   **Download Button:** Generates and serves a `.txt` file containing all extracted text.

### 4.2 OCR Engine Integration
*   **Engine:** Continued use of Tesseract OCR (via `pytesseract`).
*   **Language Support:** A dropdown menu to select the document language (e.g., English, Spanish, French, German) to improve OCR accuracy.
*   **Batch vs. Page:** Support for processing a single page (current view) or the entire document in the background.

### 4.3 State Management
*   **Client-Side Strategy:** Utilize browser-based persistence (via Streamlit session state or local storage mechanisms) to ensure that refreshes do not clear the current work-in-progress.
*   **Privacy:** No files (PDF or TXT) shall be stored permanently on the server after the user session ends.

## 5. Non-Functional Requirements
### 5.1 Performance
*   **Concurrency:** The server must handle multiple concurrent users via Streamlit's threading model.
*   **Latency:** OCR processing feedback must be provided via progress bars or spinners.

### 5.2 Usability
*   **Mobile-Friendly:** The UI should adjust for smaller screens, though primary use is desktop.
*   **Interactivity:** Immediate visual feedback when a file is uploaded or processing starts.

## 6. Data Entities
*   **UploadedFile:** Metadata including filename, size, and binary content.
*   **OCRResult:** Mapping of page numbers to extracted text strings.
*   **SessionState:** A container for `UploadedFile` and `OCRResult` bound to the user's browser session.

## 7. Success Metrics
*   **Availability:** 100% functional on a standard web browser (Chrome/Firefox).
*   **Reliability:** Successfully prevents uploads exceeding 20MB/50 pages.
*   **UX Satisfaction:** Users can complete an "Upload-to-Download" cycle in under 3 minutes for a 10-page document.
