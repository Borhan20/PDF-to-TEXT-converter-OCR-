import pytest
from typer.testing import CliRunner
from ocr_pdf_converter.cli import app
from unittest.mock import patch
from pathlib import Path
import fitz

runner = CliRunner()

def create_searchable_pdf(path, text):
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), text)
    doc.save(str(path))
    doc.close()

def create_scanned_pdf(path):
    doc = fitz.open()
    page = doc.new_page()
    page.draw_rect([10, 10, 100, 100], color=(1, 0, 0))
    doc.save(str(path))
    doc.close()

def test_mixed_batch_processing(tmp_path):
    input_dir = tmp_path / "mixed_pdfs"
    input_dir.mkdir()
    output_dir = tmp_path / "results"
    output_dir.mkdir()
    
    searchable_path = input_dir / "searchable.pdf"
    scanned_path = input_dir / "scanned.pdf"
    
    create_searchable_pdf(searchable_path, "Existing searchable text")
    create_scanned_pdf(scanned_path)
    
    with patch("pytesseract.image_to_string") as mock_ocr:
        mock_ocr.return_value = "OCR extracted text"
        
        result = runner.invoke(app, [str(input_dir), "--output-dir", str(output_dir)])
        
        assert result.exit_code == 0
        
        # Check searchable PDF result
        assert (output_dir / "searchable.txt").exists()
        searchable_content = (output_dir / "searchable.txt").read_text()
        assert "Existing searchable text" in searchable_content
        
        # Check scanned PDF result
        assert (output_dir / "scanned.txt").exists()
        scanned_content = (output_dir / "scanned.txt").read_text()
        assert "OCR extracted text" in scanned_content
        
        # Verify OCR was only called for scanned PDF
        # Note: 1 page in scanned, so 1 call to extract_text
        assert mock_ocr.call_count == 1
