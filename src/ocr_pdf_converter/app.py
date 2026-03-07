import streamlit as st
import fitz
from PIL import Image
import io
import os
import shutil
from ocr_pdf_converter.pdf_processor import PDFProcessor
from ocr_pdf_converter.ocr_engine import OCREngine

# Page Configuration
st.set_page_config(
    page_title="OCR PDF-to-Text",
    page_icon="📄",
    layout="wide"
)

# Constants
MAX_FILE_SIZE_MB = 20
MAX_PAGE_COUNT = 50

# System Check: Tesseract Availability
TESSERACT_AVAILABLE = shutil.which("tesseract") is not None

# Initialize Session State
if "pdf_content" not in st.session_state:
    st.session_state.pdf_content = None
if "page_count" not in st.session_state:
    st.session_state.page_count = 0
if "current_page" not in st.session_state:
    st.session_state.current_page = 0
if "ocr_language" not in st.session_state:
    st.session_state.ocr_language = "eng"
if "file_name" not in st.session_state:
    st.session_state.file_name = ""

# Helper: Render PDF Page to Image
def get_page_image(pdf_bytes, page_index, dpi=150):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page = doc.load_page(page_index)
    pix = page.get_pixmap(dpi=dpi)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    doc.close()
    return img

# Helper: Set OCR text for a page
def set_page_text(page_index, text):
    st.session_state[f"page_text_{page_index}"] = text

# Sidebar: OCR Settings
st.sidebar.title("OCR Settings")
languages = {
    "English": "eng",
    "Spanish": "spa",
    "French": "fra",
    "German": "deu"
}
selected_lang_name = st.sidebar.selectbox(
    "Document Language", 
    list(languages.keys()),
    index=list(languages.values()).index(st.session_state.ocr_language)
)
st.session_state.ocr_language = languages[selected_lang_name]

# Main UI
st.title("📄 OCR PDF-to-Text Converter")

if not TESSERACT_AVAILABLE:
    st.error("⚠️ **Tesseract OCR not found on this system.**")
    st.markdown("""
    To use this application, you must install the Tesseract OCR engine:
    
    - **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
    - **macOS**: `brew install tesseract`
    - **Windows**: Download the installer from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
    
    *If you are running in Docker, ensure you have rebuilt the image.*
    """)
    st.stop()

st.markdown("Upload a scanned PDF to extract text using OCR. Verify and edit results side-by-side.")

# File Uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    if uploaded_file.name != st.session_state.file_name:
        # Reset session state for new file
        st.session_state.pdf_content = uploaded_file.read()
        st.session_state.file_name = uploaded_file.name
        
        # Validate File Size
        file_size_mb = len(st.session_state.pdf_content) / (1024 * 1024)
        if file_size_mb > MAX_FILE_SIZE_MB:
            st.error(f"File size exceeds {MAX_FILE_SIZE_MB}MB limit ({file_size_mb:.1f}MB).")
            st.session_state.pdf_content = None
        else:
            # Validate Page Count
            try:
                doc = fitz.open(stream=st.session_state.pdf_content, filetype="pdf")
                st.session_state.page_count = len(doc)
                doc.close()
                
                if st.session_state.page_count > MAX_PAGE_COUNT:
                    st.error(f"Page count exceeds {MAX_PAGE_COUNT} page limit ({st.session_state.page_count} pages).")
                    st.session_state.pdf_content = None
                else:
                    # Clear old text state keys
                    for key in list(st.session_state.keys()):
                        if key.startswith("page_text_"):
                            del st.session_state[key]
                    st.session_state.current_page = 0
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
                st.session_state.pdf_content = None

if st.session_state.pdf_content:
    # Navigation and Global Actions
    st.sidebar.markdown("---")
    st.sidebar.subheader("Navigation")
    col1, col2, col3 = st.sidebar.columns([1, 2, 1])
    if col1.button("⬅️") and st.session_state.current_page > 0:
        st.session_state.current_page -= 1
    
    col2.markdown(f"**Page {st.session_state.current_page + 1} of {st.session_state.page_count}**")
    
    if col3.button("➡️") and st.session_state.current_page < st.session_state.page_count - 1:
        st.session_state.current_page += 1

    # Batch Processing Actions
    st.sidebar.markdown("---")
    st.sidebar.subheader("Batch Actions")
    
    if st.sidebar.button("🚀 Run OCR for ALL Pages"):
        progress_bar = st.sidebar.progress(0)
        status_text = st.sidebar.empty()
        
        engine = OCREngine(default_lang=st.session_state.ocr_language)
        
        for i in range(st.session_state.page_count):
            status_text.text(f"Processing Page {i+1}...")
            try:
                ocr_img = get_page_image(st.session_state.pdf_content, i, dpi=300)
                text = engine.extract_text(ocr_img)
                set_page_text(i, text)
            except Exception as e:
                set_page_text(i, f"Error on page {i+1}: {e}")
            progress_bar.progress((i + 1) / st.session_state.page_count)
        
        status_text.text("Batch OCR Complete!")
        st.rerun()

    if st.sidebar.button("⚡ Extract Existing Text Layer"):
        with st.spinner("Extracting text layer..."):
            try:
                doc = fitz.open(stream=st.session_state.pdf_content, filetype="pdf")
                for i, page in enumerate(doc):
                    set_page_text(i, page.get_text())
                doc.close()
                st.success("Extracted text layer from all pages.")
                st.rerun()
            except Exception as e:
                st.error(f"Extraction failed: {e}")

    # Main Display: Side-by-Side
    view_col, text_col = st.columns([1, 1])

    # 1. Left Column: PDF Page Image
    with view_col:
        st.subheader("Original Page")
        try:
            img = get_page_image(st.session_state.pdf_content, st.session_state.current_page, dpi=150)
            st.image(img, use_container_width=True)
        except Exception as e:
            st.error(f"Could not render page: {e}")

    # 2. Right Column: OCR Text and Controls
    with text_col:
        st.subheader("Extracted Text")
        
        text_key = f"page_text_{st.session_state.current_page}"
        
        # Trigger OCR for this page
        if st.button("🔍 Run OCR for this page"):
            with st.spinner("Processing page..."):
                try:
                    ocr_img = get_page_image(st.session_state.pdf_content, st.session_state.current_page, dpi=300)
                    engine = OCREngine(default_lang=st.session_state.ocr_language)
                    text = engine.extract_text(ocr_img)
                    set_page_text(st.session_state.current_page, text)
                    st.rerun() # Force rerun to update text area value
                except Exception as e:
                    st.error(f"OCR failed: {e}")
        
        # Ensure key exists in session state to avoid errors
        if text_key not in st.session_state:
            st.session_state[text_key] = ""
            
        # Editable Text Area: Directly bound to session state via key
        st.text_area(
            "Verify and Edit", 
            key=text_key,
            height=600
        )

    # Download Button
    full_output = []
    has_text = False
    for i in range(st.session_state.page_count):
        text = st.session_state.get(f"page_text_{i}", "")
        if text.strip():
            has_text = True
        page_text = text if text.strip() else f"--- [Page {i+1} not processed] ---"
        full_output.append(f"--- Page {i+1} ---\n{page_text}")
    
    if has_text:
        final_txt = "\n\n".join(full_output)
        st.sidebar.markdown("---")
        st.sidebar.download_button(
            label="💾 Download All Results (.txt)",
            data=final_txt,
            file_name=f"ocr_result_{st.session_state.file_name}.txt",
            mime="text/plain"
        )
else:
    st.info("Please upload a PDF file to begin.")
