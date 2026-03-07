import pytest
from ocr_pdf_converter.cli import process_single_pdf
from unittest.mock import patch, MagicMock
from pathlib import Path
import fitz

@pytest.fixture
def scanned_pdf(tmp_path):
    # A PDF without text (only an image-like page)
    pdf_path = tmp_path / "scanned.pdf"
    doc = fitz.open()
    page = doc.new_page()
    # Draw something to make it non-empty but without text
    page.draw_rect([10, 10, 100, 100], color=(1, 0, 0))
    doc.save(str(pdf_path))
    doc.close()
    return pdf_path

def test_full_pipeline_with_ocr(scanned_pdf):
    with patch("pytesseract.image_to_string") as mock_ocr:
        mock_ocr.return_value = "OCR Result from Scanned PDF"
        
        text = process_single_pdf(scanned_pdf, "eng")
        
        assert "OCR Result from Scanned PDF" in text
        mock_ocr.assert_called()

def test_full_pipeline_with_searchable(tmp_path):
    pdf_path = tmp_path / "searchable.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Directly extracted text")
    doc.save(str(pdf_path))
    doc.close()
    
    with patch("pytesseract.image_to_string") as mock_ocr:
        text = process_single_pdf(pdf_path, "eng")
        
        assert "Directly extracted text" in text
        # OCR should NOT be called if text layer is present
        mock_ocr.assert_not_called()
