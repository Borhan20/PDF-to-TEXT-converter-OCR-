import pytest
from ocr_pdf_converter.ocr_engine import OCREngine
from PIL import Image
from unittest.mock import patch

@pytest.fixture
def sample_image():
    return Image.new("RGB", (100, 100), color="white")

def test_ocr_engine_extract_text_default_lang(sample_image):
    with patch("pytesseract.image_to_string") as mock_ocr:
        mock_ocr.return_value = "English text"
        engine = OCREngine()
        text = engine.extract_text(sample_image)
        assert text == "English text"
        mock_ocr.assert_called_once_with(sample_image, lang="eng")

def test_ocr_engine_extract_text_custom_lang(sample_image):
    with patch("pytesseract.image_to_string") as mock_ocr:
        mock_ocr.return_value = "Spanish text"
        engine = OCREngine(default_lang="spa")
        text = engine.extract_text(sample_image)
        assert text == "Spanish text"
        mock_ocr.assert_called_once_with(sample_image, lang="spa")

def test_ocr_engine_extract_text_override_lang(sample_image):
    with patch("pytesseract.image_to_string") as mock_ocr:
        mock_ocr.return_value = "French text"
        engine = OCREngine(default_lang="eng")
        text = engine.extract_text(sample_image, lang="fra")
        assert text == "French text"
        mock_ocr.assert_called_once_with(sample_image, lang="fra")
