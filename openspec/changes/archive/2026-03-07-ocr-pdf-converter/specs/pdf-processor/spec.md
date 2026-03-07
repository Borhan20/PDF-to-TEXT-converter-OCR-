## ADDED Requirements

### Requirement: PDF Page to Image Conversion
The system SHALL convert each page of a PDF document into a high-resolution image (300 DPI) for OCR processing.

#### Scenario: Convert multi-page PDF
- **WHEN** a 3-page PDF is provided
- **THEN** the system MUST generate 3 distinct image objects for the OCR engine

### Requirement: Text Layer Extraction
The system SHALL attempt to extract any existing machine-readable text from the PDF before applying OCR.

#### Scenario: PDF with existing text
- **WHEN** a PDF contains a searchable text layer
- **THEN** the system MUST extract that text directly instead of using OCR to save time and increase accuracy
