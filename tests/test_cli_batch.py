import pytest
from typer.testing import CliRunner
from ocr_pdf_converter.cli import app
from unittest.mock import patch, MagicMock
from pathlib import Path

runner = CliRunner()

@pytest.fixture
def sample_dir(tmp_path):
    pdf_dir = tmp_path / "pdfs"
    pdf_dir.mkdir()
    (pdf_dir / "1.pdf").touch()
    (pdf_dir / "2.pdf").touch()
    (pdf_dir / "not_a_pdf.txt").touch()
    return pdf_dir

def test_convert_directory_workflow(sample_dir, tmp_path):
    output_dir = tmp_path / "results"
    output_dir.mkdir()
    
    with patch("ocr_pdf_converter.cli.process_single_pdf") as mock_process:
        mock_process.return_value = "Extracted Text"
        
        result = runner.invoke(app, [str(sample_dir), "--output-dir", str(output_dir)])
        
        assert result.exit_code == 0
        # Should process 2 PDFs
        assert mock_process.call_count == 2
        assert (output_dir / "1.txt").exists()
        assert (output_dir / "2.txt").exists()
        assert not (output_dir / "not_a_pdf.txt").exists()
