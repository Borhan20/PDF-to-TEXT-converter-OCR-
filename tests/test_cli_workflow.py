import pytest
from typer.testing import CliRunner
from ocr_pdf_converter.cli import app
from unittest.mock import patch, MagicMock
from pathlib import Path

runner = CliRunner()

@pytest.fixture
def sample_pdf(tmp_path):
    pdf_path = tmp_path / "test.pdf"
    pdf_path.touch()
    return str(pdf_path)

def test_convert_single_file_workflow(sample_pdf, tmp_path):
    output_path = tmp_path / "result.txt"
    
    with patch("ocr_pdf_converter.cli.PDFProcessor") as mock_pdf_class, \
         patch("ocr_pdf_converter.cli.OCREngine") as mock_ocr_class:
        
        # Mock PDFProcessor
        mock_pdf = MagicMock()
        mock_pdf_class.return_value = mock_pdf
        # Explicitly mock context manager
        mock_pdf.__enter__.return_value = mock_pdf
        
        mock_pdf.extract_text_layer.return_value = "Existing Text that is long enough to skip OCR"
        mock_pdf.get_metadata.return_value = {"page_count": 1}
        
        # Mock OCREngine
        mock_ocr = MagicMock()
        mock_ocr_class.return_value = mock_ocr
        mock_ocr.extract_text.return_value = "OCR Text"
        
        result = runner.invoke(app, [sample_pdf, "--output", str(output_path)])
        
        assert result.exit_code == 0
        assert output_path.exists()
        content = output_path.read_text()
        assert "Existing Text" in content

def test_convert_single_file_ocr_fallback(sample_pdf, tmp_path):
    output_path = tmp_path / "result_ocr.txt"
    
    with patch("ocr_pdf_converter.cli.PDFProcessor") as mock_pdf_class, \
         patch("ocr_pdf_converter.cli.OCREngine") as mock_ocr_class:
        
        # Mock PDFProcessor
        mock_pdf = MagicMock()
        mock_pdf_class.return_value = mock_pdf
        mock_pdf.__enter__.return_value = mock_pdf
        
        mock_pdf.extract_text_layer.return_value = "" # Empty
        mock_pdf.get_metadata.return_value = {"page_count": 1}
        mock_pdf.convert_to_images.return_value = [MagicMock()] # 1 page
        
        # Mock OCREngine
        mock_ocr = MagicMock()
        mock_ocr_class.return_value = mock_ocr
        mock_ocr.extract_text.return_value = "OCR Result"
        
        result = runner.invoke(app, [sample_pdf, "--output", str(output_path)])
        
        assert result.exit_code == 0
        assert output_path.exists()
        content = output_path.read_text()
        assert "OCR Result" in content
