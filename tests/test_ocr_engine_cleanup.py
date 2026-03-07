import pytest
from ocr_pdf_converter.ocr_engine import OCREngine
from PIL import Image
from unittest.mock import patch

def test_ocr_engine_cleanup():
    engine = OCREngine()
    # Test with extra whitespace and form feeds (common in OCR)
    raw_text = "  Hello World  \f\n\n"
    clean_text = engine.sanitize_text(raw_text)
    assert clean_text == "Hello World"

def test_extract_text_with_cleanup(sample_image):
    with patch("pytesseract.image_to_string") as mock_ocr:
        mock_ocr.return_value = "  OCR Output  \f"
        engine = OCREngine()
        # Assume extract_text uses sanitize_text
        text = engine.extract_text(sample_image)
        assert text == "OCR Output"

@pytest.fixture
def sample_image():
    return Image.new("RGB", (100, 100), color="white")
