import fitz
from pathlib import Path
from pdf2image import convert_from_path

class PDFProcessor:
    """Manages PDF reading, metadata extraction, and page conversion."""

    def __init__(self, pdf_path: str):
        """Initializes the processor with a PDF file path."""
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        self._doc = None

    def __enter__(self):
        """Context manager entry."""
        self._open_doc()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def _open_doc(self):
        """Opens the PDF document if not already opened."""
        if self._doc is None:
            self._doc = fitz.open(str(self.pdf_path))
        return self._doc

    def close(self):
        """Closes the document."""
        if hasattr(self, "_doc") and self._doc is not None:
            self._doc.close()
            self._doc = None

    def get_metadata(self) -> dict:
        """Extracts basic metadata from the PDF."""
        doc = self._open_doc()
        metadata = {
            "page_count": len(doc),
            "title": doc.metadata.get("title", ""),
            "author": doc.metadata.get("author", ""),
        }
        return metadata

    def extract_text_layer(self) -> str:
        """Extracts existing searchable text from all pages of the PDF."""
        doc = self._open_doc()
        full_text = []
        for page in doc:
            full_text.append(page.get_text())
        return "\n".join(full_text)

    def convert_to_images(self, dpi: int = 300):
        """Converts all PDF pages into PIL Image objects."""
        return convert_from_path(str(self.pdf_path), dpi=dpi)

    def __del__(self):
        """Ensures the document is closed."""
        self.close()
