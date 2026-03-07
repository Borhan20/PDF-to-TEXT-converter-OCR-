import pytest
from ocr_pdf_converter.pdf_processor import PDFProcessor
from ocr_pdf_converter.ocr_engine import OCREngine
from unittest.mock import patch, MagicMock
from pathlib import Path
import fitz

@pytest.fixture
def empty_pdf(tmp_path):
    pdf_path = tmp_path / "empty.pdf"
    doc = fitz.open()
    doc.new_page()
    doc.save(str(pdf_path))
    doc.close()
    return str(pdf_path)

@pytest.fixture
def text_pdf(tmp_path):
    pdf_path = tmp_path / "text.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Sample Text")
    doc.save(str(pdf_path))
    doc.close()
    return str(pdf_path)

def test_pdf_processor_metadata(text_pdf):
    processor = PDFProcessor(text_pdf)
    metadata = processor.get_metadata()
    assert metadata["page_count"] == 1
    assert "title" in metadata

def test_pdf_processor_extract_text(text_pdf):
    processor = PDFProcessor(text_pdf)
    text = processor.extract_text_layer()
    assert "Sample Text" in text

def test_ocr_engine_sanitize():
    engine = OCREngine()
    assert engine.sanitize_text("  hello  \f") == "hello"
    assert engine.sanitize_text("") == ""

def test_ocr_engine_lang():
    engine = OCREngine(default_lang="spa")
    assert engine.default_lang == "spa"
