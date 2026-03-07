import pytest
from ocr_pdf_converter.pdf_processor import PDFProcessor
from pathlib import Path
import fitz

@pytest.fixture
def sample_pdf(tmp_path):
    pdf_path = tmp_path / "test.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Hello from the text layer")
    doc.save(str(pdf_path))
    doc.close()
    return str(pdf_path)

def test_extract_text_layer(sample_pdf):
    processor = PDFProcessor(sample_pdf)
    text = processor.extract_text_layer()
    assert "Hello from the text layer" in text

def test_extract_text_layer_empty(tmp_path):
    # Empty 1-page PDF
    pdf_path = tmp_path / "empty.pdf"
    doc = fitz.open()
    doc.new_page()
    doc.save(str(pdf_path))
    doc.close()
    
    processor = PDFProcessor(str(pdf_path))
    text = processor.extract_text_layer()
    assert text.strip() == ""
