import pytest
from ocr_pdf_converter.pdf_processor import PDFProcessor
from PIL import Image

@pytest.fixture
def sample_pdf(tmp_path):
    import fitz
    pdf_path = tmp_path / "test_pages.pdf"
    doc = fitz.open()
    doc.new_page()
    doc.new_page()
    doc.save(str(pdf_path))
    doc.close()
    return str(pdf_path)

def test_convert_to_images(sample_pdf):
    processor = PDFProcessor(sample_pdf)
    images = list(processor.convert_to_images())
    assert len(images) == 2
    assert all(isinstance(img, Image.Image) for img in images)
