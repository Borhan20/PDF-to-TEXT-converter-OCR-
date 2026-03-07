import pytest
import fitz
from ocr_pdf_converter.pdf_processor import PDFProcessor
from pathlib import Path

@pytest.fixture
def sample_pdf(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Test PDF Content")
    doc.set_metadata({"title": "Test PDF", "author": "Tester"})
    doc.save(str(pdf_path))
    doc.close()
    return str(pdf_path)

def test_pdf_processor_initialization_failure():
    # Test with non-existent file
    with pytest.raises(FileNotFoundError):
        PDFProcessor("non_existent.pdf")

def test_pdf_processor_metadata(sample_pdf):
    processor = PDFProcessor(sample_pdf)
    metadata = processor.get_metadata()
    assert isinstance(metadata, dict)
    assert metadata["page_count"] == 1
    assert metadata["title"] == "Test PDF"
    assert metadata["author"] == "Tester"
