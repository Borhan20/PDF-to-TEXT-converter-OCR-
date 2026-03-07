import pytesseract
from PIL import Image

class OCREngine:
    """Core logic for image-to-text extraction using Tesseract."""

    def __init__(self, default_lang: str = "eng"):
        """Initializes the OCR engine with a default language."""
        self.default_lang = default_lang

    def extract_text(self, image: Image.Image, lang: str = None) -> str:
        """Extracts text from a given PIL Image object and sanitizes it."""
        if lang is None:
            lang = self.default_lang
        raw_text = pytesseract.image_to_string(image, lang=lang)
        return self.sanitize_text(raw_text)

    def sanitize_text(self, text: str) -> str:
        """Performs basic cleanup on the extracted text."""
        if not text:
            return ""
        # Remove form feed characters (\f) and strip surrounding whitespace
        clean_text = text.replace("\f", "")
        return clean_text.strip()
