## ADDED Requirements

### Requirement: Image Text Extraction
The system SHALL use Tesseract OCR to extract text from a given image file (PNG, JPEG).

#### Scenario: Successful extraction from high-quality image
- **WHEN** the system processes a clear, high-resolution image containing text
- **THEN** it MUST return the extracted text as a string with at least 95% accuracy for standard fonts

### Requirement: Language Support
The system SHALL support multiple languages for OCR, defaulting to English.

#### Scenario: Extraction in Spanish
- **WHEN** the user specifies "spa" (Spanish) as the language
- **THEN** the Tesseract engine MUST use the Spanish training data for recognition
